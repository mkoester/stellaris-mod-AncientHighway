#!/usr/bin/env python3
"""Generate the repetitive parts of the Ancient Highway mod.

Writes into ancient_highway/ (paths relative to this script's repo):
  common/bypass/ahw_bypasses.txt            one scripted-connection type per entry pair
  common/megastructures/ahw_megastructures.txt  the two ends of every pair
  common/scripted_effects/ahw_generated_effects.txt  outline, outer ring, pair switch, exit slots,
                                                   portal placement
  interface/ahw.gfx                         outliner icons (vanilla textures by path)
  localisation/english/ahw_generated_l_english.yml

Run it after changing the constants below; commit its output with it.
"""
import math
import random
import pathlib

MOD = pathlib.Path(__file__).resolve().parent.parent / 'ancient_highway'

PAIRS = 32  # entry-point pairs available: one per regular empire (huge galaxies: up to 30)
# The outer ring (user, 2026-11-04): round the outside of the galaxy, following its outline; once
# round it takes about as long as once round the galaxy at mid radius. Every jump costs a flat
# 15 days of windup (HYPERLANE_WINDUP = 150 micro-updates, common/defines/00_defines.txt), so the
# node count is about the jumps of that lap: circumference at mid radius (0.6 R: halfway between a
# core at ~0.2 R and the rim) x a detour factor for hyperlane paths (1.3, a guess - calibrate in
# game) / the mean star spacing (sqrt(area / stars)). Setup radius and stars per size:
# map/setup_scenarios/*.txt ("radius should be less than 500").
SETUP = {'tiny': (200, 200), 'small': (300, 400), 'medium': (400, 600), 'large': (450, 800), 'huge': (450, 1000)}
MID, DETOUR = 0.6, 1.3


def lap_nodes(radius, stars):
    spacing = math.sqrt(math.pi * radius ** 2 / stars)
    return 4 * round(2 * math.pi * MID * radius * DETOUR / spacing / 4)


NODES = {size: lap_nodes(*rs) for size, rs in SETUP.items()}
MAX_NODES = max(NODES.values())
# The outline: every system's x, y from its distances to the centre and to a compass probe
# COMPASS_R east, then north, of it (law of cosines: x = (r^2 + C^2 - d_east^2) / 2C). A node's
# edge = the farthest system within OUTLINE_HALF degrees of its direction (none: the farthest
# overall); the node goes RING_MARGIN beyond it. spawn_system takes literal distances only, so
# the radius is rounded down to RAD_STEP from RAD_MAX.
COMPASS_R = 40
OUTLINE_HALF = 15
RING_MARGIN = 25
# Smoothing (user, run 14: a lone outlying system pushed ~5 nodes out by 40-60 as a step): a node
# may sit at most RING_SLOPE lower than its neighbour, so a bulge becomes a gentle hill (two sweeps
# round the ring each way). A sector without systems starts at 0 and is lifted by its neighbours.
RING_SLOPE = 6
# The two centre probes are not left in the core (no effect deletes a system, run 9): after the
# other nodes are spawned they move into the last two node positions - the compass probe first,
# then the centre probe itself (move_system relative to its own position).
RAD_MIN, RAD_MAX, RAD_STEP = 40, 560, 5
# exit slots in a ring system: (orbit_distance, orbit_angle), far apart first
EXIT_SLOTS = [(300, a) for a in range(0, 360, 60)] + [(220, a) for a in range(30, 360, 60)]
NEAREST_STEPS = list(range(20, 401, 20)) + [600, 1000]  # search radii for the nearest ring system
# Finding the centre (run 8: spawn_system without a scope spawns nothing): leapfrog two probe
# systems with move_system direction = corewards (vanilla uses rimwards; both are in the binary),
# keeping whichever has the lower distance_to_core_percent. Step sizes in map units, tries each.
CENTRE_STEPS = [40, 30, 20, 15, 10, 7, 5]
CENTRE_TRIES = 3
INNERMOST_BANDS = [0.15, 0.2, 0.25, 0.3, 0.4, 0.6]
# Portal placement. Run 9: up to 30 random moves per empire took ~75 s and kept the last try.
# Runs 10-16 measured the portal at 4 compass points (4 moves, ~3 s per portal in run 16). 0.0.17
# computes the same numbers from the outline's coordinates and spawns the portal once: for each
# lane of the anchor to N, c = 2r cos(theta_N) = 2r dx/L and s = 2r sin(theta_N); at angle a the
# portal's margin to N is -(cos a * c + sin a * s) / 2 (= -r cos(a - theta_N)). The gate in the
# portal sits at that same orbit angle: facing away from the anchor, opposite the portal's only
# lane (orbit angles and map angles agree - confirmed in run 10).
PORTAL_R = 15
PORTAL_ANGLES = list(range(0, 360, 30))
# Run 13: a portal landed on a regular system (pair 5, on Mehsegaaran) and two next to each other
# (pairs 6, 7). Every system with coordinates within PORTAL_R + CLEAR_MIN of the anchor (other
# portals and ring nodes too) counts; at angle a its squared distance from the portal is exactly
# |u|^2 + r^2 - 2r (ux cos a + uy sin a), u = its offset from the anchor. Angles closer than
# CLEAR_MIN to any of them lose CLEAR_PENALTY.
CLEAR_MIN = 12
CLEAR_PENALTY = 100
# Portal names (2026-11-05): the builders counted in eights, so the ring is cut into eight reaches
# of 45 degrees, one name each (A..H for 0..7 as a reminder). A portal is named after the reach of
# its exit node plus an octal address: the reach's digit, then the portal's number in that reach in
# octal (Caedris 23 = reach 2, its third portal). Numbering in a reach follows the order the portals
# were made. Lore: docs/lore.md.
REACHES = ['Ashkara', 'Belun', 'Caedris', 'Dovhar', 'Eshmet', 'Furon', 'Galvaas', 'Hethra']
REACH_DEG = 360 / len(REACHES)
STATIONS = len(REACHES)  # express stations and links: one per reach
GATE_ORBIT = 230
# Express wormholes (design 2026-11-05): one station per reach, so a link spans about a reach; two
# wormholes per station on its radial line (= at right angles to the ring's lanes), inside the
# arrival radius (the asteroid at 270). Dormant until the mid game (on_mid_game_pulse), then
# unstable - each month a link flips open/closed with EXPRESS_FLIP % - until stabilised (a study at
# a station, cheaper later: EXPRESS_COST, x0.75 every 25 years after year 100). Tunable.
EXPRESS_ORBIT, EXPRESS_FLIP = 220, 25
EXPRESS_COST, EXPRESS_DAYS = 4000, 60
REPAIR_DAYS, REPAIR_ALLOYS, REPAIR_INFLUENCE = 90, 300, 50  # design 2026-11-05, "Access" 3  # run 10: lane arrivals ~150, the orange outer circle ~255 (measured in a screenshot)

GENERATED = '# GENERATED by tools/gen.py - edit the generator, not this file.\n'


def angle_switch(body, var='ahw_best_a'):
    """if/else_if over var (a portal angle) in the current scope; body(angle) -> effect text."""
    return '\n'.join(
        f'''		{'if' if k == 0 else 'else_if'} = {{
			limit = {{ check_variable = {{ which = {var} value = {a} }} }}
			{body(a)}
		}}''' for k, a in enumerate(PORTAL_ANGLES))


def gate_by_angle():
    return angle_switch(lambda a: f'spawn_megastructure = {{ type = ahw_gate_broken_$N$ orbit_distance = {GATE_ORBIT} orbit_angle = {a} }}')


def clearances():
    """this = a near system with ahw_eq, ahw_ec, ahw_es, prev = the anchor: lowers the anchor's
    ahw_cl_<a> to the system's squared distance from the portal-to-be at each candidate angle a."""
    return '\n'.join(f'''			set_variable = {{ which = ahw_t value = ahw_ec }}
			multiply_variable = {{ which = ahw_t value = {round(math.cos(math.radians(a)), 4)} }}
			set_variable = {{ which = ahw_u value = ahw_es }}
			multiply_variable = {{ which = ahw_u value = {round(math.sin(math.radians(a)), 4)} }}
			change_variable = {{ which = ahw_t value = ahw_u }}
			change_variable = {{ which = ahw_t value = ahw_eq }}
			if = {{
				limit = {{ check_variable = {{ which = ahw_t value < event_target:ahw_x_tmp.ahw_cl_{a} }} }}
				event_target:ahw_x_tmp = {{ set_variable = {{ which = ahw_cl_{a} value = prev.ahw_t }} }}
			}}''' for a in PORTAL_ANGLES)


def spawn_portal_at(a):
    """this = the anchor: the portal PORTAL_R away at angle a, with its coordinates."""
    c, s = round(PORTAL_R * math.cos(math.radians(a)), 4), round(PORTAL_R * math.sin(math.radians(a)), 4)
    return f'''spawn_system = {{
				min_distance = {PORTAL_R}
				max_distance = {PORTAL_R}
				min_orientation_angle = {a}
				max_orientation_angle = {a}
				max_jumps = 0
				initializer = ahw_portal_init
				hyperlane = no
				effect = {{
					set_star_flag = ahw_portal
					set_star_flag = ahw_unclaimable
					save_global_event_target_as = ahw_portal_tmp
				}}
			}}
			set_variable = {{ which = ahw_px value = ahw_x }}
			change_variable = {{ which = ahw_px value = {c} }}
			set_variable = {{ which = ahw_py value = ahw_y }}
			change_variable = {{ which = ahw_py value = {s} }}'''


def portal_placement():
    lines = [f'''	event_target:ahw_x_tmp = {{
		# the anchor's lanes: ahw_c = 2r cos(theta), ahw_s = 2r sin(theta) of each lane's direction
		every_neighbor_system = {{
			export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_x_tmp type = euclidean }} variable = ahw_l }}
			set_variable = {{ which = ahw_c value = ahw_x }}
			subtract_variable = {{ which = ahw_c value = prev.ahw_x }}
			multiply_variable = {{ which = ahw_c value = {2 * PORTAL_R} }}
			divide_variable = {{ which = ahw_c value = ahw_l }}
			set_variable = {{ which = ahw_s value = ahw_y }}
			subtract_variable = {{ which = ahw_s value = prev.ahw_y }}
			multiply_variable = {{ which = ahw_s value = {2 * PORTAL_R} }}
			divide_variable = {{ which = ahw_s value = ahw_l }}
		}}
{chr(10).join(f"		set_variable = {{ which = ahw_cl_{a} value = 1000000 }}" for a in PORTAL_ANGLES)}
		# every system with coordinates near the anchor (portals and ring nodes too): at angle a its
		# squared distance from the portal is eq + cos a ec + sin a es, with u = its offset from
		# the anchor: eq = |u|^2 + r^2, ec = -2r ux, es = -2r uy
		every_system = {{
			limit = {{
				has_star_flag = ahw_xy
				NOT = {{ is_same_value = event_target:ahw_x_tmp }}
				distance = {{ source = event_target:ahw_x_tmp max_distance <= {PORTAL_R + CLEAR_MIN} type = euclidean }}
			}}
			set_variable = {{ which = ahw_ec value = ahw_x }}
			subtract_variable = {{ which = ahw_ec value = prev.ahw_x }}
			set_variable = {{ which = ahw_es value = ahw_y }}
			subtract_variable = {{ which = ahw_es value = prev.ahw_y }}
			set_variable = {{ which = ahw_eq value = ahw_ec }}
			multiply_variable = {{ which = ahw_eq value = ahw_ec }}
			set_variable = {{ which = ahw_t value = ahw_es }}
			multiply_variable = {{ which = ahw_t value = ahw_es }}
			change_variable = {{ which = ahw_eq value = ahw_t }}
			change_variable = {{ which = ahw_eq value = {PORTAL_R ** 2} }}
			multiply_variable = {{ which = ahw_ec value = {-2 * PORTAL_R} }}
			multiply_variable = {{ which = ahw_es value = {-2 * PORTAL_R} }}
{clearances()}
		}}
		set_variable = {{ which = ahw_best value = -1000 }}
		set_variable = {{ which = ahw_best_a value = 0 }}
	}}''']
    for a in PORTAL_ANGLES:
        ca = round(-math.cos(math.radians(a)) / 2, 4)
        sa = round(-math.sin(math.radians(a)) / 2, 4)
        lines.append(f'''	# angle {a}: the worst margin over the anchor's lanes, then the clearance
	event_target:ahw_x_tmp = {{
		set_variable = {{ which = ahw_m value = 1000 }}
		every_neighbor_system = {{
			set_variable = {{ which = ahw_t value = ahw_c }}
			multiply_variable = {{ which = ahw_t value = {ca} }}
			set_variable = {{ which = ahw_u value = ahw_s }}
			multiply_variable = {{ which = ahw_u value = {sa} }}
			change_variable = {{ which = ahw_t value = ahw_u }}
			if = {{
				limit = {{ check_variable = {{ which = ahw_t value < event_target:ahw_x_tmp.ahw_m }} }}
				event_target:ahw_x_tmp = {{ set_variable = {{ which = ahw_m value = prev.ahw_t }} }}
			}}
		}}
		set_variable = {{ which = ahw_cl value = ahw_cl_{a} }}
		if = {{
			limit = {{ check_variable = {{ which = ahw_cl value < {CLEAR_MIN ** 2} }} }}
			subtract_variable = {{ which = ahw_m value = {CLEAR_PENALTY} }}
		}}
		if = {{
			limit = {{ check_variable = {{ which = ahw_m value > ahw_best }} }}
			set_variable = {{ which = ahw_best value = ahw_m }}
			set_variable = {{ which = ahw_best_a value = {a} }}
			set_variable = {{ which = ahw_best_cl value = ahw_cl }}
		}}
	}}''')
    lines.append('''	# the portal, once, at the best angle (run 16: four measuring moves cost ~3 s per portal)
	event_target:ahw_x_tmp = {
''' + angle_switch(spawn_portal_at) + '''
		event_target:ahw_portal_tmp = {
			set_variable = { which = ahw_x value = prev.ahw_px }
			set_variable = { which = ahw_y value = prev.ahw_py }
			set_variable = { which = ahw_best_a value = prev.ahw_best_a }
			set_star_flag = ahw_xy
		}
		log = "AHW portal placed off \\\\[This.GetName] at angle \\\\[This.ahw_best_a]: worst lane margin \\\\[This.ahw_best] (+15 = opposite every other lane, 0 = sideways, -15 = beside one; 1000 = no other lane; -''' + str(CLEAR_PENALTY) + ''' = too close to a system), nearest other system at squared distance \\\\[This.ahw_best_cl] (want >= ''' + str(CLEAR_MIN ** 2) + '''; 1000000 = none near)"
	}''')
    return '''
# Spawns the portal (-> ahw_portal_tmp) PORTAL_R from its anchor ahw_x_tmp, at the angle where its
# lane arrives farthest from the anchor's other lanes and no other system is closer than CLEAR_MIN.
# Computed from the outline's coordinates (ahw_x, ahw_y; flag ahw_xy), no moves (0.0.17).
ahw_place_portal = {
''' + '\n'.join(lines) + '\n}\n'


def bypass_block(key, name, node, nexus, *, tech, windup, lockable, sensors, frame, effect, can_use=''):
    prereq = '\n\tprerequisites = {\n\t\tahw_tech_gate_theory\n\t}\n' if tech else ''
    return f'''
{key} = {{
	name = {name}
	is_pathfind = yes
	uses_action = no
	requires_exploration = no
	always_active = yes
	windup_time = {windup}
	winddown_time = 0
	ftl_multiplier = 0
	extends_sensors = {sensors}
	icon_frame = {frame}
	remember_instances = no
	animation_time = 1
	galactic_map_tooltip_header = {name}
	galactic_map_tooltip_desc = {name}_DESC
	connection_type = scripted_connection
	ftl_ship_effect = "{effect}_ftl_ship_effect_entity"
	ftl_bypass_effect = "{effect}_ftl_bypass_effect_entity"
	can_bypass_be_locked = {lockable}
{can_use}
	scripted_connection = {{
		node = {{ {node} }}
		nexus = {{ {nexus} }}
	}}
{prereq}}}
'''


def sealed_check(n):
    """0.0.23 (run 21: a lock_bypass lock never expired): a sealed pair is closed - both ends, as
    the type covers both - to all but the sealer and its friends (0.0.24, user: allies must still
    get through). this = country."""
    return f'''
	country_can_use = {{
		custom_tooltip = {{
			fail_text = AHW_GATE_SEALED
			OR = {{
				NOT = {{ has_global_flag = ahw_sealed_{n} }}
				ahw_friend_of_sealer = {{ N = {n} }}
			}}
		}}
	}}
'''


def seal_switches():
    """this = a portal (variable ahw_pair): set or clear its pair's seal flags."""
    sw = lambda body: '\n'.join(f'''	{'if' if n == 1 else 'else_if'} = {{
		limit = {{ check_variable = {{ which = ahw_pair value = {n} }} }}
		{body(n)}
	}}''' for n in range(1, PAIRS + 1))
    return f'''
# this = a portal: its pair is sealed by $COUNTRY$ - only it and its friends may pass
# (country_can_use of the pair's type, ahw_friend_of_sealer).
ahw_seal_pair_for = {{
{sw(lambda n: f'set_global_flag = ahw_sealed_{n} $COUNTRY$ = {{ save_global_event_target_as = ahw_sealer_{n} }}')}
}}

# this = a portal: its pair is sealed against everyone (console test ahw.25).
ahw_seal_pair_for_nobody = {{
{sw(lambda n: f'set_global_flag = ahw_sealed_{n} clear_global_event_target = ahw_sealer_{n}')}
}}

# this = a portal, event_target:ahw_repairer set: the broken gate upgraded and finished by script
# (console skips, the repair project, the contract) - vanilla's upgrade_megastructure_to +
# finish_upgrade. Its on_build_complete marks the portal repaired; if the engine does not run it
# for a scripted finish, the fallback below does (ahw_mark_repaired runs once either way).
ahw_repair_gate = {{
	event_target:ahw_repairer = {{ save_global_event_target_as = ahw_script_repairer }}
	every_system_megastructure = {{
{chr(10).join(f"""		if = {{ limit = {{ is_megastructure_type = ahw_gate_broken_{n} }} upgrade_megastructure_to = ahw_gate_{n} finish_upgrade = yes }}""" for n in range(1, PAIRS + 1))}
	}}
	if = {{
		limit = {{ has_star_flag = ahw_broken }}
		log = "AHW \\\\[This.GetName]: the scripted upgrade did not mark the gate repaired - marked now"
		ahw_mark_repaired = yes
	}}
	clear_global_event_target = ahw_script_repairer
}}

# this = a portal: its pair is open again.
ahw_unseal_pair = {{
{sw(lambda n: f'remove_global_flag = ahw_sealed_{n} clear_global_event_target = ahw_sealer_{n}')}
}}
'''


def gen_bypasses():
    out = [GENERATED, '''# (0.0.8) Field meanings: the header of vanilla's common/bypass/00_bypasses.txt.
# Entry points are 1:1: one scripted-connection type per pair (run 6). node = the empire's portal
# system (flag ahw_entry_N, and not ahw_broken: until repaired, 0.0.18), nexus = the ring system with
# that pair's exit (flag ahw_exit_N). windup_time = 10 stops detours through the ring (run 6);
# extends_sensors = yes shows the exit through a usable entry point (run 7).
''']
    for n in range(1, PAIRS + 1):
        out.append(bypass_block(
            f'ahw_link_{n}', 'AHW_LINK',
            f'has_star_flag = ahw_entry_{n} NOT = {{ has_star_flag = ahw_broken }}',
            f'has_star_flag = ahw_exit_{n}',
            tech=True, windup=10, lockable='no', sensors='yes', frame=25, effect='gateway',
            can_use=sealed_check(n)))
    for j in range(1, STATIONS + 1):
        out.append(bypass_block(
            f'ahw_express_{j}', 'AHW_EXPRESS',
            f'has_star_flag = ahw_xst_a_{j}', f'has_star_flag = ahw_xst_b_{j}',
            tech=False, windup=0, lockable='no', sensors='yes', frame=12, effect='wormhole',
            can_use=f'''
	country_can_use = {{
		custom_tooltip = {{
			fail_text = AHW_EXPRESS_CLOSED
			has_global_flag = ahw_express_open_{j}
		}}
	}}
'''))
    return ''.join(out)


def mega_block(key, entity, btype, kind, comment, n):
    """kind: 'broken' (portal gate before repair), 'gate' (its repaired stage, an upgrade - 0.1.0,
    user 2026-11-06: the repair is started on the gate), 'exit' (ring end)."""
    extra = '\n\tdismantle_potential = { always = no }'  # user, 2026-11-04: repaired once, never dismantled
    head = f'\tpotential = {{ always = no }}'
    if kind == 'broken':
        # vanilla's ruined gateways carry it; lets nomads work on a gate they do not own
        extra += '\n\tnomad_reactivatable = yes'
    if kind == 'gate':
        # as vanilla's gateway_restored (05_gateways.txt): potential in country scope, possible in
        # the system's, from = the country; on_build_complete: from = the country (absent when
        # script finishes the upgrade - then ahw_repairer is set by the caller)
        head = f'''	upgrade_from = {{
		ahw_gate_broken_{n}
	}}
	potential = {{
		OR = {{
			has_country_flag = ahw_highway_studied
			is_nomadic = yes
		}}
		# run 42: a nomad on our repair contract shuttled between the anchor (the contract's work)
		# and the portal - presumably to reactivate the gate whenever it had lost its owner
		# (save 2200.07.23: unowned; the monthly check gives it back). Under contract, the contract
		# is its only way to repair.
		NOT = {{ has_event_chain = ahw_contract_repair_gate_chain }}
	}}
	possible = {{
		custom_tooltip = {{
			fail_text = AHW_REPAIR_NEEDS_TECHS
			from = {{
				has_technology = ahw_tech_gate_theory
				has_technology = ahw_tech_gate_construction
			}}
		}}
	}}
	build_time = {REPAIR_DAYS}
	resources = {{
		category = megastructures
		cost = {{
			alloys = {REPAIR_ALLOYS}
			influence = {REPAIR_INFLUENCE}
		}}
	}}
	on_build_complete = {{
		# run 41: finished by script (the contract), `from` is the gate's owner, not the nomad -
		# ahw_repair_gate hands the real repairer over in a global target
		if = {{
			limit = {{ exists = event_target:ahw_script_repairer }}
			event_target:ahw_script_repairer = {{ save_event_target_as = ahw_repairer }}
		}}
		else_if = {{
			limit = {{ exists = from }}
			from = {{ save_event_target_as = ahw_repairer }}
		}}
		solar_system = {{ ahw_mark_repaired = yes }}
	}}'''
        # 0.0.20: the repaired gate can be sealed - a mode switch on the gate
        extra += ('\n\toverclock_loc_key = AHW_SEAL\n\toverclock_cooldown = 30'
                  '\n\toverclock_types = {\n\t\tahw_gate_open\n\t\tahw_gate_sealed\n\t}')
    return f'''
# {comment}
{key} = {{
	entity = "{entity}"
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	show_galactic_map_icon = no
	show_in_outliner = yes
	construction_blocks_and_blocked_by = none
	bypass_type = {btype}

{head}{extra}
}}
'''


def megastructures():
    """key -> (entity, bypass type, kind, comment, n, name, desc, outliner texture). The descs
    point at the object texts in ahw_l_english.yml (lore, 0.1.1), shared by every pair."""
    m = {}
    for n in range(1, PAIRS + 1):
        m[f'ahw_gate_broken_{n}'] = ('deactivated_gateway_entity', f'ahw_link_{n}', 'broken',
                                     f'Portal end of entry point {n}, broken (as spawned).', n,
                                     'Broken Highway Gate', '$AHW_LORE_GATE_BROKEN$', 'gateway_ruined')
        m[f'ahw_gate_{n}'] = ('reactivated_gateway_entity', f'ahw_link_{n}', 'gate',
                              f'Portal end of entry point {n}, repaired: an upgrade of the broken gate.', n,
                              'Highway Entry Point', '$AHW_LORE_GATE$', 'gateway')
        m[f'ahw_exitgate_{n}'] = ('reactivated_gateway_entity', f'ahw_link_{n}', 'exit',
                                  f'Ring end of entry point {n}: never dismantled.', n,
                                  'Highway Exit', '$AHW_LORE_EXITGATE$', 'gateway')
    for j in range(1, STATIONS + 1):
        m[f'ahw_xhole_{j}'] = ('natural_wormhole_entity', f'ahw_express_{j}', 'exit',
                               f'Express wormhole {j}: one at each of two neighbouring stations.', j,
                               'Express Wormhole', '$AHW_LORE_XHOLE$', 'gateway')
    return m


def gen_megastructures():
    out = [GENERATED, "# (0.0.8) Entities are vanilla's, referenced by name. Both ends of a pair\n# carry the same scripted-connection bypass, as lgate_base does.\n"]
    for key, (entity, btype, kind, comment, n, *_rest) in megastructures().items():
        out.append(mega_block(key, entity, btype, kind, comment, n))
    return ''.join(out)


def gen_gfx():
    out = [GENERATED, "# Outliner icons, pointing at the game's own gateway textures (referenced by path, nothing\n# copied). Without them: \"Trying to change sprite to unknown sprite\" (run 5).\nspriteTypes = {\n"]
    for key, (*_rest, tex) in megastructures().items():
        out.append(f'\tspriteType = {{\n\t\tname = "GFX_{key}_outliner_icon"\n\t\ttextureFile = "gfx/interface/icons/megastructures/{tex}.dds"\n\t}}\n')
    out.append('}\n')
    return ''.join(out)


def gen_loc():
    lines = ['l_english:']
    for key, what in [(f'AHW_LINK_{n}', 'Highway Entry Point') for n in range(1, PAIRS + 1)] + \
                     [(f'AHW_EXPRESS_{j}', 'Express Wormhole') for j in range(1, STATIONS + 1)]:
        lines += [f' BYPASS_{key}:0 "{what}"', f' ENTRY_BYPASS_{key}:0 "Enter the {what}"',
                  f' EXIT_BYPASS_{key}:0 "Exit the {what}"']
    for key, (*_rest, name, desc, _tex) in megastructures().items():
        lines += [f' {key}:0 "{name}"', f' {key}_DESC:0 "{desc}"',
                  f' {key}_MEGASTRUCTURE_DETAILS:0 "{desc}"']
    lines += [f' ahw_ring_{i}:0 "Highway Node {i}"' for i in range(1, MAX_NODES + 1)]
    for n in sorted(set(NODES.values())):
        lines += [f' {node_labels(n)[k]}:0 "{name}"' for k, name in node_names(n).items()]
    lines += [f' ahw_portal_{r}_{s}:0 "{portal_label(r, s)}"' for r in range(len(REACHES)) for s in range(1, PAIRS + 1)]
    return '\n'.join(lines) + '\n'


def compass(angle, var):
    """Moves the second centre probe COMPASS_R from the centre at angle; every regular system's
    distance to it into var."""
    return f'''	event_target:ahw_probe_t = {{
		move_system = {{ target = event_target:ahw_centre_system min_distance >= {COMPASS_R} max_distance <= {COMPASS_R} min_orientation_angle = {angle} max_orientation_angle = {angle} max_jumps = 0 hyperlane = no }}
		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_centre_system type = euclidean }} variable = ahw_cr }}
		log = "AHW outline: compass probe at angle {angle} is \\\\[This.ahw_cr] from the centre (want {COMPASS_R})"
	}}
	every_system = {{
		limit = {{ NOT = {{ has_star_flag = ahw_unclaimable }} }}
		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_probe_t type = euclidean }} variable = {var} }}
	}}'''


def to_coord(v):
    """v holds the distance d to the compass probe; ahw_t = r^2. v = (r^2 + C^2 - d^2) / 2C."""
    return f'''		set_variable = {{ which = ahw_u value = {v} }}
		multiply_variable = {{ which = ahw_u value = {v} }}
		set_variable = {{ which = {v} value = ahw_t }}
		change_variable = {{ which = {v} value = {COMPASS_R ** 2} }}
		subtract_variable = {{ which = {v} value = ahw_u }}
		divide_variable = {{ which = {v} value = {2 * COMPASS_R} }}'''


def outline_measure():
    return f'''
# The outline: x, y (ahw_x, ahw_y) and distance ahw_r of every regular system relative to the
# centre, by the law of cosines against the second centre probe placed {COMPASS_R} east, then north,
# of the centre; the farthest distance on the centre system (ahw_rmax). No scope.
ahw_measure_outline = {{
	event_target:ahw_centre_system = {{ set_variable = {{ which = ahw_rmax value = 0 }} }}
	every_system = {{
		limit = {{ NOT = {{ has_star_flag = ahw_unclaimable }} }}
		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_centre_system type = euclidean }} variable = ahw_r }}
	}}
{compass(0, 'ahw_x')}
{compass(90, 'ahw_y')}
	every_system = {{
		limit = {{ NOT = {{ has_star_flag = ahw_unclaimable }} }}
		set_variable = {{ which = ahw_t value = ahw_r }}
		multiply_variable = {{ which = ahw_t value = ahw_r }}
{to_coord('ahw_x')}
{to_coord('ahw_y')}
		set_star_flag = ahw_xy
		if = {{
			limit = {{ check_variable = {{ which = ahw_r value > event_target:ahw_centre_system.ahw_rmax }} }}
			event_target:ahw_centre_system = {{ set_variable = {{ which = ahw_rmax value = prev.ahw_r }} }}
		}}
	}}
	event_target:ahw_centre_system = {{
		log = "AHW outline: the farthest regular system is \\\\[This.ahw_rmax] from the centre"
	}}
}}
'''


def node_xy(node, radius, a):
    """Gives a ring node its coordinates (radius in direction a) for the portals' clearance."""
    return f'''		{node} = {{
			set_variable = {{ which = ahw_x value = {radius} }}
			multiply_variable = {{ which = ahw_x value = {round(math.cos(math.radians(a)), 4)} }}
			set_variable = {{ which = ahw_y value = {radius} }}
			multiply_variable = {{ which = ahw_y value = {round(math.sin(math.radians(a)), 4)} }}
			set_star_flag = ahw_xy
		}}'''


def ring_nodes(n):
    """[(k, angle)] for nodes 1..n, evenly round the ring from angle 0."""
    return list(enumerate([round(360 * k / n, 2) for k in range(n)], 1))


def node_names(n):
    """Node k -> its display name: the reach, then the node's number in that reach in octal,
    counted from 0 (Ashkara Node 0, ..., Belun Node 0, ...)."""
    names, seen = {}, {}
    for k, a in ring_nodes(n):
        r = int(a // REACH_DEG)
        names[k] = f'{REACHES[r]} Node {seen.get(r, 0):o}'
        seen[r] = seen.get(r, 0) + 1
    return names


def node_labels(n):
    return {k: f'ahw_node_{n}_{k}' for k, _ in ring_nodes(n)}


# Octants (0.0.25, run 23: the ring took 37 s on a medium galaxy): a system is only within
# OUTLINE_HALF of the nodes near its own direction, so each system first finds its octant (signs of
# x, y and which is larger) and tests only those nodes - about a fifth of the ring instead of all.
# Octant o holds the directions [45 o, 45 (o + 1)), with ahw_nx = -x, ahw_ny = -y.
OCTANTS = [
    'check_variable = { which = ahw_y value >= 0 } check_variable = { which = ahw_x value >= ahw_y }',
    'check_variable = { which = ahw_x value >= 0 } check_variable = { which = ahw_y value >= ahw_x }',
    'check_variable = { which = ahw_y value >= 0 } check_variable = { which = ahw_y value >= ahw_nx }',
    'check_variable = { which = ahw_y value >= 0 }',
    'check_variable = { which = ahw_x value < 0 } check_variable = { which = ahw_nx value >= ahw_ny }',
    'check_variable = { which = ahw_x value < 0 }',
    'check_variable = { which = ahw_y value < 0 } check_variable = { which = ahw_ny value >= ahw_x }',
    None,  # the rest: y < 0, x > -y
]


def octant_of(x, y):
    """Mirrors the OCTANTS if/else_if chain (for the self-check)."""
    nx, ny = -x, -y
    tests = [y >= 0 and x >= y, x >= 0 and y >= x, y >= 0 and y >= nx, y >= 0,
             x < 0 and nx >= ny, x < 0, y < 0 and ny >= x]
    return next((o for o, t in enumerate(tests) if t), 7)


def octant_nodes(n, o):
    """Nodes whose direction lies within OUTLINE_HALF (plus rounding slack) of octant o."""
    lo, hi = 45 * o - OUTLINE_HALF - 0.5, 45 * (o + 1) + OUTLINE_HALF + 0.5
    return [(k, a) for k, a in ring_nodes(n) if any(lo <= a + t <= hi for t in (-360, 0, 360))]


def check_octants():
    """Every node a system can belong to (projection >= r cos OUTLINE_HALF) is in its octant's list."""
    for n in set(NODES.values()):
        for i in range(3600):
            th = math.radians(i / 10)
            x, y = math.cos(th) * 100, math.sin(th) * 100
            got = {k for k, _ in octant_nodes(n, octant_of(x, y))}
            need = {k for k, a in ring_nodes(n)
                    if x * math.cos(math.radians(a)) + y * math.sin(math.radians(a))
                    >= 100 * math.cos(math.radians(OUTLINE_HALF))}
            assert need <= got, (n, i / 10, sorted(need - got))


def outer_ring(n):
    """The ring of n nodes round the outline, joined in order. No scope."""
    cos_half = round(math.cos(math.radians(OUTLINE_HALF)), 4)
    nodes = ring_nodes(n)
    init = '\n'.join(f'\t\tset_variable = {{ which = ahw_edge_{k} value = 0 }}' for k, _ in nodes)
    sector = lambda k, a: f'''		set_variable = {{ which = ahw_p value = ahw_x }}
		multiply_variable = {{ which = ahw_p value = {round(math.cos(math.radians(a)), 4)} }}
		set_variable = {{ which = ahw_q value = ahw_y }}
		multiply_variable = {{ which = ahw_q value = {round(math.sin(math.radians(a)), 4)} }}
		change_variable = {{ which = ahw_p value = ahw_q }}
		if = {{
			limit = {{
				check_variable = {{ which = ahw_p value >= ahw_h }}
				check_variable = {{ which = ahw_r value > event_target:ahw_centre_system.ahw_edge_{k} }}
			}}
			event_target:ahw_centre_system = {{ set_variable = {{ which = ahw_edge_{k} value = prev.ahw_r }} }}
		}}'''
    indent = lambda text: '\n'.join('\t' + line for line in text.split('\n'))
    sectors = '\n'.join(
        f'''		{'if' if o == 0 else 'else_if' if cond else 'else'} = {{
{f'			limit = {{ {cond} }}' + chr(10) if cond else ''}{indent(chr(10).join(sector(k, a) for k, a in octant_nodes(n, o)))}
		}}''' for o, cond in enumerate(OCTANTS))
    rads = '\n'.join(f'''		set_variable = {{ which = ahw_rad_{k} value = ahw_edge_{k} }}
		change_variable = {{ which = ahw_rad_{k} value = {RING_MARGIN} }}''' for k, _ in nodes)
    lift = lambda k, j: f'''		set_variable = {{ which = ahw_t value = ahw_rad_{j} }}
		subtract_variable = {{ which = ahw_t value = {RING_SLOPE} }}
		if = {{
			limit = {{ check_variable = {{ which = ahw_rad_{k} value < ahw_t }} }}
			set_variable = {{ which = ahw_rad_{k} value = ahw_t }}
		}}'''
    order = list(range(1, n + 1))
    smooth = '\n'.join([lift(k, (k - 2) % n + 1) for _ in range(2) for k in order]
                       + [lift(k, k % n + 1) for _ in range(2) for k in reversed(order)])
    label = node_labels(n)
    # 0.0.29: a timestamp every 10th spawn (the index keeps the lines unique), to see whether a
    # spawn gets dearer as the ring grows.
    spawns = '\n'.join(f'\t\tahw_spawn_outer_node = {{ K = {k} ANGLE = {a} LABEL = {label[k]} }}'
                       + (f'\n\t\tlog = "AHW timing: {i + 1} ring nodes spawned"' if (i + 1) % 10 == 0 else '')
                       for i, (k, a) in enumerate(nodes[:-2]))
    (kt, at), (ka, aa) = nodes[-2], nodes[-1]
    lanes = '\n'.join(f'\tadd_hyperlane = {{ from = event_target:ahw_ring_{k} to = event_target:ahw_ring_{k % n + 1} }}'
                      for k, _ in nodes)
    reaches = '\n'.join(f'\tevent_target:ahw_ring_{k} = {{ set_variable = {{ which = ahw_reach value = {int(a // REACH_DEG)} }} }}'
                         for k, a in nodes)
    logs = '\n'.join(f'''		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_ring_{k} type = euclidean }} variable = ahw_got_{k} }}
		log = "AHW node {k} at angle {a}: edge \\\\[This.ahw_edge_{k}], wanted \\\\[This.ahw_rad_{k}], placed \\\\[This.ahw_got_{k}] from the centre"
{node_xy(f'event_target:ahw_ring_{k}', f'prev.ahw_got_{k}', a)}''' for k, a in nodes[:-1])
    return f'''
# The outer ring of {n} nodes. A node's edge: the farthest regular system within {OUTLINE_HALF} degrees of
# its direction (none: the farthest overall); the node goes {RING_MARGIN} beyond it. No scope.
ahw_build_outer_ring_{n} = {{
	event_target:ahw_centre_system = {{
{init}
	}}
	every_system = {{
		limit = {{ NOT = {{ has_star_flag = ahw_unclaimable }} }}
		set_variable = {{ which = ahw_h value = ahw_r }}
		multiply_variable = {{ which = ahw_h value = {cos_half} }}
		set_variable = {{ which = ahw_nx value = 0 }}
		subtract_variable = {{ which = ahw_nx value = ahw_x }}
		set_variable = {{ which = ahw_ny value = 0 }}
		subtract_variable = {{ which = ahw_ny value = ahw_y }}
		# only the nodes near the system's own octant (0.0.25)
{sectors}
	}}
	event_target:ahw_centre_system = {{
		log = "AHW timing: ring edges found"
{rads}
		# smoothing: at most {RING_SLOPE} below a neighbour
{smooth}
		log = "AHW timing: ring smoothed"
{spawns}
		log = "AHW timing: ring nodes spawned"
		ahw_move_probe_to_node = {{ PROBE = ahw_probe_t K = {kt} ANGLE = {at} LABEL = {label[kt]} }}
{logs}
		ahw_move_probe_to_node = {{ PROBE = ahw_probe_a K = {ka} ANGLE = {aa} LABEL = {label[ka]} }}
{node_xy('event_target:ahw_ring_' + str(ka), 'ahw_rad_' + str(ka), aa)}
	}}
{lanes}
{reaches}
	set_global_flag = ahw_ring_size_{n}
	event_target:ahw_ring_1 = {{ set_variable = {{ which = ahw_pairs_max value = {PAIRS} }} }}
	event_target:ahw_ring_{ka} = {{
		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_ring_{kt} type = euclidean }} variable = ahw_dprev }}
		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_ring_1 type = euclidean }} variable = ahw_dnext }}
		log = "AHW node {ka} (the centre probe, moved): \\\\[This.ahw_dprev] from node {kt}, \\\\[This.ahw_dnext] from node 1 (a ring neighbour is ~35 away; ~300 = it did not move)"
	}}
}}
'''


def radius_chain(body):
    """if/else_if over ahw_rad_$K$, rounded down to RAD_STEP; body(r) -> effect text."""
    bins = list(range(RAD_MAX, RAD_MIN - 1, -RAD_STEP))
    chain = [f'''	{'if' if i == 0 else 'else_if'} = {{
		limit = {{ check_variable = {{ which = ahw_rad_$K$ value >= {r} }} }}
		{body(r)}
	}}''' for i, r in enumerate(bins)]
    chain.append(f'''	else = {{
		{body(RAD_MIN)}
	}}''')
    return '\n'.join(chain)


def spawn_outer_node():
    move = lambda r: (f'event_target:$PROBE$ = {{ move_system = {{ target = event_target:ahw_centre_system '
                      f'min_distance >= {r} max_distance <= {r} min_orientation_angle = $ANGLE$ '
                      f'max_orientation_angle = $ANGLE$ max_jumps = 0 hyperlane = no }} }}')
    return f'''
# this = the centre system: outer node $K$ at the radius ahw_rad_$K$, rounded down to {RAD_STEP}
# (spawn_system takes literal distances only), direction $ANGLE$.
ahw_spawn_outer_node = {{
''' + radius_chain(lambda r: f'ahw_spawn_ring_node = {{ NAME = ahw_ring_$K$ LABEL = $LABEL$ R = {r} ANGLE = $ANGLE$ }}') + f'''
}}

# this = the centre system: the centre probe $PROBE$ becomes outer node $K$ (as above). For the
# centre probe itself, move_system's target is the system being moved: the offset is from where
# it stands, the centre (checked in the log).
ahw_move_probe_to_node = {{
''' + radius_chain(move) + '''
	event_target:$PROBE$ = {
		remove_star_flag = ahw_core
		set_star_flag = ahw_ring
		ahw_rename_system = { KEY = $LABEL$ }
		save_global_event_target_as = ahw_ring_$K$
	}
}
'''


def size_switch():
    out = [f'''	{'if' if i == 0 else 'else_if'} = {{
		limit = {{ galaxy_size = {size} }}
		ahw_build_outer_ring_{n} = yes
	}}''' for i, (size, n) in enumerate(NODES.items())]
    out.append(f"\telse = {{\n\t\tahw_build_outer_ring_{NODES['medium']} = yes\n\t}}")
    return '\n'.join(out)


def portal_label(r, s):
    return f'{REACHES[r]} {r}{s:o}'


def portal_naming():
    """Names event_target:ahw_portal_tmp by the reach of ahw_node_tmp (see REACHES)."""
    by_reach = '\n'.join(f'''	{'if' if r == 0 else 'else_if'} = {{
		limit = {{ event_target:ahw_node_tmp = {{ check_variable = {{ which = ahw_reach value = {r} }} }} }}
		event_target:ahw_ring_1 = {{ change_variable = {{ which = ahw_portals_{r} value = 1 }} }}
		ahw_name_portal_in_reach = {{ R = {r} }}
	}}''' for r in range(len(REACHES)))
    by_count = '\n'.join(f'''	{'if' if s == 1 else 'else_if'} = {{
		limit = {{ event_target:ahw_ring_1 = {{ check_variable = {{ which = ahw_portals_$R$ value = {s} }} }} }}
		event_target:ahw_portal_tmp = {{ ahw_rename_system = {{ KEY = ahw_portal_$R$_{s} }} }}
	}}''' for s in range(1, PAIRS + 1))
    return f'''
# Names the portal event_target:ahw_portal_tmp after the reach of its exit node ahw_node_tmp and
# its number in that reach (counters ahw_portals_<reach> on ring node 1). No scope.
ahw_name_portal = {{
{by_reach}
}}

# The $R$th reach's next portal name, by the counter ahw_portals_$R$.
ahw_name_portal_in_reach = {{
{by_count}
}}
'''


def stations(n):
    """[(s, k, angle)]: express station s (1..STATIONS) on ring node k - a node near the middle of
    reach s - 1, moved by -1, 0 or +1 (seeded by n: a galaxy size always gets the same); never the
    last two nodes (the centre probes, moved into the ring)."""
    rng, nodes = random.Random(n), ring_nodes(n)
    angle, out = dict(nodes), []
    for r in range(STATIONS):
        ks = [k for k, a in nodes if int(a // REACH_DEG) == r and k < n - 1]
        k = min(max(ks[len(ks) // 2] + rng.choice((-1, 0, 1)), ks[0]), ks[-1])
        out.append((r + 1, k, angle[k]))
    return out


def express():
    """The express: built after the ring (needs the ahw_ring_<k> targets), woken, flickered,
    stabilised. Link j joins station j (end a, its outward wormhole) and station j + 1 (end b,
    its inward one)."""
    nxt = lambda j: j % STATIONS + 1
    prv = lambda s: (s - 2) % STATIONS + 1
    builders = []
    for n in sorted(set(NODES.values())):
        st = stations(n)
        flags = '\n'.join(f"""	event_target:ahw_ring_{k} = {{
		set_star_flag = ahw_station
		set_variable = {{ which = ahw_station value = {s} }}
		set_star_flag = ahw_xst_a_{s}
		set_star_flag = ahw_xst_b_{prv(s)}
	}}""" for s, k, a in st)
        holes = '\n'.join(f"""	event_target:ahw_ring_{k} = {{
		spawn_megastructure = {{ type = ahw_xhole_{s} orbit_distance = {EXPRESS_ORBIT} orbit_angle = {round(a)} }}
		spawn_megastructure = {{ type = ahw_xhole_{prv(s)} orbit_distance = {EXPRESS_ORBIT} orbit_angle = {round(a + 180) % 360} }}
		log = "AHW express station {s} in \\\\[This.GetName] (node {k})"
	}}""" for s, k, a in st)
        builders.append(f"""
# The express on a ring of {n} nodes: stations on nodes {', '.join(str(k) for _, k, _ in st)}. Flags first, then the
# wormholes (vanilla sets a scripted connection's flags before spawning its bypass). No scope.
ahw_build_express_{n} = {{
{flags}
{holes}
}}
""")
    switch = '\n'.join(f"""	{'if' if i == 0 else 'else_if'} = {{
		limit = {{ has_global_flag = ahw_ring_size_{n} }}
		ahw_build_express_{n} = yes
	}}""" for i, n in enumerate(sorted(set(NODES.values()))))
    flicker = '\n'.join(f"""	if = {{
		limit = {{ NOT = {{ has_global_flag = ahw_express_stable_{j} }} }}
		random = {{
			chance = {EXPRESS_FLIP}
			if = {{
				limit = {{ has_global_flag = ahw_express_open_{j} }}
				remove_global_flag = ahw_express_open_{j}
				log = "AHW express link {j} closed"
			}}
			else = {{
				set_global_flag = ahw_express_open_{j}
				log = "AHW express link {j} opened"
			}}
		}}
	}}""" for j in range(1, STATIONS + 1))
    stabilise = '\n'.join(f"""	if = {{
		limit = {{
			OR = {{ has_star_flag = ahw_xst_a_{j} has_star_flag = ahw_xst_b_{j} }}
			NOT = {{ has_global_flag = ahw_express_stable_{j} }}
		}}
		set_global_flag = ahw_express_stable_{j}
		set_global_flag = ahw_express_open_{j}
		log = "AHW express link {j} stable (from \\\\[This.GetName])"
	}}""" for j in range(1, STATIONS + 1))
    offer = '\n'.join(f"""	{'if' if s == 1 else 'else_if'} = {{
		limit = {{ check_variable = {{ which = ahw_station value = {s} }} }}
		event_target:ahw_insp_country = {{
			add_seen_bypass_type = ahw_express_{s}
			add_seen_bypass_type = ahw_express_{prv(s)}
		}}
		if = {{
			limit = {{
				has_global_flag = ahw_express_awake
				OR = {{
					NOT = {{ has_global_flag = ahw_express_stable_{s} }}
					NOT = {{ has_global_flag = ahw_express_stable_{prv(s)} }}
				}}
				event_target:ahw_insp_country = {{
					has_technology = ahw_tech_gate_theory
					NOT = {{ has_country_flag = ahw_xoffered_{s} }}
				}}
			}}
			event_target:ahw_insp_country = {{ set_country_flag = ahw_xoffered_{s} }}
			enable_special_project = {{ name = AHW_EXPRESS_STABILISE location = this owner = event_target:ahw_insp_country }}
			log = "AHW express: stabilising station {s} offered to \\\\[ahw_insp_country.GetName]"
		}}
	}}""" for s in range(1, STATIONS + 1))
    every = lambda body: '\n'.join(body(j) for j in range(1, STATIONS + 1))
    return ''.join(builders) + f"""
# The express for the ring built (flag ahw_ring_size_<n>). No scope.
ahw_build_express = {{
{switch}
}}

# Mid game: every link turns unstable (closed until its first flip). No scope.
ahw_express_wake = {{
	set_global_flag = ahw_express_awake
	log = "AHW express awake: {STATIONS} links unstable"
}}

# Monthly while awake: each link not stable flips open/closed with {EXPRESS_FLIP} %. No scope.
ahw_express_flicker = {{
{flicker}
}}

# this = a station: both its links stable, open for good.
ahw_stabilise_station = {{
{stabilise}
}}

# this = a station a fleet of event_target:ahw_insp_country entered: the country learns its two
# link types (a known destination needs them, run 4) and, once the express is awake and with Gate
# Theory, is offered the stabilising study there (once per station and country).
ahw_express_entered = {{
{offer}
}}

# Console: every link stable. No scope.
ahw_express_stabilise_all = {{
{every(lambda j: f"	set_global_flag = ahw_express_stable_{j}{chr(10)}	set_global_flag = ahw_express_open_{j}")}
	log = "AHW express: all links stable (console)"
}}
"""


def gen_effects():
    out = [GENERATED, '''# (0.0.14) 

# The outer ring round the galaxy (user, 2026-11-04), its node count by galaxy size. No scope;
# needs ahw_find_centre and ahw_measure_outline first.
ahw_build_outer_ring = {
''' + size_switch() + '''
}
''', outline_measure(), spawn_outer_node()]
    for n in sorted(set(NODES.values())):
        out.append(outer_ring(n))

    # nearest ring system to the portal (global event target ahw_portal_tmp) -> ahw_node_tmp
    chain = []
    for k, d in enumerate(NEAREST_STEPS):
        kw = 'if' if k == 0 else 'else_if'
        chain.append(f'''	{kw} = {{
		limit = {{ any_system = {{ has_star_flag = ahw_ring distance = {{ source = event_target:ahw_portal_tmp max_distance <= {d} type = euclidean }} }} }}
		random_system = {{
			limit = {{ has_star_flag = ahw_ring distance = {{ source = event_target:ahw_portal_tmp max_distance <= {d} type = euclidean }} }}
			save_global_event_target_as = ahw_node_tmp
		}}
	}}''')
    out.append('\n# The ring system nearest to event_target:ahw_portal_tmp -> event_target:ahw_node_tmp.\nahw_find_nearest_node = {\n' + '\n'.join(chain) + '\n}\n')

    # exit slot in the node: by the node's ahw_exits count
    slots = []
    for k, (orbit, angle) in enumerate(EXIT_SLOTS):
        kw = 'if' if k == 0 else 'else_if'
        slots.append(f'''		{kw} = {{
			limit = {{ check_variable = {{ which = ahw_exits value = {k} }} }}
			spawn_megastructure = {{ type = ahw_exitgate_$N$ orbit_distance = {orbit} orbit_angle = {angle} }}
		}}''')
    slots.append('''		else = {
			spawn_megastructure = { type = ahw_exitgate_$N$ orbit_distance = 150 orbit_angle = 45 }
		}''')
    out.append('''
# Pair $N$: flags first (run 4), then the gate in the portal (ahw_portal_tmp) and the exit in the
# nearest ring system (ahw_node_tmp), in the node's next free slot.
ahw_make_pair = {
	event_target:ahw_portal_tmp = {
		set_star_flag = ahw_entry_$N$
		set_variable = { which = ahw_pair value = $N$ }
	}
	event_target:ahw_node_tmp = {
		set_star_flag = ahw_exit_$N$
	}
	event_target:ahw_portal_tmp = {
''' + gate_by_angle() + '''
	}
	event_target:ahw_node_tmp = {
''' + '\n'.join(slots) + '''
		change_variable = { which = ahw_exits value = 1 }
	}
	log = "AHW pair $N$ built"
}
''')

    # pair switch by the counter on ring node 1
    sw = []
    for n in range(1, PAIRS + 1):
        kw = 'if' if n == 1 else 'else_if'
        sw.append(f'''	{kw} = {{
		limit = {{ event_target:ahw_ring_1 = {{ check_variable = {{ which = ahw_pairs value = {n} }} }} }}
		ahw_make_pair = {{ N = {n} }}
	}}''')
    sw.append('\telse = {\n\t\tlog = "AHW no entry-point type left (more empires than PAIRS)"\n\t}')
    # the study reveals only the studied portal's own exit node (0.0.26, design 2026-11-06: the
    # rest of the ring is explored by flying it); a gate needs its destination visited (run 4)
    rev = []
    for n in range(1, PAIRS + 1):
        kw = 'if' if n == 1 else 'else_if'
        rev.append(f'''	{kw} = {{
		limit = {{ check_variable = {{ which = ahw_pair value = {n} }} }}
		random_system = {{
			limit = {{ has_star_flag = ahw_exit_{n} }}
			event_target:ahw_studier = {{ set_visited = prev }}
		}}
	}}''')
    out.append('\n# this = a portal: event_target:ahw_studier learns where its gate leads (only that ring node).\n'
               'ahw_reveal_exit = {\n' + '\n'.join(rev) + '\n}\n')

    out.append('\n# The next pair, numbered by the counter ahw_pairs on ring node 1.\nahw_make_next_pair = {\n'
               '\tevent_target:ahw_ring_1 = { change_variable = { which = ahw_pairs value = 1 } }\n'
               + '\n'.join(sw) + '\n}\n')

    # centre finder
    bands = []
    for k, f in enumerate(INNERMOST_BANDS):
        kw = 'if' if k == 0 else 'else_if'
        bands.append(f'''	{kw} = {{
		limit = {{ any_system = {{ distance_to_core_percent < {f} NOT = {{ has_star_flag = ahw_unclaimable }} }} }}
		random_system = {{ limit = {{ distance_to_core_percent < {f} NOT = {{ has_star_flag = ahw_unclaimable }} }} save_global_event_target_as = ahw_inner_tmp }}
	}}''')
    steps = '\n'.join(f'\tahw_probe_step = {{ S = {st} }}' for st in CENTRE_STEPS for _ in range(CENTRE_TRIES))
    out.append('''
# Finds the galaxy's centre: two probe systems leapfrog corewards from the innermost system; the
# better one ends as event_target:ahw_centre_system. No scope.
ahw_find_centre = {
''' + '\n'.join(bands) + '''
	event_target:ahw_inner_tmp = {
		spawn_system = {
			min_distance = 20
			max_distance = 20
			max_jumps = 0
			direction = corewards
			initializer = ahw_core_init
			hyperlane = no
			effect = { save_global_event_target_as = ahw_probe_a }
		}
	}
	event_target:ahw_probe_a = {
		spawn_system = {
			min_distance = 10
			max_distance = 10
			max_jumps = 0
			direction = corewards
			initializer = ahw_core_init
			hyperlane = no
			effect = { save_global_event_target_as = ahw_probe_t }
		}
	}
	event_target:ahw_probe_a = { ahw_measure = yes }
	event_target:ahw_probe_t = { ahw_measure = yes }
''' + steps + '''
	event_target:ahw_probe_a = {
		save_global_event_target_as = ahw_centre_system
		log = "AHW centre: best probe at distance_to_core_percent \\\\[This.ahw_d] (0 = the centre)"
	}
}
''')

    out.append(portal_placement())

    out.append(portal_naming())
    out.append(seal_switches())
    learn = '\n'.join(f'\tadd_seen_bypass_type = ahw_link_{n}' for n in range(1, PAIRS + 1))
    out.append(f'\n# this = country: knows every highway bypass type (run 4).\nahw_learn_types = {{\n{learn}\n}}\n')
    out.append(inspection())
    out.append(express())
    return ''.join(out)


CLASSES = ['SCI', 'CON', 'MIL']  # study variants: the class of the ship that found it


def inspection():
    """0.0.40 (user, 2026-11-07): the inspection grants are studies (special projects), offered
    when a ship of a studied country enters a portal or ring node, for the class of that ship.
    Per-pair memory in country flags (one block per pair); all run in a system, with
    event_target:ahw_insp_country (or ahw_repairer) the country.
    Flags per pair n: ahw_entered_n (a ship of ours has entered a system with an end of gate n),
    ahw_eng_offered_n / ahw_insp_n (gate study offered / done), ahw_first_n (offered on the first
    entry: +10 %), ahw_repaired_n (we repaired it: no study), ahw_phys_offered_n / ahw_phys_n
    (centre study of portal n offered / done), ahw_bg_offered_n / ahw_bg_n (broken-gate study of
    portal n offered / done; 2026-11-19: a foreign portal with a broken gate gives one study, the
    centre's or the broken gate's, for the tech granted less so far - ahw.60)."""
    scan, entered, gates, repairer, scan_c, centre, scan_b, broken = ([] for _ in range(8))
    for n in range(1, PAIRS + 1):
        here = f'OR = {{ has_star_flag = ahw_entry_{n} has_star_flag = ahw_exit_{n} }}'
        scan.append(f"""	if = {{
		limit = {{
			{here}
			any_system = {{ has_star_flag = ahw_entry_{n} NOT = {{ has_star_flag = ahw_broken }} }}
			event_target:ahw_insp_country = {{ NOR = {{ has_country_flag = ahw_eng_offered_{n} has_country_flag = ahw_repaired_{n} }} }}
		}}
		event_target:ahw_insp_country = {{
			set_country_flag = ahw_eng_offered_{n}
			set_country_flag = ahw_offer_gate
			if = {{
				limit = {{ NOT = {{ has_country_flag = ahw_entered_{n} }} }}
				set_country_flag = ahw_first_{n}
			}}
		}}
	}}""")
        entered.append(f"""	if = {{
		limit = {{ {here} }}
		event_target:ahw_insp_country = {{ set_country_flag = ahw_entered_{n} }}
	}}""")
        gates.append(f"""	if = {{
		limit = {{
			{here}
			event_target:ahw_insp_country = {{ has_country_flag = ahw_eng_offered_{n} NOT = {{ has_country_flag = ahw_insp_{n} }} }}
		}}
		event_target:ahw_insp_country = {{
			set_country_flag = ahw_insp_{n}
			if = {{
				limit = {{ has_country_flag = ahw_first_{n} }}
				ahw_grant_tech = {{ TECH = ahw_tech_gate_construction VAR = ahw_got_construction PROGRESS = 0.10 }}
			}}
			else = {{
				ahw_grant_tech = {{ TECH = ahw_tech_gate_construction VAR = ahw_got_construction PROGRESS = 0.07 }}
			}}
		}}
		log = "AHW gate of pair {n} inspected in \\\\[This.GetName] by \\\\[ahw_insp_country.GetName]"
	}}""")
        repairer.append(f"""	if = {{
		limit = {{ check_variable = {{ which = ahw_pair value = {n} }} }}
		event_target:ahw_repairer = {{ set_country_flag = ahw_repaired_{n} }}
	}}""")
        scan_c.append(f"""	if = {{
		limit = {{
			check_variable = {{ which = ahw_pair value = {n} }}
			event_target:ahw_insp_country = {{ NOR = {{ has_country_flag = ahw_phys_offered_{n} has_country_flag = ahw_bg_offered_{n} }} }}
		}}
		event_target:ahw_insp_country = {{
			set_country_flag = ahw_phys_offered_{n}
			set_country_flag = ahw_offer_centre
		}}
	}}""")
        centre.append(f"""	if = {{
		limit = {{
			check_variable = {{ which = ahw_pair value = {n} }}
			event_target:ahw_insp_country = {{ has_country_flag = ahw_phys_offered_{n} NOT = {{ has_country_flag = ahw_phys_{n} }} }}
		}}
		event_target:ahw_insp_country = {{ set_country_flag = ahw_phys_{n} }}
		ahw_centre_grant = yes
	}}""")
        scan_b.append(f"""	if = {{
		limit = {{
			check_variable = {{ which = ahw_pair value = {n} }}
			event_target:ahw_insp_country = {{ NOR = {{ has_country_flag = ahw_phys_offered_{n} has_country_flag = ahw_bg_offered_{n} }} }}
		}}
		event_target:ahw_insp_country = {{
			set_country_flag = ahw_bg_offered_{n}
			set_country_flag = ahw_offer_broken
		}}
	}}""")
        broken.append(f"""	if = {{
		limit = {{
			check_variable = {{ which = ahw_pair value = {n} }}
			event_target:ahw_insp_country = {{ has_country_flag = ahw_bg_offered_{n} NOT = {{ has_country_flag = ahw_bg_{n} }} }}
		}}
		event_target:ahw_insp_country = {{
			set_country_flag = ahw_bg_{n}
			ahw_grant_tech = {{ TECH = ahw_tech_gate_construction VAR = ahw_got_construction PROGRESS = 0.07 }}
		}}
		log = "AHW broken gate of pair {n} inspected in \\\\[This.GetName] by \\\\[ahw_insp_country.GetName]"
	}}""")
    offer = lambda what: '\n'.join(
        [f"""	{'if' if k == 0 else 'else_if'} = {{
		limit = {{ event_target:ahw_finder = {{ is_ship_class = {cls} }} }}
		enable_special_project = {{ name = AHW_INSPECT_{what}_{c} location = this owner = event_target:ahw_insp_country }}
	}}""" for k, (c, cls) in enumerate(zip(CLASSES, ['shipclass_science_ship', 'shipclass_constructor', 'shipclass_military']))]
        + [f"""	else = {{
		enable_special_project = {{ name = AHW_INSPECT_{what}_SCI location = this owner = event_target:ahw_insp_country }}
	}}"""])
    j = '\n'.join
    return f"""
# this = a portal or ring node a ship (fleet event_target:ahw_finder) of event_target:ahw_insp_country
# entered: offer a gate study for the repaired gates here that we did not repair and were not
# offered yet (country flag ahw_offer_gate for the caller); +10 % if this is our first entry.
ahw_scan_gates = {{
{j(scan)}
}}

# this = as above: remember the entry (after the scans).
ahw_note_entered = {{
{j(entered)}
}}

# this = a foreign portal entered (as above): offer its centre study unless offered before
# (country flag ahw_offer_centre for the caller).
ahw_scan_centre = {{
{j(scan_c)}
}}

# this = a system: the study for the class of event_target:ahw_finder (science if none fits).
ahw_offer_gate_study = {{
{offer('GATE')}
}}
ahw_offer_centre_study = {{
{offer('CENTRE')}
}}
ahw_offer_broken_study = {{
{offer('BROKEN')}
}}

# this = a foreign portal with a broken gate entered (as above), when Gate Construction is the
# tech granted less so far (ahw.60): offer its broken-gate study instead of the centre's, unless
# either was offered before (country flag ahw_offer_broken for the caller).
ahw_scan_broken = {{
{j(scan_b)}
}}

# this = the portal of a finished broken-gate study: Gate Construction +7 %, once per portal.
ahw_inspect_broken = {{
{j(broken)}
}}

# this = the system of a finished gate study: Gate Construction +7 % (+10 % if offered on our
# first entry) per gate here whose study was offered and not done, once per gate.
ahw_inspect_gates = {{
{j(gates)}
}}

# this = a portal just repaired: its repairer remembers the pair (no inspection study for it).
ahw_flag_repairer = {{
{j(repairer)}
}}

# this = the portal of a finished centre study: Gate Theory by its centre's kind
# (ahw_centre_grant), once per portal.
ahw_inspect_centre = {{
{j(centre)}
}}
"""


def gen_events():
    """The studies' withdrawal, as events (0.0.41): abort_special_project in a scripted effect is
    checked before the special projects load - 13440 "Could not find project of type" lines in
    error.log per launch (run 39), though it works in play (run 38). Events load last."""
    abort_g, abort_c, abort_b = [], [], []
    for n in range(1, PAIRS + 1):
        here = f'OR = {{ has_star_flag = ahw_entry_{n} has_star_flag = ahw_exit_{n} }}'
        for out, what, offered, done, where in (
                (abort_g, 'GATE', 'eng_offered', 'insp', here),
                (abort_c, 'CENTRE', 'phys_offered', 'phys', f'has_star_flag = ahw_entry_{n}'),
                (abort_b, 'BROKEN', 'bg_offered', 'bg', f'has_star_flag = ahw_entry_{n}')):
            ab = '\n'.join(f'\t\t\t\t\tabort_special_project = {{ type = AHW_INSPECT_{what}_{c} location = prev }}'
                           for c in CLASSES)
            out.append(f"""\t\tif = {{
\t\t\tlimit = {{ has_country_flag = ahw_{offered}_{n} NOT = {{ has_country_flag = ahw_{done}_{n} }} }}
\t\t\tevery_system = {{
\t\t\t\tlimit = {{ {where} }}
\t\t\t\tprev = {{\t# the country again; its prev = the system
{ab}
\t\t\t\t}}
\t\t\t}}
\t\t}}""")
    j = '\n'.join
    return f"""# GENERATED by tools/gen.py - do not edit by hand.
namespace = ahw

# this = a country whose Gate Construction is capped or researched: withdraw its open gate and
# broken-gate studies (ahw_cap_check).
country_event = {{
\tid = ahw.66
\thide_window = yes
\tis_triggered_only = yes
\timmediate = {{
{j(abort_g)}
{j(abort_b)}
\t}}
}}

# this = a country whose Gate Theory is capped or researched: withdraw its open centre studies.
country_event = {{
\tid = ahw.67
\thide_window = yes
\tis_triggered_only = yes
\timmediate = {{
{j(abort_c)}
\t}}
}}
"""


def main():
    check_octants()
    files = {
        'common/bypass/ahw_bypasses.txt': gen_bypasses(),
        'common/megastructures/ahw_megastructures.txt': gen_megastructures(),
        'common/scripted_effects/ahw_generated_effects.txt': gen_effects(),
        'interface/ahw.gfx': gen_gfx(),
        'events/ahw_generated_events.txt': gen_events(),
    }
    for rel, text in files.items():
        (MOD / rel).write_text(text)
    (MOD / 'localisation/english/ahw_generated_l_english.yml').write_text(gen_loc(), encoding='utf-8-sig')
    print('wrote', len(files) + 1, 'files;', PAIRS, 'pairs; outer ring nodes', NODES)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Generate the repetitive parts of the Ancient Highway spike.

Writes into ancient_highway/ (paths relative to this script's repo):
  common/bypass/ahw_spike_bypasses.txt            one scripted-connection type per entry pair
  common/megastructures/ahw_spike_megastructures.txt  the two ends of every pair
  common/scripted_effects/ahw_spike_generated_effects.txt  outline, outer ring, pair switch, exit slots,
                                                   portal placement
  interface/ahw_spike.gfx                         outliner icons (vanilla textures by path)
  localisation/english/ahw_spike_generated_l_english.yml

Run it after changing the constants below; commit its output with it.
"""
import math
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
GATE_ORBIT = 230  # run 10: lane arrivals ~150, the orange outer circle ~255 (measured in a screenshot)

GENERATED = '# GENERATED by tools/gen_spike.py - edit the generator, not this file.\n'


def angle_switch(body, var='ahw_best_a'):
    """if/else_if over var (a portal angle) in the current scope; body(angle) -> effect text."""
    return '\n'.join(
        f'''		{'if' if k == 0 else 'else_if'} = {{
			limit = {{ check_variable = {{ which = {var} value = {a} }} }}
			{body(a)}
		}}''' for k, a in enumerate(PORTAL_ANGLES))


def gate_by_angle():
    return angle_switch(lambda a: f'spawn_megastructure = {{ type = ahw_spike_entry_gate_$N$ orbit_distance = {GATE_ORBIT} orbit_angle = {a} }}')


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
				initializer = ahw_spike_portal_init
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
		log = "AHW SPIKE portal placed off \\\\[This.GetName] at angle \\\\[This.ahw_best_a]: worst lane margin \\\\[This.ahw_best] (+15 = opposite every other lane, 0 = sideways, -15 = beside one; 1000 = no other lane; -''' + str(CLEAR_PENALTY) + ''' = too close to a system), nearest other system at squared distance \\\\[This.ahw_best_cl] (want >= ''' + str(CLEAR_MIN ** 2) + '''; 1000000 = none near)"
	}''')
    return '''
# Spawns the portal (-> ahw_portal_tmp) PORTAL_R from its anchor ahw_x_tmp, at the angle where its
# lane arrives farthest from the anchor's other lanes and no other system is closer than CLEAR_MIN.
# Computed from the outline's coordinates (ahw_x, ahw_y; flag ahw_xy), no moves (0.0.17).
ahw_spike_place_portal = {
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
			fail_text = AHW_SPIKE_GATE_SEALED
			OR = {{
				NOT = {{ has_global_flag = ahw_sealed_{n} }}
				ahw_spike_friend_of_sealer = {{ N = {n} }}
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
# (country_can_use of the pair's type, ahw_spike_friend_of_sealer).
ahw_spike_seal_pair_for = {{
{sw(lambda n: f'set_global_flag = ahw_sealed_{n} $COUNTRY$ = {{ save_global_event_target_as = ahw_sealer_{n} }}')}
}}

# this = a portal: its pair is sealed against everyone (console test ahw_spike.25).
ahw_spike_seal_pair_for_nobody = {{
{sw(lambda n: f'set_global_flag = ahw_sealed_{n} clear_global_event_target = ahw_sealer_{n}')}
}}

# this = a portal: its pair is open again.
ahw_spike_unseal_pair = {{
{sw(lambda n: f'remove_global_flag = ahw_sealed_{n} clear_global_event_target = ahw_sealer_{n}')}
}}
'''


def gen_bypasses():
    out = [GENERATED, '''# SPIKE (Phase 0, 0.0.8). Field meanings: the header of vanilla's common/bypass/00_bypasses.txt.
# Entry points are 1:1: one scripted-connection type per pair (run 6). node = the empire's portal
# system (flag ahw_entry_N, and not ahw_broken: until repaired, 0.0.18), nexus = the ring system with
# that pair's exit (flag ahw_exit_N). windup_time = 10 stops detours through the ring (run 6);
# extends_sensors = yes shows the exit through a usable entry point (run 7).
''']
    for n in range(1, PAIRS + 1):
        out.append(bypass_block(
            f'ahw_spike_entry_{n}', 'AHW_SPIKE_ENTRY',
            f'has_star_flag = ahw_entry_{n} NOT = {{ has_star_flag = ahw_broken }}',
            f'has_star_flag = ahw_exit_{n}',
            tech=True, windup=10, lockable='no', sensors='yes', frame=25, effect='gateway',
            can_use=sealed_check(n)))
    return ''.join(out)


def mega_block(key, entity, btype, ring_side, comment):
    extra = '\n\tdismantle_potential = { always = no }'  # user, 2026-11-04: repaired once, never dismantled
    if not ring_side:  # 0.0.20: the portal's gate can be sealed - a mode switch on the gate
        extra += ('\n\toverclock_loc_key = AHW_SEAL\n\toverclock_cooldown = 30'
                  '\n\toverclock_types = {\n\t\tahw_spike_gate_open\n\t\tahw_spike_gate_sealed\n\t}')
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

	potential = {{ always = no }}{extra}
}}
'''


def megastructures():
    """key -> (entity, bypass type, ring side, comment, name, desc, outliner texture)"""
    m = {}
    for n in range(1, PAIRS + 1):
        m[f'ahw_spike_entry_gate_{n}'] = ('deactivated_gateway_entity', f'ahw_spike_entry_{n}', False,
                                          f'Portal end of entry point {n}.',
                                          'Highway Entry Point', 'the portal end of an entry point.', 'gateway_ruined')
        m[f'ahw_spike_entry_exit_{n}'] = ('reactivated_gateway_entity', f'ahw_spike_entry_{n}', True,
                                          f'Ring end of entry point {n}: never dismantled.',
                                          'Highway Exit', 'the ring end of an entry point. Cannot be dismantled.', 'gateway')
    return m


def gen_megastructures():
    out = [GENERATED, "# SPIKE (Phase 0, 0.0.8). Entities are vanilla's, referenced by name. Both ends of a pair\n# carry the same scripted-connection bypass, as lgate_base does.\n"]
    for key, (entity, btype, ring_side, comment, *_rest) in megastructures().items():
        out.append(mega_block(key, entity, btype, ring_side, comment))
    return ''.join(out)


def gen_gfx():
    out = [GENERATED, "# Outliner icons, pointing at the game's own gateway textures (referenced by path, nothing\n# copied). Without them: \"Trying to change sprite to unknown sprite\" (run 5).\nspriteTypes = {\n"]
    for key, (*_rest, tex) in megastructures().items():
        out.append(f'\tspriteType = {{\n\t\tname = "GFX_{key}_outliner_icon"\n\t\ttextureFile = "gfx/interface/icons/megastructures/{tex}.dds"\n\t}}\n')
    out.append('}\n')
    return ''.join(out)


def gen_loc():
    lines = ['l_english:']
    for key in [f'AHW_SPIKE_ENTRY_{n}' for n in range(1, PAIRS + 1)]:
        what = 'Highway Entry Point'
        lines += [f' BYPASS_{key}:0 "{what}"', f' ENTRY_BYPASS_{key}:0 "Enter the {what}"',
                  f' EXIT_BYPASS_{key}:0 "Exit the {what}"']
    for key, (*_rest, name, desc, _tex) in megastructures().items():
        lines += [f' {key}:0 "{name}"', f' {key}_DESC:0 "SPIKE: {desc}"',
                  f' {key}_MEGASTRUCTURE_DETAILS:0 "SPIKE: {desc}"']
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
		log = "AHW SPIKE outline: compass probe at angle {angle} is \\\\[This.ahw_cr] from the centre (want {COMPASS_R})"
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
ahw_spike_measure_outline = {{
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
		log = "AHW SPIKE outline: the farthest regular system is \\\\[This.ahw_rmax] from the centre"
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
    spawns = '\n'.join(f'\t\tahw_spike_spawn_outer_node = {{ K = {k} ANGLE = {a} LABEL = {label[k]} }}'
                       + (f'\n\t\tlog = "AHW SPIKE timing: {i + 1} ring nodes spawned"' if (i + 1) % 10 == 0 else '')
                       for i, (k, a) in enumerate(nodes[:-2]))
    (kt, at), (ka, aa) = nodes[-2], nodes[-1]
    lanes = '\n'.join(f'\tadd_hyperlane = {{ from = event_target:ahw_ring_{k} to = event_target:ahw_ring_{k % n + 1} }}'
                      for k, _ in nodes)
    reaches = '\n'.join(f'\tevent_target:ahw_ring_{k} = {{ set_variable = {{ which = ahw_reach value = {int(a // REACH_DEG)} }} }}'
                         for k, a in nodes)
    logs = '\n'.join(f'''		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_ring_{k} type = euclidean }} variable = ahw_got_{k} }}
		log = "AHW SPIKE node {k} at angle {a}: edge \\\\[This.ahw_edge_{k}], wanted \\\\[This.ahw_rad_{k}], placed \\\\[This.ahw_got_{k}] from the centre"
{node_xy(f'event_target:ahw_ring_{k}', f'prev.ahw_got_{k}', a)}''' for k, a in nodes[:-1])
    return f'''
# The outer ring of {n} nodes. A node's edge: the farthest regular system within {OUTLINE_HALF} degrees of
# its direction (none: the farthest overall); the node goes {RING_MARGIN} beyond it. No scope.
ahw_spike_build_outer_ring_{n} = {{
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
		log = "AHW SPIKE timing: ring edges found"
{rads}
		# smoothing: at most {RING_SLOPE} below a neighbour
{smooth}
		log = "AHW SPIKE timing: ring smoothed"
{spawns}
		log = "AHW SPIKE timing: ring nodes spawned"
		ahw_spike_move_probe_to_node = {{ PROBE = ahw_probe_t K = {kt} ANGLE = {at} LABEL = {label[kt]} }}
{logs}
		ahw_spike_move_probe_to_node = {{ PROBE = ahw_probe_a K = {ka} ANGLE = {aa} LABEL = {label[ka]} }}
{node_xy('event_target:ahw_ring_' + str(ka), 'ahw_rad_' + str(ka), aa)}
	}}
{lanes}
{reaches}
	set_global_flag = ahw_ring_size_{n}
	event_target:ahw_ring_1 = {{ set_variable = {{ which = ahw_pairs_max value = {PAIRS} }} }}
	event_target:ahw_ring_{ka} = {{
		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_ring_{kt} type = euclidean }} variable = ahw_dprev }}
		export_trigger_value_to_variable = {{ trigger = distance parameters = {{ source = event_target:ahw_ring_1 type = euclidean }} variable = ahw_dnext }}
		log = "AHW SPIKE node {ka} (the centre probe, moved): \\\\[This.ahw_dprev] from node {kt}, \\\\[This.ahw_dnext] from node 1 (a ring neighbour is ~35 away; ~300 = it did not move)"
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
ahw_spike_spawn_outer_node = {{
''' + radius_chain(lambda r: f'ahw_spike_spawn_ring_node = {{ NAME = ahw_ring_$K$ LABEL = $LABEL$ R = {r} ANGLE = $ANGLE$ }}') + f'''
}}

# this = the centre system: the centre probe $PROBE$ becomes outer node $K$ (as above). For the
# centre probe itself, move_system's target is the system being moved: the offset is from where
# it stands, the centre (checked in the log).
ahw_spike_move_probe_to_node = {{
''' + radius_chain(move) + '''
	event_target:$PROBE$ = {
		remove_star_flag = ahw_core
		set_star_flag = ahw_ring
		ahw_spike_rename_system = { KEY = $LABEL$ }
		save_global_event_target_as = ahw_ring_$K$
	}
}
'''


def size_switch():
    out = [f'''	{'if' if i == 0 else 'else_if'} = {{
		limit = {{ galaxy_size = {size} }}
		ahw_spike_build_outer_ring_{n} = yes
	}}''' for i, (size, n) in enumerate(NODES.items())]
    out.append(f"\telse = {{\n\t\tahw_spike_build_outer_ring_{NODES['medium']} = yes\n\t}}")
    return '\n'.join(out)


def portal_label(r, s):
    return f'{REACHES[r]} {r}{s:o}'


def portal_naming():
    """Names event_target:ahw_portal_tmp by the reach of ahw_node_tmp (see REACHES)."""
    by_reach = '\n'.join(f'''	{'if' if r == 0 else 'else_if'} = {{
		limit = {{ event_target:ahw_node_tmp = {{ check_variable = {{ which = ahw_reach value = {r} }} }} }}
		event_target:ahw_ring_1 = {{ change_variable = {{ which = ahw_portals_{r} value = 1 }} }}
		ahw_spike_name_portal_in_reach = {{ R = {r} }}
	}}''' for r in range(len(REACHES)))
    by_count = '\n'.join(f'''	{'if' if s == 1 else 'else_if'} = {{
		limit = {{ event_target:ahw_ring_1 = {{ check_variable = {{ which = ahw_portals_$R$ value = {s} }} }} }}
		event_target:ahw_portal_tmp = {{ ahw_spike_rename_system = {{ KEY = ahw_portal_$R$_{s} }} }}
	}}''' for s in range(1, PAIRS + 1))
    return f'''
# Names the portal event_target:ahw_portal_tmp after the reach of its exit node ahw_node_tmp and
# its number in that reach (counters ahw_portals_<reach> on ring node 1). No scope.
ahw_spike_name_portal = {{
{by_reach}
}}

# The $R$th reach's next portal name, by the counter ahw_portals_$R$.
ahw_spike_name_portal_in_reach = {{
{by_count}
}}
'''


def gen_effects():
    out = [GENERATED, '''# SPIKE (Phase 0, 0.0.14).

# The outer ring round the galaxy (user, 2026-11-04), its node count by galaxy size. No scope;
# needs ahw_spike_find_centre and ahw_spike_measure_outline first.
ahw_spike_build_outer_ring = {
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
    out.append('\n# The ring system nearest to event_target:ahw_portal_tmp -> event_target:ahw_node_tmp.\nahw_spike_find_nearest_node = {\n' + '\n'.join(chain) + '\n}\n')

    # exit slot in the node: by the node's ahw_exits count
    slots = []
    for k, (orbit, angle) in enumerate(EXIT_SLOTS):
        kw = 'if' if k == 0 else 'else_if'
        slots.append(f'''		{kw} = {{
			limit = {{ check_variable = {{ which = ahw_exits value = {k} }} }}
			spawn_megastructure = {{ type = ahw_spike_entry_exit_$N$ orbit_distance = {orbit} orbit_angle = {angle} }}
		}}''')
    slots.append('''		else = {
			spawn_megastructure = { type = ahw_spike_entry_exit_$N$ orbit_distance = 150 orbit_angle = 45 }
		}''')
    out.append('''
# Pair $N$: flags first (run 4), then the gate in the portal (ahw_portal_tmp) and the exit in the
# nearest ring system (ahw_node_tmp), in the node's next free slot.
ahw_spike_make_pair = {
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
	log = "AHW SPIKE pair $N$ built"
}
''')

    # pair switch by the counter on ring node 1
    sw = []
    for n in range(1, PAIRS + 1):
        kw = 'if' if n == 1 else 'else_if'
        sw.append(f'''	{kw} = {{
		limit = {{ event_target:ahw_ring_1 = {{ check_variable = {{ which = ahw_pairs value = {n} }} }} }}
		ahw_spike_make_pair = {{ N = {n} }}
	}}''')
    sw.append('\telse = {\n\t\tlog = "AHW SPIKE no entry-point type left (more empires than PAIRS)"\n\t}')
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
               'ahw_spike_reveal_exit = {\n' + '\n'.join(rev) + '\n}\n')

    out.append('\n# The next pair, numbered by the counter ahw_pairs on ring node 1.\nahw_spike_make_next_pair = {\n'
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
    steps = '\n'.join(f'\tahw_spike_probe_step = {{ S = {st} }}' for st in CENTRE_STEPS for _ in range(CENTRE_TRIES))
    out.append('''
# Finds the galaxy's centre: two probe systems leapfrog corewards from the innermost system; the
# better one ends as event_target:ahw_centre_system. No scope.
ahw_spike_find_centre = {
''' + '\n'.join(bands) + '''
	event_target:ahw_inner_tmp = {
		spawn_system = {
			min_distance = 20
			max_distance = 20
			max_jumps = 0
			direction = corewards
			initializer = ahw_spike_core_init
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
			initializer = ahw_spike_core_init
			hyperlane = no
			effect = { save_global_event_target_as = ahw_probe_t }
		}
	}
	event_target:ahw_probe_a = { ahw_spike_measure = yes }
	event_target:ahw_probe_t = { ahw_spike_measure = yes }
''' + steps + '''
	event_target:ahw_probe_a = {
		save_global_event_target_as = ahw_centre_system
		log = "AHW SPIKE centre: best probe at distance_to_core_percent \\\\[This.ahw_d] (0 = the centre)"
	}
}
''')

    out.append(portal_placement())

    out.append(portal_naming())
    out.append(seal_switches())
    learn = '\n'.join(f'\tadd_seen_bypass_type = ahw_spike_entry_{n}' for n in range(1, PAIRS + 1))
    out.append(f'\n# this = country: knows every highway bypass type (run 4).\nahw_spike_learn_types = {{\n{learn}\n}}\n')
    out.append(inspection())
    return ''.join(out)


def inspection():
    """0.0.39 (design 2026-11-06): the exploration and inspection grants keep per-pair memory in
    country flags, so they need one block per pair. All run in a system, with
    event_target:ahw_insp_country (or ahw_repairer) the country."""
    first, gates, repairer, centre = [], [], [], []
    for n in range(1, PAIRS + 1):
        here = f'OR = {{ has_star_flag = ahw_entry_{n} has_star_flag = ahw_exit_{n} }}'
        first.append(f'''	if = {{
		limit = {{ {here} }}
		event_target:ahw_insp_country = {{ set_timed_country_flag = {{ flag = ahw_first_{n} days = 30 }} }}
	}}''')
        gates.append(f'''	if = {{
		limit = {{
			{here}
			any_system = {{ has_star_flag = ahw_entry_{n} NOT = {{ has_star_flag = ahw_broken }} }}
			event_target:ahw_insp_country = {{ NOR = {{ has_country_flag = ahw_insp_{n} has_country_flag = ahw_repaired_{n} }} }}
		}}
		event_target:ahw_insp_country = {{
			set_country_flag = ahw_insp_{n}
			if = {{
				limit = {{ has_country_flag = ahw_first_{n} }}
				ahw_spike_grant_tech = {{ TECH = ahw_tech_gate_construction VAR = ahw_got_construction PROGRESS = 0.07 }}
			}}
			else = {{
				ahw_spike_grant_tech = {{ TECH = ahw_tech_gate_construction VAR = ahw_got_construction PROGRESS = 0.05 }}
			}}
		}}
		log = "AHW SPIKE gate of pair {n} inspected in \\\\[This.GetName] by \\\\[ahw_insp_country.GetName]"
	}}''')
        repairer.append(f'''	if = {{
		limit = {{ check_variable = {{ which = ahw_pair value = {n} }} }}
		event_target:ahw_repairer = {{ set_country_flag = ahw_repaired_{n} }}
	}}''')
        centre.append(f'''	if = {{
		limit = {{
			check_variable = {{ which = ahw_pair value = {n} }}
			event_target:ahw_insp_country = {{ NOT = {{ has_country_flag = ahw_phys_{n} }} }}
		}}
		event_target:ahw_insp_country = {{ set_country_flag = ahw_phys_{n} }}
		ahw_spike_centre_grant = yes
	}}''')
    return ('''
# this = a system an empire's ship entered for the first time: remember it 30 days per pair whose
# gate is here (either end), for the +7 % (on_entering_system_first_time, ahw_spike.62).
ahw_spike_mark_first_entry = {
''' + '\n'.join(first) + '''
}

# this = a system where a fleet of event_target:ahw_insp_country stayed 10 days (ahw_spike.61):
# Gate Construction +5 % (+7 % after a first entry) per repaired gate here that the country did
# not repair itself, once per gate (either end).
ahw_spike_inspect_gates = {
''' + '\n'.join(gates) + '''
}

# this = a portal just repaired: its repairer remembers the pair (no inspection grant for it).
ahw_spike_flag_repairer = {
''' + '\n'.join(repairer) + '''
}

# this = a foreign portal where a fleet of event_target:ahw_insp_country stayed 10 days: Gate
# Theory by its centre's kind, once per portal (ahw_spike_centre_grant).
ahw_spike_inspect_centre = {
''' + '\n'.join(centre) + '''
}
''')


def main():
    check_octants()
    files = {
        'common/bypass/ahw_spike_bypasses.txt': gen_bypasses(),
        'common/megastructures/ahw_spike_megastructures.txt': gen_megastructures(),
        'common/scripted_effects/ahw_spike_generated_effects.txt': gen_effects(),
        'interface/ahw_spike.gfx': gen_gfx(),
    }
    for rel, text in files.items():
        (MOD / rel).write_text(text)
    (MOD / 'localisation/english/ahw_spike_generated_l_english.yml').write_text(gen_loc(), encoding='utf-8-sig')
    print('wrote', len(files) + 1, 'files;', PAIRS, 'pairs; outer ring nodes', NODES)


if __name__ == '__main__':
    main()

# Ancient Highway

A Stellaris gameplay mod (game **4.5.x**, working title): a ring of artificial, unclaimable systems
around the galactic core, joined by hyperlanes and a few wormhole shortcuts, reachable from the
regular galaxy through entry points that must be studied, repaired and researched before use. The
point: empires stop being landlocked — help for a distant ally becomes possible. Full mechanics:
`docs/design.md`; lore (open): `docs/lore.md`.

The user's original idea and requirements are kept verbatim in `IDEA.md` on the branch `idea`
(orphan, pushed, **never merged**, never edited). This file and `docs/` are the living design.

Private for now. Workshop search 2026-11-03 found nothing alike: the nearest is *Wild Space*
(uncolonisable systems in the core and rim, no travel mechanics); *Interstellar Highways* and
*Evolving HyperLanes* are about starbases and manipulating existing lanes, and look unmaintained.

The shippable mod will live in `ancient_highway/` — only that subfolder gets linked into the game
(`../scripts/link-mod.sh stellaris-mod-AncientHighway/ancient_highway`). Dev docs stay at the top
level. Prefix every key, id, flag and variable with `ahw_`. Tested in game on Linux only.

---

## Status (2026-11-03): Phase 0 spike written, not yet run in game

`ancient_highway/` holds **only the spike** (`*spike*` files, version `0.0.1-SPIKE`). Every name
used was checked against the game's own script documentation (`logs/script_documentation/` in the
Stellaris user dir, 4.5.3); how the engine *behaves* with them is what the spike finds out.

| Console | Does |
|---|---|
| `event ahw_spike.1` | picks an anchor system at 25–40 % from the core; spawns six ring systems (black holes standing in for the artificial centre) chained from it, 40 apart, turning 60° per step; joins them by hyperlanes into a loop, with **no** hyperlane to the galaxy; puts an entry point between anchor and ring 1 (a megastructure at each end, ring end at orbit 300, bypasses linked) and a shortcut wormhole pair ring 1 (orbit 300) ↔ ring 4 (orbit 450); reports. Runs once per game |
| `event ahw_spike.2` | report only |
| `event ahw_spike.3` | `lock_bypass` the anchor's entry point for the player, 360 days; report |
| `event ahw_spike.4` | `remove_megastructure` the anchor's entry point; report now and a day later |
| `research_technology ahw_tech_spike` | the tech the entry points require |

All findings go to `game.log`, lines starting `AHW SPIKE`.

**Test** (Linux, launcher closed: `../scripts/link-mod.sh stellaris-mod-AncientHighway/ancient_highway`,
then enable it in a playset of its own). A new game, small **elliptical** galaxy; console on;
`debugtooltip`.
1. `event ahw_spike.1`. Screenshot the galaxy map around the anchor (named in the event window).
   *Answers:* where did the ring land (hexagon = absolute angles), its `distance_to_core_percent`
   values in the log (0 or missing = the export does not work for that trigger, not a wrong place).
2. Send a science ship to the anchor and order it to ring 1 **without** the tech: refused? Then
   `research_technology ahw_tech_spike` and again. *Answers:* is the entry point linked and gated.
3. In ring 1: screenshot the system view. Where are the entry point (orbit 300), the shortcut
   (orbit 300, opposite), and where do ships arriving from ring 2 and ring 6 appear? Fly from the
   entry point to the shortcut: through the centre or around? Take the shortcut to ring 4 (orbit
   450 there: did it spawn that far out?).
4. Try to build an outpost in a ring system with a construction ship: refused, with "The Ancient
   Highway cannot be claimed"? *Answers:* does the single-key game rule override win.
5. `event ahw_spike.3`, then try to pass with a ship of another empire (or check the bypass
   tooltip). *Answers:* does `lock_bypass` work on our bypass type.
6. `event ahw_spike.4`, wait a day, `event ahw_spike.2`. *Answers:* does the bypass go with the
   megastructure, and what happens to the ring end (dangling? still listed?).
7. Save, reload, `event ahw_spike.2`: does it all survive a reload?
8. Copy `logs/game.log` and `logs/error.log` before restarting the game, plus the screenshots.

Expected noise in `error.log`: a missing icon for `ahw_tech_spike` and missing portraits. Anything
naming an `ahw_` key otherwise is a finding. Record the findings here and in
`../stellaris-modding-insights` (proposed, not silently); delete the spike files once Phase 1 starts.

## Feasibility (game files 4.5.3, build 7793)

Paths are relative to the game install. "Spike" marks what only an in-game test can settle.

| Need | Building block | Verdict |
|---|---|---|
| Spawn the ring at game start | `spawn_system = { min_distance max_distance (0–100, relative to the scope) min_orientation_angle max_orientation_angle initializer hyperlane = no }` (used in `common/scripted_effects/01_start_of_game_effects.txt`, Unplugged origin), then `add_hyperlane` / `remove_hyperlane` | Feasible: chain each ring system from the previous one. **Spike:** is the angle absolute (map) or relative? How far can one step go? |
| Place it around the core | Every galaxy shape has an empty core of `core_radius_perc` 0.2–0.3 of the radius (`map/galaxy/galaxy_shapes.txt`); trigger `distance_to_core_percent` (0 = centre, 100 = rim) | Natural spot: just inside the core's edge — few existing systems and lanes to collide with |
| Shortcuts scaled by galaxy size | trigger `galaxy_size`; `spawn_natural_wormhole = { bypass_type = … }` + `link_wormholes` (`common/scripted_effects/fallen_empire_scripted_effects.txt`, `give_…` wormhole pair) | Feasible, with our own bypass type if needed |
| Ring systems stay neutral | game rules `can_build_starbase_around` and `can_add_claim` (`common/game_rules/00_rules.txt`), gated on a star flag `ahw_ring` | Feasible, but **overrides vanilla game rules** — one key each; a compat risk with mods touching the same rule |
| Entry points: broken → studied → repaired | ruined → restored megastructure pattern (`gateway_ness_ruined`/`_restored` in `common/megastructures/05_gateways.txt`, `hyper_relay_ruined` in `14_hyper_relay.txt`); study via special project or situation | Feasible |
| Using them needs a tech | own `bypass_type` with `prerequisites = { ahw_tech_… }` and `country_can_use` (`common/bypass/00_bypasses.txt`, its header documents every field) | Feasible |
| Exit only where repaired | the regular-side bypass exists only once its entry point is repaired; the pair is spawned and linked at repair | Feasible. **Spike:** how to remove a bypass on disable — there is no `remove_bypass` effect; dismantling a megastructure that carries `bypass_type` is the candidate |
| Disable at a cost, or lock | megastructure `dismantle_cost`; `can_bypass_be_locked = yes` + effect `lock_bypass = { country duration }`, rule `can_lock_bypass` (system owner, overlord, nomad waystation) — this is what the astral action uses | Feasible |
| The ring side can't be disabled | `dismantle_potential = { always = no }`, and nobody owns the system | Feasible |
| Hyper relays in neutral space | vanilla `hyper_relay`'s `possible` needs own borders (or a subject's / a nomad waystation); `connection_type = hyper_relay` links relays in adjacent systems | Feasible with an own megastructure (`ahw_highway_relay`, `bypass_type = relay_bypass`) instead of overriding the vanilla one; alternatively ruined relays pre-placed on the ring |
| Large ring systems, exit points far apart (little accidental fighting) | system initializers and `spawn_megastructure` / `spawn_natural_wormhole` take `orbit_distance` and `orbit_angle`; vanilla's farthest is the L-Gate at `orbit_distance = 360` (`common/solar_system_initializers/distant_stars_initializers.txt`); combat starts within `COMBAT_DETECT_RANGE_MULT` (1.05) × weapon range (`common/defines/00_defines.txt`) | Likely feasible. **Spike:** the largest usable orbit; where hyperlane arrival points land in a large system; whether flights between exit points cross the centre |
| Ring "above/below" the galaxy | static galaxies take a `z` coordinate; `spawn_system` and `move_system` take none | **Likely not feasible** at runtime. Look distinct instead: own star class, a nebula, the artificial centre object |
| AI uses the highway | unknown whether AI pathfinding takes custom bypasses into account | Open — test once something runs |

Alternative kept in mind: a `scripted_connection` bypass (as the L-gates and the Shroud tunnels do:
nodes by star flag or starbase building, a nexus that reaches *every* node). Too strong for entry
points (any ring system → any repaired entry galaxy-wide), but a candidate for an "express" layer.

## Decided (2026-11-03)

- Name *Ancient Highway*, prefix `ahw_`, repo `stellaris-mod-AncientHighway` (private).
- Round galaxies (elliptical, ring) first; spirals and others later or never.
- The ring is never claimable. Ring-side ends of entry points can't be damaged or disabled.
- Entry points start broken; the regular-side end can be disabled (cost) or locked by its owner.
- Ring systems are large, their exit points far apart on a wide outer orbit, so empires passing
  through can mostly avoid one another (`docs/design.md`, "The ring").

## Open questions

See `docs/design.md`, "Open questions". The main ones: who repairs an entry point (any empire, or
only the regular-side system's owner); how many entry points per ring system; whether the ring
gets pre-placed relays; how the shortcut count scales; lore (`docs/lore.md`).

## Plan

- **Phase 0 — spike**: written; what it does and the test are under "Status".
- **Phase 1** — game-start generation for all sizes, entry-point lifecycle (study → research →
  repair → use), neutrality rules, localisation.
- **Phase 2** — relays, shortcuts, events and lore, AI.

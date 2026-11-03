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

## Status (2026-11-03): Phase 0 spike, third version (`0.0.3-SPIKE`) not yet run

`ancient_highway/` holds **only the spike** (`*spike*` files). Every name used was checked
against the game's own script documentation (`logs/script_documentation/` in the Stellaris user
dir, 4.5.3); how the engine *behaves* with them is what the spike finds out. Runs 1 and 2 below.

| Console | Does |
|---|---|
| `event ahw_spike.1` | logs how empty the core is; spawns six ring systems (black holes standing in for the artificial centre) next to **our capital** (A), 40 apart, a closed loop of hyperlanes with **no** hyperlane to the galaxy; entry points of ring 1 (the nexus, ring end at orbit 300): A and a neighbour B **repaired**, another neighbour C **broken**; a shortcut wormhole pair ring 1 (orbit 300) ↔ ring 4 (orbit 450); reports. Runs once per game |
| `event ahw_spike.2` | report only |
| `event ahw_spike.3` | `lock_bypass` A's entry point for us, 360 days |
| `event ahw_spike.4` | close A's entry point (remove its "open" flag) |
| `event ahw_spike.5` | reopen it |
| `event ahw_spike.6` | tear down A's entry-point megastructure; report now and a day later |
| `research_technology ahw_tech_spike` | the tech the entry points require |

All findings go to `game.log`, lines starting `AHW SPIKE`; the event window names A, B and C.

**Test** (Linux, launcher closed: `../scripts/link-mod.sh stellaris-mod-AncientHighway/ancient_highway`,
then a playset with only this mod). A new game, small **elliptical** galaxy; console on.
1. `event ahw_spike.1`. Screenshot the galaxy map around the capital.
2. Without the tech: order the science ship from A to ring 1 (the black hole whose system holds
   the ring end). Refused? Then `research_technology ahw_tech_spike` and again. Hover over the
   entry point: where does it lead? *Answers:* does the scripted connection work, and is it gated.
3. From ring 1, can the ship go to B (repaired) and to C (broken)? Can it jump from A to B
   directly through the entry points (it should not: nodes reach only the nexus)?
4. In ring 1: screenshot the system view. Where are the ring end (orbit 300) and the shortcut
   (orbit 300, opposite); where do ships arriving from ring 2 and ring 6 appear? Fly from the ring
   end to the shortcut: through the centre or around? Take the shortcut to ring 4 (orbit 450
   there: did it spawn that far out?).
5. Construction ship: try to build an outpost in a ring system. Refused, with "The Ancient
   Highway cannot be claimed"? *Answers:* does the single-key game rule override win.
6. `event ahw_spike.4`: can ships still go from A into the ring? From ring 1 to A?
   `event ahw_spike.5`: open again? *Answers:* is the node trigger re-checked during play.
7. `event ahw_spike.3`: does the entry point show a lock, and does pathing for another empire's
   ship change (check the tooltip)? *Answers:* does `lock_bypass` work on our bypass type.
8. `event ahw_spike.6`, wait a day, `event ahw_spike.2`: is A cut off from the ring?
9. Save, reload, `event ahw_spike.2`: does it all survive a reload?
10. Copy `logs/game.log` and `logs/error.log` before restarting the game, plus the screenshots.

**Run 1 (2026-11-03, 4.5.3 open beta, elliptical galaxy, `0.0.1-SPIKE`): stopped at the anchor.**
- `random_system` with `distance_to_core_percent` 25–40 matched **nothing**, although the
  galaxy map shows plenty of stars there. Every later step ran on an undefined target, so nothing
  was spawned. Vanilla never uses this trigger. `0.0.2-SPIKE` logs what it returns on systems and
  on stars at < 10/25/40/60/101 %, and falls back to a star, then to the capital system.
- In a scripted effect with parameters, `[` in a `log` string must be written `\\[` (as vanilla's
  `common/scripted_effects/00_scripted_effects.txt` does); unescaped, error.log reports
  "Invalid macro entry … his.GetName".
- Bypass types need `BYPASS_<NAME>`, `ENTRY_BYPASS_<NAME>`, `EXIT_BYPASS_<NAME>` localisation;
  megastructures need `<key>_MEGASTRUCTURE_DETAILS`.
- The "Core / Inner Rim / Mid Rim / Outer Rim" rings on the run-1 screenshots come from a **UI
  mod**, not the game: they say nothing about `core_radius_perc` or `distance_to_core_percent`.
  Only the bright centre visibly has no stars, and it is small — whether the empty core is large
  enough for the ring is still open, per shape and size. Spike runs go with the other mods off.

**Run 2 (2026-11-03, same setup, other mods off, `0.0.2-SPIKE`): ring spawned, entry point not
linked.** Screenshots `2026_11_03_5`–`7` in the game's screenshot folder.
- **`distance_to_core_percent` is a fraction 0–1, not a percent** (despite its name and the
  documentation's example `< 60`): every threshold from 10 to 101 matched, Sol logs `0.75941`,
  the ring systems `0.69`–`0.89`. Use e.g. `< 0.4`. Run 1 failed on this, not on scope.
- **`spawn_system` orientation angles are absolute map directions**: six steps of 40 at 0°, 60°,
  …, 300° made a closed regular hexagon (galaxy map, `_6`). One step had to drop the 10-unit
  spacing (`SPAWN_SYSTEM_BUFFER_DISTANCE`, error.log), so a ring needs room.
- The ring's hyperlanes don't show on the galaxy map before exploration (`is_discovered = yes`
  shows the systems, not their lanes).
- **`link_wormholes` refuses megastructure bypasses**: "link_wormholes can be used only on
  wormholes (invalid from)". The script logged "linked" regardless; the entry point is
  unusable, so the ring was unreachable and steps 2–7 were not run. A natural-wormhole pair of
  our own type (the shortcut) linked without error.
- Next: entry points as megastructures with a **`scripted_connection`** bypass (as the L-gates):
  one bypass type per ring system, its nexus that ring system (star flag), its nodes the regular
  systems whose entry point is repaired. Nodes reach only the nexus, so "exit only where
  repaired" comes from the node trigger, and tearing down stays `remove_megastructure`.
- `$PARAM$` inside a `log` string next to `\\[` comes out mangled (`AHW SPIKEanchor$:`) —
  cosmetic.

Expected noise in `error.log`: a missing icon for `ahw_tech_spike` and missing portraits. Anything
naming an `ahw_` key otherwise is a finding. Record the findings here and in
`../stellaris-modding-insights` (proposed, not silently); delete the spike files once Phase 1 starts.

## Feasibility (game files 4.5.3, build 7793)

Paths are relative to the game install. "Spike" marks what only an in-game test can settle.

| Need | Building block | Verdict |
|---|---|---|
| Spawn the ring at game start | `spawn_system = { min_distance max_distance (0–100, relative to the scope) min_orientation_angle max_orientation_angle initializer hyperlane = no }`, then `add_hyperlane` | **Works (run 2)**: the angle is an absolute map direction; six steps closed a hexagon. Needs room: one step dropped the 10-unit spacing |
| Place it around the core | `core_radius_perc` 0.2–0.3 per shape (`map/galaxy/galaxy_shapes.txt`); trigger `distance_to_core_percent` — **a fraction 0–1** (run 2) | Open: how empty the core really is; run 3 logs it |
| Shortcuts scaled by galaxy size | trigger `galaxy_size`; `spawn_natural_wormhole = { bypass_type = … }` + `link_wormholes` (`common/scripted_effects/fallen_empire_scripted_effects.txt`, `give_…` wormhole pair) | Feasible, with our own bypass type if needed |
| Ring systems stay neutral | game rules `can_build_starbase_around` and `can_add_claim` (`common/game_rules/00_rules.txt`), gated on a star flag `ahw_ring` | Feasible, but **overrides vanilla game rules** — one key each; a compat risk with mods touching the same rule |
| Entry points: broken → studied → repaired | ruined → restored megastructure pattern (`gateway_ness_ruined`/`_restored` in `common/megastructures/05_gateways.txt`, `hyper_relay_ruined` in `14_hyper_relay.txt`); study via special project or situation | Feasible |
| Using them needs a tech | own `bypass_type` with `prerequisites = { ahw_tech_… }` and `country_can_use` (`common/bypass/00_bypasses.txt`, its header documents every field) | Feasible |
| Exit only where repaired | **`scripted_connection` bypass** (L-gates, Shroud tunnels): one type per ring system, nexus = that ring system, node = a regular system flagged repaired; `link_wormholes` refuses megastructure bypasses (run 2) | Run 3: does removing the flag close it during play |
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

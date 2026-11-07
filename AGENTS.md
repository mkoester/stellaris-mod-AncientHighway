# Ancient Highway

A Stellaris gameplay mod (game **4.5.x**, working title): a ring of artificial, unclaimable systems
**around the outside of the galaxy**, joined by hyperlanes, reachable from the regular galaxy through entry points that must be studied, repaired and researched before use. The
point: empires stop being landlocked — a second way to get everywhere that closed borders cannot
block for good (not a shortcut), so help for a distant ally becomes possible. Full mechanics:
`docs/design.md`; lore (open): `docs/lore.md`.

The user's original idea and requirements are kept verbatim in `IDEA.md` on the branch `idea`
(orphan, pushed, **never merged**; later requirements are appended there, also verbatim). Append
in its **permanent** worktree `../worktrees/stellaris-mod-AncientHighway@idea` (user, 2026-11-05:
keep it; recreate with `git worktree add ../worktrees/stellaris-mod-AncientHighway@idea idea`),
never by switching the main checkout; hand over the commit, never a `worktree remove`. Append
with the **absolute path** of the worktree's `IDEA.md`: a relative one written from the main
checkout creates a stray `IDEA.md` there (2026-11-05). This
file and `docs/` are the living design.

Private for now. Workshop search 2026-11-03 found nothing alike: the nearest is *Wild Space*
(uncolonisable systems in the core and rim, no travel mechanics); *Interstellar Highways* and
*Evolving HyperLanes* are about starbases and manipulating existing lanes, and look unmaintained.

The shippable mod will live in `ancient_highway/` — only that subfolder gets linked into the game
(`../scripts/link-mod.sh stellaris-mod-AncientHighway/ancient_highway`). Dev docs stay at the top
level. Prefix every key, id, flag and variable with `ahw_`. Tested in game on Linux only.

---

## Status (2026-11-07): Phase 1 — building the real mod (`0.1.0`)

The spike is over (runs 1–39, `docs/spike-runs.md`). Its files are now the mod's (`ahw_*`, the
generator `tools/gen.py`). Being added, so that one game tests many things at once (user,
2026-11-07: restarting and generating a galaxy is most of each run): **repair on the gate**,
**nomads study and repair**, **the repair contract**, **express wormholes** (plan:
`docs/design.md`). Nothing is public; old spike saves do not load.

**Deferred**: run 31's parts 2–3 (the mod added to a running game; a late empire's portal — user,
2026-11-06: tested once the mod is mostly done). **Parked**: the ring's exact speed (user,
2026-11-04). **Option**: fewer ring nodes on large and huge (user, 2026-11-06).

## How it works

**Generated parts: `tools/gen.py`** writes the bypass types (32 entry pairs `ahw_link_N`), their
megastructures (`ahw_gate_N` in the portal, `ahw_exitgate_N` in the ring), outliner icons, texts,
the outline measurement, the ring builders, portal placement, the inspection studies and their
withdrawal (`events/ahw_generated_events.txt`). Change the generator, rerun it, commit both.

At game start `ahw.10` (`on_game_start`, no scope; also on a save's load or the next month when
the mod joins a running game, once — `ahw_done`) builds everything inside one
`set_spawn_system_batch` (runs 26–30: medium ~4 s, huge 11 s on mkDell):
1. **finds the centre**: two probe systems leapfrog `corewards` (steps 40 → 5);
2. **measures the outline** (every regular system's x, y from two distances; star flag `ahw_xy`)
   and **builds the ring** 25 beyond the outline, smoothed, the probes becoming its last two nodes.
   Nodes by size: tiny 40, small 56, medium 68, large 80, huge 88. Ring systems are big (an
   asteroid at orbit 270), named `<reach> Node <octal>`;
3. **a portal for every regular, non-nomadic empire** (`ahw_gets_portal`; nomads are logged and
   skipped): anchor 2–3 jumps from the capital, best tier first (fewest lanes, no bypass), the
   portal 15 away where its lane arrives farthest from the anchor's other lanes and no system is
   closer than 12; one hyperlane; gate opposite the lane at orbit 230, its exit in the nearest
   ring node. Named `<reach> <octal>`. **All gates broken.**
4. after the batch: centres (`ahw_pick_centres`: black hole / pulsar / toxoid; portals also
   neutron star; tiny map icons) and debris (0–6 asteroids, a third with a deposit).

In play: `ahw.20` (monthly per country) gives the gate to the anchor's owner, offers the study
(`AHW_STUDY_PROJECT` → `ahw.22`: knows the types, its own exit node visited, 15 % of each tech),
the head start (a repaired gate on an anchor: 50 %) and the repair; `ahw.30` gives later empires
a portal; `ahw.50` drains pulsar shields monthly; `ahw.60` offers inspection studies on entering
portals and ring nodes (`.64`, `.65` grant; cap 80 %, `ahw_cap_check` → `.66`/`.67` withdraw).
Sealing: the gate's Open/Sealed mode, flags read by each pair's `country_can_use`; friends pass
(`ahw_friend_of_sealer`).

All findings go to `game.log`, lines starting `AHW`.

## Console (`events/ahw_debug_events.txt`)

**Deselect before each line** (Esc): an event typed with something selected fires on that.
**Let a day pass before judging any route** (route changes take the next daily tick).

| Line | Does |
|---|---|
| `event ahw_debug.6` | an outpost on our anchor, so we own it (owned from the next day) |
| `event ahw_debug.7` | the monthly study/head-start check for us, now |
| `event ahw_debug.8` | both gate techs |
| `event ahw_debug.40` | **a working gate**: outpost, study, techs, repair — the real stages' effects |
| `event ahw_debug.41` | a science ship, a construction ship and a 25-size fleet of ours **in our portal** |
| `event ahw_debug.42` | the same **in our exit node** |
| `event ahw_debug.43` | every warship of ours loses 100 shields |
| `event ahw_debug.44` | our gate repaired by another empire (head start on the next check) |
| `event ahw_debug.45` | our portal studied now |
| `event ahw_debug.46` | test ships next to a foreign portal of an unseen centre kind |
| `event ahw_debug.47` | ask 30 % more of each tech (the cap) |
| `event ahw_debug.25` | seal our pair against everyone, us included; again: open |
| `event ahw_debug.26` | seal our pair for another empire (we are strangers) |
| `event ahw_debug.27` | make that empire our subject (now its friend) |

## Working on it

- **Checks before each test**: `tools/gen.py` (if the generator changed), then
  `tools/check_script.py $(find ancient_highway -name '*.txt' -o -name '*.gfx')` and
  `tools/check_refs.py ancient_highway` (every used name, event, text and icon defined).
- **Test steps for the user are in plain words** — what to set up, type, click, screenshot (user,
  run 17). Console commands one per line in a code block. **Skip what already works** with the
  console shortcuts above, unless the test is about that stage. Mod files load at game start.
- **Numbers come from saves**, not screenshots (ships' `armor_hitpoints`/`shield_hitpoints`,
  `stored_techpoints_for_tech`, flags). Copy `logs/game.log` and `logs/error.log` before
  restarting the game. Expected error.log noise: the centre probes' `move_system` misses, unset
  `ahw_*_tmp` targets and `ahw_exits`/`ahw_pair` in log texts, missing modifier icons, events
  without pictures. Anything else naming `ahw_` is a finding.
- **Gotchas the spike found** (details: `docs/spike-runs.md`):
  - the game **drops a `log` line whose text it has logged before** — make each line unique
    (names, numbers);
  - in a **scripted effect**, `[` in a log string is written `\\[`; in an event, plain `[`;
  - scripted effects nest **at most 5 deep** ("Max effects post init recursive depth");
  - `abort_special_project` in a scripted effect is checked before special projects load
    (13440 error lines, run 39): put it in an event;
  - a spawned megastructure's system-view label appears only after a load (built at game start
    it has one);
  - `distance_to_core_percent` is a fraction 0–1; `spawn_system` without a scope spawns nothing;
    spawn angles are absolute map directions;
  - `create_random_fleet`'s `size` is not a ship count (25 → five corvettes);
  - a spawn counts as an entry for `on_entering_system_fleet`, not for
    `on_entering_system_first_time`;
  - a tech put among the options by `add_research_option` takes `add_tech_progress`.
- **Timings are from mkDell** (as old as the base game; acceptable there is acceptable for
  players). **Multiplayer**: every machine runs the same script in lockstep, so the build comes
  out identical as long as nothing player-local decides it (untested in MP).

## Feasibility (game files 4.5.3, build 7793)

Paths are relative to the game install. "Spike" marks what only an in-game test can settle.

| Need | Building block | Verdict |
|---|---|---|
| Spawn the ring at game start | `spawn_system = { min_distance max_distance (0–100, relative to the scope) min_orientation_angle max_orientation_angle initializer hyperlane = no }`, then `add_hyperlane` | **Works (run 2)**: the angle is an absolute map direction; six steps closed a hexagon. Needs room: one step dropped the 10-unit spacing |
| Place it around the core | `core_radius_perc` 0.2–0.3 per shape (`map/galaxy/galaxy_shapes.txt`); trigger `distance_to_core_percent` — **a fraction 0–1** (run 2) | Open: how empty the core really is; run 3 logs it |
| Shortcuts scaled by galaxy size | trigger `galaxy_size`; `spawn_natural_wormhole = { bypass_type = … }` + `link_wormholes` (`common/scripted_effects/fallen_empire_scripted_effects.txt`, `give_…` wormhole pair) | Feasible, with our own bypass type if needed |
| Ring systems stay neutral | game rule `can_build_starbase_around` (`common/game_rules/00_rules.txt`), gated on a star flag `ahw_ring`; `can_add_claim` is moot (nobody owns the ring) | **Works (run 5)**: a one-key override in `zz_` loads last and wins; the outpost order disappears. Compat risk with mods overriding the same rule |
| Entry points: broken → studied → repaired | ruined → restored megastructure pattern (`gateway_ness_ruined`/`_restored` in `common/megastructures/05_gateways.txt`, `hyper_relay_ruined` in `14_hyper_relay.txt`); study via special project or situation | Feasible |
| Using them needs a tech | own `bypass_type` with `prerequisites = { ahw_tech_… }` and `country_can_use` (`common/bypass/00_bypasses.txt`, its header documents every field) | Feasible |
| Exit only where repaired | **`scripted_connection` bypass** (L-gates, Shroud tunnels): one type per ring system, nexus = that ring system, node = a regular system flagged repaired; `link_wormholes` refuses megastructure bypasses (run 2) | **Works (run 5)**: open/close by the node flag, effective after the next daily tick. Not yet 1:1 (one type offers every end) |
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
- Entry points start broken; **the anchor's owner** studies (science ship project) and repairs them
  **once, for good** (paid, construction ship project); never dismantled. The owner **seals** a
  gate with a switch on the gate (Open / Sealed); a sealed gate blocks both ways; independent of
  the astral action and DLCs. No decisions or edicts (user, 2026-11-04).
- Entry points are 1:1: each regular-side gate has its own exit point in the ring system (one
  bypass type per pair).
- ~~Ring systems are large, their exit points far apart~~ — superseded 2026-11-04: crossings
  must be quick to meet the yardstick below; **fights between passers-by are accepted** (user,
  2026-11-04: the neutral battlefield).
- **The ring goes round the outside of the galaxy** (user, 2026-11-04), with many more systems,
  and **no shortcuts** (except the late-game express wormholes, 2026-11-05): it is a second way to everywhere that borders cannot block for good, not a
  shortcut. Yardstick: once round the ring ≈ once round the galaxy at mid radius (between core
  and outer rim), or a bit longer. **It follows the galaxy's outline** at a fixed distance
  beyond the outer rim, not a circle (user, 2026-11-04).
- **Portals** (user, 2026-11-03): an empire's entry points do not sit next to its capital. For each
  empire a new artificial, unclaimable system — the portal — hangs off a random system 2–3 jumps
  from the capital by a **single hyperlane**; the gates to the ring are in the portal. A dead end
  with one lane: easy to defend by design.
  Its lane arrives in the anchor system **away from the anchor's other lanes** (run 8), so whoever
  comes out of the portal has to cross the anchor system past its starbase.

## Open questions

`docs/design.md`, "Open questions"; lore: `docs/lore.md`.

## Plan

- **Phase 0 — spike**: runs 1–39, done (`docs/spike-runs.md`).
- **Phase 1 — the real mod** (now): the spike ported (`0.1.0`), then repair on the gate, nomads,
  the repair contract, express wormholes, console shortcuts for each; one in-game session tests
  them together.
- **Phase 2** — relays, events and lore, AI tuning, galaxy shapes beyond elliptical.

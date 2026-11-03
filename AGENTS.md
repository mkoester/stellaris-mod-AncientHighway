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

## Status (2026-11-03): Phase 0 spike done (runs 1–5) — the highway is buildable

**Answered** (details in the runs below):
- A ring of systems can be spawned by script (absolute angles), joined by hyperlanes, kept
  unclaimable by a one-key game-rule override (outpost order disappears; confirmed with a control).
- Entry points work as megastructures carrying a `scripted_connection` bypass: gated by a tech,
  opened and closed by the node's star flag, torn down with `remove_megastructure`, locked with
  `lock_bypass` (lock shown; others kept out: untested). Every change takes effect on the **next
  daily tick** — tests taken paused on day one show "no route".
- Before use the country must have seen the bypass type (`add_seen_bypass_type`) and know the
  ring systems (`set_visited`) — what the "study" stage will give.
- Shortcuts as natural-wormhole pairs of our own type link and are used by route-finding.

**Open / to design** (next spike or Phase 1):
1. ~~1:1 entry points~~ — works (run 6); Phase 1 needs a generator (or `inline_script`).
2. ~~A cost per gate jump~~ — `windup_time = 10` ended the detour (run 6); tune it.
3. **Slow crossings** of large ring systems (171–270 days early game) vs. "help a distant ally".
4. ~~Shortcut carrier~~ — a gate pair on its own scripted connection works (run 6).
5. ~~Labels after a load~~ — built at game start they show (run 6); unowned ones need sensor coverage (8).
6. Placement around the core: the core is empty to ~15–20 % of the radius (small elliptical);
   generation at game start, scaled by galaxy size.
7. AI: does it path through, repair, lock, close?
8. **Ring-side gate labels and menus** show only while we have sensor coverage of the ring system
   (run 6). Next spike: `extends_sensors = yes` on the entry types; else accept it.

### The spike (`0.0.6-SPIKE`): what it does, how to run it

`ahw_spike.1` now runs **by itself at game start** (`on_game_start_country`, human player only)
and applies runs 1–5: names "Highway Node 1"–"6"; **1:1 entry points** (one scripted-connection
type per pair); every flag set before any gate; the shortcut as a **gate pair** (no natural
wormhole); seen types and visited ring; outliner icons. Entry points get `windup_time = 10` (as
the hyper relay) to see whether a cost per jump stops detours through the ring. The ring still
sits next to our capital; placing it around the core is a separate spike.

| Entry point | Regular side | Exit in | State |
|---|---|---|---|
| 1 | A = our capital | Highway Node 1 (orbit 300, angle 0) | repaired; owned by us |
| 2 | B = a neighbour of A | Highway Node 1 (orbit 300, angle 120) | repaired |
| 3 | C = another neighbour | Highway Node 2 (orbit 300, angle 0) | broken (no "open" flag) |
| shortcut | Highway Node 1 (orbit 300, angle 240) | Highway Node 4 (orbit 300, angle 60) | open, no tech |

| Console (nothing selected) | Does |
|---|---|
| `event ahw_spike.2` | report only |
| `event ahw_spike.3` | `lock_bypass` entry point 1 for us, 360 days |
| `event ahw_spike.4` / `.5` | close / reopen entry point 1 (its "open" flag) |
| `event ahw_spike.6` | tear down entry point 1's gate; report now and a day later |
| `event ahw_spike.8` | grant `ahw_tech_spike` (or `research_technology ahw_tech_spike`) |

All findings go to `game.log`, lines starting `AHW SPIKE`; the event window names A, B and C
(random neighbours: **take the names from this run's log**, run 5 shows why).
**Deselect everything before each console `event`** (Esc): the console fires the event at the
selected object ("Event fired on wrong scope, got fleet, expected country", run 5).
**Let a day pass before judging any route**: changes reach route-finding on the daily tick.

**Before each run: `tools/check_script.py $(find ancient_highway -name '*.txt' -o -name '*.gfx')`.**
It checks nesting and the keys directly inside each event. A plain brace count is not enough:
`0.0.5-SPIKE`'s first build had a `}` moved from one block to another (balanced overall) that
closed `immediate` early; the game rejected the rest ("Unexpected token: event_target:…") and spawned
no gates. The check reports exactly those lines when that bug is put back.

**Test, run 6** (Linux; a playset with only this mod; **a new campaign**, small elliptical galaxy;
console on):
1. At start: the event window names A, B, C. Screenshot the galaxy map around A, and A's system
   view: **does gate 1 have its label right away** (built at game start, not during play)?
   Is it in the outliner?
2. `event ahw_spike.8`, unpause one day. Science ship: order A → Highway Node 1 (through gate 1),
   then on to B: does it leave through exit 2 → B (1:1: gate 1's menu should offer only Highway
   Node 1)? Order a ship to C: refused through the ring (entry 3 broken)?
3. Order A → B directly (neighbours): hyperlane, or still the detour through the ring despite
   `windup_time = 10`? Screenshot the route.
4. Fly the ring: Highway Node 1 → shortcut → Highway Node 4. Did vanilla's wormhole story stay
   quiet? How long does the crossing take?
5. Optional repeats of run 5 (lock, close/reopen, tear-down) with one day between action and check.
6. Copy `logs/game.log` and `logs/error.log` before quitting, plus the screenshots.

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

**Run 3 (2026-11-03, same setup, `0.0.3-SPIKE`): entry points exist, not visible.**
- **The core is empty out to 15–20 % of the radius** (small elliptical galaxy): no system closer
  to the centre than 0.15, some closer than 0.2. A ring at about 0.1 fits without touching anything.
- The log shows the entry-point megastructure and an `ahw_spike_entry_1` bypass in Sol, Barnard's
  Star (both open) and Alpha Centauri (broken), the nexus flag and bypass in ring 1. The scripted
  connection is accepted; whether ships can use it was not yet tried.
- The gate in Sol was not visible (screenshot `2026_11_03_8`): orbit 120 is about Mars's orbit
  (planet orbits in an initializer add up), so it sat among the inner planets, and unowned it is
  not in the outliner. `0.0.4-SPIKE`: orbit 350, A's gate owned by us.
- `research_technology` refuses a tech whose `potential` fails ("Could not research prerequisite
  technology"): `0.0.4-SPIKE` drops it (weight 0 keeps the tech out of the draw) and adds
  `event ahw_spike.8`. In the run-3 game: `effect every_country = { limit = { is_ai = no }
  give_technology = { tech = ahw_tech_spike message = no } }` (untested form).
- Bypass localisation keys derive from the bypass **key** (`BYPASS_AHW_SPIKE_ENTRY_1`), not from
  its `name`.

**Run 4 (2026-11-03, same setup, `0.0.4-SPIKE`): entry point visible and connected, no known
destination.** Screenshots `2026_11_03_10`, `_11`.
- The gate shows in Sol at orbit 350, in our outliner, with a working **Dismantle** button; its
  tooltip: "fully connected to the Highway Entry Point Network".
- Ordering the science ship through it: "Enter the Highway Entry Point" passes, **"No known
  destination"** (`USE_BYPASS_UNKNOWN_DESTINATION`) fails. The country must have seen the type:
  vanilla calls `add_seen_bypass_type = shroud_tunnel` for its scripted-connection tunnels. The
  spike now does that for both types in `ahw_spike.1`; in the mod, studying an entry point would
  teach it. In the run-4 game: `effect every_country = { limit = { is_ai = no }
  add_seen_bypass_type = ahw_spike_entry_1 }`.
- With the type seen (console: "archives Highway Entry Point information") and the tech
  researched (`research_technology` works without the `potential`), still **"No known
  destination"** (`_12`). The only destination of a node is the nexus, ring 1, unexplored to us.
  Vanilla makes the Starlit nexus known with `set_visited` (`events/biogenesis_origin_events.txt`);
  `ahw_spike.1` now does that for every ring system. In the run-4 game: `effect every_system =
  { limit = { has_star_flag = ahw_ring } every_country = { limit = { is_ai = no } set_visited =
  prev } }`. Design: knowing the ring (visited) is a second thing the study must give.
- With the ring visited too (console: "Discovers the Highway Node system" ×6), **still "No known
  destination"** (`_13`). Difference to vanilla: vanilla sets the scripted connection's flags
  **before** spawning the bypass (Starlit: `set_star_flag = starlit_nexus_system`, then
  `spawn_natural_wormhole`, `common/scripted_effects/biogenesis_effects.txt`; L-gates: initializer
  flags, then the megastructure). The spike spawned the gates in A and B first and flagged them
  after, and the ring end before both. Hypothesis: a bypass's destinations are computed when it is
  created. The spike now sets every flag first and spawns the ring end last. If that is it,
  "repair" must spawn the gate (or re-create it), and closing by removing the flag will not work:
  step 6 tests that. In the run-4 game: spawn a second gate in A/B and a second ring end, after the
  flags (`effect every_system = { limit = { has_star_flag = ahw_entry_open_1 } spawn_megastructure
  = { type = ahw_spike_entry_gate_1 orbit_distance = 300 orbit_angle = 200 } }`, then the same for
  `ahw_nexus_1` with `ahw_spike_entry_ring_1`).
- The second gates did not help either ("No known destination", `_14`), and ordering the ship
  to ring 1 on the galaxy map gave "There is no route" for all six ring systems (`_15`): ring 1
  showed **`Galactic Map Cache Distance: -1`** in the debug tooltip, while Sol's gate said "fully
  connected". **After a save and reload it works** (the user, 2026-11-03; the hyperlane
  add/remove was not run) (`_16`, `_17`): cache distance 1, the route goes Sol → ring 1 straight
  through the gate, the ring's hyperlanes are drawn, and the gate offers "Pick a destination
  system" with both ring ends of the type. So the route cache was stale; vanilla gateways get
  their rebuild through `activate_gateway`. Phase 1 must find what rebuilds it during play (an
  entry point repaired mid-game must work without a reload).
- **Decided (user, 2026-11-03): entry points are 1:1** — one regular-side gate, one exit point in
  the ring system. A scripted-connection type offers every end of its type (the destination picker
  above), so the mod needs **one bypass type per entry-point pair** (node = that regular system's
  flag, nexus = that exit's ring system), generated.
- **The shortcut is used by route-finding** (`_18`): ordered from Sol to a ring system three
  hyperlane jumps round the ring, the ship goes Sol → ring 1 (entry point) → ring 4 (shortcut, the
  long diagonal) → one ring hyperlane. **Estimated 234 days** for an early science ship: the exits
  sit far out (orbit 300 opposite each other in ring 1, 450 in ring 4), so each ring system is a
  long sub-light crossing. Large systems keep empires apart but make the highway slow — design
  tension with "help a distant ally" (smaller orbits, a speed bonus inside ring systems, exits
  placed so usual routes do not cross a whole system). The black-hole stand-in also brings its
  environmental hazards (disengagement chance −50 %, emergency FTL cooldown +50 %).

**Run 5 (2026-11-03, `0.0.5-SPIKE`, a save from 2200.01.01): labels and the stale cache.**
- First build failed to parse (a moved `}`; see `tools/check_script.py`); fixed, then rerun.
- With `interface/ahw_spike.gfx` the "unknown sprite" error is gone and the gate is in the
  outliner from creation, but **its label in the system view is missing until a save and reload**,
  also after leaving and re-entering the system view. **Control: a vanilla `gateway_ruined` spawned
  the same way (console) has no label either** (`_20`). So script-spawned megastructures get their
  system-view label only on load — an engine limitation, not our definition. The mod should place
  its gates when the galaxy is generated (or accept a missing label until the next load).
- Before the tech, the ship's order showed only the missing tech (`_19`); after `ahw_spike.8`,
  **"No known destination" again** (`_21`) — the earlier tooltip just listed the first failing
  check. Flags-first order did not fix the destination; it is the stale route cache, as in run 4.
- **`ahw_spike.9` (add and remove a ring hyperlane) does not refresh it** (`_22`–`_24`): the log
  line is there, the gate still says "No known destination", ring 1 still "There is no route" with
  cache distance −1, its name shows as "Unknown" and the ring's hyperlanes are not drawn, although
  `set_visited` ran in `ahw_spike.1`. After the run-4 reload the same ring showed as "Unsurveyed
  System, Intel Level: Low" with its hyperlanes drawn — so the stale part may be **our country's
  knowledge of the ring**, not the topology. Candidates to try for a mid-game refresh: what the
  game does when a ship first sees a system (sensor range over a ring system), `activate_gateway`,
  `upgrade_megastructure_to` on the gate, and spawning the whole highway during galaxy generation
  (before the first load).
- **A save and reload fixed both again** (route into the ring and the gate's label; the user,
  2026-11-03) — reproducible: whatever the game rebuilds on load is what the mod must trigger
  mid-game, or avoid needing.
- **Step 4, after the reload** (`_25`–`_27`): the gate offers "Travel to Highway Node"; the
  science ship reached ring 1 on 2200.02.25 (~55 days from Sol). Ring 1's system view: the ring end
  at the right edge (orbit 300, angle 0, where the ship arrived), the shortcut at the far left
  edge (300, angle 180), the hyperlane arrivals from the neighbours clearly further in (top and
  left). Exits are far apart as intended; hyperlane arrivals sit nearer the centre. Onward to
  another ring system: 171 days.
- **Vanilla's first-wormhole event fired** on arrival (`apoc.5`, "Natural Wormhole … If it could
  somehow be stabilized…"): our shortcut is spawned as a natural wormhole, so the game treats it
  as one. The mod's shortcuts need their own carrier (as the entry points) or must live with it.
- All six ring systems are named "Highway Node" — indistinguishable. `0.0.5-SPIKE` now names
  them "Highway Node 1"–"6" (`set_name` with a loc key).
- **Step 5: the ring is unclaimable — confirmed with a control.** On a surveyed ring system the
  construction ship's menu has no "Build Starbase (Outpost)" at all (`_28`); with `ahw_ring` removed
  from every ring system by console it appears (75 influence, 90 alloys; `_29`); with the flag back
  it is gone again. So the single-key override of `can_build_starbase_around` in
  `zz_ahw_spike_rules.txt` wins, and the flag alone decides. A failing rule **hides** the order,
  so the fail text `AHW_RING_UNCLAIMABLE` is never shown.
- **Step 6 (closing by flag)** (`_31`–`_33`): right after `ahw_spike.4` the ship still routes
  through Sol's gate; **after a save and reload it no longer does** (the user). So the node trigger
  is applied, at the cache's rebuild: closing by flag works, with the same reload problem. (A first
  reading — "the route uses the broken gate" — was wrong: B and C are random neighbours, different
  per run; the run-5 log says B = Alpha Centauri (open), C = Barnard's Star (broken). Check the
  log's names each run.)
- **Time refreshes the route cache too** (the user's idea): after reopening Sol (`ahw_spike.5`),
  letting the game run past the 1st of the next month brought the route Sol → ring 1 back
  without a reload. **One day is enough** (closing Sol with `ahw_spike.4`, then one day: the route
  no longer used Sol's gate). So the route cache is rebuilt on the daily tick. Every "no route" /
  "No known destination" in runs 4 and 5 was taken **paused on 2200.01.01, before any day had
  passed** — the reloads only stood in for the first tick. Opening and closing by flag work with a
  delay of at most a day; no reload needed. (Labels: still only after a load.)
- **Step 7, the lock**: after `ahw_spike.3` Sol's gate shows the lock symbol and our ships still
  pass — as expected, `lock_bypass` gives the named country *exclusive* access. Whether other
  empires are kept out is untested (needs another empire's ship at the gate).
- **Step 8, tearing down** (`_36`): `remove_megastructure` on Sol's gate removes its bypass (the
  report a day later lists none of type `ahw_spike_entry_1` in Sol) and, after the daily tick, the
  route Sol → ring 1 is gone. The gate's model stays drawn in Sol's system view until the view is
  rebuilt (zoom out to the galaxy and back in).
- **Gate jumps are almost free for route-finding**: Sol → Procyon prefers Sol → ring 1 → Alpha
  Centauri (B) → Procyon over the direct hyperlane, so the ring becomes a shortcut between neighbours.
  Needs a cost per jump (`windup_time`: hyper relay 10 days, Shroud tunnel 40).

**Run 6 (2026-11-03, `0.0.6-SPIKE`, a new campaign, small elliptical galaxy): all four
questions answered.** Screenshots `2026_11_03_37`–`_40`; A = Sol, B = Alpha Centauri, C =
Barnard's Star.
- **Built at game start, gate 1 in Sol has its system-view label from the start** (`_38`). (Run 5:
  built during play, only after a load.)
- **1:1 works**: one day after the tech, gate 1 offers "Travel to Highway Node 1" only (`_39`);
  exit 2 leads to B; C (broken) is not reachable through the ring.
- **`windup_time = 10` ends the detour**: ships between neighbours take the direct hyperlane
  (the user; run 5 went Sol → ring → neighbour).
- **The gate-pair shortcut** is usable and set off no wormhole story.
- Inside Highway Node 1 the path from exit 1 (angle 0) to the shortcut (240) is a straight chord
  that passes the black hole without crossing the centre (`_40`); Sol → Highway Node 4: 171 days.
- No system closer to the centre than 0.2 in this galaxy (0.15 in run 3's).
- **Ring-side gates (unowned) have no label and no right-click menu**; Sol's (owned) has both.
  Giving them an owner by console (`every_system_megastructure = { set_owner = … }`) added the
  labels **immediately**, but **no right-click menu**, also not after a day or a reload.
  Not where the ordering ship is: Sol's gate keeps its menu with the ship in Barnard's Star.
  **It is current sensor coverage of the gate's system**: on entering
  Highway Node 4, and Highway Node 2 mid-month, their (unowned) gates got label and menu at once;
  **once no ship of ours is in a ring system any more, both disappear again** (the user's guess:
  intel). Sol's gate is inside our sensor range all the time; owning a gate shows its label
  regardless. Candidates: `extends_sensors = yes` on the entry types (as vanilla wormholes: seeing
  through an entry point would cover its exit), a sensor source in each ring system, or accepting
  it (route-finding into the ring works without coverage, runs 4–6).

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
- Entry points start broken; the regular-side end can be disabled (cost) or locked by its owner.
- Entry points are 1:1: each regular-side gate has its own exit point in the ring system (one
  bypass type per pair).
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

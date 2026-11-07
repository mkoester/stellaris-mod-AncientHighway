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

## Status (2026-11-06): spike runs 1–31 done, run 25 completed (4.5.3 live); `0.0.31-SPIKE`'s mid-game install and late portals built, their test deferred

**Run 31's parts 2–3 (a running game, a late empire's portal) are deferred** (user, 2026-11-06:
"not my priority right now", tested once the mod is mostly done for a fresh start); the steps
stay below.

**Build cost — solved by batching** (runs 26–30): unbatched, every `spawn_system`/`move_system`
paid a recalculation growing with ~N^2.7 in the star count (huge: ~8 min at the start). Since
`0.0.30-SPIKE` the whole build runs inside `set_spawn_system_batch = begin … end` (vanilla's own
tool): medium ~4 s, huge 11 s. In play every spawn still costs ~10 s on huge (~2.5 s medium),
batched or not. Galaxy generation cannot add systems (an initializer's `neighbor_system` picks an
existing one; a static galaxy replaces the random one). Not used yet: `no_scope = { spawn_system … }`
spawns relative to the galactic core (vanilla's L-Cluster, 550 out) — could replace the centre
search. **Option, noted (user, 2026-11-06): fewer ring nodes on large and huge** (linear saving;
ties into the ring's speed, open item 1).

**Mid-game and late empires (decided 2026-11-06, `0.0.31-SPIKE`, `docs/design.md` "Portals")**:
the mod added to a running game builds everything once, in one batch, on the save's load
(`on_single_player_save_game_load`) or the next month (`on_monthly_pulse`, for multiplayer).
Every regular empire without a portal gets one (`ahw_spike.30`, monthly; country flag
`ahw_has_portal`; `ahw_spike_build_portal` serves both the start and later): empires born later,
and those with no anchor before; each costs a freeze — accepted. Anchor: unowned first, else the
empire's own, never another's (`ahw_spike_portal_anchor_own_ok`; the log's tier lines end in
`-- unowned` / `-- own`). Out of generated pairs (`PAIRS` = 32, `ahw_spike_pair_left`): no portal.
Known limits, untested: systems vanilla spawns during play beyond the rim (the L-Cluster) count
into the outline and push the ring out; the gates of a portal built in play lack their system-view
label until a load (run 5).

**Multiplayer** (2026-11-06, reasoning, untested in MP): Stellaris runs every machine in lockstep —
each one executes the same events and effects with the same random numbers, and nothing is sent
from a host (vanilla's `on_single_player_save_game_load`: "Does not run when loading MP saves due
to OOS concerns"; its L-Cluster spawns the same way on every machine). So the build runs on every
player's machine and comes out identical, as long as all run the same mod set (the game checks).
Nothing player-local may decide what is built. The freeze is the slowest machine's.

**Timings are from mkDell** (user, 2026-11-06: about as old as the base game; nobody is expected to
play on such a machine): acceptable there is acceptable for players.

**Next:** run 38 (`0.0.40-SPIKE`: inspection as studies, offered on entry, withdrawn at the cap); then the rest of the spike order in item 7 — nomads and the contract, then express (runs 36–37: techs, all grants and the 80 % cap work) (runs 32–35 finished debris, bare centres and the drain: toxoid −0.02 armour regen, pulsar no shield regen plus −10 % of max a month); then the rest of the open list (the ring's exact
speed is parked — user, 2026-11-04: "not too important to me now"). Everything is still the
spike (`*spike*` files); nothing is shippable yet.

**Redesign (user, 2026-11-04): the ring goes round the outside of the galaxy**, with many more
systems, no shortcuts, and once round it takes about as long as once round the galaxy at mid
radius — or a bit longer (`docs/design.md`, "The ring"). Runs 1–12 built it around the core; what
they found about entry points, portals, the rule and the route cache still holds, the ring's
placement and the shortcut do not.

**Answered** (details in the runs below):
- **The ring (around the core, superseded)**: built at game start around the **galaxy's centre**, found by two probe systems
  leapfrogging with `move_system direction = corewards` (run 9: nodes at 0.1018–0.1022); sized by
  galaxy size; unclaimable by a one-key game-rule override (confirmed with a control, run 5).
- **Entry points**: megastructures carrying a `scripted_connection` bypass, **1:1** (one type per
  pair, 32 generated by `tools/gen_spike.py`); gated by a tech; opened and closed by a star flag;
  torn down with `remove_megastructure`; locked with `lock_bypass`; `windup_time = 10` stops
  detours between neighbours; `extends_sensors = yes` shows the exit through a usable gate. Every
  change takes effect on the **next daily tick** — tests taken paused on day one show "no route".
  Before use the country must have seen the type and know the ring (`add_seen_bypass_type`,
  `set_visited`) — what the "study" stage will give.
- **Portals** (one per regular empire): a new unclaimable system with one hyperlane, off an anchor
  2–3 jumps from the capital; its lane placed away from the anchor's other lanes (4 compass
  measurements, one move); the gate opposite that lane, at orbit 230. Routes run end to end
  through the ring into other empires' portals (run 9).
- **Shortcuts** (dropped 2026-11-04): a gate pair on its own scripted connection works (no
  wormhole story).

**Open / to design**:
1. **The ring's speed** (parked by the user, 2026-11-04): runs 15–16 gave 104 days per node with
   the asteroid at orbit 270, ~1.5× slower than without. The like-for-like yardstick — a quarter
   lap by hyperlanes at mid radius vs. the same via the ring — is still unmeasured; tune the
   asteroid's orbit (or the node count) from it.
2. **Sealing** (user, 2026-11-04: only the owner, both ways, independent of the astral action, an
   action on the gate; **2026-11-05: friends must still get through** — "the whole idea is that
   empires can still reach their allies", esp. those on the same side of a war). The gate
   megastructure has two overclock modes, `ahw_spike_gate_open` / `ahw_spike_gate_sealed` (tab
   "Seal", 30-day cooldown, sealing costs 25 influence; run 20: the tab shows for our gate in a
   system nobody owns). The gate belongs to the anchor's owner (set on repair and by the monthly
   check). **Sealed by flags, not locks** (runs 20–21: a `lock_bypass` lock never expired, so Open
   could not undo it; the types are no longer lockable): each pair's bypass type has
   `country_can_use` = not `ahw_sealed_<n>` (global flag) or `ahw_spike_friend_of_sealer` — the
   sealer (`event_target:ahw_sealer_<n>`) or its friend: federation, overlord/subject either way,
   fellow subjects, defensive/non-aggression/commercial pact, research agreement, migration treaty,
   guarantee either way, at peace with borders open both ways (and in contact; user, 2026-11-05),
   the same side of any war. The type covers both ends, so both ways.
   **Run 22: a sealed pair refuses a stranger's ship** ("Travel to …" crossed out, the fail
   text in its tooltip) and lets it through the day after opening. **Run 23: a friend (our
   subject) passes**; the other friend kinds untested.
3. **Portal names** (built, `0.0.21-SPIKE`): "Highway Portal" for all made them indistinguishable
   in the outliner and the log (run 18: identical log lines are dropped, so the report lost most
   portals). Now named after the reach their exit node lies in, plus an octal address: the
   reach's digit, then the portal's number in that reach (`Caedris 23`; `tools/gen_spike.py`,
   `REACHES`; lore: `docs/lore.md`, "built for the Fallen Empires, kept by the Caretakers"). Run 20:
   distinct in the outliner and the log. **Ring nodes** (`0.0.22-SPIKE`, run 21: shown on the
   map): `<reach> Node <octal number in the reach, from 0>` (Ashkara Node 0 … Hethra Node 6 on a
   small galaxy). Octal past 7 (…, 7, 10, 11) is fine (user, 2026-11-05). The system view's
   label is the **star's** name: it stayed "Highway Portal" after a reload too (run 21);
   renaming the star with the system works (run 22: "Caedris 21"; `ahw_spike_rename_system`, as
   vanilla does).
4. **AI**: does it path through, study, repair, lock, close?
5. Galaxy shapes beyond small elliptical, and large/huge sizes (32 pairs, performance).
6. Labels/menus: built at game start they show; ring-side gates need sight (a usable entry point)
   for the label and a ship in the system for the right-click menu (runs 6–7).
7. **Design round 2026-11-05** (decided; `docs/design.md`; not built yet): access in three
   stages; two techs (physics: use and seal; engineering, with physics: repair; 2500 each, no
   tier prerequisites); the study grants 15 % of each, an anchor with a repaired gate 50 %
   (they add up to 65 %; each once per empire; more below, cap 80 %); centres at 20 %
   size, our own star classes, the ring a mix of black hole / pulsar / toxoid (no neutron);
   debris (~3 asteroids, a third with deposits) in ring nodes and portals; cosmic storms
   welcome on both; nomads study and repair any gate (with both techs), never seal it, get no portal, and pass
   seals unless banned (at war, or vanilla's `expelled_from_<owner>` flag; the clause is in
   `ahw_spike_friend_of_sealer` since 0.0.24, untested); late-game **express wormholes**
   (stations ~a reach apart, two wormholes each, dormant → unstable → stable, anyone stabilises);
   a **repair contract** a settled empire issues to nomads (only nomads accept contracts) on its
   own broken gate or a close friend's, no consent asked; the issuer must have studied a gate and
   pays about the repair's cost in trade. **Round 2026-11-06**: the ring is explored, not
   revealed (the study `set_visited`s only our exit node; ring stars a faint ~10 % map icon —
   per-empire hiding does not exist); portals get the centre mix too; after one's own study,
   inspecting a gate someone else repaired (a study offered on entry, 15 days — 2026-11-07) gives engineering +5 % (+7 % on
   a study offered on the first entry), a foreign portal gives physics +7 % when its
   centre is a kind not seen before, else +5 % (once per portal; portals also come as neutron
   stars, 2026-11-06: four kinds);
   all grants together at most 80 %. Spike order after run 23:
   centres and star classes (portals too, the faint icon) → debris → techs and grants (does
   `add_tech_progress` work before the tech is offered?) → exploration and inspection grants →
   nomads and the contract → express (its own run).
8. Lore (`docs/lore.md`): builders and seal decided 2026-11-05 (the Fallen Empires, the
   Ancient Caretakers, the Militant Isolationists); the Caretaker node, guardians and the
   phase-2 reactions are open.

### The spike (`0.0.26-SPIKE`): what it does, how to run it

**Generated parts: `tools/gen_spike.py`** writes the bypass types (32 entry pairs; the
shortcut is gone), their megastructures, outliner icons, texts, and the outline measurement, the
outer-ring builders, portal placement and the pair switch (`ahw_spike_generated_effects.txt`). Change the generator, rerun it, commit both.

At game start `ahw_spike.10` (from `on_game_start`, no scope, as vanilla's `game_start.31`):
1. logs how empty the core is;
2. **finds the centre** (run 8: no scope spawns nothing): two probe systems ("Highway Heart") leapfrog with `move_system` `direction = corewards`
   from the innermost system, steps 40 → 5 units, keeping the one with the lower
   `distance_to_core_percent`;
3. **measures the outline** (0.0.14): the second probe moves 40 east, then 40 north of the
   centre; every regular system's distances to centre and probe give its x, y (law of cosines).
   **Builds the outer ring**: node k's edge is the farthest system within ±15° of its direction
   (none: 0); the node goes 25 beyond it, **smoothed** (0.0.15: at most 6 below a neighbour, so
   an outlier makes a gentle hill, not a step); `spawn_system` at the centre, the radius rounded
   down to 5 (literal distances only). **The two probes become the last two nodes** (0.0.15:
   `move_system`, the centre probe relative to itself — logged), nodes joined in order. **Ring
   systems are big** (0.0.16): an asteroid at orbit 270 pushes the hyperlane arrivals from 150
   to 300 (`SYSTEM_MIN_INNER_RADIUS`, `SYSTEM_INNER_RADIUS_OFFSET`). Nodes by size
   (≈ jumps of one lap at mid radius, `tools/gen_spike.py` `lap_nodes`): tiny 40, small 56,
   medium 68, large 80, huge 88. No shortcut;
4. **a portal for every regular empire** (AI too): a system 2–3
   jumps from the capital (not the capital, not next to it, unowned, no portal yet) — **searched, not walked**: from the best
   tier (fewest lanes; without a bypass before with one; logged); a new system 15 units from it (0.0.26: a centre like the ring's),
   **spawned once** (0.0.17; runs 10–16 measured it at 4 compass points by moving it) at the angle,
   computed from the outline's coordinates, where its lane arrives
   farthest from the anchor's other lanes (worst margin logged: +15 = opposite all, −15 = beside
   one) **and no other system — portals and ring nodes included — is closer than 12** (run 13;
   −100 when no angle manages that; the squared clearance is logged). Everything with coordinates
   carries the star flag `ahw_xy` (regular systems from the outline, ring nodes, portals); then **one hyperlane**; unclaimable. In it the empire's entry gate, at that same orbit
   angle (facing away from the anchor, opposite the portal's lane — run 10), orbit 230; its exit in the nearest
   ring node, in that node's next free slot. **All broken** (0.0.18): the anchor's owner gets the
   study offered by the monthly check `ahw_spike.20`; the study (`ahw_spike.22`) teaches the types
   and **only its own exit node** (0.0.26, `ahw_spike_reveal_exit`; the rest is explored); then the tech, the paid repair offer (`ahw_spike.21`) and the repair
   (`ahw_spike.23`);
5. fires `ahw_spike.1` (our window: our portal, its anchor, our exit node) and a report.

| Console (nothing selected) | Does |
|---|---|
| `event ahw_spike.2` | report: every ring node, every portal (broken, studied), ours |
| `event ahw_spike.6` | an outpost on our anchor, so we own it |
| `event ahw_spike.7` | run the monthly study/repair check for us now |
| `event ahw_spike.8` | grant `ahw_tech_spike` |
| `event ahw_spike.25` | seal our pair against everyone, us included (a control for the seal); again: open it |
| `event ahw_spike.26` | seal our pair for another empire (we are strangers to it) |
| `event ahw_spike.27` | make that empire our subject (we become its friend) |
| `event ahw_spike.40` | (0.0.34) **skip to a working gate**: outpost on our anchor, study, tech, repair — through the same effects as the real stages |
| `event ahw_spike.41` | (0.0.34) a science ship, a construction ship and a 5-ship fleet of ours **in our portal** |
| `event ahw_spike.42` | (0.0.34) the same **in our exit node** (inside the ring) |
| `effect every_country = { limit = { is_ai = no } remove_country_flag = ahw_has_portal }` | (0.0.31) count us as an empire without a portal: the next month gives us a second one |

All findings go to `game.log`, lines starting `AHW SPIKE`. **Deselect before each console
`event`** (Esc). **Let a day pass before judging any route.**

**Test steps for the user are written in plain words** — what to set up, what to type, what to
click, what to screenshot — not as numbered checks naming internals (user, run 17: "I don't really
understand the steps"). Mod files load at game start: a change made during a run reaches only the
next game, so give a console line for the running one when needed. **Console commands go one per
line in a code block** (workspace `AGENTS.md`), never inline. **Skip what already works**
(user, 2026-11-07): `ahw_spike.40` instead of outpost → study → tech → repair by hand, `.41` /
`.42` (and the dev-tools mod's `devtools.*`) instead of flying ships there — unless the run tests
that stage itself.

**Checks before each run** (a brace count misses a `}` moved between blocks, `0.0.5-SPIKE`): `tools/gen_spike.py` (if the generator changed), then
`tools/check_script.py $(find ancient_highway -name '*.txt' -o -name '*.gfx')` and
`tools/check_refs.py ancient_highway` (every used name defined, every text and icon present).

**Centres (0.0.27)**: ring nodes, portals and the two centre probes (which become ring nodes)
are spawned with our `ahw_sc_black_hole`, the star planet at size 6 (vanilla 20–35); after the
build `ahw_spike_pick_centres` turns two in three into `ahw_sc_pulsar` / `ahw_sc_toxoid_star`
(portals, 0.0.28: three in four, `ahw_sc_neutron_star` the fourth — never in the ring)
(`change_pc` + `set_star_class`, as vanilla's storms do) and logs the resulting counts. Our classes
(`common/star_classes/ahw_spike_star_classes.txt`): vanilla's look and modifiers,
`spawn_odds = 0` (so the galaxy never draws them), `icon_scale` 10 % of vanilla's.

**Test, run 25** (in plain words for the user; Linux, only this mod, a new campaign, **medium**
elliptical as in runs 23–24 so the start times compare, AI empires on, console on). Press Esc before
each console `event`, so nothing — not even a ship — is selected.

1. **How long did the start take?** Nothing to do: the log has it.
2. **The ring on the map**: zoom out until the ring round the galaxy is in view. Are its systems
   tiny specks now (much smaller than ordinary stars)? Can you still hover one and see its
   tooltip? Screenshot, with a tooltip open.
3. **Your portal** (system view): which centre is it — black hole, pulsar or a toxoid (green)
   star — and is it small? Screenshot.
4. **Study** (`event ahw_spike.6`, `event ahw_spike.7`, send the science ship). When it is done:
   on the map, only **your exit node** should now show its hyperlanes; the rest of the ring stays
   specks without lanes. Screenshot.
5. **Exploring**: `event ahw_spike.8`, let a day pass, send the science ship through the gate
   into your exit node, then on to the next ring node along the ring. Does it go, and do that
   node's lanes appear once it arrives? Screenshot.

Copy `logs/game.log` and `logs/error.log` before restarting the game.

**Run 33, the skips (2026-11-07, `0.0.34-SPIKE`, save 2200.01.01, screenshots `2026_11_07_1`,
`_2`): they work.** `ahw_spike.40`: portal Furon 51 studied, not broken, both offer flags set,
the gate ours, the tech and `ahw_highway_studied` granted, an outpost on the anchor Sirius; no new
error.log lines. `ahw_spike.42`: the three test fleets in our exit node Furon Node 5 (system 438 =
`ahw_player_node`) — on the map only from the next day. The fleet was one corvette: `size` of
`create_random_fleet` is not a ship count → 25 in `0.0.35-SPIKE`.

**Run 33, step 1 again (2026-11-07, `0.0.35-SPIKE`, a new medium game, save 2200.01.02): the
skips work again.** Our portal Furon 51 studied, the others broken; test ships in Furon Node 5
(`ahw_node_68_49`). `size = 25` gave **five corvettes** (one per 5, not naval capacity), at
hull 200, armour 100, shields 200 each; the science and construction ships 300 / 100 / 200. No
error.log lines after the build (the build's own: the probe's `move_system` misses, the
`ahw_*_tmp` targets, `ahw_exits`/`ahw_pair` in log texts — as before).

**Inspection as studies (`0.0.40-SPIKE`, user 2026-11-07: "how would a player/AI empire know"
about 10 days of waiting?)**: `ahw_spike.60` (`on_entering_system_fleet`, every regular
country's fleets) offers a 15-day special project at the system entered — `AHW_INSPECT_GATE_*`
(Gate Construction) for repaired gates there that we did not repair, `AHW_INSPECT_CENTRE_*`
(Gate Theory) at a foreign portal — in the variant for the finder's class (`_SCI`/`_CON`/`_MIL`;
`requirements` cannot say "any class"), once per gate / portal (`ahw_eng_offered_<n>`,
`ahw_phys_offered_<n>`). Every entry is remembered (`ahw_entered_<n>`), so +7 % = offered on the
first entry (`ahw_first_<n>`, now permanent). Done: `.64` / `.65` grant. **Cap**:
`ahw_spike_cap_check` after every grant and on `on_tech_increased` (`.63`): a tech at 0.8 or
researched → `ahw_closed_<tech>`, its open studies withdrawn (`abort_special_project` at both
ends of each offered, undone pair), none offered any more. 0.0.39's waiting (`.61`, `.62`, the
timed flags) is gone.

**Test, run 38** (`0.0.40-SPIKE`, a new medium game, this mod and dev tools; Esc before each
console line; save after each step).
1. `event ahw_spike.6`, `event ahw_spike.41`, a day, `event ahw_spike.45`, `event ahw_spike.44`,
   `event ahw_spike.7`: both at 65 %.
2. Move **only the test science ship** out of our portal to the anchor and back in. Expected on
   arrival: "Inspect the Repaired Gate" in the situation log (science); start it (15 days).
   Gate Construction **72 %** (offered on our first entry: a spawn is none). Then move AHW Test
   Fleet out and in: no second study.
3. `event ahw_spike.46` (next to a foreign portal; game.log names it); move **AHW Test Fleet**
   (military) one jump into it. Expected: "Observe the Portal's Heart" for military ships; do it
   with the fleet. Gate Theory **72 %**.
4. `event ahw_spike.46` again, a ship into that portal: a second centre study shows. Do **not**
   start it; `event ahw_spike.47`: both at **80 %**, and that study **disappears** from the log.

**Run 37 (2026-11-07, `0.0.39-SPIKE`, saves 2200.01.01–06.02, game.log): every grant works, the cap
holds.** Study 15 → head start 65 (01.02); Gate Construction **+7 → 72** (03.08, our own portal
Caedris 21, repaired by "someone else" via `.44` — +7: the test ships were spawned there on 01.01,
and their return from the anchor counted as the country's **first entry**, so a spawn is no
entry); Gate Theory **+7 → 72** (05.26, the foreign portal Furon 52, a toxoid; ours a black
hole); `.47` asked 0.3 and got **+0.08** each → 0.8. Save 06.02: `stored_techpoints_for_tech`
2200 of 2750 for both, both `always_available_tech`; country flags `ahw_insp_1`,
`ahw_repaired_1` (on the "repairer"), `ahw_phys_12`, `ahw_first_12`, `ahw_kind_black_hole` /
`_toxoid`. A country with **every** tech (584, id 16777226, no type) lists ours too — a
game-internal one, not an empire.

**Exploration and inspection grants, the cap (`0.0.39-SPIKE`, design 2026-11-06; the waiting replaced by studies in 0.0.40)**: every grant
goes through `ahw_spike_grant_tech` — at most 0.8 of a tech over all grants, counted in the
country variables `ahw_got_theory` / `ahw_got_construction`. **Inspection**: a fleet of a studied
country (`ahw_highway_studied`, so the head start counts) entering a portal or ring node
(`on_entering_system_fleet` → `ahw_spike.60`) is checked 10 days later (`.61`): idle there, and no
arrival since (timed fleet flag `ahw_arrived`, 9 days — a fleet that moved on and stopped
elsewhere for under 10 days is not counted; one that arrived 1–9 days before an older check
is, a known slack). Then, generated per pair (`tools/gen_spike.py` `inspection()`):
**Gate Construction** +5 % per repaired gate with an end in that system, +7 % if the country's
first entry into it was within 30 days (`on_entering_system_first_time` → `.62`, timed country
flag `ahw_first_<n>`); once per gate (`ahw_insp_<n>`); never for a gate the country repaired
(`ahw_repaired_<n>`, set in `ahw_spike_mark_repaired`). **Gate Theory** at a foreign portal (its
anchor not ours): +7 % for a centre kind not seen (`ahw_kind_<class>`; the studied portal's kind
counts as seen), else +5 %; once per portal (`ahw_phys_<n>`). Test events: `.45` our portal
studied at once, `.46` test ships next to a foreign portal of an unseen kind, `.47` asks 30 % more
of each (the cap).

**Test, run 37** (`0.0.39-SPIKE`, a new medium game, this mod and dev tools; Esc before each
console line; save after each step — the numbers come from the saves and the log).
1. `event ahw_spike.6`, `event ahw_spike.41`, a day, `event ahw_spike.45`, `event ahw_spike.44`,
   `event ahw_spike.7`: both techs at 65 % (15 study + 50 head start).
2. Our own gate, repaired by "someone else": move AHW Test Fleet out of the portal to the anchor
   and back in; leave it idle there 10+ days. Expected: Gate Construction **70 %** (+5; the
   test ships were spawned in the portal, so it is no first entry — or 72 % if the spawn counted).
3. `event ahw_spike.46`: test ships next to a foreign portal (game.log names it). Send the test
   science ship one jump into it; idle 10+ days. Expected: Gate Theory **72 %** (+7, a new kind);
   Gate Construction unchanged (that gate is broken).
4. `event ahw_spike.47`: both at **80 %** exactly.

**Run 36 (2026-11-07, `0.0.38-SPIKE`, saves 2200.01.01–03.05, screenshots `2026_11_07_3`–`_6`):
the techs and both grants work.** After the study (03.01) Gate Construction sat among the
engineering options at **412/2750 = 15 %**; after `ahw_spike.44` + `.7` (the same day: the repair
flag counts at once) both at **1787/2750 = 65 %** — `add_tech_progress` works on a tech put among
the options by `add_research_option`, and the grants add up. The cost shows 2750, not 2500: the
game's scaling (research-cost setting / empire size), as designed. Without Gate Theory the gate
refuses the test fleet ("Travel through Highway Entry Point ✗ SPIKE: Highway Gate Theory").
Tooltip: "Rare Technology … will remain as a valid option until it is researched". **Seal is
refused** without the theory (`_7`): the Sealed mode's tooltip lists "Owner: ✗ Has SPIKE: Highway
Gate Theory Technology" (the gate is ours after the monthly check; mode stays Open). Both techs
show "Missing Icon" (an icon of our own is still to make). The log's `$PARAM$` inside a string
loses the space before it and keeps a `$` (`grantahw_grant_study$ 0.15$`), as everywhere in the
spike — readable, left.

**Techs and grants (`0.0.38-SPIKE`, design 2026-11-05)**: `ahw_tech_spike` is gone. Two techs,
`ahw_tech_gate_theory` (physics, particles) and `ahw_tech_gate_construction` (engineering,
voidcraft), `@tier2cost2` = 2500, rare, tier 1 (`previously_unlocked = 0`: no tier gate),
potential `ahw_highway_studied`. Theory: the bypasses' prerequisite (`tools/gen_spike.py`) and
the Seal mode's `possible`; both: the repair offer. Grants by `ahw_spike_grant` (once per empire by
country flag; nothing for a tech already researched): the study 15 % (`ahw_grant_study`, in
`ahw_spike_mark_studied`); the **head start** 50 % (`ahw_grant_head_start`, `ahw_spike.20`: an
anchor of ours whose gate is not broken — it also gives the study's knowledge,
`ahw_spike_country_learns`, without its 15 %); the repairer gets `ahw_grant_head_start` set, so
its own gate never counts. The 80 % cap waits for the exploration grants (study + head start
reach 65). `ahw_spike.44`: another empire repairs our portal's gate (console test).

**Test, run 36** (`0.0.38-SPIKE`, a new medium game, this mod and dev tools; Esc before each
console line). Question: does `add_tech_progress` show on a tech put among the options by
`add_research_option`, and do the grants add up?
1. `event ahw_spike.6` (outpost on the anchor), `event ahw_spike.41` (test ships in our portal),
   **let a day pass**, `event ahw_spike.7` (the study offer); the study project with the test
   science ship (30 days). (Run 36: `.7` straight after `.6` offered nothing — the outpost owns
   the anchor only from the next daily tick; the offer came with the monthly check on 02.01.)
   Expected: Gate Theory among the physics options and Gate Construction among the engineering
   ones, each at **15 %**. Screenshot both, save.
2. `event ahw_spike.44`, `event ahw_spike.7`. Expected: both at **65 %**; game.log "head start".
   Screenshot, save.
3. The gate in our portal (now ours): its Seal mode should be refused (no Gate Theory yet).

**Run 35 (2026-11-07, `0.0.37-SPIKE`, saves 2200.01.01–06.02): the pulsar drain works.** AHW Test
Fleet (shields 100 max this game) in pulsar node `ahw_node_68_64` from 03.02: 100 → 90 (04.01)
→ 80 (05.01) → 70 (06.01) — a negative `repair_shield_percentage` works and takes **10 % of the
maximum** each 1st, not of what is left; nothing comes back in between. On the way, in a toxoid
node: armour 200 → 194 → 188.8 (3 %/month, as run 33). No error.log line from it. **The drain
stage is done** (both values the user's to retune).

**Run 34 (2026-11-07, `0.0.36-SPIKE`, saves 2200.01.01–05.06; `ahw_spike.43` on 03.06): the
pulsar stops shield regeneration, but nothing drains.** The 1st Fleet at home (Sol, shields 100):
0 → 25 (03.16) → 62.5 (04.01) → 100 (05.01), **2.5/day = 0.5 × 5** as read from the files. AHW
Test Fleet in pulsar node `ahw_node_68_26`: 200 → 100, then **100 for two months**: `ship_shield_
regen_mult = -1` cancels the negative `_add_perc` too (armour 94 there, unchanged: no toxoid).
`0.0.37-SPIKE`: the pulsar keeps `_mult = -1` (drops `_add_perc`); `ahw_spike.50`
(`on_monthly_pulse`) takes **10 % of each ship's maximum shield** a month in pulsar ring nodes
and portals, by `repair_shield_percentage = -0.10` — whether it takes a negative value is
untested (the fallback: `reduce_shield` scaled by `ship_size_multiplier`, as the storms scale
weapons). 10 % is a proposal (armour: ~3 %/month).

**Test, run 35** (`0.0.37-SPIKE`; as run 34): `event ahw_spike.40`, `event ahw_spike.42`, a day,
AHW Test Fleet into a pulsar node; save there, then on each of the next three 2nds of the month.
Expected: 200 → 180 → 160 → 140 (10 % of 200 on each 1st). Still 200: a negative
`repair_shield_percentage` does nothing → the fallback.

**Run 33 (2026-11-07, `0.0.35-SPIKE`, saves 2200.01.02–2200.11.01): debris and bare centres
look right (user); the toxoid drain works, the pulsar does nothing.** Test corvettes (armour 100,
shields 200): in toxoid nodes armour 99.9 → 81.3 from 04.21 to 11.01, **0.1 a day = 0.1 %/day**,
as decided. In the pulsar exit node Furon Node 5 from 01.02 to 04.21 (and the science and
construction ships the whole ten months): shields 200/200, armour 100, unchanged. Why (from the
files): shield components regenerate by themselves, `ship_shield_regen_add_static` = 0.5/day a
small one (`@regen_S1`), ×5 out of combat (`OUT_OF_COMBAT_SHIELD_REGEN_MULT`), and that outweighs
−0.02 (~0.2/day on 200); these ships have no armour regeneration, so the toxoid drain shows.
Vanilla's electric storm does it with `affect_shield_regen = yes` (storm types only) plus a monthly
`reduce_shield` (`cstorms.1100`). `0.0.36-SPIKE`: the pulsar adds `ship_shield_regen_mult = -1`;
`ahw_spike.43` takes 100 shields off every warship we own, so refilling shows.

**Test, run 34** (`0.0.36-SPIKE`, a new medium game, this mod and dev tools; Esc before each
console line). `event ahw_spike.40`, `event ahw_spike.42`, let a day pass; move AHW Test Fleet into
a **pulsar** node (or keep it there if the exit node is one); leave the 1st Fleet at home.
`event ahw_spike.43`; save at once, then after ~10 and ~60 days. Expected: the 1st Fleet back to
full within days; the test fleet stays at ≤ 100 and sinks ~0.2 a day. If it stays at 100
exactly, `_mult = -1` zeroes our negative too — then a monthly `reduce_shield` as the storms do.

**Test, run 33** (`0.0.34-SPIKE` — 0.0.33's content plus the skips; as run 32, a new medium
game, with the dev-tools mod loaded too). Save now and then — the saves carry the numbers (armour
and shields per ship, deposits per asteroid), the screenshots only show. Press Esc before each
console line.
1. **Skip to a working gate and get ships into the ring**:
   ```
   event ahw_spike.40
   ```
   ```
   event ahw_spike.42
   ```
   Let a day pass. Three new fleets ("AHW Test …") should sit in your exit node. Screenshot.
2. A few ring nodes and portals (system view): asteroids with a deposit about one in three, the
   centre without one. Screenshot one.
3. Park "AHW Test Fleet" ~60 days in a toxoid (green) node, then ~60 days in a pulsar node; save
   at each arrival and departure.
4. **Do the skips hold?** Send the test science ship from the exit node back through the gate
   into your portal (it should go), and check that no study or repair offer pops up on the next
   1st of the month.

**Test, run 32** (`0.0.32-SPIKE`; Linux, only this mod, a new **medium** elliptical game, AI
empires on, console on; Esc before each console `event`). New: **debris** (`ahw_spike_add_debris`:
0–6 asteroids per ring node and portal, ~3 on average, a third with an orbital deposit, orbits
70–200) and **the pulsar and toxoid centres drain slowly** (`ship_shield_regen_add_perc` /
`ship_armor_regen_add_perc = -0.001` instead of −100 % shields / armour).
1. **Debris in your portal**: open its system view. Are there a few asteroids inside the gate's
   circle, not on top of the gate? Hover them: do some have a deposit? Screenshot.
2. **Reach the ring**: `event ahw_spike.6`, `event ahw_spike.7`, study with the science ship;
   then `event ahw_spike.8`, `event ahw_spike.7` again, `resource alloys 1000` if needed, accept
   the repair, let the construction ship finish.
3. **Debris in a ring node**: send the science ship into your exit node and look at its system
   view. Asteroids inside, the big one at the edge still there? Screenshot.
4. **The drain**: with the science ship, find a ring node with a **green** (toxoid) centre and one
   with a **pulsar** (your exit node or its neighbours; the system view shows the centre).
   Select your **1st Fleet**, note one ship's armour and shields (hover the bars; numbers, not
   just %), and send it into the toxoid node. Note the numbers on arrival, then after **30 days**
   parked there. Then the same in the pulsar node for shields. Then out of the ring: do they
   come back? Screenshot each reading.

Copy `logs/game.log` and `logs/error.log` before restarting the game (the log has the debris count
and how long it took: "centres and debris done" against "spawn batch ended").

**Test, run 31** (part 1 done; parts 2–3 deferred; `0.0.31-SPIKE`; Linux, only this mod, medium elliptical, AI empires on, console
on; quit the game completely between parts, and copy `logs/game.log` and `logs/error.log` before each relaunch).
1. **A new game still works**: start one, look at the map — ring round the galaxy, our portal
   off a system 2–3 jumps from the capital. Quit.
2. **Adding the mod to a running game**: switch the mod **off**, start a new medium game, play
   about **ten years** at the fastest speed (so the space round the capitals fills up), save,
   quit. Switch the mod **on** and load that save. Expected: a short freeze while it loads (a
   few seconds), then the ring and a portal for every empire. Screenshot the map round your
   capital. Note whether your portal hangs off a system you own.
3. **A late empire's portal**: in that game, press Esc and type
   `effect every_country = { limit = { is_ai = no } remove_country_flag = ahw_has_portal }`, then
   let the game run past the 1st of the next month. Expected: a freeze of a few seconds on the 1st,
   then a second portal near your capital. Screenshot.
4. Save once more and copy the logs.

**Run 32 (2026-11-06, `0.0.32-SPIKE`, medium elliptical, from the saves 2200.01.01–2202.05.18):
debris works; the drain is 20× weaker than meant.** Screenshots `2026_11_06_6`–`_8`.
- **Debris**: 239 asteroids in 80 systems (0–6 each: 5/11/16/15/19/9/5), orbits 70–200; the build's
  last step stayed within the same second. Our portal Furon 51 drew **none** (1 in 16; the user saw
  an empty portal). **Vanilla's deposits come along**: `spawn_planet` rolls the class's own (55 %
  of the asteroids had one, ours drawn on 36 %; error.log: ours refused next to one of another
  station class, e.g. research vs mining). `0.0.33`: `clear_deposits = yes` first. **Every
  centre carries a vanilla deposit too** (80 of 80: dark matter on black holes, physics or
  engineering 3–4 on the others).
- **Drain**: a corvette parked in a toxoid ring node lost **0.01 armour per day** (200 max:
  0.005 %/day; 2202.02.01 → 04.11 linear: 0.30, 0.30, 0.10 per 28, 31, 10 days) — with
  `ship_armor_regen_add_perc = -0.001`. So it lowers the current value, slowly and linearly; the
  user's 0.1 %/day would be about −0.02 (if it stays linear). **Shields**: the user saw no drain
  (their guess: shield regeneration outweighs it); no save shows the fleet in a pulsar node.
  **The construction ship** (saves): 0.45 armour a month of 300 in the same toxoid node — the
  same 0.005 %/day, so the drain scales with the maximum; then 37 days in a pulsar node
  (2202.04.11 → 05.18): armour stayed at 298.35 (lost armour does not come back outside friendly
  space), shields 100/100 throughout.
- **Decided (user, 2026-11-06)**: drain −0.02 for both (0.1 %/day if linear); the centres'
  deposits cleared. Both in `0.0.33-SPIKE`. Then: **shields need to drain more** — raise the
  pulsar's value after run 33 shows what −0.02 does to shields.
- **Read numbers from the saves, not screenshots** (per ship in `ships`: `armor_hitpoints`,
  `shield_hitpoints`, `hitpoints` and their `max_…`, `fleet`, `coordinate.origin` = the system;
  a fleet's `ship_class`; systems' name keys `ahw_portal_<reach>_<n>` / `ahw_node_<N>_<k>`;
  planets' flags and `deposits`). Every save of a run carries the history.

**Run 31, part 1 (2026-11-06, `0.0.31-SPIKE`, a new medium game, twelve empires): the refactor
builds as before.** The batch ~2 s (22:03:23 → :25); save 2200.01.01: 675 systems = 595 + 68 + 12
portals, ring nodes two lanes, portals one, 24 entry bypasses, `ahw_has_portal` on twelve
countries, no two systems closer than 10. Every anchor `-- unowned` (game start). **Bug**: the
portal lines in `ahw_spike_build_portal` came out as "portal for ): off" (the twelve identical
lines then dropped to one) with "Invalid macro entry in ahw_spike_build_portal: his.GetName" in
error.log — `[` must be escaped in a scripted effect **even without parameters of its own** (it
calls one with parameters? or every scripted effect); fixed after the run. The `$WHO$` suffix
prints as "--unowned$" (cosmetic, as the report's "--ring_node$").

**Run 30 (2026-11-06, `0.0.30-SPIKE`, huge elliptical, a fresh launch): the whole mod 11 s; one
spawn in play 10 s.**
- Every line from the start through the portals at 21:47:23 (centre search included), the batch's
  end at 21:47:34: **11 s for the whole build on huge** (992 systems; galaxy generation began
  21:45:15).
- **One unbatched `spawn_system` in play** (console, probe3): 21:49:49 → 21:49:59, **10 s** — about
  a whole batch's end (run 29: ten in a batch, 16 s). In play every spawn pays a full
  recalculation; at the start an unbatched one cost 2.4 s (run 27). The save is from 2 s before the
  probe, so the system is unchecked.

**Run 29 (2026-11-06, `0.0.30-SPIKE`, huge elliptical, 19 empires, same launch as run 28): huge
in ~15 s; a batch in play costs about as much.**
- Ring and portals logged within one second (21:34:55); the next line after `set_spawn_system_batch
  = end` at 21:35:10, so **the batch's end takes ≤ 15 s** (run 27: ~8 min). The start and centre
  lines were dropped as repeats of run 28's, so the centre search is not timed.
- **Autosave 2200.02.01 agrees**: 1105 systems = 998 + 88 ring + 19 portals; ring nodes two lanes,
  portals one, all with a star class; 38 entry bypasses; the one pair closer than 10 is vanilla's.
- **Ring nodes off near the far left of the map**: nodes 1–6 and 85–87 wanted 544–562 from the
  centre, got 538–555, without an error. In the save the ring's x never goes below −538.5.
  Inference, untested: a spawn is clamped to a map bound (|x| ≈ 540 = 1.2 × the setup radius
  450?). Matters only where the galaxy reaches its bound; the smoothing hides it.
- **Probe in play inside a batch** (2200.02.x, ten spawns): 21:37:33 → 21:37:49, **16 s**. Whether
  the ten systems exist is unchecked (the autosave is from before). So in play the batch's end is
  the cost unit — ~15 s on huge — however few systems it holds; one portal for a late empire may
  cost about that. Untested: one unbatched spawn in play on huge.

**Run 28 (2026-11-06, `0.0.30-SPIKE`, medium elliptical, fourteen empires, on mkDell): the spawn
batch takes the build from 81 s to ~4 s.**
- Every `AHW SPIKE` line up to the portals carries the same second (21:29:26); `set_spawn_system_batch
  = end` then takes 4 s (→ 21:29:30), the one recalculation. Run 26, same size: 81 s.
- **Correct inside the batch**: distances and positions of systems spawned earlier in the batch
  are current (centre probe at 0, ring nodes within 4.3 of the wanted radius, the moved centre
  probe 45/46 from its neighbours, portal margins and clearances as before: 13 of 14 clear, Zhir
  10.5 — no clear angle, as run 14's Annawan).
- **The autosave (2200.02.01) agrees**: 680 systems = 598 + 68 ring + 14 portals; every ring node
  two lanes, every portal one; star classes on all; no two systems closer than 10; 28 entry
  bypasses (14 pairs). error.log: nothing new.

**Run 27 (2026-11-06, `0.0.29-SPIKE`, every galaxy size, elliptical, one launch, on mkDell):
the cost per spawn grows with about the cube of the star count.** Logs in `~/ahw-logs/`. In one
launch the game drops a `log` line whose text **and script line** it has logged before, so the
later sizes lack the start and centre lines (their ring lines come from per-size effects and
survived); `game.log` is rewritten per launch, not per new game.

| size (setup radius) | systems | ring nodes | ring | per spawn | per portal | portals |
|---|---|---|---|---|---|---|
| tiny (200) | 201 | 38 | ~2 s | ~0.05 s | < 0.2 s | 5 in < 1 s |
| small (300) | 400 | 54 | 11 s | 0.20 s | 0.9 s | 11 in ~10 s |
| medium (400) | 597 | 66 | 37 s | 0.56 s | 2.3 s | 13 in 30 s (run 26) |
| large (450) | 797 | 78 | 108 s | 1.38 s | 6.2 s | 17 in 106 s |
| huge (450) | 989 | 86 | 208 s | 2.42 s | 13.5 s | 18 in ~250 s |

- **Per spawn ∝ ~N^2.7** (small → huge: 12× for 2.5× the stars); the whole build ∝ ~N^3.2 (√N
  nodes and portals). Huge: **~8 minutes** of the mod at game start (ring + portals, centre not
  logged).
- **It follows the stars, not the radius**: large and huge share radius 450, huge costs 1.75×.
- A portal costs a steady ~4–5 ring spawns at every size. Spawns stay flat within a run (each
  ten as dear as the first ten).
- In play (probe of ten spawns): tiny ~0.1 s, medium 2.5 s per spawn (2× / 4.5× the start).
- Inference, not tested: every spawn or move rebuilds something over all systems (the route
  cache is a candidate — run 5's "Galactic Map Cache Distance"), so the levers are fewer calls
  or calls the engine does not pay for (systems made during galaxy generation), not faster script.

**Run 26 (2026-11-06, `0.0.29-SPIKE`, medium elliptical, thirteen empires, on mkDell): a
mid-game spawn costs ~4.5× a start-time one.**
- **597 regular systems.** Game start 81 s of the mod (20:36:10 → 20:37:31): centre 13 s, ring
  38 s, thirteen portals 30 s (2.3 s each).
- **Ring spawns are flat within the run**: 5–6 s per 10 nodes from the first ten to the last
  (≈ 0.55 s each; runs 24–25: 0.74). The cost per call depends on the galaxy, not on how many
  nodes are already spawned.
- **Mid-game probe** (2200.3.18, console `effect`, ten `spawn_system`s with `while = { count = 10
  }` off a ring node): 20:39:23 → 20:39:48, **25 s, 2.5 s per spawn**; no error.log lines.
  Whether all ten systems appeared was not checked. So spreading the build over days would mean a
  ~2.5 s freeze per spawn on medium; the cheapest moment is the start.

**Run 25, steps 3–5 (2026-11-06, `0.0.31-SPIKE`, a new medium game, twelve empires): the ring
is explored, not revealed — passed.** Screenshots `2026_11_06_1` (our portal Eshmet 41: a small
black hole), `_2` (the gate before the tech: red ✗ "SPIKE: Highway Entry Points"). Study done
2200.12.20; after it only our exit node (Eshmet Node 5) showed lanes; with the tech and the repair
the science ship went through and on round the ring, each node's lanes appearing on arrival (user:
"looks good"). The 0.0.31 log fix holds: the portal lines name every empire and capital. The
step list had left out the repair (`event ahw_spike.7` again after the tech, 500 alloys) — the
gate stays broken without it. **User: the repair belongs on the gate**, not in a pop-up
(`docs/design.md`, Access 3); **the centres' full effects may be too hard** (`docs/design.md`,
centre types).

**Run 25 (2026-11-06, `0.0.27-SPIKE`, medium elliptical, twelve empires, on mkDell): centres
work; tiny on the map.** Screenshots `2026_11_06_8`, `_9`.
- **Centres**: black hole 25, pulsar 33, toxoid 22, other 0 (68 nodes + 12 portals).
- **At 10 % a ring node shows only its frame** — the star a faint dot at most (`_8`); our portal
  Furon 51 a tiny blue speck in its frame, with name and lane (`_9`). **Kept** (user,
  2026-11-06: "that's ok").
- **Game start 104 s of the mod**: centre 13 s, spawning 68 nodes 52 s, twelve portals 36 s.
  **All runs were on mkDell** (user): small 0.18 s per spawn/move (runs 15–17), medium ~0.75 s —
  the cost grows faster than the system count. Building at game start cannot ship for large/huge.
  Open: does a spawn cost as much mid-game (a 10-spawn console probe, logged)? If not, the ring
  is built in the background after the start.

**Run 24 (2026-11-06, `0.0.26-SPIKE`, medium elliptical, eleven empires, on mkDell): the ring
and portals came out empty; spawning is the cost.**
- **An initializer whose `class` is a random list of our star classes spawned empty systems**:
  no star, not even the asteroid (the save has no `planet=`/`star_class` in ring node 1).
  error.log, once (identical lines are dropped): "Failed to find star class or valid random_list
  by key: ahw_rl_centres". The path `common/star_classes/randomizers/` is the one the binary
  reads; every vanilla list holds only classes with `spawn_odds` > 0, ours have 0 — likely the
  list draws by `spawn_odds`. `0.0.27-SPIKE`: no list; a fixed class, then `set_star_class`.
  A system without a star (error.log: "Unable to initialize system due to invalid star class …
  skip initialization") shows a **black system view** (`2026_11_06_7`, our portal Furon 51); on the
  map it has no icon, but its frame and name still show and can be hovered and clicked (`_6`).
  The ring was invisible for that reason, so run 24 says nothing about the 10 % icon.
- **Game start 101 s of the mod** (19:58:59 → 20:00:40): centre 19 s, outline 2 s, **ring edges
  and smoothing under 1 s, spawning the 68 nodes 50 s** (0.74 s each), the last two nodes and the
  lanes 2 s, eleven portals 28 s (2.5 s each). So the octant search (0.0.25) did not matter:
  the cost is `spawn_system`/`move_system`, ~0.5–0.75 s per call on a medium galaxy on mkDell
  (the farthest system 482). Fewer or cheaper spawns are the lever, not the loops.

**Run 23 (2026-11-06, `0.0.24-SPIKE`, medium elliptical, twelve empires, on mkDell): a seal
lets friends through.** Screenshot `2026_11_06_1` (the map round Sol; our portal Galvaas 61, exit Galvaas
Node 1). **Steps 1–4 passed.**
- **Game start: 90 s of the mod** (19:31:40 → 19:33:10; the game's own generation 32 s before):
  centre 12 s, ring 37 s (68 nodes), portals 40 s (3.3 s each). Run 17 (small): 4 / 10 / 8 s.
  The centre search makes ~21 moves whatever the size, yet took 3× longer, so the machine (or a
  per-call cost growing with the galaxy) carries much of it. `0.0.25-SPIKE`: the ring's edge
  search tests only the nodes near each system's octant (14 of 68 instead of all; the generator
  checks the octant lists before writing), and logs timing after the edges, the smoothing and the
  spawns, to split the 37 s.
- **Ring stars carry the node names** (step 1): the save (2201.11.16) names all 68 ring systems
  *and* their stars `ahw_node_68_<k>` (the system view's label is the star's); no "recursive
  depth" error any more (run 22's). On the map, hovering a node shows "Furon Node 7" (`_2`).
- After the study the whole ring shows with its hyperlanes (`_2`) — the `set_visited` that the
  2026-11-06 design replaces by exploration.
- **A stranger's seal refuses us** (step 3, `_3`, 2201.11.16): after `ahw_spike.26` the gate's
  order "Travel to Galvaas Node 1" is crossed out, the tooltip: "… sealed by its keeper, and we
  are no friend of theirs." The portal's own label reads "Galvaas 61".
- **A friend passes the seal** (step 4, user): after `ahw_spike.27` (that empire becomes our
  subject) and a day, our ship went through. So `ahw_spike_friend_of_sealer` works, at least for
  overlord/subject; the other friend kinds and the nomad clause are untested.
- The monthly check still re-takes the repaired-to-be gate each month ("now owns the gate" ×5
  between study and repair), as in run 21.

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

**Run 7 (2026-11-03, `0.0.7-SPIKE`, a new campaign): entry points give sight of their exits.**
- At the start (no tech, no ship in the ring): exits in Highway Node 1 (entries 1, 2 repaired)
  and Node 2 (entry 3 broken) have **no label and no menu**.
- After `ahw_spike.8` (the tech) and a day: **Node 1's exits have their labels, but no menu;
  Node 2's have neither**. So `extends_sensors = yes` shows the exit only through a usable entry
  point (tech + repaired); a broken one gives no sight.
- A ship in Node 1 and back to Sol: the labels stay, the menu goes again. A ship in Node 2 and
  back to Node 1: Node 2's label and menu both go. **The right-click menu needs a ship of ours in
  the system; the label needs sight** (through a usable entry point, or a ship). Route-finding
  needs neither, so the menu is a convenience only.

**Run 8 (2026-11-03, `0.0.8-SPIKE`, small elliptical): portals work, the ring is off-centre.**
- **`spawn_system` without a scope spawns nothing** (no node; `add_hyperlane` errors). The fallback
  ring around a system < 0.3 from the centre is lopsided: its nodes at 0.16–0.35.
- Seven empires, **seven portals**, pairs 1–7; ours 3 jumps from the capital, one lane. Exits
  pile up on the near side of the lopsided ring (node 7: four, node 1: two, node 2: one).
- No system closer to the centre than 0.2.
- **Portal lane placement (user)**: our portal's lane arrives in the anchor system next to the
  lane to Barnard's Star, so an attacker from the portal can pass the anchor's starbase at the
  centre. Decided: the portal's lane must arrive away from the anchor's other lanes.
- Found in the binary: `move_system`/`spawn_system` take **`direction = corewards`** (vanilla
  uses `rimwards`, `events/origin_events_shadows_shroud.txt`). `check_variable` compares against
  another scope's variable as `value < event_target:x.var` (vanilla).

**Run 9 (2026-11-03, `0.0.9-SPIKE`, small elliptical): the ring is centred; portal placement
failed and was slow.** Screenshot `2026_11_03_43`.
- **The centre search works**: the best probe at `distance_to_core_percent` 0; all eight ring
  nodes at 0.1018–0.1022; centred on the map (the user). The probes stay as "Unknown" systems in
  the middle (no lanes, unexplored).
- **`export_trigger_value_to_variable` exports `distance`** (`parameters = { source = … type =
  euclidean }`): real values in the log.
- **Exits spread**: nodes 1, 2, 5, 6, 6, 7, 7, 8 (run 8, lopsided: four on one node).
- **Routes through the ring work end to end**: after the tech and a day, ships route from our
  portal through the ring into other empires' portals (the user).
- **Portal placement failed**: margins −15.6 (ours: lane right beside another), −11 … +5.7. The
  search moved while below the bar, so it ended on the *last* random try, not the best.
- **Game start hung ~80 s at "Loading Map Graphics"** — the mod: `AHW SPIKE` lines 21:42:28 →
  21:43:48; the centre search 4 s (21 moves), the portals ~75 s (up to 30 `move_system` + scores
  each, ~9 s per empire). `move_system` costs ~0.2 s.
- `0.0.10-SPIKE`: the portal is measured at 4 compass points (spawned at 0°, moved to 90/180/270),
  each anchor lane's direction computed from the distances, then **one** move to the best of 12
  angles — 4 moves instead of ≤ 30. The gate in the portal at that orbit angle (user: opposite
  the portal's lane).

**Run 10 (2026-11-03, `0.0.10-SPIKE`, small elliptical): portal placement works.** Screenshots
`2026_11_03_44` (our anchor Vohaul), `_45` (our portal).
- **Game start: 16 s of the mod's work** (centre 4 s, seven portals 12 s; run 9: 80 s) — faster,
  "not really fast" on the older machine.
- **`move_system` honours `min/max_orientation_angle`**: the portals took the computed angles
  (180, 300, 90, 210, 60, 240, 60), margins 14.6, 10.0, 7.7, 1.4, −1.4, −5.9, −10.8. Negative ones
  are anchors with lanes all around (no far side) → `0.0.11-SPIKE` prefers anchors with at most
  two lanes (user), falling back to any.
- Our portal's lane arrives in Vohaul away from its three other lanes (user: looks good).
- **The gate sits opposite the portal's lane — orbit angles in a system match map angles.**
- Scale in the portal's system view (`_45`): gate at orbit 80; the hyperlane arrival circle ~150,
  the orange outer circle ~255. User: gate just inside the orange circle → `GATE_ORBIT = 230`.

**Run 11 (2026-11-03, `0.0.11-SPIKE`, small elliptical): gate placement right, anchor choice
weak.** Screenshots `2026_11_03_46` (map around Sol), `_47` (our portal).
- **The gate at orbit 230 sits just inside the orange circle**; the circle did not grow (user).
- Our portal hangs off Saonus (four lanes, margin −11): "no anchor with <= 2 lanes within 3 jumps";
  yet Bapagia and Edemar (3 jumps, few lanes) were there (user). The random walk sees one path,
  not all candidates. Other margins: 12.7, 11.9, 9.2, 8.7, 5.5, 1.8.
- `0.0.12-SPIKE`: **a tiered search over every system 2–3 jumps out** — dead ends first, then at
  most two lanes, three, more; within a lane count, systems without a bypass (gateway, wormhole —
  Xir's red icon; user: de-prioritise) before those with one. The tier is logged.

**Run 12 (2026-11-04, 4.5.3 live, `0.0.12-SPIKE`, small elliptical, ten empires): the tiered
search works; two empires shared an anchor; log lines went missing.** Screenshot `2026_11_04_1`.
- 4.5.3 went live with `can_build_starbase_around` unchanged: the override still matches vanilla.
- **Tiers logged**: ours tier 4 (Ushakaron, three lanes, margin 5.8); others 2, 4, 3, 1 — but
  only **6 tier lines for 10 portals**, and only 9 "portal for" lines. The missing ones would
  have repeated an earlier line's exact text (unmet empires are all "Unidentified Empire"; pair 8
  = pair 7's anchor and node). Inference, not confirmed: **the game drops a `log` line whose text
  it has logged before**. `0.0.13-SPIKE` adds the capital's name, which makes each line unique.
- Margins: 13.5, 12.6, 9.6, 8.3, 7.2, 5.8, 4.2, 0.8, −0.6, −3.0 (run 11 included −11).
- **Two portals off the dead end Tiblic** (pairs 7 and 8): it lies 2–3 jumps from two capitals,
  and the second portal's lane arrives beside the first (−0.55). `0.0.13-SPIKE`: an anchor that
  already holds a portal is excluded (`ahw_spike_portal_anchor_ok`).
- **Game start: 21 s of the mod** (15:27:12 → :33; centre 4 s, ten portals 17 s ≈ 1.7 s each;
  run 10: 1.7 s each too). The search over every system costs nothing noticeable.
- Ring centred again (nodes 0.1059/0.1064, an octagon clear of every system, `_1`). Exits: nodes
  1, 2, 3 three each, node 7 one — four nodes have none.
- Our portal shows (black hole, "Unsurveyed") but **its lane does not**: hyperlanes of unexplored
  systems are not drawn, and Ushakaron is unexplored, so the screenshot cannot show the anchor.
- error.log, new but harmless: the centre probes' `move_system` "failed to find a position …
  sending it to the galactic core instead" (×20; that is how the probe reaches 0); portals
  spawned without the 10-unit spacing (×8); `Unknown property ahw_exits/ahw_pair` in the report
  where the variable is unset (cosmetic).

**Run 13 (2026-11-04, `0.0.13-SPIKE`, small elliptical, seven empires): portal anchors right,
portal positions not.** Screenshots `2026_11_04_2` (full sensor, our anchor Carynno), `_3`, `_4`.
- **Every line logged**: seven "anchor for … (capital …)" and seven "portal for" lines. Fits run
  12's inference (identical `log` text is dropped) without proving it.
- **Seven different anchors, all tier 1–2** (dead ends: ours, Synthus's, Balkgaz'Yta's; the rest
  two lanes). **All margins positive**: 14.8, 14.7, 14.0, 4.6, 3.1, 3.0, 1.4.
- Ours: Carynno, a dead end 3 jumps from Sol; the portal's lane arrives opposite its only lane
  (margin 14.0, `_2`).
- Game start: 17 s of the mod (centre 6 s, seven portals 11 s).
- error.log: nothing new; "Trying to remove undefined event target" ×3 is the first empire's
  clearing of not-yet-set targets.
- **Three portals badly placed** (user, `_3`, `_4`): pair 5's portal sits on top of a regular
  system (Mehsegaaran, 15 units from its anchor Thabit at angle 0); pairs 6 and 7 (anchors
  Tauagawa and Pathabaan Vortex, neighbours) almost on top of each other between their anchors.
  The margin only saw the anchor's own lanes, and `spawn_system`/`move_system` drop the 10-unit
  spacing when they cannot keep it (the "retrying without SPAWN_SYSTEM_BUFFER_DISTANCE" lines).
  `0.0.14-SPIKE`: every system within 27 of the anchor is measured at the same 4 points; the exact
  squared distance at each candidate angle follows from them (checked numerically against random
  geometry: error ≤ 0.02).

**Run 14 (2026-11-04, `0.0.14-SPIKE`, small elliptical, seven empires): the outer ring
works.** Screenshot `2026_11_04_5`.
- **Systems can be spawned beyond the outer rim** and the camera reaches them: all 56 nodes
  round the outside, placed within 4 of the wanted radius (the 5-unit rounding), the compass
  probes at 40.18. The farthest system 363 from the centre (setup radius 300).
- **Two bulges** (user: looks good, smooth it): a lone outlying system pushed ~5 nodes 40–60
  out as a step (edges 363, 338 vs ~300) → `0.0.15-SPIKE` smooths (run 14's radii through the
  ramp: largest step 48 → 6).
- **The two "Highway Heart"s** in the core are the centre probes (user asked) → `0.0.15-SPIKE`
  moves them into the ring.
- Portals: clearances 703, 380, 246, 201, 165 (≥ 144) — and Annawan −100 (5.4 from another
  system; no angle clear in a dense spot). Margins 15.1, 14.4, 13.5, 8.2, 3.7, −7.7.
- **Game start 39 s** (16:00:38 → 16:01:17): centre 4 s, outline < 1 s, ring 10 s, seven portals
  25 s — 3.5 s each (run 13: 1.7): the clearance looped over every system once per angle →
  `0.0.15-SPIKE`: one pass for all 12 angles (7 passes per portal instead of 19).
- The yardstick (step 4) not yet measured.

**Run 15 (2026-11-04, `0.0.15-SPIKE`, small elliptical, no AI empires): ring smooth, probes
in it, the ring too fast.** Screenshots `2026_11_04_6` (the ring), `_7` (ETA via the ring), `_8`
(ETA by hyperlanes).
- **Smoothing works** (`_6`): no steps; the bulge of this galaxy (farthest system 399) is a
  gentle hill over nodes 41–55. **No "Highway Heart" left**: node 56 (the centre probe, moved
  relative to itself) sits 44 / 43 from its ring neighbours — `move_system` with the moved system
  as its own target works.
- **Game start 14 s** with one empire (centre 4 s, ring 10 s, our portal 4 s — no AI empires,
  so the per-portal time is not comparable with run 14; the anchor search and the nearest-node
  search are unmeasured).
- **The yardstick** (science ship from Sol, after the tech and a day): (b) **via the ring** to
  Highway Node 8 (top right): **1859 days** — Sol → portal (off Appon) → exit in node 39 → 25
  nodes round the bottom: ~70 days per node. (a) **by hyperlanes** to Pithria, the regular system
  next to node 8: **2507 days**, and the route cuts across the galaxy near the core (a chord), so
  a half lap round the galaxy at mid radius would take longer still. **The ring is faster than
  the yardstick — roughly 1.5–2× too fast** (a crude estimate: one route, chord vs. half lap).
- error.log: nothing new.

**Run 16 (2026-11-04, `0.0.16-SPIKE`, small elliptical, eight empires): bigger ring systems
are ~1.5× slower.** Screenshots `2026_11_04_9`–`_13`.
- **The asteroid makes the systems bigger**: it shows at orbit 270 (named like "RLS-285"), and the
  lanes to the neighbouring nodes arrive at the outer edge (`_9`, `_12`).
- **Per node: 104 days** — exit node 22 → node 32 by the ring: 1038 days for 10 nodes (`_12`,
  `_13`), Clarke-class science ship. Run 15: ~70 (crude). So **~1.5× slower**, the low end of
  the 1.5–2× run 15 suggested. Sol → our exit node: 351 days.
- The quarter-lap comparison was not done; the user parked the fine-tuning (orbit 270 stays).
- **Game start 41 s** (eight empires): centre 4 s, ring 10 s, portals 27 s — still 3.4 s each,
  so the merged clearance loop was not the cost: ~3 s between "anchor for" and "portal placed",
  i.e. the portal's spawn and its five `move_system` calls.
- Portals: clearances all ≥ 144 (lowest 148); margins 13.2, 11.1, 9.6, 8.4, 3.5, 0.05, −1.9,
  −4.7.
- error.log: nothing new.

**Run 17 (2026-11-04, `0.0.17-SPIKE`, small elliptical, eleven empires): portals from
coordinates — five times faster, as good.** Screenshot `2026_11_04_1` (the second of that name:
the game restarted its numbering).
- **Game start 22 s** for the mod (19:35:31 → :53): centre 4 s, ring 10 s, **eleven portals 8 s —
  0.7 s each** (run 16: 3.4 s). The scoring from coordinates (and `prev` = the outer scope inside
  `every_neighbor_system`/`every_system`) works: margins as before.
- Margins 15.1, 15.0, 15.0, 14.8, 14.6, 14.3, 13.8, 12.0, 5.8, 1.8 (ours), −10.7; squared
  clearances all ≥ 144 (lowest 193). Six dead-end anchors (tier 1), four tier 2, ours tier 4.
- Ours (`_1`): off Ladellikon (three lanes: Jishui to the north, Alpha Centauri to the
  south-east), the portal's lane leaves due west — the far side; margin only 1.8 because the lane
  to Jishui is perpendicular. Uraku's portal (off Condarra) sits ~15 units north of ours —
  clear, but close.
- error.log: nothing new (the centre probes' 20 `move_system` failures as always).

**Run 18 (2026-11-04, `0.0.18-SPIKE`, small elliptical, AI empires): study, repair and the
lock order work.** No screenshots; the user: "everything worked as expected".
- **Study**: `ahw_spike.6` (outpost on our anchor Sirius), `ahw_spike.7` → the project offered
  (19:57:49), done by the science ship (19:59:22). **The tech did not show** among the research
  options: options are drawn only when a project in that area starts or ends, and the shown ones
  stay → `add_research_option` in the study event (vanilla does this for
  `tech_gateway_activation` after a gateway study), after the run; granted by `ahw_spike.8` here.
- **Repair**: the offer came with the next check (20:02:51), the construction ship finished
  (20:05:20); routes through the repaired gate worked (user).
- **The Dimensional Lock order is offered on our gate** once we own the anchor
  (`ahw_spike.3`; user): the `can_lock_bypass` override works.
- `ahw_spike.4` / `.5` locked our gate and the ring end for another empire (report: LOCKED); the
  direction test was not done (no ship went from the ring into the portal).
- **Identical log lines are dropped — confirmed**: the report printed one "Highway Portal:
  BROKEN" for six broken AI portals (run 12's inference). The log line for the study named the
  ship instead of the system (`[This.System.GetName]` in ship scope) → fixed after the run.
- **A second `lock_bypass` replaces the first** (there is no unlock effect): both test locks
  (360 days, for another empire) re-locked for us for 1 day by console `effect`, two days later
  our ship passed the gate again (user). So a lock can be lifted early, and `ahw_spike.9` does
  that from the next game on.
- AI empires had not studied their portals by 20:06 (their anchors unowned; ~a year in).
- error.log: nothing new.

**Run 22 (2026-11-05, `0.0.23-SPIKE`, small elliptical, eleven empires): a seal refuses
strangers; stars carry the names.** Screenshots `2026_11_05_8`–`_10`.
- **The portal's system-view label says "Caedris 21"** (`_8`): renaming the star works. Ring
  nodes on the map: Caedris Node 5, 6, Dovhar Node 0 (`_9`).
- **Sealed against everyone** (`ahw_spike.25` on 2201.5.1): on 5.2 our science ship's order
  "Travel to Caedris Node 6" is crossed out, the tooltip shows the fail text (`_10`) —
  `country_can_use` refuses. Opened again on 5.2, the ship went (user). Sealed for us (5.20) and
  opened (6.21) by the gate's modes: the log has both.
- error.log, new: **"CRITICAL: Max effects post init recursive depth of 5 reached … 164512
  effects left"**, at `ahw_spike_spawn_ring_node` calling `ahw_spike_rename_system`: scripted
  effects nest at most 5 deep, and the deeper ones are left uninitialised (so the ring stars were
  probably not renamed). `0.0.24-SPIKE` inlines the rename there.
- `_10`: an `event` typed with the ship selected fired on the ship ("Event fired on wrong scope.
  Got fleet").

**Run 21 (2026-11-05, `0.0.22-SPIKE`, small elliptical, nine empires): node names work; a
lock never expires.** Screenshots `2026_11_05_4`–`_7`.
- **Ring nodes carry their names** on the map (`_4`: Dovhar Node 5, 6, then Eshmet Node 0, 1 —
  a reach boundary). Our exit: Furon Node 2, our portal Furon 51 (reach digit matches).
- **The portal's system-view label still says "Highway Portal"**, also after a save and reload
  (`_5`, `_6`): it is the star's name → `0.0.23-SPIKE` renames the star too.
- **Sealed for us**: our science ship got through both ways (user; also in run 20).
- **The 1-day lock after Open never expired**: Open on 2201.2.18, the report on 2.20 and on 3.2
  still LOCKED; no `on_dimensional_lock_expired` line. Whether a lock never expires, expires much
  later, or a shorter lock cannot replace a longer one is unknown, and no longer matters:
  `0.0.23-SPIKE` seals by flags.
- `_7`: an `event` typed with the gate selected fired on the gate ("Event fired on wrong scope.
  Got megastructure, expected country") — deselect first, as the table says.
- Between study and repair the monthly check takes the gate again each month ("now owns the
  gate" on 8.25, 9.1, 10.1; none after the repair): something resets the broken gate's owner.
  Harmless so far; not looked into.
- error.log: nothing new.

**Run 20 (2026-11-05, `0.0.21-SPIKE`, small elliptical, ten empires): the Seal switch and
portal names work; a lock outlived Open.** Screenshots `2026_11_05_1`–`_3` (the game's folder).
- **The tech shows after the study** (`_1`, 2200.11.01: "SPIKE: Highway Entry Points" among the
  physics options): `add_research_option` in the study event works.
- **The Seal tab shows** for our gate in a system nobody owns (`_3`): Open / Sealed, 25 influence
  to switch, the tooltip text. Sealed on 2201.3.17 (log "SEALED"); the report on 2201.5.16 lists
  our portal as LOCKED.
- **After Open (2201.5.16) the report on 5.18 still shows LOCKED.** Open re-locks for 1 day; that
  lock had not visibly expired after two. Run 18 never proved expiry either: it re-locked *for
  us*, and our ships pass our own lock. Unknown whether the game expires locks only on some
  later tick, or whether `has_lock` stays true. `0.0.22-SPIKE` logs `on_dimensional_lock_expired`
  (`ahw_spike.24`). Our ship's passage while sealed was not recorded in the log.
- **Portal names**: the report lists all ten portals under their own names (Furon 51, Dovhar 32,
  Ashkara 02, Caedris 22, Dovhar 31, Caedris 21, Belun 12, Eshmet 41, Belun 11, Ashkara 01 for
  ours). The reach digit matches the exit node (ours: Highway Node 7 → reach 0; node 12 → Belun).
  Outliner and the bottom bar say "Ashkara 01"; **the system view's label still says "Highway
  Portal"** (`_2`, `_3`). The gate's order "Travel to Highway Node 7": nodes were not renamed yet.
- error.log: the monthly check's `owner = { … }` on an unowned gate errors ("Invalid context
  switch [owner]", ×3, logged as "now owns the gate" each time) → guarded in `0.0.22-SPIKE`.
  Otherwise only the expected missing icons.

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

See "Status" above for what the spike left open, and `docs/design.md`, "Open questions", for the
design ones: who repairs an entry point (with portals: the empire it belongs to?), whether the
ring gets relays, how the shortcut count scales, lore (`docs/lore.md`).

## Plan

- **Phase 0 — spike**: runs 1–22 done (see "Status").
- **Phase 1** — the real mod from the spike's findings (drop the `*spike*` files, keep the
  generator): game-start generation for all sizes and shapes, entry-point lifecycle (study →
  research → repair → use), locking portals, localisation.
- **Phase 2** — relays, shortcuts, events and lore, AI.

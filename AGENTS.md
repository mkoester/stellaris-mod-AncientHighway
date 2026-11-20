# Ancient Highway

A Stellaris gameplay mod (game **4.5.x**, working title): a ring of artificial, unclaimable systems
**around the outside of the galaxy**, joined by hyperlanes, reachable from the regular galaxy through entry points that must be studied, repaired and researched before use. The
point: empires stop being landlocked — a second way to get everywhere that closed borders cannot
block for good (not a shortcut), so help for a distant ally becomes possible. Full mechanics:
`docs/design.md`; lore (open): `docs/lore.md`.

The user's original idea and requirements are kept verbatim in `IDEA.md` on the branch `idea`
(orphan, pushed, **never merged**; later requirements are appended there, also verbatim). Append
in its **permanent** worktree `../worktrees/stellaris-mod-AncientHighway@idea` (user, 2026-11-05:
keep it; `../bootstrap.sh` recreates it),
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
generator `tools/gen.py`). Tests now cover many features per game (user, 2026-11-07:
restarting and generating a galaxy is most of each run). Nothing is public; old spike saves do
not load. As of runs 40–43:
- **Work in game**: repair as an upgrade on the gate, the seal, a second (late) portal, the
  express (closed tooltip, flips, routes through an open link), the repair contract with a nomad
  to the head start (run 43), the yearly summary `ahw.80`.
- **The AI** claims its anchor after 5–10 years and then studies within 1–2 (run 43); it
  researched no gate tech until the techs got `ai_weight` 3 — then one empire in 18 months;
  in the user's unforced campaign (2026-11-18, `docs/test-runs.md`) none of 13 in up to 12 years.
  Since then ×3 with a friend out of reach, ×5 more if also threatened; since 2026-11-20 the
  weight steps with the grants received (×1 / ×3 / ×6 / ×12 at 30/50/70 %, ×4 with the other
  tech), fed also by travel techs and close friends' knowledge (`ahw_tech.txt`, `docs/design.md`
  "Without exploring"); in game untested.
  With working gates (run 44, `docs/test-runs.md`) the AI repairs within 3–4 months of having both techs. **Run
  44 passed** the 0.1.1 features: object texts, shared charts, ally under attack, the three
  Galactic Community resolutions (after the flag fix, 2026-11-09); the Seal mode refused on a
  forced-open gate (2026-11-12).
- **Open**: what clears a portal gate's owner (run 43: in ~60 % of months, **all gates at once** —
  one game-wide cause; 0.1.1's daily watch `ahw.90` logs the day and gives it back; **one cause
  found 2026-11-12: loading a save** — `docs/test-runs.md`, "Quick checks"); one unexplained contract cancel 12 days
  after acceptance (run 43, first try — `on_cancel` now logs the cause); the issue-contract menu
  appeared only months after console `communications` (run 40); an AI nomad's study completed
  without effect (2026-11-19): its `on_success` ran with THIS (the ship) empty (replay
  2026-11-20, `docs/test-runs.md`); now falls back to FROM's system and PREV, the fix untested in
  game; AI nomads repairing on their own not seen yet; the express's stabilise cost (4000) is untested at the mid game;
  a portal can sit behind a marauder empire (run 44, user).

**Deferred**: run 31's part 2, the mod added to a running game (user, 2026-11-06: tested once
the mod is mostly done); part 3, a late empire's portal, came unasked in run 43. **Parked**: the ring's exact speed (user,
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
(`AHW_STUDY_PROJECT` → `ahw.22`: knows the types, its own exit node visited, 15 % of each tech)
and the head start (a repaired gate on an anchor: 50 %). **The repair is an upgrade on the gate**
(0.1.0): `ahw_gate_broken_N` → `ahw_gate_N` (both techs, 300 alloys + 50 influence, 90 days,
`nomad_reactivatable`); its `on_build_complete` → `ahw_mark_repaired` (once; the gate goes to the
anchor's owner, never to a nomad). By script: `ahw_repair_gate` (upgrade + `finish_upgrade`, with
a fallback if the engine skips `on_build_complete`) — the console skips and the contract.
**Nomads** (0.1.0) get no portal; `ahw.60` offers a nomad the study once, on its first entry into
a portal with a broken gate (it teaches the nomad, not the portal's owner); they repair by the
upgrade (`nomad_reactivatable`); the Sealed mode refuses them. **The repair contract**
(`common/missions/missions/ahw_contracts.txt`, after vanilla's `contract_clear_blockers`): issued
in an anchor (own, or a close friend's — `ahw_close_friend`) by a country that has studied a
gate; a nomad with both techs accepts; its arkship's `AHW_CONTRACT_REPAIR_PROJECT` (90 days) only
counts, the repair runs in the contract's `on_success` (`ahw_repair_gate`). `ahw.30` gives later
empires a portal; `ahw.50` drains pulsar shields monthly; `ahw.60` offers inspection studies on entering
portals and ring nodes (`.64`, `.65` grant; cap 80 %, `ahw_cap_check` → `.66`/`.67` withdraw).
Sealing: the gate's Open/Sealed mode, flags read by each pair's `country_can_use`; friends pass
(`ahw_friend_of_sealer`). **Wanted by Vassal Orders** (2026-11-12, not built yet): an overlord
ordering its subject to seal that subject's entry point. No effect sets a mode, so this mod needs
a hook that `country_can_use` honours (a flag or scripted effect), plus a flag that tells other
mods AncientHighway is loaded. Design it with `../stellaris-mod-VassalOrders/AGENTS.md`.

**Express** (0.1.0, generated `express()`): one station per reach (8 on every size, near each
reach's middle, ±1 node, seeded), each with two wormhole megastructures `ahw_xhole_j` on its
radial line (outward: the link to the next station, inward: to the previous) at orbit 220; link
`ahw_express_j` joins stations j and j+1 (star flags `ahw_xst_a_j` / `_b_j`). Usable while
`ahw_express_open_j`. Dormant until `on_mid_game_pulse` (`ahw.70`), then each month an unstable
link flips with 25 % (`ahw.71`). Entering a station teaches its two link types and, once awake
and with Gate Theory, offers `AHW_EXPRESS_STABILISE` (4000, ×0.75 after years 125/150/175;
→ `ahw.72`: both links stable, for everyone).

**0.1.1 (run 44)**: `ahw.90` (daily, on the global event country; started once by `ahw.91`)
gives a gate whose anchor has an owner back to it and logs "owner lost by <date>". Entering a ring
node sets the star flag `ahw_mapped@<country>` (its chart) and counts the entry (country
variables `ahw_n_ring_mil` / `_civ`, printed and reset by `ahw.80`). **Shared charts**
(`ahw_copy_charts`: `set_visited` + the flag): close friends yearly (`ahw_share_charts_friends`),
the Galactic Community's members at passing and yearly (`ahw_share_charts_gc`). **Ally under
attack** (`ahw.95`, monthly per country that has studied a gate): a close friend, not a
neighbour, at war and not with us → charts swapped both ways, message `ahw.96`; once per friend
in five years (`ahw_ally_warned@`). **Resolutions** (`common/resolutions/ahw_resolutions.txt`,
category `resolution_category_ahw_highway`): Share Ring Charts (repeal ends Unrepaired Gates
too), Unrepaired Gates (breach: `ahw_gate_breach`), Force a Gate Open (targeted, as Denounce:
`ahw_force_open`, star flag `ahw_forced_open` for 10 years, which the Sealed mode refuses; the
gate's mode reads Sealed until switched — no effect sets a mode). AI weights: `ahw_far_friend`,
`ahw_threatened` and the gate triggers in `ahw_triggers.txt`. **Object texts**: the gates', exit
gates', express wormholes' and centre star classes' descriptions (`AHW_LORE_*`, `ahw_sc_*_desc`)
and both techs' carry a line of lore each.

**Story** (2026-11-19, `events/ahw_story_events.txt`, texts in `ahw_story_l_english.yml`; human
players only): three core pop-ups everyone sees — `ahw_story.1` on the study or the head start
(`ahw_country_learns`), `.2` on the first gate tech (`ahw.63`), `.3` on the first ring node
(`ahw_story_entered`, from `ahw.60`) — and twelve fragments `.11`–`.22`, one unseen one at random
(`ahw_story.10`, flags `ahw_frag_N`, counter `ahw_n_frags`) on the first entry into each foreign
portal (star flag `ahw_toured@<country>`) and each further reach (`ahw_reach_seen_<r>`). Lore
and its checks against vanilla: `docs/lore.md`. **Inspection balance** (same day): a foreign
portal with a broken gate offers one study, for the tech granted less so far
(`ahw_construction_behind`): the centre's (Theory) or the broken gate's (`AHW_INSPECT_BROKEN_*`
→ `ahw.62`, Construction +7 %; the inspections raised to 10/7 % on 2026-11-20). **Without
exploring** (2026-11-20, `ahw_travel_grants` via `ahw.63`/`ahw.68`, `ahw_diffuse_all` in `ahw.80`;
country flags `ahw_travel_<tech>`): +10 % of both techs per vanilla travel tech, and yearly up to
+3 % from close friends (2 % each) and contacts (0.5 %) who hold a gate tech.

All findings go to `game.log`, lines starting `AHW`.

## Console and test runs

- The console events in `events/ahw_debug_events.txt` are listed in `docs/console.md`. Read it
  before running or adding one.
- Test runs 40 onwards, with what each found and what is still open, are in
  `docs/test-runs.md`, newest first. Read the latest run before planning the next, and record
  each new run there.

## Working on it

- **The dashboard reads this mod** (`stellaris-empire-dashboard`, branch `feature/highway`,
  `src/lib/highway.ts`; 2026-11-07): the star flags, global and country flags, variables and
  megastructure types named in "How it works", and the texts in `localisation/english/`. Renaming
  one of them needs the dashboard changed in the same session, or its highway tab goes wrong
  silently.

- **Thumbnail** (2026-11-07): `assets/thumbnail.svg`, our own art — a faint galaxy, a road of
  light, a fleet racing along it; on purpose nothing of how the highway works (user: no ring, no
  gates). Render: `rsvg-convert -w 512 -h 512 assets/thumbnail.svg -o ancient_highway/thumbnail.png`
  (`picture="thumbnail.png"` in the descriptor).

- **Checks before each test**: `tools/gen.py` (if the generator changed), then
  `tools/check_script.py $(find ancient_highway -name '*.txt' -o -name '*.gfx')` and
  `tools/check_refs.py ancient_highway` (every used name, event, text and icon defined).
- **Test steps for the user are in plain words** — what to set up, type, click, screenshot (user,
  run 17). Console commands one per line in a code block. **Skip what already works** with the
  console shortcuts in `docs/console.md`, unless the test is about that stage. Mod files load at game start.
- **Numbers come from saves**, not screenshots (ships' `armor_hitpoints`/`shield_hitpoints`,
  `stored_techpoints_for_tech`, flags). Where things are in the `gamestate` (2026-11-08): who
  has entered a system is the country's `visited_objects` (every non-`default` country lists
  every system — ignore them); a fleet names no owner, the country's `owned_fleets` does; a
  fleet's position is the `origin` in its `movement_manager`'s `coordinate` (the first `origin`
  in the block is its combat's); a body's surveyor is `surveyed_by` in `planets`. With the
  dashboard's feed mod in the playset, game.log marks each load as `SDASH|…|<date>|…|load|` —
  the way to tell a load-caused owner loss from another (2026-11-18). Copy `logs/game.log` and `logs/error.log` before
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
- **Gotchas of Phase 1** (runs 40–43):
  - `check_variable` compares against another variable: `value < ahw_got_theory` (vanilla does
    it, e.g. `value < thought_police_purchased`; used by `ahw_construction_behind`, 2026-11-19,
    not yet seen in game);
  - `give_technology` refuses a tech whose `potential` fails ("invalid technology"): set the
    potential's flag first (`ahw_debug.73`);
  - a special project's `cost` and `days_to_research` are exclusive (error.log at load); `cost`
    modifiers want a `desc`;
  - a megastructure upgrade finished by script (`upgrade_megastructure_to` + `finish_upgrade`)
    runs `on_build_complete` at once, with `from` = the megastructure's owner, not the caller —
    hand the real actor over in a global target;
  - a contract's AI operator goes to the contract's location: its work project must be there,
    not in a neighbouring system (run 40); and the result belongs in the contract's `on_success`
    (vanilla's note), or the abort trigger fires first;
  - the AI researches a custom tech only with an `ai_weight` (vanilla's gateway tech has one for
    human auto-research only);
  - tech definitions (and other `common/` files) load from the mod at each game start, so a
    resumed save picks up a changed weight; flags set at the build do not reach old saves;
  - a megastructure in a system nobody owns loses its owner from time to time (cause unknown);
  - an upgrade's button reads a disabled "Complete" while the megastructure has no owner.
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
- **Phase 2** — relays, events and lore, AI tuning, galaxy shapes beyond elliptical. Chosen
  2026-11-08: lore through object texts, a situation-log chain, one Caretaker fragment per reach
  and Fallen Empire voices (`docs/lore.md`, "How players learn it"); shared charts between close
  friends, threat-based AI weights, the ally-under-attack event and the AI sealing when
  threatened, and three Galactic Community resolutions (share charts; unrepaired gates a
  breach; force a gate open for 10 years) (`docs/design.md`, "Exploration and incentives").

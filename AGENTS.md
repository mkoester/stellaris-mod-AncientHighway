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
generator `tools/gen.py`). Tests now cover many features per game (user, 2026-11-07:
restarting and generating a galaxy is most of each run). Nothing is public; old spike saves do
not load. As of runs 40–43:
- **Work in game**: repair as an upgrade on the gate, the seal, a second (late) portal, the
  express (closed tooltip, flips, routes through an open link), the repair contract with a nomad
  to the head start (run 43), the yearly summary `ahw.80`.
- **The AI** claims its anchor after 5–10 years and then studies within 1–2 (run 43); it
  researched no gate tech until the techs got `ai_weight` 3 — then one empire in 18 months.
  With working gates (run 44, below) the AI repairs within 3–4 months of having both techs. **Run
  44 passed** the 0.1.1 features: object texts, shared charts, ally under attack, the three
  Galactic Community resolutions (after the flag fix, 2026-11-09). **Next**: the Seal mode
  refused on a forced-open gate (`ahw_debug.8`, `ahw_debug.81`, screenshots before and after).
- **Open**: what clears a portal gate's owner (run 43: in ~60 % of months, **all gates at once** —
  one game-wide cause; 0.1.1's daily watch `ahw.90` logs the day and gives it back; **one cause
  found 2026-11-12: loading a save** — below, "Quick checks"); one unexplained contract cancel 12 days
  after acceptance (run 43, first try — `on_cancel` now logs the cause); the issue-contract menu
  appeared only months after console `communications` (run 40); nomads studying or repairing on
  their own — not seen yet; the express's stabilise cost (4000) is untested at the mid game;
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
(`ahw_friend_of_sealer`).

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

All findings go to `game.log`, lines starting `AHW`.

## Console (`events/ahw_debug_events.txt`)

**Deselect before each line** (Esc): an event typed with something selected fires on that.
**Let a day pass before judging any route** (route changes take the next daily tick).

| Line | Does |
|---|---|
| `event ahw_debug.6` | an outpost on our anchor, so we own it (owned from the next day) |
| `event ahw_debug.7` | the monthly study/head-start check for us, now |
| `event ahw_debug.8` | both gate techs |
| `event ahw_debug.40` | **a working gate**: outpost, study, techs, repair (the scripted upgrade) — the real stages' effects |
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
| `event ahw_debug.70` | the express awake now (as at the mid game) |
| `event ahw_debug.71` | every express link stable |
| `event ahw_debug.72` | our three test fleets at the express station nearest our exit node |
| `event ahw_debug.74` | every AI empire's portal studied now (an outpost on a free anchor first) — to watch the AI research |
| `event ahw_debug.73` | a nomad in contact with us, with both techs, its arkship at our anchor |
| `event ahw_debug.75` | every AI empire's portal studied, both techs; **every other one repaired** |
| `event ahw_debug.76` | one AI empire seals its repaired gate (a target for Force a Gate Open) |
| `event ahw_debug.77` | a Galactic Community now: us and every empire we have met |
| `event ahw_debug.78` | an AI empire beyond our borders becomes our subject, and another AI empire attacks it (game.log says whether the war started) |
| `event ahw_debug.79` | the yearly chart exchange now (friends; the Community under Share Ring Charts) |
| `event ahw_debug.80` | Force a Gate Open passed now (no vote) against an empire with a sealed gate |
| `event ahw_debug.81` | our own gate forced open (Force a Gate Open's effect) — to see the Seal mode refused (needs `ahw_debug.8`'s techs) |
| `effect pass_resolution_no_cooldown = resolution_ahw_share_charts` | Share Ring Charts passed now, no vote, no category cooldown (vanilla effect; likewise `resolution_ahw_gate_breach`) |
| `effect every_country = { limit = { is_ai = no } remove_country_flag = ahw_has_portal }` | we get a second portal on the next 1st (the console targets move to it) |

**Run 41, steps 1–2 (2026-11-07): the contract works end to end; the head start did not come.**
Three nomads logged. Gate study on 01.02, the Upgrade at once (user). `ahw_debug.73`: Roaming
Uqo'Praknaran, techs given (no error). Contract accepted 01.11, **repaired 04.13** — the arkship
worked from the anchor. But game.log: "repaired by United Nations of Earth": finished by script,
the repaired gate's `on_build_complete` has `from` = the gate's owner (us), which overwrote the
nomad as `ahw_repairer`; the repairer is denied the head start, so we got none. Fixed after the
run: `ahw_repair_gate` hands the repairer over in the global target `ahw_script_repairer`, which
`on_build_complete` prefers (also fixes `ahw_debug.44`). **The rest of the head start works**:
with our `ahw_grant_head_start` removed by console and `ahw_debug.7`, both techs went 412 →
1787/2750 (15 → 65 %, `2026_11_07_33`–`_37`); the techs show vanilla's gateway icons. Step 3:
no "cost and days exclusive" error at load any more; the stabilise study is not offered without
Gate Theory researched (as designed).

**Run 42, step 1 (2026-11-07, screenshots `_38`–`_72`): the contracted nomad's arkship shuttles
between anchor and portal.** Study by the real offer (02.01 → 03.01) and the contract (accepted
03.07) work; the work project is at the anchor's star (save), but the Scientific Arkship ("GSS
Trok Petroisal", it carries the colony) keeps flying into the portal and back, months long. Not
the test ships in the portal (moved away: no change), not alloys (1000 given: no change, no
repair). **The broken gate loses its owner now and then** (save 2200.07.23: no owner; the 1st's
check takes it back — the "now owns the gate" lines since run 21); presumably the nomad then
heads off to reactivate it (`nomad_reactivatable`). Fixed after the run (untested): a nomad on
our contract does not qualify for the upgrade (`potential`). Open: what clears the owner.
The yearly summary `ahw.80` works. **Step 2 passed** (`_73`, 2201.08.02): the stabilise study
shows "Cost: 4000" (153 months), no error. Step 3 (decades of play) moved to run 43.

**Run 43 (2026-11-07, `_74`): the contract was cancelled 12 days after acceptance.** Study by
the offer, `ahw_debug.73` (Nomadic Rackuddon, arkship at the anchor Bindur), accepted 04.06,
"abandoned" 04.19 (save 2200.05.01: `TOAST_CONTRACT_ABORTED_ISSUER`; the nomad holds the chain as
completed; our borders open to it). Vanilla AI abandons only after 20 years, so an abort trigger
fired — which one, unknown (no save in between). The arkship stayed in the anchor (no shuttling).
After the run: `on_cancel` logs which abort conditions hold, the work project logs success and
failure. Run 41's contract, same code but the upgrade `potential`, succeeded.

**Run 43, second attempt (2026-11-07, with the cancel logging): the contract completes.** Study by
the offer (03.01), `ahw_debug.73` (Roaming Quentian Starfarers), accepted 03.28, work done 07.04,
gate repaired 07.05 "by Roaming Quentian Starfarers" — the repairer fix holds (run 41: "by"
us). No shuttling, no cancel; the first attempt's cancel stays unexplained (the logging stays in).

**Run 43, years 2200–2205**: the head start came on 08.01 (15 → 65 %) — contract to head start
works without console help. The yearly lines: only we and the contracted nomad have studied a
gate. **No AI empire owns its anchor after five years** (save 2205.01.15: 8 of 8 AI anchors
without a starbase), so no AI study, repair or use is possible yet — dead-end anchors seem low on
the AI's outpost list. Check again around 2230; if still unclaimed: offer study and repair to
the portal's own empire while nobody owns the anchor, or find a lever for the AI's outpost
choice. **The repaired gate loses its owner in 14 of 41 months** (the monthly check takes it
back); cause open, its Seal switch is unusable meanwhile.

**Run 43, years 2205–2211: the AI takes part.** By 2211 six of eight AI anchors have an outpost
(save 2211.01.01); the study is offered from 2205.11 and done within 1–2 years (Lavan Order
2207.03, Chimm Coalition 2207.12, Ztrakporan Corporate Union 2208.04, Ztrakporan Fire Tribes
2209.08; Commonwealth of Man offered 2206.07, not done; Wacegian offered 2210.10). No AI has a
gate tech or a repaired gate yet. **Every gate loses its owner** — the AI's broken gates are taken
back almost every month (171 "now owns the gate" lines); open whether it hinders the AI's repair
(the upgrade needs the gate's owner). Next look: ~2230.

**Run 43, years 2211–2220: the AI studies, but researches no gate tech.** By 2220 seven AI
empires have studied their gate (Wacegian 2211.10, Andarian 2212.06, Shapan 2212.11 joined);
none has either tech, though four have had the option 8–13 years (`add_research_option` keeps
it). We got Gate Theory 2213. Our techs had no `ai_weight` (vanilla's gateway tech has one only
for human auto-research). Fixed after the run: `ai_weight` factor 3 on both (vanilla priorities
are 1.25–2) — needs a new game to show.

**Run 43, resumed at 2220 with `ai_weight` 3** (tech definitions load from the files, not the
save): Shapan Entity researched Gate Theory 2221.06.02 — the first AI gate tech; by 2222 still
the only one (seven AI empires have both options). Slow; raise the weight if it stays so.

**Run 43, years 2222–2245 (saves read 2026-11-08): the AI repairs, and one empire explores
the ring on its own.** Gates repaired (save of 1 January): Chimm 2229, Wacegian and Shapan 2237,
Ztrakporan Fire Tribes 2241, Lavan 2244; Andarian and the Corporate Union not yet. **Shapan
Entity** sent two science ships through Furon 53 by 2238 and mapped nodes 40–52 (4 by 2239, 8,
10, 13 by 2242) — no AI empire else ever left its exit node (the one the study reveals). **Then
it stalled**: no new node 2242–2245, though nothing blocks either end (no fleets, lanes go on to
39 and 53; both ships have scientists, so `LIMITED_EXPLORATION` is not it). One ship idles in
node 42 beside three unsurveyed asteroids; the other shuttles 51 → 44 → 51 inside the known
stretch, ~80 days per node (runs 15–16's 104, parked). Their armour wears down (toxoid drain:
78/250 and 186/250, never repaired). Cause open; a lead: Shapan's gate loses its owner almost
monthly (the open issue) — whether the way home then looks blocked is unchecked. So natural
exploration exists but does not reach far: the shared charts stay needed.

**Run 43, the log (read 2026-11-08):** owner losses come **for all nine gates in the same
months** (1197 "now owns the gate" lines, nine per month, ~60 % of months) — one game-wide cause;
**no AI sealed in 45 years** (zero "SEALED"; the Sealed mode's `ai_weight` 50 is not enough —
Phase 2's sealing when threatened); **a late empire's portal works unattended** (Yl'Khahan
Entity, 2241.09.01, `ahw.30`) — the deferred late-portal test is covered.

## Test, run 44 (0.1.1: the AI with working gates, and the first Phase 2 features)

One game of ~10 years answers several things that do not get in each other's way: what the AI
does with a working gate (`ahw_debug.75` skips the decades of run 43), the owner loss's day
(`ahw.90`, automatic), and the new features — each tested by its own console line. Threat-based
AI weights and AI sealing are left out: they change what this run measures.

A new **medium** game, this mod and dev tools, AI empires on, 2–3 nomadic empires, console on.
Esc before each console line. Copy `logs/game.log` and `logs/error.log` before restarting.
1. **After the first 1st** (2200.02.01): every AI portal studied and teched, half repaired:
   ```
   event ahw_debug.75
   ```
2. **The contract again** (catches run 43's unexplained cancel; ~5 months): `ahw_debug.6`, a
   day, `ahw_debug.41`, the study on the next 1st with the test science ship, `ahw_debug.73`,
   issue the contract in the anchor. (This also makes us "studied", which step 4 needs.)
3. **Object texts** (a minute, any time): hover — and screenshot — our broken gate, the repaired
   one later, a ring exit gate (`ahw_debug.42` puts ships in our exit node), the portal's centre
   star, both techs (research screen). Each should end in a grey lore line.
4. **Ally under attack** (any time after step 2):
   ```
   event ahw_debug.78
   ```
   On the next 1st: the message "A Friend Under Attack", game.log "ally under attack … charts
   swapped".
5. **Play fast to ~2205** — the baseline: five years of what the AI does by itself.
6. **The Galactic Community** (~2205):
   ```
   event ahw_debug.77
   ```
   ```
   event ahw_debug.76
   ```
   Propose "Share Ring Charts" (category "The Ancient Highway"), let the vote run; then
   "Unrepaired Gates" and "Force a Gate Open" against the empire that sealed (game.log names
   it). Screenshot each proposal's tooltip. Expected: charts pooled at passing (game.log
   "charts: … from the Galactic Community"), members with a broken gate and both techs in breach
   (yearly line), the forced gate open and its Sealed mode refused (tooltip).
7. **Play fast to ~2210**, quit, copy both logs.

Read afterwards (agent): the "owner lost by" days (regular? what else happened that day?); the
yearly "ring" lines (entries per empire, nodes charted, before and after 2205); "repaired by"
for the broken half (the AI itself, a nomad?); the contract's end; error.log for `ahw_` lines
beyond the known noise. Control for the watch: with it running, the monthly "now owns the gate"
lines should all but stop.

**Galactic Community timing** (vanilla defines): a vote runs 1440 days, a recess 720, and a
category takes no new proposal for 2520 days after a vote — all three of ours share one category.
For tests: pass by console (`pass_resolution_no_cooldown`, `ahw_debug.80`), and DevTools'
`devtools.7`/`.8`/`.9` set our diplomatic weight ×10 / ×0.1 / normal for a real vote.

**Run 44, steps 1–4 (2026-11-08, to 2200.11, screenshots `2026_11_08_1`–`_5`):**
- **Owner loss, by day**: all nine gates on the same day, 2200.02.03, 08.26 and 09.14 — not on a
  1st, no fixed interval; the monthly "now owns the gate" line never appeared (the watch works).
- **AI repair with both techs: 3–4 months** (Commonwealth of Man 05.15, Heejam 05.22, Theian
  Preservers 05.27; Thimoan not yet). The bottleneck of run 43 was the techs, not the repair.
- **Contract: no cancel** this time (accepted 05.29, repaired 09.03, head start 10.01).
- **Object texts show** (broken gate, repaired gate, both techs, exit gate); the centre star's
  not yet looked at. The exit gate's panel shows a "Dismantle" button (disabled?) — to check.
- `ahw_debug.75`: one "Failed to create a starbase" (an anchor not free for an outpost); harmless.
- **Step 4 failed in the console line, not the feature**: `ahw_debug.78` wanted an attacker
  bordering the ally — nobody borders anybody in 2200, so nothing happened, silently. Fixed: any
  AI attacks if no neighbour does, and every outcome is logged.
- **Step 4 again (after a restart, from the 2200.11.01 autosave): ally under attack works.**
  `ahw_debug.78`: Silicron Sacred Nation our subject, at war with the Theian Preservers. On 12.01
  the message (`2026_11_08_6`) and the charts swapped: our one charted node (Caedris Node 3,
  system 618) is in Silicron's `visited_objects` in the 12.01 save — `set_visited` from a chart
  works. Silicron got the message about us too (as overlord we joined its war): harmless, kept.
  In the save the chart flag reads `ahw_mapped<country id>` (`ahw_mapped0`, `ahw_mapped1`).
- Owner lost again on 11.02, the day after that load — whether loads explain the other days is
  unknown (run 43 lost owners in ~60 % of months over long unbroken play, so not loads alone).

**Run 44, steps 5–6 (to 2207.03; the 2026-11-08 session played to 2207.01, proposed Share Ring
Charts by hand (2206.04, screenshots `2026_11_08_7`, `_8`) and ran `ahw_debug.76`; the votes were
passed by console on 2026-11-09 from the 2207.01.01 save, screenshots `2026_11_09_3`–`_9`):**
- **Share Ring Charts works**: on passing, every member ends at the pool's 12 nodes (we 9 + 3,
  Silicron 9 + 3 after the friend swap, the Theians 3 + 9, the rest 0 + 12); game.log "charts: n
  ring nodes from the Galactic Community to …". **No error at passing.** The one error.log line
  `Could not get dynamic flag 'ahw_mapped' with target 'event_target:ahw_chart_from'`
  (`ahw_share_charts_gc`, line 659) comes before it: at proposing (2026-11-08 21:45) and 14 s
  before the pass (14:23:17 / 14:23:31) — the game evaluating the effect for a tooltip, before
  any target is saved. Harmless; an `exists = event_target:ahw_chart_from` guard might silence it
  (whether a `limit` stops at the first false trigger is unchecked).
- **Unrepaired Gates passed** (2207.02.01); the breach is checked yearly, so unseen until 2208.
- **Force a Gate Open** (`ahw_debug.80`, against the Commonwealth of Man): "gate in Eshmet 41
  forced open", listed active under The Ancient Highway with its tooltip (`_3`). The 2207.03.01
  autosave is 2 s older than the console line, so it still shows `ahw_sealed`. **The Sealed
  mode's refusal is untested**: only the gate's owner sees the switch (`_4`, "You are not the
  owner of this Megastructure") — needs our own gate forced open (a debug line to write).
- Owner lost again the day after this load (2207.01.02), then 01.16 and 02.05 — the second load in
  a row followed by a loss the next day.
- Exit gate: "Dismantle" greyed out, "You are not the owner of the Megastructure"; its text says
  "Cannot be dismantled" (`_9`). Entry point and exit show their lore lines (`_4`, `_9`).
- **User: the centres should not look like colonies.** Clicking a centre opens vanilla's planet
  view: Colony Summary with Habitability "?", a Terraform button, "Frontier Planet", Colony
  Ascension (Eshmet 41's neutron star `_5`/`_6`, Caedris Node 3's black hole `_7`/`_8`). They are
  vanilla planet classes (`pc_neutron_star`, `pc_black_hole`, `common/star_classes/
  ahw_star_classes.txt`), and both systems are unsurveyed. Compared below: every vanilla star
  shows the same. The centre's lore line (step 3) is not in this view — its text is vanilla's.
- **User: the Commonwealth of Man can hardly reach its anchor and portal (Eshmet 41) early** —
  the way runs through a marauder empire. Portal placement does not look at what lies between an
  empire and its portal; a rule is to design (e.g. no marauder or fallen empire on the path, or
  within N jumps of its space).
- **To 2208.01.01 (same day, screenshots `_10`–`_12`): the yearly pooling and the breach never
  ran.** No "in force" lines; we had 19 nodes, the Theians 13, everyone else stayed at 12; Thimoan
  (Dovhar 31 broken, both techs) not named in breach. Cause: **a resolution category has one
  current resolution, the last passed** — the save's `galactic_community.passed` holds all three,
  but the window shows Force a Gate Open as the category's resolution, Share Ring Charts back to
  "Proposed" (an AI proposed it again, which its `allow` refuses while it is active) and Unrepaired
  Gates "Passed" (`_12`), and `is_active_resolution` was false for both. **Fixed (untested):** as
  vanilla's Galactic Reforms (`galactic_council_veto`), global flags `ahw_gc_charts` and
  `ahw_gc_breach` set on passing, cleared by the repeal, checked instead of
  `is_active_resolution` everywhere; Force a Gate Open is `fire_and_forget` (README: never on the
  list of active/passed resolutions). A save from before has neither flag, and **passing again
  does not set it**: `pass_resolution_no_cooldown` on a type already in `galactic_community.passed`
  does nothing — the console says "Executing effect script", no effect runs, no error (2208.02.01
  save: `passed` still 0 6 7, no flag; screenshot `_13`). Set the flags by console instead
  (`effect set_global_flag = ahw_gc_charts`, `… ahw_gc_breach`).
- **Fix, first check** (reloaded 2207.01.01 → 2207.02.01, screenshots `_15`–`_18`, save
  `2207.02.01.sav`): Unrepaired Gates passed by console, **`ahw_gc_breach` set**, the category shows
  it Active; its tooltip asks for the `ahw_gc_charts` flag. **Share Ring Charts did not pass**: it
  had left `proposed` without passing — not on the floor (no `voting` field), and the recess
  `cooldown` (359 at 2207.01.01) was gone too; what removed it is unknown (a lead: the two
  wrong-scope attempts just before). At 2207.01.01, proposed only, the same line passed it. So the
  console pass does nothing, silently, for a type already passed or no longer proposed. **Console `effect` runs in the selected
  object's scope**: with a fleet selected, `pass_resolution_no_cooldown` fails ("Wrong scope …
  Current Scope: fleet", error.log only) — click empty space first.
- **Fix confirmed on passing** (reloaded 2207.01.01 again, all three by console, screenshots
  `_19`–`_21`, save `2207.02.02.sav`): Share Ring Charts passed with the pooling (all to 12),
  Unrepaired Gates, Force a Gate Open ("Eshmet 41 forced open", star flag `ahw_forced_open`). The
  save has `ahw_gc_charts` and `ahw_gc_breach`; `passed` holds 0 and 6 only — **`fire_and_forget`
  keeps Force a Gate Open off it**, and the category still shows Unrepaired Gates afterwards (`_21`).
  The repeal is offered (its potential reads the flag).
- **And yearly** (played on to 2208.01.01): both "in force" lines, the pool lifting every member
  to our 19 nodes (+7 each), **"Thimoan Trade Association in breach (broken gate, both techs)"**
  (Dovhar 31), Eshmet 41 "forced open"; no new error. The pooling logged "0 ring nodes" for
  members that already had them — now logged only above 0, like the friends' swap. Still open: the
  Sealed mode refused on a forced-open gate — `ahw_debug.81` forces ours.
- **The colony-like view is vanilla's for every star** (`_10`, `_11`: Mewash A, a G star in an
  unsurveyed vanilla system — the same Colony Summary, Terraform, Frontier Planet, Colony
  Ascension). Not the mod's doing; changing it would mean the centre is no star.
- The dashboard ran next to this game (develop, 2026-11-09): its data extracted with this
  playset's two mods, and the data DB holds the mod's resolution category and its four resolutions.

## Quick checks, 2026-11-12 (run 44's 2208.01.01 save on 4.5.4, screenshots `2026_11_12_1`–`_5`)

- **A load clears every gate's owner.** Right after loading, still paused at 2208.01.01, our
  repaired gate said "You are not the owner of this Megastructure" (`_1`, `_2`), though the save
  holds `owner=0` (us) on `ahw_gate_1` and an owner on all nine. On 01.02 `ahw.90` logged "owner
  lost by 2208.01.02" for all nine and gave them back; the Seal tab worked again (`_3`). So the
  engine drops megastructure owners when it loads a save, before any script runs. Run 43 also lost
  owners in long unbroken play, so a load is one cause, not the only one. The daily watch covers
  both.
- **The centre star shows no lore line in the system view** (`_4`, Caedris 21's black hole): the
  hover is the star *body*, which keeps vanilla's planet class `pc_black_hole` and its
  `pc_black_hole_desc`; our line is in the star class's `ahw_sc_black_hole_desc`, which this
  tooltip does not show. To show it: our own star planet classes (copies of vanilla's with our
  desc) — not done.
- `ahw_debug.8` and `ahw_debug.81` ran ("Executed", game.log "gate in Caedris 21 forced open by
  the Galactic Community"); the mode still reads Open (`_5`), as expected — **the refusal itself
  is still unseen**: it needs a click on the Sealed mode.
- error.log: `Trying to remove undefined event target: ahw_sealer_1` at `ahw_debug.81` (the
  forced opening clears a sealer that never existed); harmless.

## Test, run 43 (a new campaign: the contract again, then a long game)

Run 42's plan, with the shuttling fix: a new medium game, this mod and dev tools, AI empires and
nomads on. `ahw_debug.6`, `ahw_debug.41`; the study on the next 1st with the test science ship;
then `ahw_debug.73` and the contract in the anchor. Expected: the arkship stays in the anchor
for the 90 days, the gate is repaired, and on the next 1st both techs +50 %. Watch whether the
monthly "now owns the gate" line still appears (what clears the owner is open). Then play on
for decades; game.log's "AHW yearly" lines and the saves tell what the AI did.

## Test, run 42 (a long game)

The real stages by hand, then decades of play to see what the AI and the nomads do. New: the
yearly summary `ahw.80` in game.log (who studied, who has which tech, which portals are repaired
or sealed, the express). A new medium game, this mod and dev tools, AI empires and nomads on.
1. **Contract → head start, in one go**: `ahw_debug.6` (outpost on the anchor) and
   `ahw_debug.41` (test ships in the portal; user: claiming and flying take too long for a test);
   on the next 1st the study is offered — do it with the test science ship (30 days); then
   `ahw_debug.73` and issue the contract in the anchor. After the repair, on the next 1st: both techs +50 % (no console help).
2. **The express study's cost on screen**: `ahw_debug.8`, `ahw_debug.70`, `ahw_debug.72`, a day:
   the study shows 4000 physics.
3. **Play on** at a high speed for a few decades, as you like. Autosaves yearly. Then quit and
   copy both logs; game.log's "AHW yearly" lines and the saves tell what the AI did.

## Test, run 41 (`0.1.0` + run 40 fixes)

Only what changed or failed in run 40; the rest works. A new medium game, this mod and dev tools,
AI empires and nomads on; Esc before each console line; save after each step; copy both logs
before quitting.
1. `ahw_debug.6`, a day, `ahw_debug.45`: the broken gate's **Upgrade** is clickable at once (run
   40: only after the next 1st). Do not start it.
2. `ahw_debug.73` (game.log: "test nomad … both techs" — no "invalid technology" in error.log).
   Right-click the anchor on the galaxy map, nothing selected: issue "Repair a Highway Gate" (if
   no menu, let a few months pass, as in run 40). Let time run: a nomad accepts, its arkship
   comes to the anchor and works there 90 days, the gate is repaired, and on the next 1st both
   techs jump by the head start.
3. `ahw_debug.70`, `ahw_debug.72`, a day: "Stabilise the Express Station" shows its cost, and
   error.log has no "both set both days_to_research and cost".

## Test, run 40 (`0.1.0`)

A new **medium** elliptical game, this mod and the dev-tools mod, AI empires on, **three nomadic
empires** (as in run 39), console on. Press Esc before every console line. **Save after each
part** (the numbers come from the saves); copy `logs/game.log` and `logs/error.log` before
quitting.

**A. The start** — nothing to do; the logs say whether the build, the nomads and the express
stations came out, and error.log should hold no "Could not find project" any more.

**B. Repairing on the gate.** Own the anchor, then skip the study and the techs:
```
event ahw_debug.6
```
Let a day pass.
```
event ahw_debug.45
```
```
event ahw_debug.8
```
Open your portal's system view and click the broken gate. Is there an upgrade to "Highway Entry
Point" (300 alloys, 50 influence)? Screenshot its tooltip. If short of alloys:
```
resource alloys 1000
```
Start it, let the 90 days pass. Does the gate change its look? Then: its Seal tab
— can you switch it to Sealed? Screenshot.

**C. A second portal, and the contract.** Ask for a second portal:
```
effect every_country = { limit = { is_ai = no } remove_country_flag = ahw_has_portal }
```
Run past the next 1st (a short freeze, then a new portal near your capital; screenshot the map).
Then own its anchor and fetch a nomad:
```
event ahw_debug.6
```
Let a day pass.
```
event ahw_debug.73
```
In the new anchor system, issue the contract "Repair a Highway Gate" (system view, contracts).
Screenshot the contract list. Let time run (fast) until a nomad accepts — or a few years pass —
and note what happens: does its arkship fly into the portal and work there, does the gate get
repaired, did you get the head start (both techs jump to 65 % or more)? If instead the nomad
repairs the gate by itself (the upgrade), the contract should cancel — note that too.

**D. The express.** Wake it and put ships at a station:
```
event ahw_debug.70
```
```
event ahw_debug.72
```
Let a day pass. In that station's system view: two wormholes, one on each side of the centre,
along the line from the galaxy's middle? Screenshot. A study "Stabilise the Express Station"
should be offered (situation log); before starting it, order the science ship through a
wormhole: refused while the link is closed (tooltip)? Then start the study with the science ship
(research points; it may take a while). Afterwards: order the ship to the next station — does the route go through the
wormhole? Screenshot the route.

**E. Nomads on their own** (no action): at the end, game.log's lines "study … offered to the
nomads", "repaired by …" show whether nomads studied or repaired anything unasked.

**Run 40, steps 1–4 (2026-11-07, `0.1.0`, medium, nine portals, two nomads logged, screenshots
`2026_11_07_15`–`_23`): repair on the gate, the seal and the express work.**
- Build 3 s; the express's 8 stations logged; error.log free of "Could not find project".
- **Repair as an upgrade works**: the broken gate shows a disabled "Complete" until it has an
  owner (`_15`, 01.02 — the console study ran before the monthly check gave it to us; since then
  the study gives it at once), "Upgrade" from 02.01 (`_16`), repaired 05.01 (`_17`, "repaired by"
  in game.log): the engine ran `on_build_complete` (no fallback line).
- **Seal**: Sealed for 25 influence (71 → 46, `_22`, `_23`).
- **Express**: two wormholes on opposite sides of the station (`_18`); a closed link refuses with
  our tooltip ("Travel to Unknown" crossed out); links flipped 4 + 5 (06.01), 7 (07.01); with
  link 4 open the science ship's route took the wormhole (`_21`) and reached the next station in
  29 days. The stabilise study: 4000 physics = **149 months in year 2200** (`_19`) — fine at the
  mid game, where it starts; to tune later.
- **Step 5**: the second portal works (Dovhar 32 off Procyon, 08.01; study offered 09.01).
  **The contract is untested**: right-clicking any system on the galaxy map (nothing selected)
  opens no contract menu at all — vanilla contracts neither — after console `communications`
  (Nomads DLC active; no define, game rule or tech gates issuing). Decided (user, 2026-11-07):
  test it later in a game where nomads are met the normal way; a control without the mod if it
  fails again. `ahw_debug.73` failed to give the techs ("invalid technology": their potential
  needs `ahw_highway_studied`) — fixed after the run. The monthly check logs "now owns the gate"
  for an already owned gate each month (runs 21, 23 too) — to look into.
- **The contract** (later in run 40): the issue menu appeared by itself a few months after the
  console `communications` (cause unknown; normal contact should not need it). Issued in Procyon
  for 1000 (`_24`, `_25`); **Nomadic Alarian accepted** (2201.03.28, `_26`); its arkship flew to
  Procyon — the contract's location — and left: the work project was in the portal (save
  2202.04.18: location the star of Dovhar 32), where the AI never went. Fixed after the run: the
  project is in the anchor (`location = fromfrom`). The contract's rewards preview lists our
  repair's ownership change (`_27`).
- **Fixed after the run**: the express study had `cost` and `days_to_research` (exclusive,
  error.log); cost modifiers lacked `desc`; the first grant read unset variables.

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
  console shortcuts above, unless the test is about that stage. Mod files load at game start.
- **Numbers come from saves**, not screenshots (ships' `armor_hitpoints`/`shield_hitpoints`,
  `stored_techpoints_for_tech`, flags). Where things are in the `gamestate` (2026-11-08): who
  has entered a system is the country's `visited_objects` (every non-`default` country lists
  every system — ignore them); a fleet names no owner, the country's `owned_fleets` does; a
  fleet's position is the `origin` in its `movement_manager`'s `coordinate` (the first `origin`
  in the block is its combat's); a body's surveyor is `surveyed_by` in `planets`. Copy `logs/game.log` and `logs/error.log` before
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

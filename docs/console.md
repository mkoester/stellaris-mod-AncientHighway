# Ancient Highway — console events

Moved out of `AGENTS.md` on 2026-11-14 to keep that file under the size at which an on-demand instruction file is cut off. Read this before running or adding a console event.

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

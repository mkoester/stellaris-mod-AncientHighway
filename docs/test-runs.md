# Ancient Highway — test runs 40 onwards

Moved out of `AGENTS.md` on 2026-11-14. Newest first; the spike's runs 1–39 are in `spike-runs.md`. Add each new run at the top of this file, not to `AGENTS.md`.

## Observation: the count in the campaign (2234.10.01–2236.01.01, read 2026-11-22)

The user's campaign with the count (`ahw.90` → `ahw_repair_watch`) and `ahw.26`, loaded from
`autosave_2234.10.01`, observed with `play 0`; run 46's step 1 (a player's repair) was not played.
- **Five gates repaired, all by the count**: Interstellar Yibrak Hierarchy (Caedris 23, upgrade
  seen 2234.10.05), Vran Free Traders (Eshmet 43, 10.09), Haddam Harmony (Ashkara 01, 10.25) and
  Great Model-16 Pact (Belun 11, 2235.08.17) started the **engine upgrade themselves** — each
  dropped by the next owner loss (2234.10.29, 2235.08.21), each finished by the count 90 days after
  it was seen (`… finished by the count`, `AHW entry point … repaired by …`). None of the 71 saves
  before the fix holds an upgrade in progress, so whether the AI had started and lost repairs
  before stays open; these four got their second tech recently, and acted within weeks (as in
  run 44).
- **Thembolon by script**: `AHW AI repair: Thembolon Accord pays and starts the gate in Eshmet 42 on
  2235.10.01` — the 12th month of `ahw_both_months`; repaired 2236.01.01. Charged once:
  2235.09.01 → 10.01 alloys −275.6, influence −43.85, against a monthly net of +24.4 / +6.15 the next
  month — exactly 300 + 50, so `upgrade_megastructure_to` from script charges nothing (run 46,
  step 2). The engine's upgrade ran alongside (`progress=30` at 11.01) until an owner loss dropped
  it on 2236.01.01, the count's last day.
- **Not yet**: no AI entry into the ring by 2236.01 (no ring lines in the yearly summary); the
  pop-up `ahw.93` and the disabled second click (a human repair).
- **error.log**: one new line, on 2235.01.09 (days after the first repair): `Could not get dynamic
  flag 'ahw_mapped' with target 'event_target:ahw_chart_from'` in `ahw_share_charts_gc`, called
  from the Share Ring Charts resolution's effect — no resolution passed (no `AHW resolution` line),
  so presumably the engine evaluating the effect (tooltip or AI) with the target unset. Harmless
  so far. The user: the resolution was proposed among the first, with high support (the Galactic
  Community formed after 2234.09). Guarded the same day (`exists = event_target:…` before each
  flag lookup in `ahw_share_charts_gc`); to confirm: the line gone from error.log, and at passing
  `AHW resolution Share Ring Charts passed` (no node charted yet, so no `AHW charts:` line).
  **Passed by console** 2236.02 (`effect pass_resolution_no_cooldown = resolution_ahw_share_charts`
  — in observer mode the console's `effect` does nothing: `play 0` first): the line logged, no
  `AHW charts:`, no new error. The community formed 2235.01.01, days before the error line.
  The game ran the pre-guard code (mod files load at start), so the guard is still unconfirmed.
- Owner losses: 14 days with losses in 15 months.

## Observation: two more years observed (2236.02–2238.01, read 2026-11-22)

Same session, observer mode, after Share Ring Charts passed.
- **No AI uses the ring**: three years after the first repair (Caedris 23, 2235.01) no fleet is in
  a ring node or a repaired portal (`autosave_2238.01.01`), no `ahw_mapped@` flag exists, and the
  yearly summaries list no ring entries. The ring is no shortcut by design, so shortest-path routing
  should not pick it while the lanes are open — whether the AI takes it when borders are closed
  (the point of the mod) is still untested: it needs a set-up game.
- **Second late portal**: League of Vartivar IV, 2236.10.01 (Eshmet 45 off Icheon, worst lane
  margin −5.4: beside a lane, the fallback placement).
- Studies go on: Bloomwrought Wildscape of Tellon (2237.05.05) and Havariggan Purifiers (05.12),
  both with their ship this time. Free Beldroan Battle Clans holds both techs since 2236, not yet
  repaired (`ahw.26` waits 12 months).
- error.log: nothing new naming `ahw_`.
- **To 2239.01.01** (same session): still no ring node charted, no fleet in the ring. Free Beldroan
  Battle Clans (16777245, `ahw_gate_broken_10`) has `ahw_both_months` 28 but never reached the
  600-alloy reserve: 242 → 307 alloys from 2238.09 to 2239.01 (+16 a month), influence at its
  1000 cap — the AI keeps few alloys, so the reserve, not the will, decides. Roaming Cybergang
  (AI-run while observed) now holds both techs. `ahw_yearly`: "resolution Share Ring Charts in
  force". error.log: nothing new.
- **2239.01.01–2240.01.01** (a new session, loaded at 2239.01.01, with the guard in
  `ahw_share_charts_gc`): three more AI repairs started by the AI itself — Misharan Pact (Dovhar 32,
  seen 01.06), Pact of Fellnoll (Dovhar 34, 01.10), Free Beldroan Battle Clans (Ashkara 02, 01.16,
  with ~307 alloys: the cost, not the 600 reserve) — all dropped by the owner loss of 02.16, all
  finished by the count (04.06–04.16). Eight gates repaired. **Both batches of self-started repairs
  came within three weeks of a load** (2234.10.01 → 10.05/09/25; 2239.01.01 → 01.06/10/16), the one
  exception Great Model-16 Pact (2235.08.17): perhaps the AI plans the upgrade after a load, or it
  started repairs before too and lost them to owner losses unseen between monthly saves. The user
  keeps the 600 reserve for `ahw.26` (2026-11-22): the AI pays the cost on its own when it can.
  Still no ring node charted; error.log nothing naming `ahw_`.
- **2240 — the first ring use**: Slerpanoran Hegemony repaired Dovhar 35 the same way (seen
  2240.01.12, dropped 02.30, counted to 04.12; nine gates). The yearly summary of 2241.01.01:
  `ring Haddam Harmony: 3 nodes charted, entries this year 0 military, 5 civilian`, `ring Free
  Beldroan Battle Clans: 2 nodes charted, … 0 military, 3 civilian` — **AI civilian ships (science
  ships exploring, presumably) enter the ring; no military fleet yet.** Then the sharing ran:
  close friends (`2 ring nodes from Free Beldroan Battle Clans to Great Model-16 Pact`, `… to
  Havariggan Allied Stars`) and Share Ring Charts — 4 nodes from the Galactic Community to every
  member (1 or 2 to those that had some). Both chart paths now seen in a real game.
- **2241**: still civilian only — Haddam Harmony 4 entries (5 nodes), Free Beldroan Battle Clans 2
  (5 nodes); the yearly sharing passed the new nodes on (2 to each member). On 2241.07.01 `ahw.20`
  handed all 26 gates back before the daily watch did (as on 2225.04.01). error.log: nothing new.
- **2242**: civilian only again (Haddam Harmony 2 entries, Free Beldroan Battle Clans 3; 7 nodes
  each) — though 8 "ally under attack" swaps came in the year (Great Model-16 Pact and Havariggan
  Allied Stars, friends of Free Beldroan, at war): far friends at war did not send a fleet round.
  No new repair; error.log nothing new.
  **Could they have gone round?** (`autosave_2243.01.01`, asked by the user): no gate is sealed (no
  `ahw_sealed_*` flag). Havariggan Allied Stars could not be reached by the ring: its gate
  (`ahw_gate_broken_15`) is broken and it holds Gate Construction only. Free Beldroan (pair 10, exit
  Node 88-11) and Great Model-16 Pact (pair 2, exit Node 88-15): both gates repaired, both hold both
  techs, four ring nodes apart. Free Beldroan's `visited_objects` hold Nodes 88-6 to 88-14 — all
  but the friend's exit node, which it sees as a neighbour; Great Model-16's 88-6 to 88-13 and 88-15.
  So the route was open and nearly known. No fleet went: "ally under attack" is not a war
  participation, so the AI had no reason to send one (whether it would, as a war ally, is run 47's
  question). Side note: the chart flags (`ahw_mapped@`) cover only 88-6 to 88-13 for every
  country, while Free Beldroan visited 88-14 and Great Model-16 88-15 — an entry that set no chart
  (its own exit node from the study's `set_visited`, presumably; 88-14 unexplained).
- **2243**: three more self-started repairs, each dropped and counted to the end — Bloomwrought
  Wildscape of Tellon (Ashkara 04, Hethra 73), Havariggan Purifiers (Dovhar 31); twelve gates
  repaired. Ring entries still civilian only (Haddam Harmony 5, Free Beldroan Battle Clans 4; 10
  and 9 nodes charted of 88).
- **2244**: Havariggan Purifiers' repair started by `ahw.26` (Caedris 21, paid 2244.09.01, dropped
  09.29, counted to 12.01) — the script path's second use; Alliance of Tarassian Systems started its
  own (Galvaas 63, 12.06). Thirteen gates repaired. A third empire enters the ring (Slerpanoran
  Hegemony, 1 civilian); still no military entry. Every one of the 30 countries holds the same 15
  chart flags (the Community's sharing evens them out). **The console grant meant for Free
  Beldroan Battle Clans landed on Roaming Cybergang**: `autosave_2245.01.01` has all 88 ring nodes in
  Roaming Cybergang's `visited_objects`, Free Beldroan 16 — the `effect` ran with the player's
  empire as root (the `play` had not taken). League of Vartivar IV (74) also lists all 88, as every
  non-default country does — presumably kept from before it became a regular empire.
  error.log: nothing new.
- **2245 — the first military entry**: Havariggan Purifiers (40, fanatic purifiers, the player's
  rival): `1 nodes charted, entries this year 1 military, 1 civilian` — presumably its own exit
  node, after its two repairs (Dovhar 31, Caedris 21). Civilian traffic grows: Slerpanoran Hegemony
  6, Roaming Cybergang (AI-run while observed) 6, Haddam Harmony 5, Free Beldroan Battle Clans 4;
  nine civilian fleets sit in ring nodes at 2246.01.01, none military. Fifteen gates repaired
  (Alliance of Tarassian Systems' Galvaas 63, NEX Core's Hethra 71, both counted to the end).
  **The first head start in the campaign**: `head start at the entry point in Caedris 21 for Qvefoz
  Covenant` (+50 % of each tech) — Caedris 21's anchor changed hands after Havariggan Purifiers
  repaired it. A story fragment (5 of 12) for Roaming Cybergang on 2245.06.29, while the user
  played it. Free Beldroan still knows 22 of 88 nodes: the redone console grant did not reach it.
  error.log: nothing new.
- **2246 — the whole ring known to the Community**: Roaming Cybergang held all 88 chart flags by
  1 January (`ring Roaming Cybergang: 88 nodes charted`; the console line with `ahw_mapped@root`,
  run on the player's empire). Its close friends got 64–67 nodes, then Share Ring Charts gave every
  member 65–67: at `autosave_2247.01.01` all 30 Community members hold 88 chart flags and 88 visited
  ring nodes; Havariggan Purifiers (not a member) 1. From 2247 every member can plot a route along
  the whole ring — the condition for watching military use. 2246 itself: civilian only (Roaming
  Cybergang 23, Haddam Harmony 9, Slerpanoran Hegemony 8, Free Beldroan Battle Clans 4); Giroan Star
  Regime repaired Galvaas 64 and 61 (counted): seventeen gates. A broken-gate inspection by a nomad
  (Nomadic Techaran Wayfarers, pair 4). error.log: nothing new.
- **2247, the first year with the whole ring known**: still no military use by a Community member.
  Civilian entries grow (Roaming Cybergang 28, Haddam Harmony 12, Slerpanoran Hegemony 9, Free
  Beldroan Battle Clans 5, NEX Core 2, Great Model-16 Pact 1); Havariggan Purifiers (no charts,
  not a member) again 1 military entry — its own exit node, presumably. Backattan Empire (Dovhar 33)
  and Havariggan Allied Stars (Ashkara 03) repaired (counted): nineteen gates — Free Beldroan's two
  friends can now both be reached through the ring. Only one "ally under attack" in the year.
  error.log: nothing new.

## Test, run 46 (planned 2026-11-22: the repair counted by script, the AI's repair)

In the campaign, from `2234.10.01_repair-stopped` (Thembolon's dropped repair is lost: the count
starts only with an upgrade seen after the fix). Copy `logs/game.log` before restarting.
1. **A repair survives a load**: `play 16777233`, `resource alloys 300`, click Upgrade on the gate
   in Eshmet 42, run 2 days — game.log `AHW repair of the gate in Eshmet 42 seen …`. Save, load,
   run 2 days: `… the engine dropped its upgrade …, N days left`, the pop-up *The Gate Repair Goes
   On* (does the day count show, or a raw `[…]`?), and the Upgrade button disabled with "already
   under way". Alloys and influence not charged again. Run on until `… finished by the count`
   (~88 days, `fast_forward`?): the gate repaired, `AHW entry point in Eshmet 42 repaired by
   Thembolon Accord`.
2. **Unanswered by step 1**: whether `upgrade_megastructure_to` from script charges the cost (the AI
   path pays by hand — Thembolon's stockpile before and after an `ahw.26` start shows it).
3. **The AI**: `play 0`, observe ~13 months. Any AI with both techs, 600 alloys and 100 influence:
   `AHW AI repair: … pays and starts the gate …`, then `… finished by the count` 90 days later.
   Thembolon's counter starts with the fix, so its first chance is 12 months on.
4. error.log: nothing new naming `ahw_`.

## Observation: the user's campaign continued (2226.08–2234.09, read 2026-11-22)

Roaming Cybergang again, with `4835f95` and `5edaa00`. Read from the saves `2227.01.30`–
`autosave_2234.09.01` and the session's logs (2228.04.09–2234.09.01, loaded twice).
- **An AI with both techs never repairs**: Thembolon Accord (16777233) has held both gate techs
  since 2227.01.30 at the latest (2226.08: Construction only), and at 2228.04.09 had 2376 alloys
  and 911 influence (cost 300 + 50). Its gate (`ahw_gate_broken_18`, Eshmet 42) is its own
  (`owner=16777233`) and never had a build queued (`build_queue` empty in every save), 7.5 years
  on. Run 44's AIs repaired within 3–4 months. **Not** a missing `ai_weight`: the game's
  `99_README_MEGASTRUCTURES.txt` gives a default of 100 (vanilla's gateway: 5). Cause open —
  candidates: the owner losses (~every 26 days here), the AI's megastructure budget, war.
  **In game as Thembolon** (`play`, 2026-11-22, screenshots `2026_11_22_2`, `_3`): right after the
  load the button read a disabled "Complete" (the load clears the owner); a day later (`ahw.90`)
  "Upgrade", its tooltip "Cost: 50 influence, 300 alloys — Lacking 222 alloys". So the upgrade is
  open to the AI, and today only the cost blocks it — but it had 2376 alloys at 2228.04 and spent
  them elsewhere (military power 1681 → 1925 by 2230): the AI does not pick the repair while it
  can afford it.
- **An owner loss stops a repair for good** (2026-11-22, the user as Thembolon, from
  `autosave_2234.09.01`): the upgrade started ~09.02; `autosave_2234.10.01` holds it on the gate,
  `upgrade = { upgrade_to="ahw_gate_18" progress=29 halted=0 indefinitely_halted=no }`. Loading that
  autosave cleared the owner; afterwards the repair did not go on and the 300 alloys + 50 influence
  were not refunded (the user's report). With a loss every few weeks, a 90-day repair rarely
  survives — for players too. **Dropped, not halted**: a manual save right after the load
  (`2234.10.01_repair-stopped`, no day passed) has the gate with neither `owner` nor `upgrade`, and
  Thembolon's alloys and influence as before the load (102.6 / 504.7). The progress is gone; a
  script must count the repair itself.
- **The shipless study fix works unforced**: Nomadic Techaran Wayfarers' study on 2230.06.20 ran
  with THIS empty (`AHW study without a ship: Galvaas 61 …`) and got its grant; Priman Matrix's
  (2230.01.28) ran with its ship.
- **Work in the campaign**: a late portal (`ahw.30`) for Commonwealth of Deteenal II on
  2230.11.01 (Galvaas 65 off Giedi; Giedi still unowned at 2234.09, so the gate has no owner);
  the travel grants (`AHW travel tech tech_hyper_drive_2 feeds …`, two countries); the yearly
  "learns from others"; the broken-gate study (`ahw_construction_behind`, so `check_variable`
  against a variable works); ally under attack (9 swaps); the cap withdrawals.
- **Log texts**: the grant lines print `+0.02 ofahw_tech_gate_theory$ (askedahw_d$)` and
  `grantahw_grant_study$ 0.15$` — a `$PARAM$` in a log string eats the space before it and
  leaves a `$`; `asked` prints the variable's name, not its value. Cosmetic.
- **Owner loss**: all gates at once, 89 times in ~77 months, two loads in that time. `ahw.90`
  gave each back.
- Still no ring node charted, express dormant. error.log: only the modifier-icon noise.

## Test, run 45 (planned 2026-11-19: the story events and the inspection balance)

A new **medium** game, this mod and dev tools, console on, at least 4 AI empires. Esc before
each console line. Copy `logs/game.log` and `logs/error.log` before restarting.
1. **Read the texts** (a few minutes, any time): all twelve fragments, then the core three. Each
   is a pop-up with one button. Screenshot any that read wrong or overflow.
   ```
   event ahw_debug.83
   ```
   ```
   event ahw_debug.8
   ```
   ```
   event ahw_debug.82
   ```
2. **A new game for the real triggers.** Own the anchor and study the gate the normal way:
   `ahw_debug.6`, then on the next 1st start the study with a science ship. When it ends, *A Door
   Shut From Inside* pops up.
3. **The alternating studies**: `ahw_debug.46` puts test ships next to a foreign portal. Fly a
   **military** ship into it, then into two more foreign portals (broken gates: nobody has
   repaired yet). The offered study should go Theory ("Observe the Portal's Heart"), then
   Construction ("Examine the Broken Gate"), then Theory again — game.log `AHW centre study` /
   `AHW broken-gate study … offered`. Finish them: `+0.1 of ahw_tech_gate_theory` (a new kind of
   centre, else `+0.07`), `+0.07 of ahw_tech_gate_construction`. Each portal's first entry also pops up a fragment, a
   different one each time (`AHW story fragment 1 of 12`, `2 of 12`, …).
4. **The other two chapters**: finish a gate tech by the vanilla command, which should fire
   `on_tech_increased` (whether `ahw_debug.8`'s `give_technology` does is unknown):
   ```
   research_technology ahw_tech_gate_theory
   ```
   *Written in Eights* pops up. Repair
   the gate (`ahw_debug.40`) and fly into the ring: *The Road Round the Outside*, and no fragment
   in that first reach. Fly on until the next reach: a fragment.
5. **The grants without exploring** (2026-11-20). Before step 2's study, research a travel tech:
   ```
   research_technology tech_hyper_drive_2
   ```
   At the study game.log shows `AHW travel tech tech_hyper_drive_2 feeds …` and `+0.1` of each
   gate tech. On the next 1 January: `AHW yearly …` and, for any country in contact with one that
   holds a gate tech, `learns from others`. The AI weights read a variable: an error.log line
   naming `ahw_got_` or `ai_weight` is a finding.
6. error.log: nothing new naming `ahw_` beyond the known noise.

## Replay: the AI nomad's study (2026-11-20, `autosave_2226.07.01` → `2226.08.02_replay`)

The user's campaign replayed for a month with the instrumented study project (`9ffc058`) and
`4835f95`. The autosave `2226.08.01` was overwritten by the replay.
- **Cause found**: Roaming Mirovandian's `AHW_STUDY_PROJECT` completed on 2226.07.27, and its
  `on_success` ran, but with THIS empty — `AHW study project done: this , owner , date
  2226.07.27`. So `ship_event = { id = ahw.22 }` fired nothing: no `ahw.22 fired` line, no flag, no
  error. The documentation (`common/special_projects/documentation.txt`) names THIS = the ship,
  FROM = the location, PREV = the country. Why the ship is missing for an AI nomad is unknown.
  **Fix (same day)**: `on_success` keeps the ship path when THIS exists, else marks FROM's system
  with PREV as the studier (`AHW study without a ship: …`), and logs all three scopes.
  **Fix confirmed** (second replay, same day): `this , from Ashkara 01, prev Roaming
  Mirovandian`, then the study's grant (+0.15 of each tech) and `AHW study without a ship:
  Ashkara 01 studied by Roaming Mirovandian on 2226.07.27`. Its only error.log line, `Unknown
  property ahw_got_construction`, came from the first grant's log printing a total not yet set;
  `ahw_grant_tech` now sets both totals up front.
- **Travel grants**: no line, as expected — of the 20 countries that had studied, only the player
  and one AI empire (16777241) hold a travel tech (Hyper Drive II), and neither finished a tech in
  the month, so `on_tech_increased` (`ahw.63`) never ran for them. Every studied country still
  holds just the study's 15 % (the player 0.59 / 0.3). The yearly "learns from others" is due on
  1 January.
- **Owner loss**: all 22 gates at once on 2226.07.02 (the day after the load) and 07.15 (no load
  near), each given back by `ahw.90`.
- error.log: only the modifier-icon noise for `ahw_`.

## Observation: the user's campaign continued (2217.01–2226.08, read 2026-11-19)

The same campaign (Roaming Cybergang, huge, 22 portals with an owned anchor), resumed with the
tech weights of 2026-11-18 (`8b563e9`) and, in the last session (2225.03.12–2226.08.01), the
story events and the inspection balance (`c0a6ab5`). Read from the saves `2217.07.01`–
`autosave_2226.08.01` and that session's logs.
- **AI gate techs, at last**: the first between 2221.10 and 2223.04 (4–6 years after the weight
  change); at 2226.08 seven empires hold one each — Gate Theory: Havariggan Purifiers, Mandate of
  Evari, Interstellar Yibrak, Vran; Gate Construction: Haddam, Fellnoll, Thembolon. **None holds
  both**, so still no repair, no charted ring node, 26 years in. 20 countries have studied.
- **Works in the campaign**: a story fragment (3 of 12) on the player's first entry into Furon
  52; the broken-gate study offered there and finished (+0.05 Construction; the player's grants:
  theory 0.59, construction 0.3); "ally under attack" (four swaps, 2225.10.01); the cap
  withdrawals (`ahw_cap_check`, three lines). error.log: only the modifier-icon noise.
- **AI nomads study, but it does not take**: Roaming Mirovandian (country 1) was offered the
  study at Ashkara 01 on 2226.06.11 (`ahw.60`). Autosave 2226.07.01: `AHW_STUDY_PROJECT`
  `in_progress`, its science ship (fleet 16778092, ship 3507) on a `survey_planet_order` of the
  portal's black hole (planet 10227, the project's carrier — as for every AI empire's study).
  Autosave 2226.08.01: `last_completed_special_project="AHW_STUDY_PROJECT"`, the ship surveying
  another body in the same portal — but no `ahw_highway_studied` flag, no "studied by" line, no
  error. The player's own nomad study (same `ahw.60` path) worked earlier, and the AI empires'
  (`ahw.20`) do. Cause open: whether `on_success` runs, and in which scope. Instrumented
  2026-11-19 (a log line in the project's `on_success` and at the top of `ahw.22`); replay from
  `autosave_2226.07.01` to 08.01 and read game.log.
- **AI exploration of foreign portals is rare**: `ahw_entered_N` (any portal or exit node, own
  included) is 1 for most AI empires, presumably their own portal; three entered 2–4; one was
  offered two centre studies and did neither. The inspection studies are effectively
  player-only so far.
- **Owner loss**: all 22 gates at once, 27 times in 17 months (every 1–7 weeks); two right
  after a load (2225.03.13, a day after; 2226.04.01, two days after the 2226.03.30 load), the
  rest with no load near. On 2225.04.01 `ahw.20` handed out all 22 before the watch did. `ahw.90` gave each
  back.
- **Express**: dormant.

## Observation: the user's campaign, no console (0.1.1, 2200–2217.01, read 2026-11-18)

Not a test run: a real game, played as a nomadic empire (Roaming Cybergang), **huge** galaxy
(88 ring nodes, 28 portals), game 4.5.4, 33 mods (the highway as the local dev copy). Read from
the saves `2200.12.01`–`2217.01.13` and the last session's logs (2216.12.01–2217.01.13).
- **Build**: all 28 portals and the ring as designed; error.log has only the known modifier-icon
  noise for `ahw_`.
- **Studies, unforced**: the first between 2203.09 and 2205.05; then 3 (2208.11), 6 (2213.01),
  10 (2215.03), 13 (2216.12) countries — 12 of the 19 anchor owners, and the player as a nomad
  (`ahw.60`, on entering a portal: works).
- **Techs: none in 17 years.** All 13 have both gate techs among their options, with the study's
  15 % stored, some for ~12 years; one AI empire was researching Gate Theory at 2217.01.13.
  So every gate is still `ahw_gate_broken_*` and no ring node is charted (`ahw_mapped@` absent).
  `ai_weight` 3 (×1.5 rare, `AI_TECHNOLOGY_RARE_WEIGHT_MULT`) loses to vanilla's priority factors
  (5 for labs, alloys, ship types, starbases). Run 44's quick AI repairs came after
  `ahw_debug.75` had given the techs: the tech choice is the bottleneck, left alone.
- **Owner loss**: all 19 gates with an owned anchor at once on 2216.12.02 (the day after the
  load: the known cause), 12.29 and 2217.01.13 (no load; 27 and 15 days apart). A manual save
  (2216.12.11) and pauses of 9–99 s did not line up with either. `ahw.90` gave each back.
- **Express**: dormant (the mid-game pulse has not come).

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
- **The Sealed mode is refused on a forced-open gate.** `ahw_debug.8` and `ahw_debug.81` ran
  (game.log "gate in Caedris 21 forced open by the Galactic Community"); the mode stays Open
  (`_5`), and the Sealed button's tooltip lists "The Galactic Community has forced this gate open;
  it cannot be sealed for now" as the one unmet condition (`_16`).
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

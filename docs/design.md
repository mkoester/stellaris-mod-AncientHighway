# Design

Status 2026-11-07: Phase 1, the real mod (`0.1.0`), after a feasibility spike (runs 1–39,
`spike-runs.md`). The building blocks behind each mechanic, and how sure we are of them, are in
`../AGENTS.md`, "Feasibility".

## The problem

In other 4X games one settles on land but can still reach almost any place via the oceans (unless
landlocked, or the target is). Stellaris has no ocean: after a few decades most empires are boxed in
by their neighbours. An ally on the far side of the galaxy, or a war one wants to join, is out of
reach — and that makes distant alliances pointless in many playthroughs.

## The Ancient Highway

### The ring

**Decided 2026-11-04 (user; replaces the ring around the core, runs 1–12):** the ring runs
**around the outside of the galaxy**, beyond the outer rim, with **many more** systems.

Why: the highway is **not a shortcut** but a **second way to get everywhere that closed borders
cannot block for good**. Hence the yardstick: **going once round the ring takes about as long as
going once round the galaxy at mid radius** (halfway between the core and the outer rim) by
ordinary hyperlanes — or a bit longer, never shorter.

- **It follows the galaxy's outline** at a fixed distance beyond the outer rim, not a circle
  (decided 2026-11-04): an elliptical galaxy is not round, and a circle would leave long empty
  stretches on its short sides.
- Ring systems are joined to each other by ordinary hyperlanes, one after the other; no lanes
  into the regular galaxy (that is what entry points are for).
- They can never be claimed or settled: no outposts, no claims — always neutral ground.
- No ordinary star in the centre, but something artificial (see `lore.md`), **drawn at 20 % of
  vanilla's size** in both the galaxy map and the system view (user, 2026-11-05): our own star
  classes (`icon_scale`) and a small `size` in the initializer.
- **Centre types (decided 2026-11-05): a mix, no slowdown.** Look and ship effect come from the
  star class, so we define our own. The ring **and the portals** mix three (portals: user,
  2026-11-06, replacing "portals stay black holes" — a new kind of centre feeds the physics tech,
  "Access"):

  | Type | Effect on ships in the system (vanilla's) |
  |---|---|
  | Black hole | disengage chance −50 %, emergency FTL takes 50 % longer |
  | Pulsar | shields −100 % |
  | Toxoid star | armour −100 % |

  **To rethink (user, 2026-11-06, after run 25):** the full vanilla effects may be too hard —
  "especially toxoid: 0% armor instantly and normally no repair on route might defeat the purpose
  of the mod." Idea: keep each centre's general effect but apply it slowly, "like 0.1% damage per
  day in that system".
  **What vanilla's −100 % does** (game files read 2026-11-06, plus the user's test): the modifiers
  are `ship_armor_reduction` / `ship_shield_reduction`, named "Armor Nullification" / "Shield
  Nullification"; the engine applies them, nothing in `common/` explains more. The user's
  construction ship came out of a toxoid system **still at 0 % armour** — it is lost, not just
  ignored in combat, and comes back only by repair (a ship without armour regeneration needs a
  starbase). Shields come back by themselves (shield regeneration, ×5 out of combat,
  `OUT_OF_COMBAT_SHIELD_REGEN_MULT`), so a pulsar costs much less than a toxoid star.
  **The slow drain exists in vanilla:** negative regeneration modifiers — the Cetana storm's
  starbase aura (`common/component_templates/00_starbase_building_auras.txt`,
  `STARBASE_AURA_CETANA_STORM`) gives hostile ships system-wide `ship_hull_regen_add_perc = -0.15`
  and `ship_armor_regen_add_perc = -0.05`; `ship_shield_regen_add_perc` is used negatively too.
  So the star class's `modifier` can swap the nullification for a negative regen of armour
  (toxoid) or shields (pulsar). **Measured (run 32)**: −0.001 takes 0.005 % of the maximum
  armour per day, linearly, whatever the maximum; lost armour stays lost outside friendly space.
  **Decided (user, 2026-11-06): −0.02 for both** (0.1 %/day if it scales). Shields did not drop
  at −0.001 (regeneration outweighs it?). **Shields need to drain more** (user, 2026-11-06):
  more than armour, since they regenerate; run 33 measures −0.02 first, then the pulsar's value
  goes up (or regeneration is cut as well) until shields actually fall. **Run 33**: armour
  −0.1 %/day as meant; shields untouched — shield components regenerate 0.5/day each (×5 out
  of combat), far above −0.02. So the pulsar also cuts regeneration (`ship_shield_regen_mult
  = -1`, run 34). **Run 34**: that stops regeneration but cancels the negative one too; the
  drain is now monthly, 10 % of the maximum shield (`ahw.50`, as vanilla's electric storm).
- **The centres carry no deposit** (user, 2026-11-06; vanilla gave all 80 one in run 32): the
  debris is the road's only resource.

  The combat terrain varies round the ring, which gives the neutral battlefield some character.
  In a portal it varies the dead end's defence per empire: a pulsar portal strips shields, a
  toxoid one armour, and a **neutron-star portal** (portals only, user 2026-11-06) halves
  sub-light speed for whoever comes and goes.
  **No neutron stars in the ring**: −50 % sub-light speed would throw off the ring's speed
  tuning. Not used either: the rift star (no effect, Astral Planes look).
- **Collected debris (decided 2026-11-05)**: the road is old and has gathered asteroids, about 3
  per system on average (0–6), in ring nodes **and** portals. About a third carry a valuable
  deposit. Only nomads profit, since they harvest without owning anything. They sit inside the
  orbits that matter: below 240 in ring nodes, where the asteroid at 270 sets the arrival radius
  and so the speed, and below 200 in portals, where the gate is at 230.
- **Cosmic storms reach both** the ring and the portals (user, 2026-11-05: yes to both). This
  needs no work: natural storms start at a random system (`choose_storm_location_weighted`), and
  ring nodes and portals are systems. On a small galaxy about one storm in eight would start on
  the ring. If the spike shows them crowding there, the ring's spawn weight gets damped by
  overriding that one vanilla effect.
- **The time per ring system is the tuning knob.** A crossing is the sub-light flight from the
  arrival to the departure point plus the jump; with many systems the crossings must be short. The
  ring's length and node count follow from the galaxy's outer edge, the per-system time from the
  yardstick above — measured in game, not guessed.
- **Superseded:** "ring systems are large, their exit points far apart" (2026-11-03, so empires
  passing through could avoid one another). With the yardstick a run-4 crossing (171 days for an
  early science ship) is far too slow. **Fights are accepted** (decided 2026-11-04): with quick
  crossings, passing empires meet; the ring is the neutral battlefield ("Consequences for play").
- **Explored, not revealed (user, 2026-11-06).** The study reveals only the empire's own exit
  node (`set_visited`; a gate needs its destination known, run 4); the rest of the ring is found
  by flying it, node by node, as in vanilla. **On the map the ring is hard to see**: its centres
  are artificial, with a far smaller centre of mass than a star, so our ring star classes get a
  faint, tiny icon (`icon_scale` 10 % of vanilla's; run 25: a node shows as its frame, the star a dot at most — kept, user 2026-11-06) — unexplored nodes read as specks, and their hyperlanes are
  not drawn until explored (vanilla, runs 2 and 12). **Hiding a system from one empire only is not
  possible** (4.5.3: no such trigger or effect; `is_hidden` is for leaders, star classes and
  `set_star_class` are global), so every empire sees the same specks.
- Visually distinct from the rest of the galaxy (own star class, possibly a nebula). The first
  idea — the ring sitting a bit above or below the galactic plane — is likely impossible: systems
  spawned during a game get no height coordinate.

### Shortcuts

**Dropped (2026-11-04)**: a pair across the ring would be exactly the shortcut the highway must not
be. The spike's gate-pair shortcut goes with the move. **Exception: the late-game express below.**

### Express wormholes (decided 2026-11-05)

The user's "fast-forward wormholes": the ring keeps up later in the game, when ships are faster.
The base ring still meets the yardstick; the express is a late-game addition.

- **Express stations** are spread round the ring, on average N nodes apart (N ≈ the nodes per
  reach, about a lap / 8: tiny 5 … huge 11, a little jitter). Lore: the Caretakers' reach hubs.
- **A station always has exactly two wormholes**: one to the next station forward, one back.
  They sit **opposite each other and at right angles to the ring's hyperlanes**, computed from the
  node's coordinates, inside the arrival radius so the crossing time doesn't change.
- **Carrier**: our own 1:1 bypass per pair, as the entry gates have. Vanilla natural wormholes
  would fire vanilla's first-wormhole story (run 5).
- **States** per pair: *dormant* → *unstable* → *stable*.
  - Dormant until the mid game (or a tech).
  - Unstable: open and closed in turn, at random. Open/closed is a global flag that the bypass
    checks, as the seal does.
  - Stabilised by events, situations or a paid project, **cheaper the later in the game**.
    Stable means open for good. Nobody owns or seals them.
- **Anyone may stabilise** (2026-11-05). Open: the exact odds and durations of the
  unstable phase; whether the AI handles a route that keeps opening and closing.

### Entry points

The connections between the ring and the regular galaxy are special, not hyperlanes.

- A ring system can connect to **several** regular systems — **each connection is 1:1**: one
  regular-side entry point, one exit point of its own in the ring system (decided 2026-11-03).
- **Access (decided 2026-11-05): three stages after owning the anchor, and the tech is the
  throttle.** It should be easy to get shortly before an empire develops wormhole travel
  (`tech_wormhole_stabilization`: tier 3, 4000, rare). A costly early rush is possible, which is
  the user's speed-up: expensive early (opportunity cost), affordable a few decades later.
  1. **Study** (science ship, ~60 days, cheap). It unlocks both techs as research options and
     **grants 15 % of each** (user: 10–20 %; `add_tech_progress`).
  2. **Two techs (user, 2026-11-05): one has to understand the gates from both sides to repair
     them.** Both are rare and have no tier prerequisites, so they can be researched as soon as the
     study is done. They are researched in parallel, in two departments.
     - **Physics: the gates' theory.** Needed to **use** a gate and to **seal** one.
       `@tier2cost2` (**2500**, user 2026-11-05).
     - **Engineering: the gates' construction.** Needed, **with the physics one**, to **repair**.
       `@tier2cost2` (**2500**).
     For comparison, vanilla's `tech_wormhole_stabilization` costs `@tier3cost1` = **4000** base
     (tier 3, rare, after `tech_hyper_drive_2`). The game then scales every tech cost by the
     galaxy's research-cost setting and by +0.2 % per point of empire size over the base
     (`EMPIRE_SIZE_TECH_COST_PENALTY`); ours scale the same way. With 2500 in each of two
     departments, run in parallel, both are done a bit before a 4000 tech in one department
     would be: shortly before wormhole travel. At year 5 they are a real rush (opportunity cost); a few
     decades in, they are routine. Possible cost modifiers: ×0.75 once known empires have them.
  3. **Repair** (construction ship, ~90 days): about 300 alloys + 50 influence. Both techs.
     **Started on the gate** (user, 2026-11-06, run 25: "the repair event should be rather on the
     gate"): an action on the broken gate megastructure, not a pop-up offer (the spike's
     `ahw.21`).
  **Head start**: an empire that owns an anchor whose gate is already repaired (by a nomad, or by
  a former owner) gets the study for free and **50 % of each tech**.
  **The grants add up: 15 % + 50 % = 65 %** (user, 2026-11-05: having studied the broken gate,
  then seeing how somebody else repaired it, is worth more than never having seen it broken).
  **More by looking around (user, 2026-11-06)**, each once per empire, and only **after its own
  study** (one has to know what one is looking at):
  **As studies (user, 2026-11-07, replacing "a fleet stays ~10 days", which neither a player nor
  the AI could know about):** when any ship of a country that has studied a gate (or got the
  head start) enters a portal or ring node where one is due, a **study pops up there** (a special
  project at that system, **15 days**), for the **class of the ship that found it** (science,
  construction or military; a study names one class) — that ship is already there and can start
  at once. Once a tech's grants reach the cap (or it is researched), its open studies are
  withdrawn and no new ones offered.
  - **Engineering: a gate somebody else repaired**, at either end (in its portal or at its exit
    in the ring). **+7 %** when the study was offered on the country's first entry into that
    system, else **+5 %**. Once per gate; never for a gate the country repaired itself.
  - **Physics: other centres.** A foreign portal (its anchor not ours): **+7 %** when its centre
    is a kind the empire has never seen before, **+5 %** when it has (user, 2026-11-06: the
    higher grant is for the first sight of a kind, not for a first entry into the system). Once
    per portal. Four kinds exist (black hole, pulsar, toxoid, and the neutron star in portals
    only); the own portal's kind counts as seen. Ring centres cannot feed physics: no ship
    reaches the ring without it.
  - **Cap: all grants together give at most 80 % of each tech** (user, 2026-11-06), so a
    study-only empire can still earn up to 65 % by exploring.
  They meet when an empire studies its own gate and a nomad then repairs it, or when it gives up
  a studied anchor and later owns it again (or another anchor) with a repaired gate. **Each grant
  at most once per empire**, so 65 % is the ceiling of these two: no farming by giving anchors up and taking
  them back, and that detour gains nothing over the honest case. A tech already researched gets
  nothing.
  The network adds a throttle of its own: one can exit only at gates others have repaired.
- **At first every entry point is broken.** **The anchor's owner** — whoever owns the system the
  portal hangs off — studies it with a science ship (a special project), which reveals its exit node (the
  rest of the ring is explored, "The ring") and makes the technologies researchable; then pays alloys and repairs it with a
  construction ship (a special project) — **once, for good** (decided 2026-11-04).
- **Using entry points needs a special technology**, unlocked by the study.
- **One can only exit at an entry point that is already repaired.** An unrepaired entry point
  leads nowhere. This keeps empires from expanding early through the ring and overrunning
  arbitrary empires, or being overrun too early.
- **A repaired entry point is never dismantled** (decided 2026-11-04). To keep others out, **its
  owner — the anchor's owner — seals it**: a switch on the gate itself, **Open / Sealed** (the
  megastructure's mode tab, vanilla's "overclocking"), with a small cost and a cooldown. **A sealed
  gate blocks both ways**: no one but the owner leaves the portal through it or comes in from the
  ring. Independent of the astral action and any DLC; the vanilla Dimensional Lock cannot be
  placed on portals at all (nobody owns them). Underneath, a global flag per pair is checked by the
  pair's bypass type (runs 20–22: a `lock_bypass` lock never expired). **Friends still pass**
  (2026-11-05): federation, overlord/subject, pacts, guarantees, open borders both ways, the same
  side of a war. **Nomads count as friends** unless the sealer has banned them: at war with it,
  or expelled (vanilla's 10-year flag `expelled_from_<owner>` after an Expel Nomads war).
- **Nomads (decided 2026-11-05)** own no systems, so they **can always study and repair** any
  broken gate, never seal one, and get no portal of their own. Like everyone else they need
  **both techs** to repair (2026-11-05). When a nomad has repaired a gate, the anchor's owner
  later gets the head start above (50 % of each tech), so they can seal sooner.
- **Repair contract (user, 2026-11-05)**: a settled empire can hire a nomad to repair its gate,
  as a contract (vanilla's contracts are `common/missions/missions/`; the model is
  `contract_clear_blockers` in `02_contracts.txt`). Proposed shape:
  - **Issuer**: may issue contracts (`can_issue_contracts_trigger`), owns the anchor
    (`contract_system_is_own`; issued in the anchor, since nobody owns the portal), its gate
    broken, **and has done the study itself** (one has to know what it is before one can commission
    it; decided 2026-11-05). The issuer pays the contract's `cost`, most likely in trade (vanilla's
    run 500–5000), **about what the repair costs** (300 alloys + 50 influence; decided 2026-11-05),
    instead of the repair's alloys and influence.
  - **Operator** (the nomad): both techs (`contract_requires_operator_technology`), not at war
    with the issuer, the portal reachable (`contract_target_system_reachable`).
  - **On accept**: our repair special project, for the nomad, at the gate. **On success**: the
    gate is repaired, with vanilla's reward for the nomad (`contract_scaling_reward_effect`) plus
    trust and opinion; the issuer gets the head start (50 % of each tech) on top of the study's
    15 %, which makes 65 %, the same as a nomad repairing the gate unasked. **Aborted** when the
    gate gets repaired some other way, or the issuer loses the anchor.
  - The AI's weight follows vanilla's (`ai_weight`).
- **For a friend's gate too (user, 2026-11-05)**: the contract may also be issued on a broken gate
  whose anchor **a friend** owns, not only one's own; a nomad still does the work. "Friend" here is
  stricter than at a seal, since a commercial pact or a research agreement alone is not enough.
  Proposed: federation, overlord/subject either way, fellow subjects, defensive pact, guarantee
  either way, the same side of a war; **not** a non-aggression pact, a migration treaty or open
  borders (decided 2026-11-05). Feasible: vanilla contracts already target systems the issuer doesn't own
  (`contract_system_is_owned_by_other_empire`, the raid contracts).
  - The issuer pays the fee and has done a study (of any gate). The **anchor's owner** gets the
    head start, as with any gate a nomad repairs; the issuer gets nothing beyond the friend's
    open gate.
  - **The anchor's owner is not asked** (decided 2026-11-05). Asking could be done with vanilla
    means (`on_issue` sends the owner an event with accept/decline, and a decline aborts the
    contract through `issued_abort_trigger`), but friends are trusted, and a gate repaired this
    way can still be sealed once the owner has the physics tech.
  No decisions or edicts (the user's preference).
- **The ring-side end can never be disabled or damaged.**

### Portals

Entry points do not open next to an empire's capital (decided 2026-11-03). Each empire gets a
**portal**: a new artificial system, unclaimable like the ring, joined by **one hyperlane** to a
system 2–3 jumps from its capital. The empire's gates to the ring are in the portal. A dead end
with a single lane is easy to defend: whoever comes out of the ring has to pass the anchor system,
which the empire can claim and fortify. Placement details (decided 2026-11-03):

- the anchor is a system 2–3 jumps out with as few lanes as possible — a dead end best — and
  preferably without a gateway or wormhole of its own;
- the portal's lane arrives in the anchor on the far side from the anchor's other lanes, so
  whoever comes out of the portal has to cross the anchor system past its starbase;
- the gate inside the portal sits opposite the portal's lane, near the system's edge.

Mid-game (decided 2026-11-06): **the mod can be added to a running game**, and **every regular
empire without a portal gets one**, including empires born later (rebels, secessions, released
subjects). In a running game the anchor may be unowned or the empire's own, never another
empire's. Each such portal costs a freeze while the game spawns its system (runs 29–30: ~10 s on a
huge galaxy, ~2.5 s on medium) — **accepted** (user, 2026-11-06). Adding the mod to a running game
costs one freeze of about the same size, for the whole highway built in one spawn batch.
**Removing the mod from a save is not supported**: the save keeps our star classes, megastructures
and bypass types, and without their definitions systems break (run 24: a missing star class gives
a black system view) or the save may not load.

### Hyper relays

Possibly everyone may build hyper relays on the ring (vanilla relays need own territory, so this is
an own megastructure type). Alternative: ruined relays come with the ring and can be restored.

## Consequences for play

- The ring becomes the galaxy's ocean: fleets of empires at war meet there, on ground nobody owns —
  a neutral battlefield.
- Entry points are chokepoints. Repairing one opens one's own space to everyone with the tech;
  owners will weigh that against the reach it gives. Locks and disabling are the counter.
- Federations and defensive pacts become worth something across the galaxy.
- Crises, marauders and nomads: open how they interact (can a crisis use the ring?).

## Open questions

1. ~~Who can repair~~ — the anchor's owner (2026-11-04); nomads too (2026-11-05). Until someone owns the anchor, the
   portal stays broken.
2. ~~Study~~ — a special project per entry point; the first one teaches the whole network.
3. How many entry points per ring system, and how are their regular-side systems chosen (nearest
   systems at game start, one per sector of the galaxy)?
4. Ring size: systems per ring by galaxy size, and the time per system, both from the yardstick
   ("The ring"). How far beyond the outer rim?
5. ~~What keeps passing empires apart~~ — nothing: fights accepted (2026-11-04).
6. Relays: built by anyone, or pre-placed ruins?
7. Galaxy shapes: round ones first; outside the galaxy a ring fits any shape, if the map allows
   systems beyond the outer rim.
8. AI: can it plan routes through custom bypasses; should it repair, lock, disable?
9. Fallen and awakened empires, crises: special rules?
10. ~~Disabling~~ — none; the gate's Seal switch (2026-11-04). ~~The repair's cost and time~~ —
    "Access" under Entry points (2026-11-05).
11. ~~Can systems be spawned beyond the galaxy's outer edge~~ — yes (run 14). A spawn seems to be
    clamped at the map's bound on huge (run 29: no ring node further left than x ≈ −538), which
    matters only where the galaxy reaches it.

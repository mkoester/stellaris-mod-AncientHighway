# Design

Status 2026-11-05: in a feasibility spike (runs 1–22). The building blocks behind each mechanic, and how
sure we are of them, are in `../AGENTS.md`, "Feasibility".

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
  star class, so we define our own. The ring mixes three, the portals stay black holes:

  | Type | Effect on ships in the system (vanilla's) |
  |---|---|
  | Black hole | disengage chance −50 %, emergency FTL takes 50 % longer |
  | Pulsar | shields −100 % |
  | Toxoid star | armour −100 % |

  The combat terrain varies round the ring, which gives the neutral battlefield some character.
  **No neutron stars**: −50 % sub-light speed would throw off the ring's speed tuning. Not used
  either: the rift star (no effect, Astral Planes look).
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
- Open: who may stabilise (anyone, or only with the tech); the exact odds and durations of the
  unstable phase; whether the AI handles a route that keeps opening and closing.

### Entry points

The connections between the ring and the regular galaxy are special, not hyperlanes.

- A ring system can connect to **several** regular systems — **each connection is 1:1**: one
  regular-side entry point, one exit point of its own in the ring system (decided 2026-11-03).
- **Access (decided 2026-11-05): three stages after owning the anchor, and the tech is the
  throttle.** It should be easy to get shortly before an empire develops wormhole travel
  (`tech_wormhole_stabilization`: tier 3, 4000, rare). A costly early rush is possible, which is
  the user's speed-up: expensive early (opportunity cost), affordable a few decades later.
  1. **Study** (science ship, ~60 days, cheap). It unlocks the tech option.
  2. **Tech** (physics, rare). **No tier prerequisites, cost ≈ 5000** (`@tier3cost2`), so
     it can be researched as soon as the study is done. At year 5 that is years of physics; by
     year 30 it is an ordinary tier-3 research. Possible cost modifiers: ×0.75 once known empires
     have it, ×0.5 late in the game.
  3. **Repair** (construction ship, ~90 days): about 300 alloys + 50 influence.
  The network adds a throttle of its own: one can exit only at gates others have repaired.
  **Sealing needs the tech too** (2026-11-05).
- **At first every entry point is broken.** **The anchor's owner** — whoever owns the system the
  portal hangs off — studies it with a science ship (a special project), which reveals the ring
  and the network and makes the technology researchable; then pays alloys and repairs it with a
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
  broken gate, never seal one, and get no portal of their own. When a nomad has repaired a gate,
  the anchor's owner later gets **a head start on the tech** (the study counts as done, plus tech
  progress), so they can seal sooner. Open: whether nomads need the tech before repairing.
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
11. Can systems be spawned beyond the galaxy's outer edge at all (map bounds, camera, the galaxy
    map's background)? Spike first.

# Design

Status 2026-11-04: in a feasibility spike (runs 1–12); the ring moves to the galaxy's outside. The building blocks behind each mechanic, and how
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

- Ring systems are joined to each other by ordinary hyperlanes, one after the other; no lanes
  into the regular galaxy (that is what entry points are for).
- They can never be claimed or settled: no outposts, no claims — always neutral ground.
- No ordinary star in the centre, but something artificial (see `lore.md`).
- **The time per ring system is the tuning knob.** A crossing is the sub-light flight from the
  arrival to the departure point plus the jump; with many systems the crossings must be short. The
  ring's length and node count follow from the galaxy's outer edge, the per-system time from the
  yardstick above — measured in game, not guessed.
- **Superseded:** "ring systems are large, their exit points far apart" (2026-11-03, so empires
  passing through could avoid one another). With the yardstick a run-4 crossing (171 days for an
  early science ship) is far too slow. Open what replaces it (see "Open questions").
- Visually distinct from the rest of the galaxy (own star class, possibly a nebula). The first
  idea — the ring sitting a bit above or below the galactic plane — is likely impossible: systems
  spawned during a game get no height coordinate.

### Shortcuts

**Dropped (2026-11-04)**: a pair across the ring would be exactly the shortcut the highway must not
be. The spike's gate-pair shortcut goes with the move.

### Entry points

The connections between the ring and the regular galaxy are special, not hyperlanes.

- A ring system can connect to **several** regular systems — **each connection is 1:1**: one
  regular-side entry point, one exit point of its own in the ring system (decided 2026-11-03).
- **At first every entry point is broken.** It must be studied (event chain, special project or
  situation — open which) before it can be repaired.
- **Using entry points needs a special technology**, unlocked by the study.
- **One can only exit at an entry point that is already repaired.** An unrepaired entry point
  leads nowhere. This keeps empires from expanding early through the ring and overrunning
  arbitrary empires, or being overrun too early.
- **The regular-side end can be disabled again** by its system's owner, at a cost, **or locked**
  with the existing mechanics (the dimensional lock of the astral actions).
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

1. Who can repair an entry point — any empire, or only the owner of the regular system? What if the
   regular system is unowned?
2. Study: special project, event chain or situation? Per entry point, or once per empire?
3. How many entry points per ring system, and how are their regular-side systems chosen (nearest
   systems at game start, one per sector of the galaxy)?
4. Ring size: systems per ring by galaxy size, and the time per system, both from the yardstick
   ("The ring"). Does it follow the galaxy's outline (elliptical galaxies are not round) or is it a
   circle?
5. With small, quick ring systems, what keeps passing empires from fighting all the time — or is
   that now accepted as the "neutral battlefield"?
6. Relays: built by anyone, or pre-placed ruins?
7. Galaxy shapes: round ones first; outside the galaxy a ring fits any shape, if the map allows
   systems beyond the outer rim.
8. AI: can it plan routes through custom bypasses; should it repair, lock, disable?
9. Fallen and awakened empires, crises: special rules?
10. Cost and timing of disabling (and re-repairing).
11. Can systems be spawned beyond the galaxy's outer edge at all (map bounds, camera, the galaxy
    map's background)? Spike first.

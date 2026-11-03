# Design

Status 2026-11-03: idea, not yet tested in game. The building blocks behind each mechanic, and how
sure we are of them, are in `../AGENTS.md`, "Feasibility".

## The problem

In other 4X games one settles on land but can still reach almost any place via the oceans (unless
landlocked, or the target is). Stellaris has no ocean: after a few decades most empires are boxed in
by their neighbours. An ally on the far side of the galaxy, or a war one wants to join, is out of
reach — and that makes distant alliances pointless in many playthroughs.

## The Ancient Highway

### The ring

- A ring of artificial systems around the galactic core, just inside the edge of the empty core.
- Ring systems are joined to each other by ordinary hyperlanes.
- They can never be claimed or settled: no outposts, no claims — always neutral ground.
- No ordinary star in the centre, but something artificial (see `lore.md`).
- **Ring systems are large, and their exit points far apart** (decided 2026-11-03). Why: little
  accidental fighting — empires passing through should mostly be able to avoid one another.
  Fleets in the same system only fight within weapon range (`COMBAT_DETECT_RANGE_MULT` = 1.05 ×
  the fleet's longest range) or a hostile's aggro range, so distance is the protection:
  - exit points (ring side of entry points, hyperlane arrivals, shortcut ends) sit on a wide outer
    orbit, spread evenly around the system;
  - the artificial centre object stays in the middle, so routes between exit points should run
    along the edge, not through a shared centre — open whether in-system movement allows that
    (ships fly straight lines);
  - nothing worth stopping for on the way (no planets to survey or mine, no shared station), so
    nobody loiters;
  - evasive/passive fleet stances remain the player's own tool to avoid combat.
- Visually distinct from the rest of the galaxy (own star class, possibly a nebula). The first
  idea — the ring sitting a bit above or below the galactic plane — is likely impossible: systems
  spawned during a game get no height coordinate.

### Shortcuts

- A few wormhole pairs across the ring, each bridging several ring systems at once.
- How many, and how long a gap they bridge, depends on the galaxy size.
- Open: are the shortcuts usable from the start (once inside), or do they need the same tech?

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
4. Ring size: systems per ring by galaxy size; spacing.
5. Shortcuts: count and span by galaxy size; usable by whom?
6. Relays: built by anyone, or pre-placed ruins?
7. Galaxy shapes beyond elliptical/ring: spirals have arms reaching close to the core — does the
   ring still fit?
8. AI: can it plan routes through custom bypasses; should it repair, lock, disable?
9. Fallen and awakened empires, crises: special rules?
10. Cost and timing of disabling (and re-repairing).
11. How large can a ring system be, and how far apart can its exit points sit? Where do hyperlane
    arrival points land in a large system? Does a straight flight between two exit points cross
    the centre (and thus everyone else's path)?

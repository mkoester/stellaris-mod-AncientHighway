# Lore (to be worked out)

Status 2026-11-08: who built and sealed the road is decided (below), and how players learn it;
the texts are open.

## Starting point

- The ring is artificial: built long ago for today's Fallen Empires, in their prime, and kept by
  the Ancient Caretakers (below).
- Its systems have no ordinary star in the centre but a Caretaker node: what it looks like and
  whether it still does something is open.
- Its connections to the regular galaxy were sealed and have decayed; studying them is how an
  empire learns the road's story and how to repair them.

## Decided (2026-11-05): built for the Fallen Empires, kept by the Caretakers

Accepted by the user on 2026-11-05 (Claude's proposal, made with the portal names). The names in
`0.0.21-SPIKE` follow it. The phase-2 reactions below are still ideas. It ties the road to the game's own Fallen Empire types (`common/personalities/
01_fallen_empire_personalities.txt`, names from `localisation/english/`). The game's only lore
for them: "ancient precursor civilizations", fallen into "a dark age long ago", some of them
"ancient foes" who may fight the War in Heaven.

- **Why it exists**: in their prime, today's Fallen Empires were rivals who still had to trade
  and talk. They agreed on one road that none of them could close: round the outside, because a
  road through the middle would cross somebody's territory.
- **Who kept it: the Ancient Caretakers** ("an ancient artificial intelligence … operating on
  some sort of caretaker protocol"). The road was what they took care of. The artificial object
  in each ring system's centre is a Caretaker node. The Caretakers count in eights, as machines
  do, so the protocol cuts the ring into **eight reaches** and gives every gate an **octal
  address**: the reach's digit, then the gate's number in it (*Caedris 23*). The reach names
  (Ashkara, Belun, Caedris, Dovhar, Eshmet, Furon, Galvaas, Hethra; initials A–H for 0–7) are
  the protocol's own names. No address has an 8 or a 9: the first clue the study events give.
- **Why it decayed: the Militant Isolationists sealed it.** When the old order broke (the first
  War in Heaven), they closed every gate from the inside. The Seal switch on our gates is theirs.
  The Caretakers, gone erratic, never reopened them. The road outlasted the reasons for it, and
  the younger empires never knew it was there.
- **Each Fallen Empire type has its own view of it**, to use in phase 2 when that type is in the
  game. Without them the lore still stands: the road needs none of them alive.
  - **Ancient Caretakers**: the road is their charge. A repaired gate pleases them: a favour or
    an opinion bonus. They might even send a task: "repair the gate at Belun 14".
  - **Keepers of Knowledge**: they hold the old records. They sell the study's findings, or
    demand them as tribute.
  - **Holy Guardians**: they see the road as a pilgrims' way. Ships passing through: tolerated.
    A *sealed* gate offends them.
  - **Militant Isolationists**: they closed it. Repairing the gate nearest their space angers them.
  - **Enigmatic Observers**: they want the younger races connected. They approve of every
    repair, and might help pay for one.
  - **Shattered Fragment** (the hive): no part in the road. It remembers it only as the thing
    the others used against it.
  - **War in Heaven / awakening**: an awakened empire may take "its" stretch of the ring back,
    sealing the gates there.
- **The story is revealed step by step** ("How players learn it", below): the octal numbering, a
  reach's name, the Caretakers' protocol, the Isolationists' seal, the compact.
- Still open: whether the Caretakers left guardians on the ring; how far the phase-2 reactions
  go (opinion modifiers only, or events and tasks).

## How players learn it (decided 2026-11-08)

The user chose all four channels (2026-11-08); none is built yet.

1. **Object texts**, always there: the gates (broken and repaired), the centre star classes, the
   ring nodes, both techs and the express carry the story passively — a description each, in the
   voice of whoever would know (our scientists for the techs, the Caretaker protocol for the
   nodes).
2. **A situation-log chain, "The Ancient Highway"** (`common/event_chains/`, as the contract's
   chain): one chapter per milestone, a short pop-up once, readable later in the log. Proposed
   chapters and what each reveals:
   - the study: the gate is artificial, older than anyone, and was sealed from the inside;
   - the first ring node entered: a road round the galaxy, kept by something still running;
   - the first repair (own, contracted or seen): the Caretakers' protocol answers the gate;
   - the first foreign portal: every empire has one — the road was meant for everyone;
   - the first express station: the reach hubs, and the road outlasting its builders.
3. **Caretaker fragments**: the first node an empire enters in each of the eight reaches plays
   that reach's piece. Eight fragments, in any order, each readable on its own: the counting in
   eights (no 8 or 9 in any address), the reach names, the caretaker protocol, the rivals' compact
   to build round the outside, the first War in Heaven, the Isolationists' seal, the Caretakers
   gone erratic, the younger races who never knew. The story itself rewards exploring the ring.
4. **Fallen Empire voices** (phase 2): the per-type reactions above, when that type is in the
   game.

## Open questions

- What does a Caretaker node look like (the black hole is the spike's stand-in), and does it
  still do something (power, a beacon, a lock)?
- Is the ring guarded (Caretaker defences, dormant or erratic), or simply abandoned?
- Which Fallen Empire reactions make it into phase 2: opinion modifiers only, or events and tasks?
- How does the lore fit the game's existing precursors and the L-Cluster's gates — related, or
  deliberately separate?
- The chapters' and fragments' actual texts (outline under "How players learn it").
- Implications for gameplay: anything the lore promises (e.g. a guardian, an awakening) must exist
  in the mod.

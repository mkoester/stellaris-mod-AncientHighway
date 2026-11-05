# The original idea, verbatim

Recorded as written on 2026-11-03; later requirements appended below, also verbatim. This branch
is never merged; the living design is on `main` (`AGENTS.md`, `docs/`).

## First message

I have another idea for a stellaris mod (inspired by the `super highway` in `X4`)

motivation:
with other 4X games, one explores the world, settles on land, but can still reach almost any other place on the world (unless one is landlocked or the target is landlocked and we don't have permission to pass) via the oceans.
in stellaris there is no concept of ocean - so a lot of empires are basically "landlocked" after a few decades.
this makes having allies somewhere else in the galaxy quite hard in some play throughs. being at war with some other empire but being unable to help sucks...

possible solution
I am thinking of having a ring of systems around the core which are connected. these systems should not be able to be settled (so always stay "neutral"). and then they would have a few connected wormholes to bridge a few of these systems at once (number of wormhole pairs and the gap they bridge should depend on the size of the galaxy; I am thinking of "round" galaxies for now, not sure about spirals or other forms yet).
maybe we can allow everyone to build `Hyper Relays` in this neutral space.
I imagine these systems would be a bit above (or below) all the other systems.
A bit of lore: these are artificial systems, built a long time ago by a long lost and forgotten space empire. there is no ordinary star in the center but <something artificial>.

the connections between those artificial systems are regular `hyperlanes`. but the connections to the rest of the galaxy are special. one needs to research a special technology to be able to use them.
at first all these "entry points" would be broken and must be studied (events? situation?). after the research is done, one would be able to use these entry points. but one would only be able to exit to systems where the entry point is also repaired already (preventing early expansion and overrunning arbitraries empires / being overrun too early). empires should be able to disable the entry points again (with costs) or lock them with the existing mechanics (e.g. via an astral action)
an artificial systems could be connected to several regular systems
the counterpart of the entry points within an artificial system should not be able to be disabled or damaged

## Second message

another requirement: the "exit points" in the artificial systems should be far apart - I would make these artificial systems rather large.
reason: I don't want to much accidental fighting in these systems - empires should be mostly able to avoid one another

## Later requirements, from the testing session (2026-11-03)

Recorded as written, in the order given.

### On the gates (after spike run 4)

our gates should be 1:1 connections (not like the L-gate)

### On portals (before spike run 8)

let's do the ring around the core

and one more thing: the gates should appear a bit appart from the capitol of any empire.
do it like this: choose a random system 2-3 jumps from the capitol. place a new artificial system (also not claimable) with only one hyperlane. in that artificial system we put the gates to the ring.
these shortcuts should be rather easy to defend by design

### On the portal's lane (after spike run 8)

for the real deal: try to place the portal systems in a way that the new hyperlane in the connected system is rather far away from other hyperlanes (in my screenshot: an attacker could bypass my station in the center and just go to Bernard's star without having to fight)

### On the gate in the portal (after spike run 9)

can we place the gates at the opposite of the hyperlane in the artificial `portal` systems?

### On the gate's distance (after spike run 10)

yes, but please place it even further away from the black whole (just a bit inside the orange dotted/lined circle)

### On the anchor system (after spike runs 10 and 11)

yes, prefer anchors with fewer lanes

should have picked another system to connect the portal system (Bapagia, Edemar, Xir (although it already has some gateway, maybe de-prioritize these))

### The ring around the galaxy (after spike run 12)

I want the ring go around the galaxy. and I want many more empty systems inbetween
reason: I don't want to create shortcuts - I want to create a second way to get everywhere which cannot be permanently blocked by closed borders
so I would say it should take roughly the same time (or a bit more) to go around the outer highway as goind around the galaxy once (in the middle between the core and outer rim)

### On fights and the ring's shape (after the redesign)

accept the fights, follow the outline

### On the ring's speed (after spike run 15)

Slower ring systems: make them bigger (that way the same highway can be crossed later in the game when ship speed increases)

### On locking and repairing (after spike run 17)

let's tackle 2 and 3

2: repair once. I don't think they should be dismantled to disable passage. I would like to re-use the portal lock astral action somehow. how could we trigger this? (other mods use decisions on their capital, but that should be our last resort)

edicts are being used by mods, too - but I am not a fan of that way

(Answers to the questions that followed: who may study, repair and lock a portal — the anchor's owner; repair — a special project; without the Astral Planes DLC — no locking.)

### On the lock's direction (spike run 18)

so the lock is only one way?

can we make it that locking locks both directions (I want them tightly coupled)

- only the owner should be able to lock
- it should not matter from which side
- can it be independent of the astral action? we define our own action on the gate and just re-use the effects of astral locks?

(Answers to the questions that followed: "it should not matter from which side" means a locked gate blocks both ways; our own action is a switch on the gate megastructure.)

### Portal names and lore (after spike run 18)

do the portal names first

let's come up with something that fits the lore

maybe we number them but with base 8 numbers? we could number them by quadrant and each quadrant gets their own "ancient" name? maybe we could tie the highway to some fallen empire?
get creative

well, I meant the existing fallen empires from the game

(Answer to the proposal that followed — built for the Fallen Empires, kept by the Ancient Caretakers, sealed by the Militant Isolationists, eight reaches with octal gate addresses: accepted.)

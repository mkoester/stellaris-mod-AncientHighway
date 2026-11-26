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

### Who may pass a sealed gate (after spike run 22)

It would be ok when numbers go higher than (decimal) 8, ...7,10,11,...

`The type then lets only the sealer through`: the whole idea is that empires can still reach their allies - every type of friend must still be allowd through (esp. empires fighting on the same side of a war)

one more definition of friends: two empires not at war with each other and having open borders for the other (both directions)

### Access, debris, centres, storms, nomads, fast-forward wormholes (after spike run 22)

- let's discuss when the access should become available
  + what should it cost?
  + how many stages?
  + this should easily be available shortly before empires develop wormhole travel
  + there should be a costly way to speed it up. my idea: high tech cost. expensive when done early (opportunity costs), rather affordable a few decades later
- the highway is old. so it makes sense that some of them "collected" asteroids etc. should we add x (x=3?; on average) items to the orbit? and then 1/3 of them would actually have valuable deposits (relevant only for nomads)
- can we draw the `artificial centers of mass` smaller? like only 20% the original size? (in both views: galaxy and system)
- let's also use some other types of `artificial centers of mass` besides `black holes` - let's look at what is available and which effect each of them has on ships in the system
- should `cosmic storms` be able to affect our artificial systems (I would say yes)?
  + should they be able to affect the ring, too?
- how would `nomadic empires` be able to repair the gate? they can't own systems
- let's discuss my idea of `fast forward wormholes` in the ring

(Answers to the questions that followed:)

Fast-forward wormholes: rather the late game express: jump (on average) N nodes (both ways). wormholes: always 2 in a system, but on opposite sides of each other and orthogonal to the axis of the hyperlanes. and maybe we can mix in your `unstable` idea. and there could be events/situations/costs to make them more stable the later you are in game

Nomads: nomads can always study and repair (no concept of ownership, thus no locking). if they do so, the "real owner" get's a boost for the tech once he owns the anchor system so he would be able to lock it a bit earlier

Centres (option chosen: black hole, pulsar and toxoid mixed round the ring, no neutron stars): Mix, no slowdown (Rec.)

Debris (option chosen: ring nodes and portals): Both

nomads should count as "friends" regarding the lock, unless an empire explicitly "banned" them from their territory (e.g. during and after a war)

### Techs and grants (after the design round)

- nomads need the tech too; anyone may stabilise

- the study should grant 10%-20% of the tech cost. the owner of an anchor system with an already repaired gate should be granted 50% of the tech cost
- how about two techs? one physics, one engineering? one needs to understand the gates from both perspectives to be able to repair it
- what is the cost of the wormhole tech?

let's change the base cost for both to 2500.

`The two add up`: not sure about that
when would it happen? when an empire does the study itself, then someone else repairs it? we must prevent that this could be abused

let's allow the 65%
doing the study, then seeing how somebody else did it should give a bonus compared to an empire that never saw the broken gate in their study

non-nomadic empires can offer contracts to nomadic empires
let's add a contract type to repair their broken gate

keep the study requirement, fee as you suggest (most likely the currency is trade)

ideally one would be able to issue a contract for most types of "friends", too (just having some commercial or tech pact would not suffice)

wait, we got a missunderstanding regarding `issue a contract for most types of "friends"`

only nomads can execute them. I meant that we could issue the contract on a broken gate which is not "ours"

- Should a non-aggression pact, a migration treaty, or open borders both ways count too? no
- Does the anchor's owner have to agree?
  + is that even possible to model with vanilla methods?
  + I lean towards `no`

## 2026-11-06

- I don't want the whole ring to be discovered at once. the user should explore it
- if possible: don't even show the ring systems on the map until you explore them. the idea: they are artificial and their center of mass way smaller than regular ones, thus way harder to detect
- let's add some more possible progress to the research. currently we can get up to 65%, right?
  + when visiting other gates which are already repaired by someone else: grant another small bonus, but only via a (relatively short) event which every type of ship should be able to complete
  + another though: only visiting repaired gates in not-seen artificial centers grants a bonus / or grants a bonus which is a little bit higher (e.g. seen: +5%, not seen: +7%
  + but one should never get more than 80%
  +since we have to techs: maybe seeing other types of artificial stars grants bonuses to the physics one while seeing repaired ones grants bonuses to the engineering one
  + let's discuss this

Answers in the discussion:
- physics bonus source: Varied portal centres
- unexplored ring nodes on the map: Faint specks
- the 80 % cap: One cap, 80 %
- own study first before inspections count: Yes

- are the ring nodes too faint? no, that's ok
- and for the system with the gates inside the galaxy: allow for that star type which slows down ships by 50%, too (and grant the higher physics reward for that, too)
  + answer in the discussion: a 4th type, same rule
- physics: +7 % if it's also your first time in that system
  not first time in the system, but first time seeing that that new type
  + new system, type seen: +5%
  + new system, new type: + 7%

- the repair event should be rather on the gate

- having the full effects of the stars might be too hard, especially tocix: 0% armor instantly and normally no repair on route might defeat the purpuse of the mod.
  maybe we keep the general effect of each star and apply it's effect slowly, like 0.1% damage per day in that system

- shield needs to drain more

### Lore and incentives (2026-11-08)

let's discuss
- how we tell the lore to players
- and how to give ai empires as well as players incentives to explore the ring

the main incentive would be for ai empires: they feel threatened by a close empire, but they have friends somewhere in the galaxy who can't reach them regularly

but for any empire to take the route through the ring, they must know it is a valid path (we disabled the all-at-once exploration of the ring)

+ answers in the discussion:
  - lore: Situation-log chain, Caretaker fragments, Lore in object texts, Fallen Empire voices
  - route known: Shared charts
  - incentives: Threat-based AI weights, Ally-under-attack nudge, AI seals when threatened

### Galactic Community (2026-11-08)

I have an idea: the GalCom

a resolution where members share their ring charts
- if accepted: all members share their explored ring nodes with each other regularly

defensive / peacefull empires would vote for it (since it means they can get help from friends far away)
aggressive empires would oppose it (since their targets could get help from their firends)
more ideas for weights?

we would still have our own category, right?
1. entry: share
2. every empire which did not yet repair their gate is in breach of galactic law (needs 1.)
3. force a specific empire to unlock (needs 1.)

+ answers in the discussion:
  - breach: repairs only
  - 10 years sounds good, or maybe as long as a truce lasts

### Story events and tech balance (2026-11-19)

let's work on it. it functions, but we don't tell a story yet. just the flavor texts on some celestial objects doesn't do it for me as a player.

let's
- check the stellaris lore, especially regarding the fallen empires - does our story fit?
- make the flavor texts into some lightweight events. no decisions, just let the player acknowledge them
  + some of them should always show up (why was it built, by whom? what can one do with it now?)
  + the rest should be random and vary. the story should not suffer if a player goes straight for the research themselves. but players who explore other portal systems should get more of our backstory - but not always in the same order. they should get bits and pieces
- discuss the tech boni again. in my current playthrough I basically do the short projects with military ships only. do both techs still get some bonus? or is it one sided?

lore questions:
- did the fallen empires exist in parallel? or at different times?
- would some have worked together to create the ring?

and check what stellaris lore exists outside the game

+ answers in the discussion:
  - tech boni: alternate, but keep the bigger boost when it is already repaired
  - fragments: foreign portals + new reaches
  - reread: pop-ups only

### Gate tech bonuses and the AI (2026-11-20)

let's discuss 1

- the player usually explores more than AI, we can expect them to do some projects to get the boost
  + let's go from +5/+7% to +7/+10% for players
- let's find another way to give some bonuses to the AI as well - expecting them to explore is not the way to go
- I don't mind that by 2226 the AI is not yet on the ring - by that time the ring offers almost no benefit to empires anyway
- can we increase the AI weight for the 2 techs proportional to the received bonus? I don't want the AI to research it early for a high tech cost when it is not even utilizing it

+ answers in the discussion:
  - yes to all, both sources, close friends get a higher bonus (but the bonus should also not be too high, otherwise it would snowball too much)

### Pop-ups and resolutions (2026-11-23)

let's work a bit more on the ancient highway

- I want the event popups to
  + have this little camera icon so one can jump right to the gate, etc
  + show where this is coming from:
    - once the purpose is clear we should name it ancient highway
    - before that I want it to be something more "mysterious", but hinting at the highway

and regarding the GalCom resolution: only an empire with a repaired gate should be able to propose it

+ answers in the discussion:
  - name ancient highway from the first ring node on, before that "The Shut Doors"
  - a situation-log entry for the chain is fine
  - repaired gate needed for all three resolutions

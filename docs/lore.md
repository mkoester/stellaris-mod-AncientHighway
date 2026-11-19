# Lore

Status 2026-11-19: who built and sealed the road is decided, checked against the game's own
texts, and told in game. The object texts carry one hint each, and the story events tell it
("How players learn it"). The texts themselves are in
`ancient_highway/localisation/english/ahw_story_l_english.yml` and `ahw_l_english.yml`
(`AHW_LORE_*`).

## Starting point

- The ring is artificial: built long ago for today's Fallen Empires, in their prime, and kept by
  the Ancient Caretakers (below).
- Its systems have no ordinary star in the centre, but a Caretaker node. What that looks like, and
  whether it still does something, is open.
- Its connections to the regular galaxy were sealed and have decayed. Studying them is how an
  empire learns the road's story and how to repair them.

## Decided (2026-11-05): built for the Fallen Empires, kept by the Caretakers

Accepted by the user on 2026-11-05 (Claude's proposal, made with the portal names). It ties the
road to the game's own Fallen Empire types (`common/personalities/
01_fallen_empire_personalities.txt`, names from `localisation/english/`).

- **Why it exists**: in their prime, today's Fallen Empires were rivals who still had to trade
  and talk. They agreed on one road that none of them could close alone, and put it round the
  outside, because a road through the middle would cross somebody's territory. This is the
  **compact**.
- **Who kept it: the Ancient Caretakers.** Vanilla calls them "an ancient artificial
  intelligence … operating on some sort of caretaker protocol". They are **one of the Fallen
  Empires** (the machine one, `fallen_empire_machine`), not an outside keeper: the compact gave
  the road to the one signatory that never sleeps (2026-11-19). The artificial object in each
  ring system's centre is a Caretaker node. The Caretakers count in eights, as machines do, so the
  protocol cuts the ring into **eight reaches** and gives every gate an **octal address**: the
  reach's digit, then the gate's number in it (*Caedris 23*). The reach names (Ashkara, Belun,
  Caedris, Dovhar, Eshmet, Furon, Galvaas, Hethra; initials A–H for 0–7) are the protocol's own
  call signs. No address has an 8 or a 9.
- **Why it decayed: the Militant Isolationists sealed it.** The compact let any signatory seal
  the road in wartime. At the first War in Heaven the Isolationists invoked that clause and closed
  every gate from the inside, by hand. They never rescinded the order, which is why every exit
  gate reads "SEALED BY ORDER OF THE COMPACT" (2026-11-19: this reconciles that text with the
  Isolationists). The Seal switch on our gates is theirs. The Caretakers, gone erratic, never
  reopened the gates. The road outlasted the reasons for it, and the younger empires never knew
  it was there.
- **Each signatory's part** (2026-11-19, proposed to answer the user's question "would some have
  worked together?"; used in the fragments):
  - **Keepers of Knowledge** drew the plans and took tolls, in knowledge, not energy.
  - **Ancient Caretakers** built and kept the road.
  - **Holy Guardians** walked it as a pilgrims' way.
  - **Enigmatic Observers** insisted on the clause for "parties not yet risen" and paid for the
    extra gates: the reason every young empire finds a portal near home.
  - **Militant Isolationists** signed unwillingly, then sealed it.
  - **The hive**, later the Shattered Fragments (vanilla: "a fragment of a once great
    civilization … before it splintered"), did not sign. The signatories moved their fleets round
    it along the road, and the road had a part in its breaking.
- **Fallen Empire reactions** (phase 2, when that type is in the game; still ideas). The lore
  stands without any of them alive.
  - **Ancient Caretakers**: a repaired gate pleases them, as a favour or an opinion bonus. They
    might send a task: "repair the gate at Belun 14".
  - **Keepers of Knowledge**: they sell the study's findings, or demand them as tribute.
  - **Holy Guardians**: ships passing through are tolerated, and a *sealed* gate offends them.
  - **Militant Isolationists**: repairing the gate nearest their space angers them.
  - **Enigmatic Observers**: they approve of every repair, and might help pay for one.
  - **Shattered Fragment**: hostile to the road.
  - **War in Heaven / awakening**: an awakened empire may take "its" stretch of the ring back and
    seal the gates there.

## Checked against the Stellaris lore (2026-11-19)

**In the game files (4.5.x)** the road fits:
- The Fallen Empires lived **at the same time**, not one after another. Vanilla gives no dates,
  but calls them "ancient rivals of a forgotten age" who "rekindled their cosmic war"
  (`TIMELINE_EVENT_WAR_IN_HEAVEN_TOOLTIP`), "though the reasons for their rivalry has long since
  faded into history" (`war_in_heaven.2.desc`). That gives rivals who had to deal with each other,
  and a first War in Heaven.
- The Caretakers "behave erratically" (`personality_fallen_empire_machine_desc`), as ours do.
- Nothing in vanilla says the Fallen Empires built anything together, and nothing rules it out.
- **Gateways and L-Gates stay deliberately separate.** Vanilla credits the Gateways to "the
  gateway's enigmatic builders" (`origin.1050.desc`), and our gates are another network.

**Outside the game** there is little canon, and it is deliberately vague:
- Dev diary #15 *Fallen Empires* (2016), as quoted in search results (the forum page would not
  load here): "once-glorious empires that for unknown reasons have stagnated and often fallen to
  infighting or crippling apathy". Infighting fits the first War in Heaven.
- Dev diary #43 *The Fallen* (1.3): designers' notes on the awakening and the War in Heaven, no
  history.
- The novel *Stellaris: Infinite Frontiers* (Steven Savile, 2016; the Commonwealth of Man's first
  contact) and the announced Dren graphic novel *Stellaris: Earthfall*: nothing found on the
  Fallen Empires.

So the road adds lore without contradicting any canon we could find.

## How players learn it (decided 2026-11-08, built 2026-11-19)

1. **Object texts**, always there: the gates (broken and repaired), the centre star classes, the
   exit gates, both techs and the express wormholes carry one hint each (`AHW_LORE_*`,
   `ahw_sc_*_desc`).
2. **Story events** (`events/ahw_story_events.txt`): short pop-ups with one button, for human
   players only. The situation-log chain proposed on 2026-11-08 is dropped (user, 2026-11-19:
   pop-ups only).
   - **Three core chapters** every player sees, also one who goes straight for the research:
     - `ahw_story.1` *A Door Shut From Inside*, on the study or the head start: what the gate
       is, and what now (both techs, the repair, other portals teach more);
     - `.2` *Written in Eights*, on the first gate tech: by whom (the protocol, the Fallen
       Empires in their prime, the Caretakers);
     - `.3` *The Road Round the Outside*, on the first ring node entered: why (the compact).
   - **Twelve fragments** (`.11`–`.22`), one at random from those not yet seen. One plays on the
     first entry into each foreign portal (star flag `ahw_toured@<country>`) and into each reach
     after the first (country flags `ahw_reach_seen_<0-7>`). Each stands on its own, so the order
     never matters: the eights, the reach names, *Keeper: None*, the compact's terms, the first
     War in Heaven, the seal clause, the Caretakers gone erratic, faint stars at the edge,
     the pilgrims' way, the toll ledger, parties not yet risen, the road against the hive mind.
     The fragments name no Fallen Empire present in the game, so they read the same in any galaxy.
3. **Fallen Empire voices** (phase 2): the reactions above, when that type is in the game.

## Open questions

- What does a Caretaker node look like (the black hole is the spike's stand-in), and does it
  still do something (power, a beacon, a lock)?
- Is the ring guarded (Caretaker defences, dormant or erratic), or simply abandoned?
- Which Fallen Empire reactions make it into phase 2: opinion modifiers only, or events and tasks?
- Implications for gameplay: anything the lore promises (for example a guardian or an
  awakening) must exist in the mod.

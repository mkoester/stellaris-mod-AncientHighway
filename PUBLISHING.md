# Publishing

Store copy and checklist for **Ancient Highway**. Both stores are uploaded through the **Paradox
Launcher** (Mod Tools → Upload Mod). Only `ancient_highway/` ships. `assets/thumbnail.svg` is the
thumbnail's source (our own art; render command in `AGENTS.md`, "Thumbnail").

The store texts are deliberately open about what is unfinished (user, 2026-11-23: "we should be
very transparent"). When a point under "Still being tuned" or "What we are watching" is settled,
update both texts and re-upload the description.

## Checklist (first release, 1.0.0)

- [x] Run 47 (2026-11-23, `docs/test-runs.md`): the story pop-ups' source line and camera, and the
      resolutions' repaired-gate requirement.
- [x] `version="1.0.0"`, `supported_version="v4.5.*"`, tags, `picture="thumbnail.png"` (512×512,
      our own art).
- [x] Discord: forum `ancient-highway` under MODS, invite `FBEW9qBwWp` (2026-11-23), in
      `../docs/discord.md`'s table, `README.md` and both store texts below.
- [ ] Store screenshots — not for 1.0.0 (user, 2026-11-23); later: the ring on the galaxy map, a
      portal with its gate, a story pop-up.
- [x] `../scripts/clean-mods.sh -n`, then without `-n`: it removes the empty `.claude/` that Claude
      Code leaves in `ancient_highway/` (the launcher would upload it).
- [x] Launcher closed → `../scripts/link-mod.sh stellaris-mod-AncientHighway/ancient_highway`
      (already linked for testing) → launcher open. If the upload dialog does not see the symlinked
      mod (Linux), copy the folder into `<user dir>/mod/` and upload the copy.
- [x] Upload to **Steam Workshop**. Description: the BBCode below, then the "More from me" block
      from `../docs/store-more-from-me.md`. A first upload
      starts **Hidden**: set it Public. The launcher writes `remote_file_id` into
      `descriptor.mod`: commit it.
- [x] Upload to **Paradox Mods** (plain text below; make headings, lists and links with the
      website editor, then check the saved page).
- [x] IDs into the table below (Paradox Mods: `remotePdxId` in the launcher's
      `<user dir>/launcher-v2.sqlite`, table `mods`), and into `../docs/store-more-from-me.md`: a line in both blocks,
      a row in "Where it goes", and remove it from "Not public yet". Then re-paste the blocks into
      every listed mod's descriptions, both stores.
- [x] GitHub repo public (2026-11-23):
      `gh repo edit mkoester/stellaris-mod-AncientHighway --visibility public --accept-visibility-change-consequences`.
      This publishes the `idea` branch too: your own notes, verbatim. The docs name the test machine
      (`mkDell`, in `AGENTS.md` and `docs/spike-runs.md`, and in the history).
- [x] Workspace `AGENTS.md`: AncientHighway moves from Private to Public under "Member repos".
- [ ] Announcement in `../docs/announcement.md`, and on our Discord's `#announcements`.

## Published IDs

| Store | Item ID | URL |
|---|---|---|
| Steam Workshop | `3844723172` | https://steamcommunity.com/sharedfiles/filedetails/?id=3844723172 |
| Paradox Mods | `168844` | https://mods.paradoxplaza.com/mods/168844/Any |

`descriptor.mod` carries only the Workshop ID (`remote_file_id`); the launcher keeps the Paradox
one in its own database.

---

## Store description — Steam Workshop (BBCode)

```bbcode
[h1]Ancient Highway[/h1]

In other 4X games you settle on land but can still sail almost anywhere across the oceans. In Stellaris there is no ocean: after a few decades most empires are boxed in by their neighbours, and an ally at war on the far side of the galaxy is beyond help.

[b]The Ancient Highway is that ocean.[/b] A ring of ancient, artificial systems runs round the outside of the galaxy, built long ago for today's Fallen Empires. Every empire has a broken gate to it near home. Study it, research how it works, repair it, and you have a second way to everywhere: one that closed borders cannot block for good.

[h2]How it works[/h2]
[list]
[*][b]The ring[/b] follows the galaxy's outline, beyond the outer rim. Its systems are joined by hyperlanes, and nobody can claim or settle them: neutral ground, and a neutral battlefield.
[*][b]A portal for every empire:[/b] a small dead-end system, one hyperlane away from a system 2–3 jumps from your capital. Its gate to the ring is broken.
[*][b]Study[/b] the gate with a science ship (30 days). It unlocks two rare techs: [b]Highway Gate Theory[/b] (use a gate, seal your own) and [b]Highway Gate Construction[/b] (with the theory, repair one).
[*][b]Repair[/b] the gate on the gate itself: 300 alloys, 50 influence, 90 days.
[*][b]Seal[/b] your gate with its Open/Sealed switch. A sealed gate blocks both ways, except for your friends.
[*][b]Not a shortcut:[/b] once round the ring is meant to take about as long as once round the galaxy by ordinary hyperlanes. A gate jump winds up for 60 days.
[*][b]Express wormholes[/b] wake up in the mid game between hubs on the ring. They flicker open and closed until somebody pays to stabilise them, for everyone.
[*][b]Learn more by looking:[/b] other empires' portals and the ring's reaches hold studies that speed up your research, and the road's story, told in short pop-ups.
[*][b]Who uses it:[/b] empires (nomadic ones too), caravaneers and enclaves; from the mid game, Fallen Empires and marauders. Never space monsters, crises or pirates.
[*][b]The AI[/b] researches, repairs and travels the ring. Its interest grows when a friend is out of reach or it feels threatened.
[*][b]Galactic Community:[/b] three resolutions in a category of their own. Share Ring Charts, Unrepaired Gates (holding back a repair puts a member in breach) and Force a Gate Open. Only an empire with a repaired gate can propose them.
[*][b]Nomads[/b] can be contracted to repair a gate for you.
[/list]

[h2]Still being tuned[/h2]
This is a first public version. It works, and I play with it, but some things will still change. Please tell me how it plays for you.
[list]
[*][b]Pacing across a whole campaign:[/b] when empires get the techs, repair their gates and stabilise the express wormholes. The numbers may change.
[*][b]Galaxy shapes:[/b] tested on elliptical (almost round) galaxies only. The ring follows the outline, so other shapes should work, but they are untested. A screenshot of an odd-looking ring helps a lot.
[*][b]Travel time through the ring:[/b] how long a lap and a gate jump take may change.
[/list]
A change to costs or weights can reach a running campaign too: the game reads them from the mod at every start.

[h2]What I am watching[/h2]
Open questions, not known bugs. If you notice one of them in your game, I'd love to hear about it.
[list]
[*][b]Influence costs that grow with distance:[/b] outposts, and branch offices (+5 influence per jump). Does the game measure that distance through the highway, so that far-off outposts or offices get cheaper once your gate is open? Not tested yet.
[*][b]Psionic auras:[/b] do they reach through the ring, and should they?
[*][b]The Willpower expansion and its update[/b] (due 23 November 2026): this version was built and tested on 4.5.x, before it came out. I'll test against the update as soon as I can.
[/list]

[h2]Compatibility[/h2]
[list]
[*]Built for Stellaris 4.5.x. No DLC required.
[*][b]Start a new game.[/b] Adding the mod to a running save is built in, but not tested yet.
[*][b]Removing it from a save is not supported:[/b] the save keeps the highway's systems, and without the mod they break.
[*]Overrides one vanilla game rule, [i]can_build_starbase_around[/i], to keep the ring unclaimable. A mod that overrides the same rule will conflict.
[*]Multiplayer: not tested.
[*]Building the highway at game start takes a few seconds (about 4 s on a medium galaxy, 11 s on huge, on an old machine). An empire born later gets its own portal, with a short freeze.
[*]Changes the checksum: no achievements or Ironman while it is active.
[/list]

[h2]Bugs & feedback[/h2]
Post them in the [url=https://discord.gg/FBEW9qBwWp]ancient-highway forum on Discord[/url]. Your game version, a screenshot and [i]logs/game.log[/i] help: the mod logs what it does there, in lines starting with "AHW".

[i]Unofficial fan project, not affiliated with Paradox Interactive.[/i]
```

---

## Store description — Paradox Mods (plain text)

```text
Ancient Highway

In other 4X games you settle on land but can still sail almost anywhere across the oceans. In Stellaris there is no ocean: after a few decades most empires are boxed in by their neighbours, and an ally at war on the far side of the galaxy is beyond help.

The Ancient Highway is that ocean. A ring of ancient, artificial systems runs round the outside of the galaxy, built long ago for today's Fallen Empires. Every empire has a broken gate to it near home. Study it, research how it works, repair it, and you have a second way to everywhere: one that closed borders cannot block for good.

How it works
• The ring follows the galaxy's outline, beyond the outer rim. Its systems are joined by hyperlanes, and nobody can claim or settle them: neutral ground, and a neutral battlefield.
• A portal for every empire: a small dead-end system, one hyperlane away from a system 2–3 jumps from your capital. Its gate to the ring is broken.
• Study the gate with a science ship (30 days). It unlocks two rare techs: Highway Gate Theory (use a gate, seal your own) and Highway Gate Construction (with the theory, repair one).
• Repair the gate on the gate itself: 300 alloys, 50 influence, 90 days.
• Seal your gate with its Open/Sealed switch. A sealed gate blocks both ways, except for your friends.
• Not a shortcut: once round the ring is meant to take about as long as once round the galaxy by ordinary hyperlanes. A gate jump winds up for 60 days.
• Express wormholes wake up in the mid game between hubs on the ring. They flicker open and closed until somebody pays to stabilise them, for everyone.
• Learn more by looking: other empires' portals and the ring's reaches hold studies that speed up your research, and the road's story, told in short pop-ups.
• Who uses it: empires (nomadic ones too), caravaneers and enclaves; from the mid game, Fallen Empires and marauders. Never space monsters, crises or pirates.
• The AI researches, repairs and travels the ring. Its interest grows when a friend is out of reach or it feels threatened.
• Galactic Community: three resolutions in a category of their own. Share Ring Charts, Unrepaired Gates (holding back a repair puts a member in breach) and Force a Gate Open. Only an empire with a repaired gate can propose them.
• Nomads can be contracted to repair a gate for you.

Still being tuned
This is a first public version. It works, and I play with it, but some things will still change. Please tell me how it plays for you.
• Pacing across a whole campaign: when empires get the techs, repair their gates and stabilise the express wormholes. The numbers may change.
• Galaxy shapes: tested on elliptical (almost round) galaxies only. The ring follows the outline, so other shapes should work, but they are untested. A screenshot of an odd-looking ring helps a lot.
• Travel time through the ring: how long a lap and a gate jump take may change.
A change to costs or weights can reach a running campaign too: the game reads them from the mod at every start.

What I am watching
Open questions, not known bugs. If you notice one of them in your game, I'd love to hear about it.
• Influence costs that grow with distance: outposts, and branch offices (+5 influence per jump). Does the game measure that distance through the highway, so that far-off outposts or offices get cheaper once your gate is open? Not tested yet.
• Psionic auras: do they reach through the ring, and should they?
• The Willpower expansion and its update (due 23 November 2026): this version was built and tested on 4.5.x, before it came out. I'll test against the update as soon as I can.

Compatibility
• Built for Stellaris 4.5.x. No DLC required.
• Start a new game. Adding the mod to a running save is built in, but not tested yet.
• Removing it from a save is not supported: the save keeps the highway's systems, and without the mod they break.
• Overrides one vanilla game rule, can_build_starbase_around, to keep the ring unclaimable. A mod that overrides the same rule will conflict.
• Multiplayer: not tested.
• Building the highway at game start takes a few seconds (about 4 s on a medium galaxy, 11 s on huge, on an old machine). An empire born later gets its own portal, with a short freeze.
• Changes the checksum: no achievements or Ironman while it is active.

Bugs & feedback
Post them in the ancient-highway forum on Discord: https://discord.gg/FBEW9qBwWp
Your game version, a screenshot and logs/game.log help: the mod logs what it does there, in lines starting with "AHW".

Unofficial fan project, not affiliated with Paradox Interactive.
```

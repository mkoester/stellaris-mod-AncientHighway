# Publishing

Store copy and checklist for **Ancient Highway**. Both stores are uploaded through the **Paradox
Launcher** (Mod Tools → Upload Mod). Only `ancient_highway/` ships. `assets/thumbnail.svg` is the
thumbnail's source (our own art; render command in `AGENTS.md`, "Thumbnail").

The store texts are deliberately open about what is unfinished (user, 2026-11-23: "we should be
very transparent"). When a point under "Still being tuned" or "What we are watching" is settled,
update both texts and re-upload the description.

## Update 1.0.1 (game 4.6.0, 2026-11-23)

- [x] `version="1.0.1"`, `supported_version="v4.6.*"`; store copy says 4.6.x, the Willpower line
      under "What I am watching" is gone.
- [x] A 4.6.0 throwaway game built the highway; `error.log` without the 120 modifier-icon lines,
      only the expected noise (`AGENTS.md`).
- [ ] Not seen in game: the resolutions refused to an empire with a repaired gate but no Gate
      Theory (the tooltip's new text).
- [ ] Upload to both stores. Change note: "Supports Stellaris 4.6 (Willpower). Galactic Community
      resolutions: proposing one now also needs Highway Gate Theory, so an empire whose gate a nomad
      repaired can no longer propose them without being able to use the gate. Own icons for the
      gates' windup modifiers (120 fewer error.log lines at every start)."

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

## Store description

`store/ancient_highway.bbcode` is the Steam Workshop text (BBCode). `scripts/store_texts.py` in the workspace (run by `slink`, or on its own with the launcher closed) writes it into the launcher's upload form, with the "More from me" block appended, and makes the Paradox Mods HTML and short description from it. Edit the file, never the form.

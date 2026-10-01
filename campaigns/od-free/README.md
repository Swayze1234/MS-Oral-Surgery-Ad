# OD Free Mississippi on MCTV — social campaign kit

MCTV Digital is running the Mississippi State Department of Health's (MSDH)
**OD Free Mississippi** campaign on its screens: six silent spots pushing free
naloxone kits, with a QR code that opens MSDH's Naloxone (Narcan) Kit Request
Form. The spots came from Creed's email to Dominic DeLeo (MSDH) on Sep 30,
subject "Re: OD Free on MCTV screens - stop by tomorrow".

This folder is everything Creed needs to promote it on the MCTV Facebook,
Instagram and LinkedIn pages. **Lead angle on every post: partnership with MSDH.**

## What's here

| File | What it is |
|------|------------|
| `social/facebook-instagram-post.md` | The page post: caption (two versions), hashtags, alt text, step-by-step posting instructions, pinned comment, DM reply, comment moderation |
| `social/reels/README.md` | Four reels: scripts, on-screen text, shot lists, captions, cover text, audio notes |
| `social/reels/build_reels.py` | One command that restacks the six screen spots into vertical (9:16) reels and stills using the spots' own panels, logos and QR |
| `social/linkedin-post.md` | Company LinkedIn post, plus a short version for Creed to post from his own profile |
| `assets/spots/` | Drop the six MP4s and the approval PDF here (see `assets/spots/README.md`) |
| `assets/approval-sheet-summary.md` | The spot copy, timings and pilot terms from Creed's approval sheet, for reference |

## The facts every post is built on

- **Partner:** Mississippi State Department of Health, OD Free Mississippi campaign.
- **What runs:** six silent spots (three :15, three :10), four plays an hour, every screen, all open hours, 30 days. No charge to MSDH, no contract.
- **Where:** the approval sheet describes an Oxford pilot (75+ screens). Swayze's brief says all MCTV screens in North Mississippi (Oxford, Tupelo, Golden Triangle). Copy is written for North Mississippi; one find-and-replace fixes it if launch is Oxford-only.
- **Why:** recent overdose deaths in the Ole Miss community. Posts reference this respectfully, with no numbers or names.
- **Call to action:** scan the QR on any MCTV screen, or go to odfree.org, to request a free naloxone kit. Available to all Mississippi residents at no cost.
- **Health wording:** every health line in the posts is MSDH's or OD Free's own approved wording from the spots. MCTV wrote only the framing around it. Keep it that way if you edit.

## Before anything goes out (checklist)

1. MSDH approves the six spots (Dominic). Spots load the next day. **Post on go-live day, not before.**
2. Get Dominic's OK on the phrase "in partnership with the Mississippi State Department of Health" and on tagging MSDH. Send him the FB/IG caption and LinkedIn post with the spots. The approval sheet already asked MSDH which pages to tag.
3. Get the direct link to the naloxone request form (same destination as the QR). Captions use `odfree.org` until then.
4. Confirm the launch footprint (Oxford only vs. all North Mississippi) and fix the copy.
5. Drop the six MP4s into `assets/spots/` and run `python3 social/reels/build_reels.py` to make the reels (needs ffmpeg and Pillow).
6. Film Reel 2 (Creed on camera) and Reel 3 (QR scan) — about an hour at one venue.

## Suggested 30-day cadence

| Day | Post |
|-----|------|
| 1 (go-live) | Facebook + Instagram page post. LinkedIn company post. Creed reposts LinkedIn from his profile. |
| 3 | Reel 1 (the spots, vertical) on Instagram + Facebook. |
| 7 | Reel 2 (Creed on camera, why we're doing this). |
| 14 | Reel 3 (scan the screen, 10 seconds). Story: screen in a venue, "Seen this yet?" |
| 21 | Reel 4 (Fentanyl can be anywhere), or reshare MSDH/OD Free's own post. |
| 30 | Wrap-up post with MSDH's count of kit requests from screens, and a thank-you to host venues. |

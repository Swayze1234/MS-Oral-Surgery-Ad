# Reels (Instagram + Facebook)

Four reels. Reels 1 and 4 are built automatically from the screen spots by
`build_reels.sh`. Reels 2 and 3 need about an hour of filming at one venue.

**Specs for all:** 1080 x 1920 (9:16), MP4, under 60 seconds, keep key text out
of the top 220 px and bottom 420 px (Instagram's UI covers those). Post each
reel to Instagram with "Also share to Facebook" turned on.

Audio: the spots are silent. Add a licensed track from Instagram's audio
library at upload (something low and steady, no lyrics). Reel 2 uses Creed's
voice, no music needed.

---

## Reel 1 — "Every screen. Starting today." (built by script, ~45 s)

**What it is:** the three :15 spots stacked back to back, vertical, with an
MSDH-partnership banner above and the call to action below.
File: `out/reel_1_all-three-15s.mp4`

**Cover text (choose cover frame in Instagram, add text):** "Partnering with MSDH"

**Caption:**
```
MCTV Digital × Mississippi State Department of Health.

Every MCTV screen in North Mississippi is now running OD Free Mississippi, four times an hour, all day, at no charge. Scan the QR on any screen for a free naloxone kit, or go to odfree.org.

Save a life. Get naloxone at no cost.

[tag MSDH page] [tag OD Free page]
#ODFreeMS #MSDH #Naloxone #NorthMississippi #OxfordMS #MCTVDigital
```

---

## Reel 2 — "Why we're doing this" (Creed on camera, 30 to 40 s)

**Setup:** phone, vertical, at a venue with an MCTV screen behind Creed playing
the spot. Natural light or the venue's lights. Hold the phone at chest height,
Creed fills the middle of the frame, the screen is visible over his shoulder.
One take is fine. Record a second take in case.

**Script (Creed, to camera):**

> Every MCTV screen in North Mississippi is running one message right now, and we're not charging anybody a dime for it.
>
> We've partnered with the Mississippi State Department of Health on their OD Free campaign. Free naloxone kits for every Mississippian. You scan the code on the screen, you fill out a short form, and the kit comes to you.
>
> Our community has lost people to accidental overdose this year. We own the screens in the places people already go. This is the least we can do with them.
>
> So next time you see our screen, scan it. Or go to odfree.org. Save a life. Get naloxone at no cost.

**On-screen text (add in Instagram's text tool, bottom third):**
- 0 to 5 s: "Every MCTV screen. No charge."
- 5 to 15 s: "Partnering with MSDH"
- 15 to 25 s: "Free naloxone. Every Mississippian."
- 25 to end: "Scan the screen · odfree.org"

**B-roll to cut in (3 to 4 s each, shot on the same visit):** the screen
playing the spot, close-up of the QR code, a hand holding a phone up to the
screen, wide shot of the venue with the screen in it.

**Cover text:** "Why we're doing this"

**Caption:**
```
Creed on why every MCTV screen in North Mississippi is running OD Free Mississippi, in partnership with the Mississippi State Department of Health, at no charge.

Scan the screen or go to odfree.org. Save a life. Get naloxone at no cost.

[tag MSDH page] [tag OD Free page]
#ODFreeMS #MSDH #Naloxone #NorthMississippi #MCTVDigital
```

---

## Reel 3 — "Scan it" (10 to 15 s, no talking)

**Setup:** three shots, phone vertical.
1. (0 to 4 s) Someone walks up to an MCTV screen playing the spot.
2. (4 to 9 s) Over the shoulder: they raise their phone, the QR scans, the form opens. Hold on the phone screen for 2 seconds.
3. (9 to 13 s) They put the phone away and walk off. Freeze on the MCTV screen.

**On-screen text:**
- Shot 1: "See this on a screen near you?"
- Shot 2: "Scan it."
- Shot 3: "Free naloxone kit. Every Mississippian. MCTV × MSDH"

**Audio:** trending sound from Instagram's library; keep it under the text.

**Cover text:** "Scan it."

**Caption:**
```
Takes about ten seconds. Scan the QR on any MCTV screen, or go to odfree.org, and the Mississippi State Department of Health sends you a free naloxone kit.

Save a life. Get naloxone at no cost. #ODFreeMS #MSDH #Naloxone #MCTVDigital
```

---

## Reel 4 — "Fentanyl can be anywhere" (built by script, 15 s)

**What it is:** the Fentanyl :15 spot, vertical, with banners.
File: `out/reel_4_fentanyl-anywhere.mp4`

**Cover text:** "Fentanyl can be anywhere"

**Caption:**
```
Fentanyl in lethal doses can be anywhere. In pills, powders, and marijuana.
Prevent overdose deaths with naloxone.

From OD Free Mississippi, now on every MCTV screen in North Mississippi in partnership with the Mississippi State Department of Health. Scan the screen or go to odfree.org.

[tag MSDH page] [tag OD Free page] #ODFreeMS #MSDH #Naloxone #MCTVDigital
```

---

## Building Reels 1 and 4

1. Put the six MP4s in `campaigns/od-free/assets/spots/` (exact names in that folder's README).
2. From this folder run:
   ```bash
   ./build_reels.sh
   ```
3. Output lands in `out/`: Reel 1, Reel 4, plus a vertical version of each individual spot (`spot_*.mp4`) for stories.

The script needs `ffmpeg`. It centers the 16:9 spot on a navy canvas with
"MCTV × MSDH / On every MCTV screen in North Mississippi" above and "Free naloxone for every Mississippian / Scan the screen · odfree.org" below. Edit the
`TOP_TEXT`, `BOTTOM_TEXT` and `BG` lines at the top of the script to change
them. The spots themselves are never altered.

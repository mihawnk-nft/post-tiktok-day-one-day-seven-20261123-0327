# Agent notes — Day one, day seven

Bounty: post-tiktok-day-one-day-seven-20261123-0327 ("Day one, day seven",
Growth, $20, deadline 24 Nov 2026 10:27 WIB). Entry: a TikTok video.

## Creative (decided in the build session)

The brief wants identical moments a week apart: same map, same start,
visibly more going on the second time, camera still. So the video is one
continuous simulated play-through of the same tiny game, Star Catch:

- Hook first (3 s, magenta): "DAY ONE vs DAY SEVEN" — the contrast is the
  whole video, so it is stated up front.
- Day 1 (8 s): bare navy screen, one yellow star, one basket, a score.
- Day 7 (8 s): the same basket and ground line, but a gradient night sky,
  twinkling stars, three falling stars, particle bursts on every catch, a
  combo counter, hearts and a golden star worth 5.
- Close (5 s): the newer build still being played, dimmed, "Now it's a
  real game. Start yours at make.fun".
- The make.fun referral end card over the last 2.5 s, referral code
  `02e4etp3` typed into its field (Inter Bold, ink #191419, per the press
  pack's guide).

Why it holds a viewer: the before/after contrast lands in the first
seconds, the gameplay is genuinely the same game continuing (the score
carries over from Day 1 into Day 7), and the whole clip is 24 s.

## How it was made (in this session)

- `star-catch.html` — the playable game, Day 1 and Day 7 modes.
- `render_video.py` — deterministic PIL simulation of the game's own
  mechanics, 1080×1920 @ 30 fps, piped to ffmpeg → `clip.mp4`.
- End card: transparent 9:16 WebM from https://make.fun/press/manifest.json
  (sha256 verified), overlaid per https://make.fun/press/llms.txt
  (blur σ28 + desaturate easing in over 0.8 s, code typed after the field
  rests at 1.433 s) → `final.mp4`.
- Frames at 1.5 s, 6 s, 14 s, 20 s, 22.2 s and the last frame were
  inspected; the code sits in the white field, left of the copy button.

## What is still missing

The video is rendered but **not posted**: posting needs the person's public
TikTok account (TikTok makes every video an unaudited API app posts
private, so the person posts it from the app). After posting, fill the
video's full address into `VIDEO.json` and submit. Nothing here is
submitted without the person's explicit go-ahead.

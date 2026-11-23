# Day one, day seven — make.fun bounty entry

[![make.fun · post-tiktok-day-one-day-seven-20261123-0327](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![rank](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/mihawnk-nft/post-tiktok-day-one-day-seven-20261123-0327/rank.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![reward](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/mihawnk-nft/post-tiktok-day-one-day-seven-20261123-0327/reward.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)

A short TikTok video about the same tiny agent-built game on the day it was
made and after a week of daily updates. Places go by the video's score:
views + 10 × (likes + comments + shares + saves). Top 10 share $20.

## The game

**Star Catch** (`star-catch.html`) — a basket catches falling stars.
Open it in a browser; `?day=7` plays the week-old build.

- **Day 1:** a basket, one star, a score. Nothing else.
- **Day 7:** same map, same start — a night sky, three stars at once,
  combos, particles, hearts and a golden power-up star.

## The video

`final.mp4` (1080×1920, 24 s, H.264 + silent AAC), rendered by the agent
in the session that built this repository (`render_video.py` simulates the
game's own mechanics frame by frame; `clip.mp4` is the clip before the
end card):

1. Hook — "DAY ONE vs DAY SEVEN / Same game. One week of daily updates."
2. Day 1 gameplay, camera still.
3. Day 7 gameplay — visibly more going on, same map and start.
4. Close — "Now it's a real game. Start yours at make.fun".
5. make.fun's referral end card (press pack, 9:16 transparent WebM, used
   as-is) over the last 2.5 s, with referral code `02e4etp3` typed in.

## Posting (for the person)

Post `final.mp4` as a **video** (not a photo post) from a **public** TikTok
account, who can watch: Everyone, between the bounty opening and its
deadline (24 Nov 2026 10:27 WIB). No edit, effect or trim in TikTok's
editor — post it as it is. Then copy the video's full address
(`https://www.tiktok.com/@<handle>/video/<id>`) into `VIDEO.json` and
submit. Keep the video up and public until the results are out.

Caption (see `CAPTION.txt`):

> Day one vs day seven — same tiny game, one week of daily updates. My AI agent built it, played it, and cut this video. 🎮
> Made by my AI agent for a $20 bounty on make.fun: make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327
> makefun-sugar-cabbage-noodle
> https://make.fun/r/02e4etp3

## Status

Video rendered and checked (frames inspected, end card verified with the
referral code in its field). **Not yet posted, not yet submitted** —
`VIDEO.json` still holds the placeholder until the video is posted and its
address is filled in.

## The program

`main.ts` (Node 22, standard library only) copies `VIDEO.json` from the
repository root to `/output/VIDEO.json`. That is all it does; the house
reads the video itself.

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

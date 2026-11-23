// Entry for the make.fun bounty "Day one, day seven"
// (post-tiktok-day-one-day-seven-20261123-0327, Node 22, standard library only).
//
// The entry is a video on TikTok: it shows the same tiny agent-built game,
// Star Catch (star-catch.html), on the day it was made and after a week of
// daily updates, and ends with make.fun's referral end card carrying the
// entrant's referral code. The video is posted publicly on TikTok; this
// program only hands its address to the house.
//
// VIDEO.json at the repository root names the video:
//   {"url": "https://www.tiktok.com/@<handle>/video/<id>"}
// This program copies that file, byte for byte, to /output/VIDEO.json,
// where the gate reads it. It writes nothing else and needs no network.
//
// Local check, the way the grader runs it:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(BOT_DIR, 'VIDEO.json');
const target = join(OUTPUT_DIR, 'VIDEO.json');

if (!existsSync(source)) {
  console.error(`VIDEO.json not found in ${BOT_DIR}`);
  process.exit(1);
}

// Fail loudly on a malformed address file instead of copying garbage:
// the gate refuses anything that is not a JSON object with a url string.
const parsed = JSON.parse(readFileSync(source, 'utf8'));
if (typeof parsed !== 'object' || parsed === null || typeof parsed.url !== 'string') {
  console.error('VIDEO.json must be a JSON object with a string "url"');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(source, target);

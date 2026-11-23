#!/usr/bin/env python3
"""Render the 'Day one, day seven' TikTok clip (1080x1920, 30fps, 24s).

The clip shows the same tiny agent-built game — Star Catch
(see star-catch.html) — on the day it was made and after a week of
daily updates. The gameplay is a deterministic simulation of that
game's own mechanics (basket, falling stars, catches, score), drawn
frame by frame with PIL and piped to ffmpeg.

Scenes:
  0.0-3.0s  hook: DAY ONE vs DAY SEVEN
  3.0-11.0s DAY 1: one star, one basket, a score. Nothing else.
 11.0-19.0s DAY 7: same map, same start — 3 stars, particles,
            combos, hearts, a golden power-up star.
 19.0-24.0s close: "Now it's a real game." / "Start yours at make.fun"
            (the make.fun referral end card is laid over the last
            2.5s in a second ffmpeg pass, per press/llms.txt)
"""
import math
import random
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 24.0
NFRAMES = int(DUR * FPS)
FONT = "/home/hatch/workspace/makefun/Inter-Bold.ttf"
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MAGENTA = (230, 0, 126)
NAVY = (11, 16, 38)
GROUND_Y = 1500
BASKET_W, BASKET_H = 260, 56

rng = random.Random(7)


def font(size, path=FONT):
    return ImageFont.truetype(path, size)


def text_center(draw, y, s, f, fill):
    w = draw.textlength(s, font=f)
    draw.text(((W - w) / 2, y), s, font=f, fill=fill)


def star_points(cx, cy, r, rot):
    pts = []
    for i in range(10):
        ang = rot + i * math.pi / 5 - math.pi / 2
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
    return pts


def draw_star(draw, cx, cy, r, color, rot):
    draw.polygon(star_points(cx, cy, r, rot), fill=color)


def draw_basket(draw, x):
    draw.rounded_rectangle(
        [x - BASKET_W / 2, GROUND_Y, x + BASKET_W / 2, GROUND_Y + BASKET_H],
        radius=18, fill=(255, 255, 255))
    draw.rectangle(
        [x - BASKET_W / 2 + 18, GROUND_Y + 14, x + BASKET_W / 2 - 18, GROUND_Y + 26],
        fill=(255, 210, 63))


def draw_hearts(draw, lives, x, y):
    f = font(64, DEJAVU)
    draw.text((x, y), "\u2665 " * lives, font=f, fill=(255, 93, 143))


def make_day7_sky():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top = (27, 16, 64)
    mid = (59, 29, 110)
    bot = (11, 16, 38)
    for y in range(H):
        if y < H * 0.6:
            t = y / (H * 0.6)
            c = tuple(int(top[i] + (mid[i] - top[i]) * t) for i in range(3))
        else:
            t = (y - H * 0.6) / (H * 0.4)
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img


DAY7_SKY = make_day7_sky()
BG_STARS = [(rng.uniform(0, W), rng.uniform(0, H * 0.7),
             rng.uniform(0, 6.28), rng.uniform(2, 4)) for _ in range(48)]


class Sim:
    """Deterministic play-through of Star Catch, day 1 and day 7."""

    def __init__(self):
        self.basket_x = W / 2
        self.score = 0
        self.combo = 0
        self.best = 0
        self.lives = 3
        self.stars = [self._spawn(0, -60)]
        self.particles = []

    def _spawn(self, i, y=None):
        return {
            "x": rng.uniform(90, W - 90),
            "y": -60 if y is None else y,
            "r": 46,
            "vy": rng.uniform(7.5, 10.5),
            "color": [(255, 210, 63), (255, 93, 143), (77, 215, 255)][i % 3],
            "golden": False,
            "rot": rng.uniform(0, 6.28),
        }

    def to_day7(self):
        self.stars = [self._spawn(0, 200), self._spawn(1, -160), self._spawn(2, -520)]
        for s in self.stars:
            s["vy"] = rng.uniform(9.0, 13.0)
        if rng.random() < 0.9:
            self.stars[1]["golden"] = True
            self.stars[1]["color"] = (255, 233, 138)

    def burst(self, x, y, color):
        for _ in range(16):
            a = rng.uniform(0, 6.28)
            sp = rng.uniform(4, 11)
            self.particles.append({
                "x": x, "y": y,
                "vx": math.cos(a) * sp, "vy": math.sin(a) * sp - 4,
                "life": 1.0, "color": color,
            })

    def step(self, day7):
        target = min(self.stars, key=lambda s: s["y"] if s["y"] > 0 else 1e9)
        dx = target["x"] - self.basket_x
        self.basket_x += max(-16, min(16, dx * 0.12))
        self.basket_x = max(BASKET_W / 2, min(W - BASKET_W / 2, self.basket_x))
        for i, s in enumerate(self.stars):
            s["y"] += s["vy"]
            s["rot"] += 0.04
            caught = (s["y"] + s["r"] >= GROUND_Y and s["y"] < GROUND_Y + BASKET_H + 24
                      and abs(s["x"] - self.basket_x) < BASKET_W / 2 + s["r"] * 0.6)
            if caught:
                self.score += 5 if s["golden"] else 1
                self.combo += 1
                self.best = max(self.best, self.combo)
                if day7:
                    self.burst(s["x"], GROUND_Y, s["color"])
                self.stars[i] = self._spawn(i)
                if day7:
                    self.stars[i]["vy"] = rng.uniform(9.0, 13.0)
                    self.stars[i]["golden"] = rng.random() < 0.12
                    if self.stars[i]["golden"]:
                        self.stars[i]["color"] = (255, 233, 138)
            elif s["y"] - s["r"] > H:
                self.combo = 0
                if day7:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.lives = 3
                self.stars[i] = self._spawn(i)
                if day7:
                    self.stars[i]["vy"] = rng.uniform(9.0, 13.0)
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.3
            p["life"] -= 0.035
        self.particles = [p for p in self.particles if p["life"] > 0]


def caption_bar(draw, s):
    draw.rectangle([0, 1720, W, 1920], fill=(0, 0, 0, 160))
    f = font(46)
    w = draw.textlength(s, font=f)
    # wrap to two lines if too wide
    if w > W - 80:
        words = s.split(" ")
        line1, line2 = "", ""
        for wd in words:
            test = (line1 + " " + wd).strip()
            if draw.textlength(test, font=f) <= W - 80:
                line1 = test
            else:
                line2 = (line2 + " " + wd).strip()
        text_center(draw, 1752, line1, f, (255, 255, 255))
        text_center(draw, 1822, line2, f, (255, 255, 255))
    else:
        text_center(draw, 1780, s, f, (255, 255, 255))


def draw_hud(img, sim, day):
    d = ImageDraw.Draw(img, "RGBA")
    d.text((48, 48), "DAY %d" % day, font=font(64), fill=(255, 255, 255))
    score = "SCORE %d" % sim.score
    w = d.textlength(score, font=font(64))
    d.text((W - 48 - w, 48), score, font=font(64), fill=(255, 255, 255))
    if day == 7:
        if sim.combo > 1:
            d.text((48, 140), "COMBO x%d" % sim.combo, font=font(56),
                   fill=(255, 210, 63))
        draw_hearts(d, sim.lives, 48, 1620)
        best = "best combo x%d" % sim.best
        d.text((48, 240), best, font=font(40), fill=(200, 200, 220))
    d.rectangle([0, GROUND_Y + BASKET_H + 26, W, GROUND_Y + BASKET_H + 32],
                fill=(255, 255, 255))


def frame_hook(t):
    img = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(img)
    text_center(d, 560, "DAY ONE", font(170), (255, 255, 255))
    text_center(d, 760, "vs", font(110), (255, 255, 255))
    text_center(d, 900, "DAY SEVEN", font(170), (255, 255, 255))
    text_center(d, 1180, "Same game. One week", font(58), (255, 255, 255))
    text_center(d, 1260, "of daily updates.", font(58), (255, 255, 255))
    text_center(d, 1420, "built by my AI agent", font(44), (255, 220, 240))
    return img


def frame_game(sim, day, t, caption):
    if day == 1:
        img = Image.new("RGB", (W, H), NAVY)
    else:
        img = DAY7_SKY.copy()
        d = ImageDraw.Draw(img, "RGBA")
        for (x, y, ph, r) in BG_STARS:
            tw = 0.35 + 0.65 * abs(math.sin(t * 2 + ph))
            d.ellipse([x - r, y - r, x + r, y + r],
                      fill=(255, 255, 255, int(200 * tw)))
    d = ImageDraw.Draw(img, "RGBA")
    for s in sim.stars:
        draw_star(d, s["x"], s["y"], s["r"], s["color"], s["rot"])
    for p in sim.particles:
        a = max(0, min(255, int(255 * p["life"])))
        d.ellipse([p["x"] - 9, p["y"] - 9, p["x"] + 9, p["y"] + 9],
                  fill=p["color"] + (a,))
    draw_basket(d, sim.basket_x)
    draw_hud(img, sim, day)
    caption_bar(ImageDraw.Draw(img, "RGBA"), caption)
    return img


def frame_close(sim, t):
    img = frame_game(sim, 7, t, "")
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, H], fill=(0, 0, 0, 150))
    text_center(d, 700, "Now it's a real game.", font(92), (255, 255, 255))
    text_center(d, 860, "Start yours at make.fun", font(72), (255, 210, 63))
    return img


def main():
    out = sys.argv[1]
    sim = Sim()
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "medium",
        "-movflags", "+faststart", out,
    ], stdin=subprocess.PIPE)
    try:
        for i in range(NFRAMES):
            t = i / FPS
            if t < 3.0:
                img = frame_hook(t)
            else:
                day7 = t >= 11.0
                if abs(t - 11.0) < 1 / FPS:
                    sim.to_day7()
                sim.step(day7)
                if t < 11.0:
                    img = frame_game(sim, 1, t,
                                     "Day 1 — a basket, one star, nothing else.")
                elif t < 19.0:
                    img = frame_game(sim, 7, t,
                                     "Day 7 — combos, particles, power-ups. Same map, same start.")
                else:
                    img = frame_close(sim, t)
            ff.stdin.write(img.tobytes())
            if i % 120 == 0:
                print(f"frame {i}/{NFRAMES} t={t:.1f}s", flush=True)
    finally:
        ff.stdin.close()
    rc = ff.wait()
    if rc != 0:
        raise SystemExit(f"ffmpeg failed with rc={rc}")
    print("wrote", out)


if __name__ == "__main__":
    main()

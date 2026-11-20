"""Animated (video) versions of selected pins: 8 s, 30 fps, 1000x1500 MP4 for Pinterest video pins.

Usage: py -3 scripts/make_video_pins.py
Needs Node (portable install) and ffmpeg (winget) on PATH; frames are captured with Playwright.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import make_pins  # noqa: E402

VIDEOS = {"rice-left-out-overnight": 1.8, "ground-beef": 2.6}  # slug -> when the stamp slams (s)
SECONDS, FPS = 8, 30


def tool(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise SystemExit(f"{name} not found on PATH")
    return found


def main() -> int:
    node, ffmpeg = tool("node"), tool("ffmpeg")
    out = make_pins.OUT
    by_slug = {p.slug: p for p in make_pins.PINS}
    for slug, slam in VIDEOS.items():
        work = Path(tempfile.mkdtemp())
        page = work / "pin.html"
        page.write_text(make_pins.html(by_slug[slug], animated=True, slam=slam), encoding="utf-8")
        frames = work / "frames"
        subprocess.run([node, str(ROOT / "scripts" / "capture_frames.mjs"), str(page), str(frames), str(SECONDS), str(FPS)],
                       check=True)
        mp4 = out / f"{slug}.mp4"
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow",
                        "-movflags", "+faststart", str(mp4)], check=True)
        shutil.rmtree(work, ignore_errors=True)
        print(f"made pins/{mp4.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

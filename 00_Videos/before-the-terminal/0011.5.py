from manim import *
from pathlib import Path

BG    = "#000000"
WHITE = "#E8F1FF"
MUTED = "#7C8DA6"
MONO  = "JetBrains Mono"

# Resolve assets relative to this file's location, not CWD.
# 0011.5.py lives at: d:\manim-projects\00_Videos\before-the-terminal\
# Assets live at:     d:\manim-projects\01_Assets\Images\
_ASSETS = Path(__file__).parent.parent.parent / "01_Assets" / "Images"

WIN_SVG   = str(_ASSETS / "windows-11.svg")
APPLE_SVG = str(_ASSETS / "apple.svg")
ARCH_SVG  = str(_ASSETS / "arch-linux.svg")

# Brand colors
WIN_COLOR   = "#0078D4"
APPLE_COLOR = "#FFFFFF"
ARCH_COLOR  = "#1793D1"

LOGO_HEIGHT = 1.6   # uniform height for all three logos
GAP         = 1.4   # horizontal gap between logo centers


class Shot0011_5(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Build logos ──────────────────────────────────────────────
        win = SVGMobject(WIN_SVG).set_color(WIN_COLOR)
        win.set_height(LOGO_HEIGHT)

        apple = SVGMobject(APPLE_SVG).set_color(APPLE_COLOR)
        apple.set_height(LOGO_HEIGHT)

        arch = SVGMobject(ARCH_SVG).set_color(ARCH_COLOR)
        arch.set_height(LOGO_HEIGHT)

        # ── Layout: win | apple | arch  centered on screen ───────────
        apple.move_to(ORIGIN)
        win.next_to(apple, LEFT, buff=GAP - apple.get_width() / 2 - win.get_width() / 2)
        arch.next_to(apple, RIGHT, buff=GAP - apple.get_width() / 2 - arch.get_width() / 2)

        # Use arrange for cleaner equal spacing
        logos = VGroup(win, apple, arch)
        logos.arrange(RIGHT, buff=1.2)
        logos.move_to(ORIGIN)

        # ── Animate: DrawBorderThenFill one by one ────────────────────
        for logo in logos:
            self.play(
                DrawBorderThenFill(logo),
                run_time=0.9,
                rate_func=smooth,
            )

        self.wait(0.5)
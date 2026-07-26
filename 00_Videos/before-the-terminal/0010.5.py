from manim import *
import random
from pathlib import Path

ASSETS = Path(__file__).parent.parent.parent / "01_Assets" / "Images"


# 480 frames @ 24 FPS = 20 seconds


class SoftwareMachine(Scene):
    def construct(self):

        BG    = "#000000"
        TEXT  = "#F0F4FF"
        MUTED = "#6B7A99"
        CYAN  = "#00E5FF"
        PINK  = "#FF2D95"
        GOLD  = "#FFB800"
        LIME  = "#39FF14"
        MONO  = "JetBrains Mono"

        self.camera.background_color = BG

        # --------------------------------------------------
        # Ambient particles
        # --------------------------------------------------

        ambient = VGroup()
        for _ in range(25):
            d = Dot(radius=random.uniform(0.003, 0.012), color=MUTED)
            d.set_opacity(random.uniform(0.06, 0.18))
            d.move_to([random.uniform(-7, 7), random.uniform(-4, 4), 0])
            ambient.add(d)
        self.add(ambient)

        # --------------------------------------------------
        # Gear core — the software machine
        # --------------------------------------------------

        gear = SVGMobject(str(ASSETS / "gear.svg"))
        gear.set_fill(opacity=0)
        gear.set_stroke(color=MUTED, width=2.5)
        gear.scale(1.8)
        gear.move_to(ORIGIN)
        gear.set_opacity(0)

        # --------------------------------------------------
        # Field rings
        # --------------------------------------------------

        rings = VGroup()
        for r, sw in [(1.4, 0.6), (2.0, 0.4), (2.8, 0.3), (3.8, 0.2)]:
            ring = Circle(radius=r, stroke_color=MUTED, stroke_width=sw)
            ring.set_opacity(0.12)
            ring.move_to(ORIGIN)
            rings.add(ring)

        # --------------------------------------------------
        # Instruction tokens
        # --------------------------------------------------

        instr_data = [
            ("LDF", CYAN),
            ("LDC", GOLD),
            ("CAL", PINK),
            ("STF", LIME),
            ("LDF", CYAN),
            ("RET", GOLD),
        ]

        tokens = VGroup()
        for label, color in instr_data:
            rect = RoundedRectangle(
                width=1.5, height=0.7, corner_radius=0.08,
                stroke_color=color, stroke_width=2.5,
                fill_opacity=0,
            )
            txt = Text(label, font=MONO, font_size=20, color=color)
            txt.move_to(rect)
            token = VGroup(rect, txt)
            token.move_to(RIGHT * 8 + UP * random.uniform(-1.5, 1.5))
            token.set_opacity(0)
            tokens.add(token)

        # ==========================================================
        # TIMELINE (20.0 seconds)
        # ==========================================================

        # --- Act 1: Core awakens (0 - 5.0s) ---

        self.play(
            LaggedStart(
                *[FadeIn(r, scale=3) for r in rings],
                lag_ratio=0.1,
            ),
            run_time=2.0,
        )

        self.play(
            gear.animate.set_opacity(1),
            run_time=1.5,
        )

        gear.add_updater(lambda g, dt: g.rotate(dt * 0.3))
        self.wait(1.5)

        # --- Act 2: Instructions enter the machine (5.0 - 17.0s) ---

        for i, token in enumerate(tokens):
            color = instr_data[i][1]
            arc = PI/4 if i % 2 == 0 else -PI/4

            # Fly in from right, settle momentarily
            self.play(
                token.animate.set_opacity(1).move_to([
                    2.2 + random.uniform(-0.2, 0.2),
                    random.uniform(-1.0, 1.0),
                    0,
                ]),
                run_time=0.5,
            )
            self.wait(0.2)

            # Arc into the gear and vanish
            self.play(
                token.animate(path_arc=arc).move_to(gear.get_center()).set_opacity(0),
                run_time=0.4,
            )

            # Gear flashes with the instruction color
            self.play(
                gear.animate.set_stroke(color=color, width=4),
                run_time=0.08,
            )
            self.play(
                gear.animate.set_stroke(color=MUTED, width=2.5),
                run_time=0.15,
            )
            self.wait(0.4)

        # --- Act 3: Afterglow (17.0 - 20.0s) ---

        gear.clear_updaters()

        self.play(
            gear.animate.set_opacity(0.6),
            *[r.animate.set_opacity(0.04) for r in rings],
            run_time=1.0,
        )

        self.wait(2.0)

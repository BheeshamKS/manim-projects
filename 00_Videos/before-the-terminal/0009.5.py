from manim import *
import random
from pathlib import Path

ASSETS = Path(__file__).parent.parent.parent / "01_Assets" / "Images"


# 528 frames @ 24 FPS = 22 seconds


class PrivateLanguage(Scene):
    def construct(self):

        # --------------------------------------------------
        # Colors
        # --------------------------------------------------

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
        for _ in range(30):
            d = Dot(
                radius=random.uniform(0.004, 0.018),
                color=MUTED,
            )
            d.set_opacity(random.uniform(0.06, 0.15))
            d.move_to([
                random.uniform(-7, 7),
                random.uniform(-4, 4),
                0,
            ])
            ambient.add(d)
        self.add(ambient)

        # --------------------------------------------------
        # Map constellation (left side)
        # --------------------------------------------------

        map_pos = [
            LEFT * 5.2 + UP * 1.6,
            LEFT * 4.0 + UP * 0.2,
            LEFT * 5.8 + DOWN * 0.2,
            LEFT * 4.4 + DOWN * 1.4,
            LEFT * 5.5 + DOWN * 2.6,
        ]

        map_colors = [CYAN, GOLD, PINK, LIME, CYAN]

        map_dots = VGroup()
        for i, pos in enumerate(map_pos):
            d = Dot(pos, radius=0.1, color=map_colors[i])
            map_dots.add(d)

        edges = [(0,1),(1,2),(0,2),(1,3),(3,4),(0,4)]
        map_lines = VGroup()
        for i, j in edges:
            l = Line(
                map_pos[i], map_pos[j],
                color=MUTED, stroke_width=1.5,
            )
            l.set_opacity(0.4)
            map_lines.add(l)

        # --------------------------------------------------
        # Gear translator (center)
        # --------------------------------------------------

        gear = SVGMobject(str(ASSETS / "gear.svg"))
        gear.set_fill(opacity=0)
        gear.set_stroke(color=MUTED, width=6)
        gear.scale(1.0)
        gear.move_to(ORIGIN)
        gear.set_opacity(0)

        # --------------------------------------------------
        # Output primitives (right, vertical stack)
        # --------------------------------------------------

        out_colors = [CYAN, GOLD, LIME, PINK, CYAN]
        output = VGroup()
        for i in range(5):
            s = Square(
                side_length=0.35,
                stroke_color=out_colors[i],
                stroke_width=5,
                fill_opacity=0,
            )
            s.move_to(RIGHT * 4.0 + UP * (1.8 - i * 0.9))
            s.set_opacity(0)
            output.add(s)

        # --------------------------------------------------
        # TIMELINE  (22.0 seconds)
        # --------------------------------------------------

        # --- Act 1: Map appears (0 - 4.0s) ---
        # "Now Python takes that map..."

        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in map_dots],
                lag_ratio=0.08,
            ),
            run_time=1.5,
        )

        self.play(
            LaggedStart(
                *[Create(l) for l in map_lines],
                lag_ratio=0.06,
            ),
            run_time=1.8,
        )
        self.wait(0.7)

        # --- Act 2: Gear appears (4.0 - 7.0s) ---
        # "...and translates it into its own private language."

        self.play(
            gear.animate.set_opacity(1),
            run_time=1.0,
        )

        # Continuous rotation
        gear.add_updater(lambda g, dt: g.rotate(dt * 0.4))
        self.wait(2.0)

        # --- Act 3: Flow (7.0 - 14.0s) ---
        # "Not the code you wrote... Something simpler."

        # Constellation lines fade
        self.play(
            *[l.animate.set_opacity(0) for l in map_lines],
            run_time=0.5,
        )

        for i in range(5):
            # Gear pulses brighter during flow
            if i == 2:
                self.play(
                    gear.animate.set_stroke(color=CYAN, width=4),
                    run_time=0.3,
                )
                self.play(
                    gear.animate.set_stroke(color=MUTED, width=3),
                    run_time=0.3,
                )

            # Dot arcs toward gear and vanishes
            self.play(
                map_dots[i].animate(path_arc=-PI/4).move_to(gear.get_center()).set_opacity(0),
                run_time=0.8,
            )

            # Output primitive lights up
            self.play(
                output[i].animate.set_opacity(1),
                run_time=0.4,
            )
            self.wait(0.3)

        # Stop gear rotation
        gear.clear_updaters()

        # --- Act 4: Output shines (14.0 - 17.0s) ---
        # "Each one so small and clear..."

        self.play(
            *[Indicate(s, scale_factor=1.2, color=out_colors[i]) for i, s in enumerate(output)],
            run_time=1.2,
        )
        self.wait(1.2)

        # Light pulse across output
        self.play(
            output.animate.shift(RIGHT * 0.1),
            run_time=0.3,
            rate_func=there_and_back,
        )
        self.wait(1.0)

        # --- Act 5: Hold (17.0 - 22.0s) ---
        self.wait(5.0)

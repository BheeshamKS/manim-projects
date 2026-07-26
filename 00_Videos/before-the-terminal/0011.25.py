from manim import *
import random


# 576 frames @ 24 FPS = 24.0 seconds


class TheBarrier(Scene):
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
        for _ in range(35):
            d = Dot(radius=random.uniform(0.002, 0.012), color=MUTED)
            d.set_opacity(random.uniform(0.04, 0.15))
            d.move_to([random.uniform(-7, 7), random.uniform(-4, 4), 0])
            ambient.add(d)
        self.add(ambient)

        # --------------------------------------------------
        # Code fragments
        # --------------------------------------------------

        frag_data = [
            ('print("Hello, World")', CYAN,   -2.5,  1.0),
            ('import sys',             GOLD,    1.2, -0.6),
            ('sys.stdout.write(buf)',  PINK,   -1.5, -1.3),
            ('os.write(1, b"...")',   LIME,    2.8,  0.3),
        ]

        fragments = VGroup()
        for text, color, x, y in frag_data:
            t = Text(text, font=MONO, font_size=22, color=color)
            t.move_to([x, y, 0])
            t.set_opacity(0)
            self.add(t)
            fragments.add(t)

        print_frag = fragments[0]
        frag_initial = [f.get_center().copy() for f in fragments]

        # --------------------------------------------------
        # Barrier line (added to scene but invisible)
        # --------------------------------------------------

        barrier = Line(
            LEFT * 7, RIGHT * 7,
            stroke_color=MUTED, stroke_width=1.2,
        )
        barrier.move_to([0, 2.0, 0])
        barrier.set_opacity(0)
        self.add(barrier)

        # Barrier halves for the opening effect
        bh_left = Line(LEFT * 7, ORIGIN, stroke_color=MUTED, stroke_width=1.2)
        bh_left.move_to(LEFT * 7, LEFT)
        bh_left.shift(UP * 2.0)
        bh_left.set_opacity(0)
        self.add(bh_left)

        bh_right = Line(ORIGIN, RIGHT * 7, stroke_color=MUTED, stroke_width=1.2)
        bh_right.move_to(ORIGIN, LEFT)
        bh_right.shift(UP * 2.0)
        bh_right.set_opacity(0)
        self.add(bh_right)

        # --------------------------------------------------
        # Request diamond + glow (added to scene but invisible)
        # --------------------------------------------------

        diamond = Square(side_length=0.35, stroke_color=CYAN, stroke_width=2.5)
        diamond.rotate(PI / 4)
        diamond.set_opacity(0)
        diamond.fill_opacity = 0
        self.add(diamond)

        diamond_glow = Square(side_length=0.55, stroke_color=CYAN, stroke_width=1.0)
        diamond_glow.rotate(PI / 4)
        diamond_glow.set_opacity(0)
        self.add(diamond_glow)

        ripple = Circle(radius=0.2, stroke_color=CYAN, stroke_width=1.5)
        ripple.move_to([0, 2.0, 0])
        ripple.set_opacity(0)
        self.add(ripple)

        # ==========================================================
        # TIMELINE (24.0 seconds)
        # ==========================================================

        # --- Act 1: Fragments emerge (0 - 4.0s) ---
        # "Here is the part most people don't expect."

        self.play(
            LaggedStart(
                *[f.animate.set_opacity(1) for f in fragments],
                lag_ratio=0.15,
            ),
            run_time=2.5,
        )
        self.wait(1.5)

        # --- Act 2: Print tries to rise (4.0 - 8.0s) ---
        # "Python cannot put text on your screen."

        self.play(
            print_frag.animate.shift(UP * 1.1),
            run_time=1.2,
            rate_func=smooth,
        )

        for _ in range(4):
            self.play(
                print_frag.animate.shift(RIGHT * 0.04),
                run_time=0.03,
            )
            self.play(
                print_frag.animate.shift(LEFT * 0.04),
                run_time=0.03,
            )

        self.play(
            barrier.animate.set_opacity(0.35),
            run_time=0.1,
        )
        self.play(
            barrier.animate.set_opacity(0),
            run_time=0.4,
        )

        self.play(
            print_frag.animate.shift(DOWN * 1.1),
            run_time=0.8,
            rate_func=rate_functions.ease_out_sine,
        )

        self.play(
            print_frag.animate.shift(LEFT * 0.1),
            run_time=0.6,
        )
        self.wait(0.4)

        # --- Act 3: Others try (8.0 - 12.0s) ---
        # "No program does — not on its own."

        second = fragments[2]
        self.play(
            second.animate.shift(UP * 1.8 + RIGHT * 0.2),
            run_time=1.2,
            rate_func=smooth,
        )
        for _ in range(3):
            self.play(
                second.animate.shift(RIGHT * 0.03),
                run_time=0.03,
            )
            self.play(
                second.animate.shift(LEFT * 0.03),
                run_time=0.03,
            )
        self.play(
            barrier.animate.set_opacity(0.3),
            run_time=0.08,
        )
        self.play(
            barrier.animate.set_opacity(0),
            run_time=0.3,
        )
        self.play(
            second.animate.shift(DOWN * 1.8 + LEFT * 0.2),
            run_time=0.7,
            rate_func=rate_functions.ease_out_sine,
        )

        third = fragments[3]
        self.play(
            third.animate.shift(UP * 1.6 + LEFT * 0.3),
            run_time=1.0,
            rate_func=smooth,
        )
        for _ in range(3):
            self.play(
                third.animate.shift(LEFT * 0.03),
                run_time=0.03,
            )
            self.play(
                third.animate.shift(RIGHT * 0.03),
                run_time=0.03,
            )
        self.play(
            barrier.animate.set_opacity(0.25),
            run_time=0.08,
        )
        self.play(
            barrier.animate.set_opacity(0),
            run_time=0.3,
        )
        self.play(
            third.animate.shift(DOWN * 1.6 + RIGHT * 0.3),
            run_time=0.6,
            rate_func=rate_functions.ease_out_sine,
        )

        self.play(
            *[f.animate.set_opacity(0.6) for f in fragments],
            run_time=0.6,
        )
        self.wait(0.8)

        # --- Act 4: The request (12.0 - 16.5s) ---
        # "Every program ... has to ask the operating system first."

        self.play(
            print_frag.animate.set_opacity(1),
            run_time=0.5,
        )

        diamond.move_to(print_frag.get_center())
        diamond_glow.move_to(print_frag.get_center())

        self.play(
            print_frag.animate.set_opacity(0),
            diamond.animate.set_opacity(1),
            diamond_glow.animate.set_opacity(0.25),
            run_time=0.8,
        )

        self.play(
            diamond.animate.scale(1.2),
            diamond_glow.animate.scale(1.2).set_opacity(0.1),
            run_time=0.4,
            rate_func=there_and_back,
        )

        diamond_target = [0, 2.0, 0]
        self.play(
            diamond.animate.move_to(diamond_target),
            diamond_glow.animate.move_to(diamond_target),
            run_time=1.5,
            rate_func=smooth,
        )

        self.play(
            bh_left.animate.set_opacity(0.4),
            bh_right.animate.set_opacity(0.4),
            run_time=0.3,
        )

        self.play(
            bh_left.animate.shift(LEFT * 0.8),
            bh_right.animate.shift(RIGHT * 0.8),
            run_time=0.4,
        )

        self.play(
            ripple.animate.set_opacity(0.5).scale(3),
            run_time=0.3,
        )

        self.play(
            diamond.animate.shift(UP * 1.5).set_opacity(0),
            diamond_glow.animate.shift(UP * 1.5).set_opacity(0),
            ripple.animate.set_opacity(0),
            run_time=0.6,
        )

        self.play(
            bh_left.animate.shift(RIGHT * 0.8),
            bh_right.animate.shift(LEFT * 0.8),
            run_time=0.3,
        )

        self.play(
            bh_left.animate.set_opacity(0),
            bh_right.animate.set_opacity(0),
            run_time=0.3,
        )

        self.wait(0.5)

        # --- Act 5: Afterglow (16.5 - 24.0s) ---
        # "The operating system is what you're using right now."

        self.play(
            *[f.animate.set_opacity(0.15) for f in fragments[1:]],
            run_time=1.0,
        )

        glow = Rectangle(
            width=14, height=1.5,
            fill_color=CYAN,
            fill_opacity=0,
            stroke_opacity=0,
        )
        glow.move_to([0, 3.0, 0])
        self.add(glow)
        self.play(
            glow.animate.set_fill(opacity=0.06),
            run_time=1.5,
        )
        self.wait(1.0)

        self.play(
            glow.animate.set_fill(opacity=0.02),
            run_time=1.0,
        )
        self.wait(3.0)

        self.play(
            *[f.animate.set_opacity(0) for f in fragments],
            glow.animate.set_fill(opacity=0),
            run_time=1.0,
        )
        self.wait(0.5)

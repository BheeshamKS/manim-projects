from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = DARK_GRAY
COLOR_ACCENT = "#00E5FF" # Tracr Cyan


class Shot017_AlreadySpent(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0017: A Receipt Already Spent (20 Seconds / 480 Frames)
        # =====================================================================

        # --- BEAT 1: Eavesdropper Setup (0s - 6s) ---
        # Voiceover: "So if someone could somehow listen in on your tap - realistically they can't get close enough to matter, but even if they did -"
        
        # 1. The Original Code (Carried over from Shot 16, centered)
        # We use a fixed random seed here so the barcode looks exactly the same every time you render
        np.random.seed(42) 
        original_code = VGroup(*[
            Line(UP, DOWN, color=COLOR_ACCENT, stroke_width=np.random.randint(3, 9))
            for _ in range(16)
        ]).arrange(RIGHT, buff=0.15).set_height(0.8)
        
        # 2. Eavesdropper Antenna Icon (Right side, neutral/abstract design)
        antenna_base = Line(DOWN*0.5, UP*0.5, color=COLOR_MAIN, stroke_width=4)
        antenna_dot = Dot(color=COLOR_MAIN).next_to(antenna_base, UP, buff=0)
        arc1 = Arc(radius=0.4, angle=PI/2, start_angle=-PI/4, color=COLOR_MAIN, stroke_width=3).next_to(antenna_dot, RIGHT, buff=0.2)
        arc2 = Arc(radius=0.7, angle=PI/2, start_angle=-PI/4, color=COLOR_MAIN, stroke_width=3).next_to(antenna_dot, RIGHT, buff=0.2)
        eavesdropper = VGroup(antenna_base, antenna_dot, arc1, arc2).shift(RIGHT * 4 + UP * 1.5)

        # Introduce the code, then the eavesdropper
        self.play(FadeIn(original_code), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(eavesdropper, shift=LEFT * 0.3), run_time=1.5)
        self.wait(2.0)
        # (Total elapsed: 6s)

        # --- BEAT 2: The Catch, Stamp & Fade (6s - 14s) ---
        # Voiceover: "...what they'd get is a code that's already spent. Not your number. Not even a reusable clue."
        
        # The Eavesdropper "catches" a duplicate of the code
        caught_code = original_code.copy()
        
        self.play(
            caught_code.animate.next_to(eavesdropper, DOWN, buff=1.0).set_color(COLOR_MAIN), # Turns white as it's copied
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.5)

        # The "USED" stamp crashes down on the stolen code
        used_stamp_text = Text("USED", font=FONT, font_size=48, color=COLOR_ACCENT, weight=BOLD)
        used_stamp_box = RoundedRectangle(width=2.2, height=1.0, corner_radius=0.1, color=COLOR_ACCENT, stroke_width=6)
        stamp_group = VGroup(used_stamp_text, used_stamp_box).move_to(caught_code.get_center()).rotate(PI/8)

        # Dramatic "thunk" animation for the stamp
        self.play(
            FadeIn(stamp_group, scale=2.5),
            run_time=0.4,
            rate_func=rate_functions.ease_in_expo
        )
        
        # The entire stolen sequence fades to an inert, MUTED state
        self.play(
            caught_code.animate.set_color(COLOR_MUTED),
            stamp_group.animate.set_color(COLOR_MUTED),
            eavesdropper.animate.set_color(COLOR_MUTED),
            run_time=1.6
        )
        
        self.wait(4.0)
        # (Total elapsed: 14s)

        # --- BEAT 3: Original Transaction Resolves (14s - 20s) ---
        # Voiceover: "Just a receipt for a transaction that already happened."
        
        # Reader icon for the legitimate transaction (Left side)
        reader_box = Rectangle(width=1.5, height=2.2, color=COLOR_MAIN, stroke_width=4)
        reader_text = Text("READER", font=FONT, font_size=18, color=COLOR_MAIN).move_to(reader_box)
        reader = VGroup(reader_box, reader_text).shift(LEFT * 4 + UP * 1.0)
        
        self.play(FadeIn(reader), run_time=1.0)
        
        # Original code travels to the legitimate reader
        self.play(
            original_code.animate.next_to(reader, DOWN, buff=0.8).scale(0.8),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Success Checkmark inside the reader (proving the *real* one worked)
        check_p1 = original_code.get_bottom() + DOWN * 0.4 + LEFT * 0.2
        check_p2 = check_p1 + RIGHT * 0.15 + DOWN * 0.15
        check_p3 = check_p2 + RIGHT * 0.3 + UP * 0.4
        checkmark = VGroup(
            Line(check_p1, check_p2, color=GREEN, stroke_width=5),
            Line(check_p2, check_p3, color=GREEN, stroke_width=5)
        )
        
        self.play(Create(checkmark), run_time=0.5)
        
        # Final hold for the remainder of the shot
        self.wait(3.0)
        # (Total elapsed: 20s / 480 frames)
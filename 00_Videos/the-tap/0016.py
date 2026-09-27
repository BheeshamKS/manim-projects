from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = DARK_GRAY
COLOR_ACCENT = "#00E5FF" # Tracr Cyan


class Shot016_SecretKey(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0016: Secret Key Plus Counter (15 Seconds / 360 Frames)
        # =====================================================================

        # --- BEAT 1: Establish Key and Counter (0s - 4s) ---
        # Voiceover: "That code comes from a secret key buried in the chip, combined with a counter..."
        
        # 1. The Secret Key (Left side)
        key_circle = Circle(radius=0.4, color=COLOR_MAIN, stroke_width=4)
        key_shaft = Line(key_circle.get_right(), key_circle.get_right() + RIGHT * 1.2, color=COLOR_MAIN, stroke_width=4)
        key_tooth1 = Line(key_shaft.get_end() + LEFT * 0.4, key_shaft.get_end() + LEFT * 0.4 + DOWN * 0.3, color=COLOR_MAIN, stroke_width=4)
        key_tooth2 = Line(key_shaft.get_end(), key_shaft.get_end() + DOWN * 0.3, color=COLOR_MAIN, stroke_width=4)
        key_icon = VGroup(key_circle, key_shaft, key_tooth1, key_tooth2)
        
        key_label = Text("secret key", font=FONT, font_size=20, color=COLOR_MUTED).next_to(key_icon, DOWN, buff=0.4)
        key_group = VGroup(key_icon, key_label).shift(LEFT * 4 + UP * 1.5)

        # 2. The Counter (Right side)
        counter_digits = Text("0041", font=FONT, font_size=60, color=COLOR_MAIN)
        counter_label = Text("counter", font=FONT, font_size=20, color=COLOR_MUTED).next_to(counter_digits, DOWN, buff=0.4)
        counter_group = VGroup(counter_digits, counter_label).shift(RIGHT * 4 + UP * 1.5)

        self.play(FadeIn(key_group), FadeIn(counter_group), run_time=1.5)
        self.wait(2.5)
        # (Total elapsed: 4s)

        # --- BEAT 2: The Counter Ticks (4s - 8s) ---
        # Voiceover: "...that ticks up with every transaction."
        
        new_counter_digits = Text("0042", font=FONT, font_size=60, color=COLOR_MAIN).move_to(counter_digits)
        
        # Visual ticking animation
        self.play(
            counter_digits.animate.shift(UP * 0.5).set_opacity(0),
            FadeIn(new_counter_digits, shift=UP * 0.5),
            run_time=0.6,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(3.4)
        # (Total elapsed: 8s)

        # --- BEAT 3: Convergence (8s - 12s) ---
        # Voiceover: "Change the tap, change the counter..."
        
        # Bring back the Stamp Glyph from Shot 15 as the target
        stamp_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.15, color=COLOR_MAIN, stroke_width=6)
        stamp_text = Text("OTC", font=FONT, font_size=36, color=COLOR_MAIN, weight=BOLD)
        stamp_glyph = VGroup(stamp_box, stamp_text.move_to(stamp_box.get_center()))
        stamp_glyph.shift(DOWN * 0.5)

        # Converging Arrows (Accent color)
        arrow_left = Line(key_group.get_bottom() + DOWN * 0.2, stamp_glyph.get_top() + LEFT * 0.5, color=COLOR_ACCENT, stroke_width=5).add_tip(tip_length=0.25)
        arrow_right = Line(counter_group.get_bottom() + DOWN * 0.2, stamp_glyph.get_top() + RIGHT * 0.5, color=COLOR_ACCENT, stroke_width=5).add_tip(tip_length=0.25)

        self.play(
            Create(arrow_left),
            Create(arrow_right),
            run_time=1.5
        )
        self.play(FadeIn(stamp_glyph, scale=0.8), run_time=0.5)
        
        self.wait(2.0)
        # (Total elapsed: 12s)

        # --- BEAT 4: New Code Output (12s - 15s) ---
        # Voiceover: "...get a completely different code. Nothing about it is copy-paste."
        
        # Create a visually distinct code output (a barcode-like structure)
        new_code = VGroup(*[
            Line(UP, DOWN, color=COLOR_ACCENT, stroke_width=np.random.randint(3, 9))
            for _ in range(16)
        ]).arrange(RIGHT, buff=0.15).set_height(0.8)
        new_code.next_to(stamp_glyph, DOWN, buff=0.8)

        # The stamp pulses cyan as it outputs the new code
        self.play(
            stamp_glyph.animate.set_color(COLOR_ACCENT),
            run_time=0.3
        )
        self.play(
            FadeIn(new_code, shift=DOWN * 0.3),
            stamp_glyph.animate.set_color(COLOR_MAIN),
            run_time=0.7
        )
        
        self.wait(2.0)
        # (Total elapsed: 15s / 360 frames)
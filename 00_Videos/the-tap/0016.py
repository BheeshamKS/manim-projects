from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = "#CBD5E1"   # High-contrast technical slate for mobile readability
COLOR_ACCENT = "#00E5FF"  # Tracr Cyan
COLOR_BG = BLACK


class Shot016_SecretKey(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0016: Secret Key Plus Counter (15 Seconds / 360 Frames @ 24fps)
        # =====================================================================

        # --- BEAT 1: Establish Key and Counter (0s - 4s) ---
        # Voiceover: "That code comes from a secret key buried in the chip, combined with a counter..."
        
        # 1. The Stamp Glyph (Continuity from Shot 0015, established in center)
        stamp_box = RoundedRectangle(
            width=2.8, height=1.1, corner_radius=0.16,
            color=COLOR_MAIN, stroke_width=4
        )
        stamp_text = Text("OTC", font=FONT, font_size=40, color=COLOR_MAIN, weight=BOLD)
        stamp_glyph = VGroup(stamp_box, stamp_text.move_to(stamp_box.get_center()))
        stamp_glyph.shift(DOWN * 0.2)

        # Initial code output from the previous transaction (Tap 0041)
        prev_code_box = RoundedRectangle(
            width=3.8, height=0.85, corner_radius=0.1,
            color="#64748B", stroke_width=2.5, fill_color=COLOR_BG, fill_opacity=0.9
        )
        prev_code_text = Text("3182  9405", font=FONT, font_size=30, color="#CBD5E1", weight=BOLD)
        prev_code_tag = Text("tap #0041", font=FONT, font_size=20, color="#94A3B8", weight=BOLD).next_to(prev_code_box, DOWN, buff=0.16)
        prev_code_group = VGroup(prev_code_box, prev_code_text.move_to(prev_code_box.get_center()), prev_code_tag)
        prev_code_group.next_to(stamp_glyph, DOWN, buff=0.7)

        # 2. The Secret Key Icon (Left side)
        key_ring_outer = Circle(radius=0.38, color=COLOR_MAIN, stroke_width=4)
        key_ring_inner = Circle(radius=0.18, color=COLOR_MAIN, stroke_width=2.5)
        key_head = VGroup(key_ring_outer, key_ring_inner)
        key_shaft = Line(key_ring_outer.get_right(), key_ring_outer.get_right() + RIGHT * 1.1, color=COLOR_MAIN, stroke_width=4)
        tooth1 = Line(key_shaft.get_end() + LEFT * 0.35, key_shaft.get_end() + LEFT * 0.35 + DOWN * 0.28, color=COLOR_MAIN, stroke_width=4)
        tooth2 = Line(key_shaft.get_end(), key_shaft.get_end() + DOWN * 0.28, color=COLOR_MAIN, stroke_width=4)
        key_icon = VGroup(key_head, key_shaft, tooth1, tooth2)
        key_label = Text("secret key", font=FONT, font_size=26, color=COLOR_MAIN, weight=BOLD).next_to(key_icon, DOWN, buff=0.35)
        key_group = VGroup(key_icon, key_label).shift(LEFT * 4.0 + UP * 2.0)

        # 3. The Counter Readout (Right side)
        counter_bezel = RoundedRectangle(
            width=2.5, height=1.15, corner_radius=0.12,
            color="#64748B", stroke_width=2.5, fill_color=COLOR_BG, fill_opacity=0.6
        )
        counter_prefix = Text("004", font=FONT, font_size=48, color=COLOR_MAIN)
        counter_digit_1 = Text("1", font=FONT, font_size=48, color=COLOR_MAIN)
        counter_digits = VGroup(counter_prefix, counter_digit_1).arrange(RIGHT, buff=0.08)
        counter_digits.move_to(counter_bezel.get_center())
        counter_label = Text("counter", font=FONT, font_size=26, color=COLOR_MAIN, weight=BOLD).next_to(counter_bezel, DOWN, buff=0.35)
        counter_group = VGroup(counter_bezel, counter_digits, counter_label).shift(RIGHT * 4.0 + UP * 2.0)

        # Establish Stamp Glyph & previous code smoothly
        self.add(stamp_glyph, prev_code_group)
        self.play(
            FadeIn(key_group, shift=RIGHT * 0.3),
            FadeIn(counter_group, shift=LEFT * 0.3),
            run_time=1.5,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(2.5)
        # (Total elapsed: 4.0s)

        # --- BEAT 2: The Counter Ticks (4s - 8s) ---
        # Voiceover: "...that ticks up with every transaction."
        
        counter_digit_2 = Text("2", font=FONT, font_size=48, color=COLOR_MAIN)
        counter_digit_2.move_to(counter_digit_1.get_center() + DOWN * 0.45)
        
        # Mechanical tick accent pulse
        tick_pulse = counter_bezel.copy().set_color(COLOR_ACCENT).set_stroke(width=3.5)
        tick_badge = Text("+1", font=FONT, font_size=24, color=COLOR_ACCENT, weight=BOLD).next_to(counter_bezel, UP, buff=0.18)

        self.play(
            counter_digit_1.animate.shift(UP * 0.45).set_opacity(0),
            counter_digit_2.animate.move_to(counter_digit_1.get_center()).set_opacity(1),
            FadeIn(tick_badge, shift=UP * 0.2),
            Create(tick_pulse),
            run_time=0.65,
            rate_func=rate_functions.ease_out_back
        )
        self.play(
            FadeOut(tick_badge, shift=UP * 0.2),
            FadeOut(tick_pulse),
            run_time=0.55
        )
        self.wait(2.8)
        # (Total elapsed: 8.0s)

        # --- BEAT 3: Convergence (8s - 12s) ---
        # Voiceover: "Change the tap, change the counter..."
        
        # Converging lines feeding directly into the stamp engine
        start_left = key_shaft.get_end() + RIGHT * 0.3 + DOWN * 0.1
        end_left = stamp_box.get_top() + LEFT * 0.7
        arrow_left = Arrow(
            start=start_left, end=end_left,
            color=COLOR_ACCENT, stroke_width=4.5, buff=0.08, max_tip_length_to_length_ratio=0.14
        )

        start_right = counter_bezel.get_left() + LEFT * 0.3 + DOWN * 0.1
        end_right = stamp_box.get_top() + RIGHT * 0.7
        arrow_right = Arrow(
            start=start_right, end=end_right,
            color=COLOR_ACCENT, stroke_width=4.5, buff=0.08, max_tip_length_to_length_ratio=0.14
        )

        # Draw converging arrows
        self.play(
            GrowArrow(arrow_left),
            GrowArrow(arrow_right),
            run_time=1.2,
            rate_func=rate_functions.ease_out_cubic
        )

        # Dynamic data pulses flowing down the arrows into the stamp
        dot_left = Dot(point=start_left, radius=0.1, color=COLOR_ACCENT)
        dot_right = Dot(point=start_right, radius=0.1, color=COLOR_ACCENT)
        
        self.play(
            MoveAlongPath(dot_left, Line(start_left, end_left)),
            MoveAlongPath(dot_right, Line(start_right, end_right)),
            stamp_box.animate.set_color(COLOR_ACCENT).set_stroke(width=6),
            stamp_text.animate.set_color(COLOR_ACCENT),
            run_time=1.3,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.remove(dot_left, dot_right)

        # Stamp engine charging
        self.play(
            stamp_glyph.animate.scale(1.08),
            run_time=0.6,
            rate_func=rate_functions.ease_out_sine
        )
        self.wait(0.9)
        # (Total elapsed: 12.0s)

        # --- BEAT 4: New Code Output (12s - 15s) ---
        # Voiceover: "...get a completely different code. Nothing about it is copy-paste."
        
        # New, visually distinct one-time code output (Tap 0042)
        new_code_box = RoundedRectangle(
            width=3.8, height=0.85, corner_radius=0.1,
            color=COLOR_ACCENT, stroke_width=3.5, fill_color=COLOR_BG, fill_opacity=0.9
        )
        new_code_text = Text("8492  0317", font=FONT, font_size=30, color=COLOR_ACCENT, weight=BOLD)
        new_code_tag = Text("tap #0042", font=FONT, font_size=20, color=COLOR_ACCENT, weight=BOLD).next_to(new_code_box, DOWN, buff=0.16)
        new_code_group = VGroup(new_code_box, new_code_text.move_to(new_code_box.get_center()), new_code_tag)
        new_code_group.move_to(prev_code_group.get_center())

        # Impact shockwave ring
        impact_ring = stamp_box.copy().set_color(COLOR_ACCENT).set_stroke(width=3)

        # Stamp slam punch down
        self.play(
            stamp_glyph.animate.scale(1 / 1.08).shift(DOWN * 0.15),
            FadeOut(prev_code_group, shift=DOWN * 0.2),
            FadeIn(new_code_group, scale=1.3),
            run_time=0.35,
            rate_func=rate_functions.ease_in_expo
        )
        self.play(
            stamp_glyph.animate.shift(UP * 0.15).set_color(COLOR_MAIN),
            stamp_box.animate.set_stroke(width=4),
            stamp_text.animate.set_color(COLOR_MAIN),
            impact_ring.animate.scale(1.6).set_opacity(0),
            run_time=0.65,
            rate_func=rate_functions.ease_out_cubic
        )

        # Final hold to reach exactly 15.0 seconds (360 frames)
        self.wait(2.0)
        # (Total elapsed: 15.0s / 360 frames)


SecretKey = Shot016_SecretKey
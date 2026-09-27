from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = "#CBD5E1"     # High-contrast technical slate for mobile readability
COLOR_ACCENT = "#00E5FF"    # Tracr Cyan
COLOR_BG = BLACK


class Shot021_ArchitectureSplit(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0021: Secure Element vs HCE Split
        # (13 Seconds / 312 Frames @ 24fps)
        # =====================================================================

        # --- BEAT 1: Gate Splits Into Two Paths (0s - 4s) ---
        # Voiceover: "Your phone keeps its version of the secret either in a separate, isolated chip..."
        
        # Security Gate Icon (from Shot 0020, centered at the top)
        gate_box = RoundedRectangle(
            width=2.5, height=0.95, corner_radius=0.12,
            color=COLOR_ACCENT, stroke_width=3.5, fill_color=COLOR_BG, fill_opacity=0.9
        )
        gate_lock_body = RoundedRectangle(width=0.45, height=0.38, corner_radius=0.06, color=COLOR_ACCENT, stroke_width=2.5)
        gate_shackle = Arc(radius=0.14, angle=PI, color=COLOR_ACCENT, stroke_width=3.5).next_to(gate_lock_body, UP, buff=0)
        gate_lock = VGroup(gate_lock_body, gate_shackle).move_to(gate_box.get_center())
        gate_label = Text("SECURITY GATE", font=FONT, font_size=18, color=COLOR_ACCENT, weight=BOLD).next_to(gate_box, UP, buff=0.14)
        top_gate = VGroup(gate_box, gate_lock, gate_label).shift(UP * 2.8)

        # Subtle vertical dividing line for split screen
        center_divider = DashedLine(
            UP * 1.8, DOWN * 3.4, color="#64748B", stroke_width=2, stroke_opacity=0.5
        )

        # Branching paths left and right
        branch_left = Arrow(
            start=top_gate.get_bottom() + LEFT * 0.4,
            end=LEFT * 3.8 + UP * 1.55,
            color=COLOR_ACCENT, stroke_width=3.5, buff=0.1, max_tip_length_to_length_ratio=0.16
        )
        branch_right = Arrow(
            start=top_gate.get_bottom() + RIGHT * 0.4,
            end=RIGHT * 3.8 + UP * 1.55,
            color=COLOR_ACCENT, stroke_width=3.5, buff=0.1, max_tip_length_to_length_ratio=0.16
        )

        self.play(FadeIn(top_gate, shift=DOWN * 0.2), run_time=1.0)
        self.play(
            Create(center_divider),
            GrowArrow(branch_left),
            GrowArrow(branch_right),
            run_time=1.5,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(1.5)
        # (Total elapsed: 4.0s)

        # --- BEAT 2: Left Side - Isolated Separate Chip (4s - 8s) ---
        # Voiceover: "...in a separate, isolated chip..."

        # Left header - boosted for phone visibility
        left_header = Text("SEPARATE CHIP", font=FONT, font_size=22, color=COLOR_MAIN, weight=BOLD).move_to(LEFT * 3.8 + UP * 1.25)

        # Left phone outline ("rest of phone")
        phone_left = RoundedRectangle(
            width=4.6, height=3.8, corner_radius=0.3,
            color="#64748B", stroke_width=2, stroke_opacity=0.55
        ).move_to(LEFT * 3.8 + DOWN * 1.15)
        phone_left_label = Text("phone system", font=FONT, font_size=17, color=COLOR_MUTED, weight=BOLD).move_to(phone_left.get_corner(UL) + RIGHT * 1.2 + DOWN * 0.28)

        # Main processor inside left phone
        main_proc_l = RoundedRectangle(
            width=1.5, height=1.3, corner_radius=0.1,
            color="#64748B", stroke_width=2, fill_color=COLOR_BG, fill_opacity=0.5
        ).move_to(phone_left.get_center() + LEFT * 1.0)
        main_proc_l_text = Text("MAIN\nCPU", font=FONT, font_size=16, color=COLOR_MAIN, line_spacing=0.8, weight=BOLD).move_to(main_proc_l)

        # The Isolated Chip (Secure Element)
        isolated_chip = RoundedRectangle(
            width=1.2, height=1.2, corner_radius=0.1,
            color=COLOR_MAIN, stroke_width=3, fill_color=COLOR_BG, fill_opacity=0.9
        ).move_to(phone_left.get_center() + RIGHT * 1.1)
        
        # Pin traces on isolated chip
        pins_top = VGroup(*[Line(UP*0.08, DOWN*0.08, color=COLOR_MAIN, stroke_width=2).shift(isolated_chip.get_top() + RIGHT * (x*0.25)) for x in [-1, 0, 1]])
        pins_bot = VGroup(*[Line(UP*0.08, DOWN*0.08, color=COLOR_MAIN, stroke_width=2).shift(isolated_chip.get_bottom() + RIGHT * (x*0.25)) for x in [-1, 0, 1]])
        isolated_chip_pins = VGroup(pins_top, pins_bot)
        
        chip_inner_key = Circle(radius=0.15, color=COLOR_MAIN, stroke_width=2).move_to(isolated_chip.get_center() + UP * 0.08)
        chip_inner_shaft = Line(chip_inner_key.get_right(), chip_inner_key.get_right() + RIGHT * 0.25, color=COLOR_MAIN, stroke_width=2)
        chip_glyph = VGroup(chip_inner_key, chip_inner_shaft)
        
        chip_label = Text("separate chip", font=FONT, font_size=17, color=COLOR_MAIN, weight=BOLD).next_to(isolated_chip, DOWN, buff=0.35)
        isolated_chip_group = VGroup(isolated_chip, isolated_chip_pins, chip_glyph, chip_label)

        # Draw left phone and components
        self.play(
            FadeIn(left_header),
            Create(phone_left),
            FadeIn(phone_left_label),
            FadeIn(main_proc_l),
            FadeIn(main_proc_l_text),
            FadeIn(isolated_chip_group),
            run_time=1.5,
            rate_func=rate_functions.ease_out_cubic
        )

        # The Fortified Isolation Wall draws in around the separate chip
        isolation_wall = RoundedRectangle(
            width=1.8, height=1.8, corner_radius=0.15,
            color=COLOR_ACCENT, stroke_width=4
        ).move_to(isolated_chip.get_center())
        wall_badge = Text("HARDWARE ISOLATED", font=FONT, font_size=15, color=COLOR_ACCENT, weight=BOLD).next_to(isolation_wall, UP, buff=0.12)

        self.play(
            Create(isolation_wall),
            FadeIn(wall_badge),
            isolation_wall.animate.set_stroke(width=6),
            run_time=1.2,
            rate_func=rate_functions.ease_out_sine
        )
        self.play(isolation_wall.animate.set_stroke(width=4), run_time=0.4)
        self.wait(0.9)
        # (Total elapsed: 8.0s)

        # --- BEAT 3: Right Side - Software in Main Processor (8s - 11s) ---
        # Voiceover: "...or in software running through the main processor — protected by keeping the real number off the device entirely."

        # Right header - boosted for phone visibility
        right_header = Text("MAIN PROCESSOR", font=FONT, font_size=22, color=COLOR_MAIN, weight=BOLD).move_to(RIGHT * 3.8 + UP * 1.25)

        # Right phone outline ("rest of phone")
        phone_right = RoundedRectangle(
            width=4.6, height=3.8, corner_radius=0.3,
            color="#64748B", stroke_width=2, stroke_opacity=0.55
        ).move_to(RIGHT * 3.8 + DOWN * 1.15)
        phone_right_label = Text("phone system", font=FONT, font_size=17, color=COLOR_MUTED, weight=BOLD).move_to(phone_right.get_corner(UL) + RIGHT * 1.2 + DOWN * 0.28)

        # Large Main Processor Chip integrated in center
        main_proc_r = RoundedRectangle(
            width=2.6, height=2.05, corner_radius=0.15,
            color=COLOR_MAIN, stroke_width=3, fill_color=COLOR_BG, fill_opacity=0.9
        ).move_to(phone_right.get_center())
        
        proc_title = Text("MAIN PROCESSOR", font=FONT, font_size=18, color=COLOR_MAIN, weight=BOLD).next_to(main_proc_r.get_top(), DOWN, buff=0.22)
        proc_caption = Text("software, encrypted", font=FONT, font_size=17, color=COLOR_MUTED, weight=BOLD).next_to(main_proc_r, DOWN, buff=0.35)
        
        # Integrated Encryption Glyph inside the Main Processor
        enc_box = RoundedRectangle(width=0.75, height=0.58, corner_radius=0.08, color=COLOR_ACCENT, fill_color=COLOR_BG, fill_opacity=1, stroke_width=3)
        enc_shackle = Arc(radius=0.18, angle=PI, color=COLOR_ACCENT, stroke_width=4).next_to(enc_box, UP, buff=0)
        enc_glyph = VGroup(enc_box, enc_shackle).move_to(main_proc_r.get_center() + DOWN * 0.2)
        enc_badge = Text("ENCRYPTED SOFTWARE", font=FONT, font_size=15, color=COLOR_ACCENT, weight=BOLD).next_to(enc_box, DOWN, buff=0.14)
        encryption_layer = VGroup(enc_glyph, enc_badge)

        # Fade in right side architecture
        self.play(
            FadeIn(right_header),
            Create(phone_right),
            FadeIn(phone_right_label),
            FadeIn(main_proc_r),
            FadeIn(proc_title),
            FadeIn(proc_caption),
            run_time=1.3,
            rate_func=rate_functions.ease_out_cubic
        )

        # Encryption layer activates on top with cyan pulse
        self.play(
            FadeIn(encryption_layer, scale=1.3),
            main_proc_r.animate.set_stroke(color=COLOR_ACCENT, width=4),
            run_time=1.0,
            rate_func=rate_functions.ease_out_back
        )
        self.play(
            main_proc_r.animate.set_stroke(color=COLOR_MAIN, width=3),
            run_time=0.4
        )
        self.wait(0.3)
        # (Total elapsed: 11.0s)

        # --- BEAT 4: Simultaneous Hold (11s - 13s) ---
        self.wait(2.0)
        # (Total elapsed: 13.0s / 312 frames @ 24fps)


ArchitectureSplit = Shot021_ArchitectureSplit


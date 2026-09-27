from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = "#CBD5E1"     # High-contrast technical slate for mobile readability
COLOR_INERT = "#64748B"     # Spent state slate (clearly legible on black OLED)
COLOR_ACCENT = "#00E5FF"    # Tracr Cyan
COLOR_SUCCESS = "#2EA043"   # Clean approved green
COLOR_BG = BLACK


class Shot017_AlreadySpent(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0017: A Receipt Already Spent (20 Seconds / 480 Frames @ 24fps)
        # =====================================================================

        # --- BEAT 1: Eavesdropper Setup (0s - 6s) ---
        # Voiceover: "So if someone could somehow listen in on your tap - realistically, they can't get close enough to matter, but even if they did -"
        
        # 1. The Original One-Time Code (Carried over directly from Shot 16)
        code_box = RoundedRectangle(
            width=3.8, height=0.85, corner_radius=0.1,
            color=COLOR_ACCENT, stroke_width=3.5, fill_color=COLOR_BG, fill_opacity=0.9
        )
        code_text = Text("8492  0317", font=FONT, font_size=30, color=COLOR_ACCENT, weight=BOLD)
        code_tag = Text("ONE-TIME CODE", font=FONT, font_size=20, color=COLOR_ACCENT, weight=BOLD).next_to(code_box, DOWN, buff=0.15)
        original_code = VGroup(code_box, code_text.move_to(code_box.get_center()), code_tag)
        original_code.shift(DOWN * 0.2)

        # 2. Eavesdropper Glyph (Right side)
        antenna_stem = Line(DOWN * 0.5, UP * 0.5, color=COLOR_MAIN, stroke_width=4)
        antenna_tip = Dot(antenna_stem.get_top(), radius=0.09, color=COLOR_MAIN)
        arc1 = Arc(radius=0.35, angle=PI/2, start_angle=3*PI/4, color=COLOR_MAIN, stroke_width=3.5).next_to(antenna_tip, LEFT, buff=0.15)
        arc2 = Arc(radius=0.6, angle=PI/2, start_angle=3*PI/4, color=COLOR_MAIN, stroke_width=3.5).next_to(antenna_tip, LEFT, buff=0.15)
        eavesdropper_icon = VGroup(antenna_stem, antenna_tip, arc1, arc2)
        eavesdropper_label = Text("eavesdropper", font=FONT, font_size=26, color=COLOR_MAIN, weight=BOLD).next_to(eavesdropper_icon, DOWN, buff=0.3)
        eavesdropper = VGroup(eavesdropper_icon, eavesdropper_label).shift(RIGHT * 4.2 + UP * 1.6)

        # Establish code instantly (cut from shot 16)
        self.add(original_code)
        self.wait(1.5)

        # Eavesdropper fades in on the right
        self.play(
            FadeIn(eavesdropper, shift=LEFT * 0.3),
            run_time=1.3,
            rate_func=rate_functions.ease_out_cubic
        )

        # Antenna reception pulse
        self.play(
            arc1.animate.set_color(COLOR_ACCENT),
            arc2.animate.set_color(COLOR_ACCENT),
            run_time=0.35,
            rate_func=rate_functions.ease_in_sine
        )
        self.play(
            arc1.animate.set_color(COLOR_MAIN),
            arc2.animate.set_color(COLOR_MAIN),
            run_time=0.35,
            rate_func=rate_functions.ease_out_sine
        )

        # Eavesdropper "catches" a duplicate copy of the code
        caught_box = RoundedRectangle(
            width=3.8, height=0.85, corner_radius=0.1,
            color=COLOR_MAIN, stroke_width=3.5, fill_color=COLOR_BG, fill_opacity=0.9
        )
        caught_text = Text("8492  0317", font=FONT, font_size=30, color=COLOR_MAIN, weight=BOLD)
        caught_tag = Text("ONE-TIME CODE", font=FONT, font_size=20, color=COLOR_MUTED, weight=BOLD).next_to(caught_box, DOWN, buff=0.15)
        caught_code = VGroup(caught_box, caught_text.move_to(caught_box.get_center()), caught_tag)
        caught_code.move_to(original_code.get_center())

        target_caught_pos = eavesdropper.get_bottom() + DOWN * 1.3

        # Duplicate peels off from original_code and moves across to the eavesdropper
        self.play(
            caught_code.animate.move_to(target_caught_pos),
            run_time=2.0,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.5)
        # (Total elapsed: 6.0s)

        # --- BEAT 2: The "USED" Stamp & Fade (6s - 14s) ---
        # Voiceover: "...what they'd get is a code that's already spent. Not your number. Not even a reusable clue."
        
        # The bold, authoritative "USED" stamp mark directly over the caught code
        used_text = Text("USED", font=FONT, font_size=44, color=COLOR_ACCENT, weight=BOLD)
        used_box = RoundedRectangle(
            width=2.8, height=1.05, corner_radius=0.1,
            color=COLOR_ACCENT, stroke_width=5.5
        )
        stamp_group = VGroup(used_box, used_text.move_to(used_box.get_center())).move_to(target_caught_pos).rotate(14 * DEGREES)

        # Dramatic slam stamp animation
        impact_wave = used_box.copy().rotate(14 * DEGREES).move_to(target_caught_pos)
        
        self.play(
            FadeIn(stamp_group, scale=2.8),
            run_time=0.35,
            rate_func=rate_functions.ease_in_expo
        )
        self.play(
            impact_wave.animate.scale(1.5).set_opacity(0),
            run_time=0.45,
            rate_func=rate_functions.ease_out_cubic
        )

        # Caught duplicate and eavesdropper fade to a spent state
        self.play(
            caught_box.animate.set_stroke(color=COLOR_INERT, opacity=0.5),
            caught_text.animate.set_color(COLOR_INERT).set_opacity(0.5),
            caught_tag.animate.set_color(COLOR_INERT).set_opacity(0.5),
            used_box.animate.set_stroke(color=COLOR_INERT, opacity=0.6),
            used_text.animate.set_color(COLOR_INERT).set_opacity(0.6),
            eavesdropper.animate.set_color(COLOR_INERT).set_opacity(0.5),
            run_time=1.8,
            rate_func=rate_functions.ease_out_sine
        )
        
        # Hold while voiceover finishes the thought
        self.wait(5.4)
        # (Total elapsed: 14.0s)

        # --- BEAT 3: Original Transaction Resolves in Parallel (14s - 20s) ---
        # Voiceover: "Just a receipt for a transaction that already happened."
        
        # Reader icon for the legitimate transaction (Left side)
        reader_box = RoundedRectangle(
            width=2.6, height=3.4, corner_radius=0.18,
            color=COLOR_MAIN, stroke_width=4
        )
        reader_title = Text("READER", font=FONT, font_size=24, color=COLOR_MAIN, weight=BOLD).next_to(reader_box.get_top(), DOWN, buff=0.22)
        reader_screen = RoundedRectangle(
            width=2.1, height=1.5, corner_radius=0.1,
            color=COLOR_MUTED, stroke_width=2.5, fill_color=COLOR_BG, fill_opacity=0.8
        ).next_to(reader_title, DOWN, buff=0.18)
        reader_status = Text("PROCESSING", font=FONT, font_size=18, color=COLOR_MUTED, weight=BOLD).move_to(reader_screen.get_center())
        
        # Contactless wave indicator on terminal
        nfc_arc1 = Arc(radius=0.16, angle=PI/2, start_angle=PI/4, color=COLOR_MUTED, stroke_width=2.5).next_to(reader_screen, DOWN, buff=0.25)
        nfc_arc2 = Arc(radius=0.30, angle=PI/2, start_angle=PI/4, color=COLOR_MUTED, stroke_width=2.5).next_to(reader_screen, DOWN, buff=0.25)
        nfc_glyph = VGroup(nfc_arc1, nfc_arc2)
        
        reader_terminal = VGroup(reader_box, reader_title, reader_screen, reader_status, nfc_glyph).shift(LEFT * 4.2 + UP * 0.5)

        # Legitimate reader terminal fades in
        self.play(
            FadeIn(reader_terminal, shift=RIGHT * 0.3),
            run_time=1.0,
            rate_func=rate_functions.ease_out_cubic
        )

        # Original code glides into the legitimate reader
        self.play(
            original_code.animate.move_to(reader_screen.get_center()).scale(0.45),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )

        # Reader approves the transaction: Screen lights up green with checkmark
        check_p1 = reader_screen.get_center() + UP * 0.2 + LEFT * 0.24 + DOWN * 0.05
        check_p2 = check_p1 + RIGHT * 0.18 + DOWN * 0.18
        check_p3 = check_p2 + RIGHT * 0.36 + UP * 0.4
        checkmark = VGroup(
            Line(check_p1, check_p2, color=COLOR_SUCCESS, stroke_width=6),
            Line(check_p2, check_p3, color=COLOR_SUCCESS, stroke_width=6)
        )
        approved_text = Text("APPROVED", font=FONT, font_size=22, color=COLOR_SUCCESS, weight=BOLD).move_to(reader_screen.get_center() + DOWN * 0.35)

        self.play(
            FadeOut(original_code),
            FadeOut(reader_status),
            Create(checkmark),
            FadeIn(approved_text),
            reader_screen.animate.set_stroke(color=COLOR_SUCCESS, width=3.5).set_fill(color=COLOR_SUCCESS, opacity=0.22),
            run_time=0.9,
            rate_func=rate_functions.ease_out_cubic
        )

        # Final hold on the stark contrast: Approved Legit vs Spent Eavesdropped
        self.wait(2.6)
        # (Total elapsed: 20.0s / 480 frames)


AlreadySpent = Shot017_AlreadySpent
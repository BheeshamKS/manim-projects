from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = "#CBD5E1"     # High-contrast technical slate for mobile readability
COLOR_ACCENT = "#00E5FF"    # Tracr Cyan
COLOR_BG = BLACK


class Shot023_PhoneAsksFirst(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0023: The Card Cannot Ask - Phone Asks First
        # (148 Frames / ~6.17 Seconds @ 24fps)
        # =====================================================================

        # --- BEAT 1: Split Screen Establish (0s - 2s) ---
        # Voiceover: "The card can't ask that question..."

        # Vertical center dividing line
        center_divider = DashedLine(
            UP * 3.3, DOWN * 3.3, color="#64748B", stroke_width=2, stroke_opacity=0.45
        )

        # 1. Left Side: The Card (Enlarged fonts for phone)
        left_title = Text("THE CARD", font=FONT, font_size=24, color=COLOR_MAIN, weight=BOLD).move_to(LEFT * 3.6 + UP * 2.6)
        
        card_outline = RoundedRectangle(
            width=3.6, height=2.3, corner_radius=0.18,
            color=COLOR_MAIN, stroke_width=3.5, fill_color=COLOR_BG, fill_opacity=0.9
        ).move_to(LEFT * 3.6 + UP * 0.4)
        
        card_chip = RoundedRectangle(
            width=0.85, height=0.7, corner_radius=0.08,
            color="#94A3B8", stroke_width=2.5, fill_color=COLOR_BG, fill_opacity=1
        ).move_to(card_outline.get_center() + LEFT * 0.8)
        
        chip_line = Line(card_chip.get_left(), card_chip.get_right(), color="#64748B", stroke_width=2)
        
        card_caption = Text("answers anyone in range", font=FONT, font_size=20, color=COLOR_MUTED, weight=BOLD).next_to(card_outline, DOWN, buff=0.45)
        card_group = VGroup(card_outline, card_chip, chip_line, card_caption)

        # 2. Right Side: The Phone (Enlarged fonts for phone)
        right_title = Text("YOUR PHONE", font=FONT, font_size=24, color=COLOR_MAIN, weight=BOLD).move_to(RIGHT * 3.6 + UP * 2.6)
        
        phone_outline = RoundedRectangle(
            width=2.5, height=4.2, corner_radius=0.38,
            color=COLOR_MAIN, stroke_width=3.5, fill_color=COLOR_BG, fill_opacity=0.9
        ).move_to(RIGHT * 3.6 + DOWN * 0.2)
        
        phone_screen = RoundedRectangle(
            width=2.1, height=3.6, corner_radius=0.22,
            color="#64748B", stroke_width=1.5, stroke_opacity=0.45
        ).move_to(phone_outline.get_center())
        
        phone_speaker = RoundedRectangle(
            width=0.5, height=0.08, corner_radius=0.04,
            color="#64748B", stroke_width=1.5
        ).next_to(phone_outline.get_top(), DOWN, buff=0.15)
        
        # Biometric Authorization Gate inside Phone
        gate_badge = RoundedRectangle(
            width=2.1, height=1.3, corner_radius=0.12,
            color=COLOR_ACCENT, stroke_width=2.5, fill_color=COLOR_BG, fill_opacity=0.95
        ).move_to(phone_outline.get_center())
        
        gate_lock_body = RoundedRectangle(width=0.38, height=0.32, corner_radius=0.05, color=COLOR_ACCENT, stroke_width=2)
        gate_lock_shackle = Arc(radius=0.11, angle=PI, color=COLOR_ACCENT, stroke_width=2.5).next_to(gate_lock_body, UP, buff=0)
        gate_lock_icon = VGroup(gate_lock_body, gate_lock_shackle).next_to(gate_badge.get_top(), DOWN, buff=0.16)
        gate_text = Text("AUTH REQUIRED", font=FONT, font_size=16, color=COLOR_ACCENT, weight=BOLD).next_to(gate_lock_icon, DOWN, buff=0.12)
        gate_group = VGroup(gate_badge, gate_lock_icon, gate_text)
        
        phone_caption = Text("asks first", font=FONT, font_size=20, color=COLOR_MUTED, weight=BOLD).next_to(phone_outline, DOWN, buff=0.35)
        phone_group = VGroup(phone_outline, phone_screen, phone_speaker, gate_group, phone_caption)

        # Establish split screen
        self.play(
            Create(center_divider),
            FadeIn(left_title),
            FadeIn(card_group),
            FadeIn(right_title),
            FadeIn(phone_group),
            run_time=1.2,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(0.8)
        # (Total elapsed: 2.0s)

        # --- BEAT 2: Card Answers Immediately (2s - 4s) ---
        # Voiceover: "It answers anyone in range."

        # Approaching RF reader query wave from left - bright electric cyan-blue
        query_wave1 = Arc(radius=0.6, angle=PI/2, start_angle=-PI/4, color="#0284C7", stroke_width=3.5).next_to(card_outline, LEFT, buff=0.9)
        query_wave2 = Arc(radius=1.0, angle=PI/2, start_angle=-PI/4, color="#0284C7", stroke_width=3.5).next_to(card_outline, LEFT, buff=0.9)
        incoming_query = VGroup(query_wave1, query_wave2)

        # Immediate broadcast response from card
        card_response_glow = card_outline.copy().set_color(COLOR_ACCENT).set_stroke(width=6)
        card_burst = card_outline.copy().set_color(COLOR_ACCENT).set_stroke(width=2.5)
        response_caption = Text("BROADCASTS INSTANTLY", font=FONT, font_size=20, color=COLOR_ACCENT, weight=BOLD).move_to(card_caption.get_center())

        self.play(
            incoming_query.animate.shift(RIGHT * 0.7).set_opacity(0),
            card_outline.animate.set_stroke(color=COLOR_ACCENT, width=4.5),
            card_chip.animate.set_stroke(color=COLOR_ACCENT, width=3.5),
            FadeIn(card_burst),
            Transform(card_caption, response_caption),
            run_time=0.8,
            rate_func=rate_functions.ease_out_cubic
        )
        self.play(
            card_burst.animate.scale(1.3).set_opacity(0),
            run_time=0.5,
            rate_func=rate_functions.ease_out_sine
        )
        self.wait(0.7)
        # (Total elapsed: 4.0s)

        # --- BEAT 3: Phone Asks First / Withholds (4s - 6.17s) ---
        # Voiceover: "Your phone asks first."

        # Query wave arrives at phone from right
        query_p1 = Arc(radius=0.6, angle=PI/2, start_angle=3*PI/4, color="#0284C7", stroke_width=3.5).next_to(phone_outline, RIGHT, buff=0.9)
        query_p2 = Arc(radius=1.0, angle=PI/2, start_angle=3*PI/4, color="#0284C7", stroke_width=3.5).next_to(phone_outline, RIGHT, buff=0.9)
        incoming_phone_query = VGroup(query_p1, query_p2)

        # Phone withholds: gate flashes warning/scan laser, no broadcast occurs
        scan_line = Line(gate_badge.get_left() + RIGHT * 0.1, gate_badge.get_right() + LEFT * 0.1, color=COLOR_ACCENT, stroke_width=3.5)
        scan_line.move_to(gate_badge.get_top() + DOWN * 0.2)
        
        withheld_caption = Text("TRANSMISSION WITHHELD", font=FONT, font_size=20, color="#F87171", weight=BOLD).move_to(phone_caption.get_center())

        self.play(
            incoming_phone_query.animate.shift(LEFT * 0.7).set_opacity(0),
            gate_badge.animate.set_stroke(width=4.5),
            Transform(phone_caption, withheld_caption),
            Create(scan_line),
            run_time=0.7,
            rate_func=rate_functions.ease_out_cubic
        )
        self.play(
            scan_line.animate.move_to(gate_badge.get_bottom() + UP * 0.2).set_opacity(0),
            gate_badge.animate.set_stroke(width=2.5),
            run_time=0.6,
            rate_func=rate_functions.ease_in_out_sine
        )

        # Hold on the contrast: Instant Broadcast (Card) vs Auth Gate (Phone)
        self.wait(0.866)
        # (Total elapsed: 148 frames / 6.166s @ 24fps)


PhoneAsksFirst = Shot023_PhoneAsksFirst


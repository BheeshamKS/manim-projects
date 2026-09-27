from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = "#CBD5E1"     # High-contrast technical slate for mobile readability
COLOR_ACCENT = "#00E5FF"    # Tracr Cyan
COLOR_BG = BLACK


class Shot020_SameMechanism(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0020: Same Mechanism - What Changes Is What's In Front
        # (8 Seconds / 192 Frames @ 24fps)
        # =====================================================================

        # --- BEAT 1: Phone Outline & Recap Icons (0s - 3s) ---
        # Voiceover: "Assuming yours has it: same wake-up, same handshake, same one-time code."

        # 1. Phone silhouette outline
        phone_body = RoundedRectangle(
            width=4.4, height=6.6, corner_radius=0.55,
            color=COLOR_MAIN, stroke_width=3.5
        )
        speaker = RoundedRectangle(
            width=0.9, height=0.12, corner_radius=0.06,
            color="#64748B", stroke_width=2
        ).next_to(phone_body.get_top(), DOWN, buff=0.25)
        screen_area = RoundedRectangle(
            width=3.9, height=5.7, corner_radius=0.35,
            color="#64748B", stroke_width=2, stroke_opacity=0.45
        ).move_to(phone_body.get_center())
        phone_group = VGroup(phone_body, speaker, screen_area)

        # 2. Three miniature recap icons inside the phone (boosted text size for phone)
        # Icon 1: Wake-up (Coil)
        coil_outer = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.1, color=COLOR_MAIN, stroke_width=2.5)
        coil_inner = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06, color=COLOR_MAIN, stroke_width=2)
        coil_label = Text("wake-up", font=FONT, font_size=20, color=COLOR_MUTED, weight=BOLD).next_to(coil_outer, DOWN, buff=0.18)
        icon_wakeup = VGroup(coil_outer, coil_inner, coil_label)

        # Icon 2: Handshake (2 opposing exchange arrows)
        arrow_r = Arrow(start=LEFT * 0.32, end=RIGHT * 0.32, color=COLOR_MAIN, stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.3).shift(UP * 0.12)
        arrow_l = Arrow(start=RIGHT * 0.32, end=LEFT * 0.32, color=COLOR_MAIN, stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.3).shift(DOWN * 0.12)
        handshake_box = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.1, color="#64748B", stroke_width=1.5, stroke_opacity=0.6)
        handshake_arrows = VGroup(arrow_r, arrow_l).move_to(handshake_box.get_center())
        handshake_label = Text("handshake", font=FONT, font_size=20, color=COLOR_MUTED, weight=BOLD).next_to(handshake_box, DOWN, buff=0.18)
        icon_handshake = VGroup(handshake_box, handshake_arrows, handshake_label)

        # Icon 3: One-Time Code (Mini OTC Stamp)
        otc_box = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.1, color=COLOR_MAIN, stroke_width=2.5)
        otc_text = Text("OTC", font=FONT, font_size=20, color=COLOR_MAIN, weight=BOLD).move_to(otc_box.get_center())
        otc_label = Text("code", font=FONT, font_size=20, color=COLOR_MUTED, weight=BOLD).next_to(otc_box, DOWN, buff=0.18)
        icon_otc = VGroup(otc_box, otc_text, otc_label)

        # Arrange icons inside phone
        recap_icons = VGroup(icon_wakeup, icon_handshake, icon_otc).arrange(RIGHT, buff=0.25)
        recap_icons.move_to(phone_body.get_center() + DOWN * 0.4)

        # Header tag inside phone - boosted for phone visibility
        phone_header = Text("NFC SUBSYSTEM", font=FONT, font_size=24, color=COLOR_MAIN, weight=BOLD).next_to(speaker, DOWN, buff=0.45)

        # Establish phone and recap icons
        self.add(phone_group, phone_header, recap_icons)
        self.wait(0.5)

        # Pulse icons in sequence matching voiceover cadence
        # Pulse 1: "same wake-up"
        self.play(
            coil_outer.animate.set_color(COLOR_ACCENT).set_stroke(width=3.5),
            coil_inner.animate.set_color(COLOR_ACCENT).set_stroke(width=3.5),
            coil_label.animate.set_color(COLOR_ACCENT),
            run_time=0.35,
            rate_func=rate_functions.ease_out_sine
        )
        self.play(
            coil_outer.animate.set_color(COLOR_MAIN).set_stroke(width=2.5),
            coil_inner.animate.set_color(COLOR_MAIN).set_stroke(width=2),
            coil_label.animate.set_color(COLOR_MUTED),
            run_time=0.35,
            rate_func=rate_functions.ease_in_sine
        )

        # Pulse 2: "same handshake"
        self.play(
            arrow_r.animate.set_color(COLOR_ACCENT),
            arrow_l.animate.set_color(COLOR_ACCENT),
            handshake_label.animate.set_color(COLOR_ACCENT),
            run_time=0.35,
            rate_func=rate_functions.ease_out_sine
        )
        self.play(
            arrow_r.animate.set_color(COLOR_MAIN),
            arrow_l.animate.set_color(COLOR_MAIN),
            handshake_label.animate.set_color(COLOR_MUTED),
            run_time=0.35,
            rate_func=rate_functions.ease_in_sine
        )

        # Pulse 3: "same one-time code"
        self.play(
            otc_box.animate.set_color(COLOR_ACCENT).set_stroke(width=3.5),
            otc_text.animate.set_color(COLOR_ACCENT),
            otc_label.animate.set_color(COLOR_ACCENT),
            run_time=0.35,
            rate_func=rate_functions.ease_out_sine
        )
        self.play(
            otc_box.animate.set_color(COLOR_MAIN).set_stroke(width=2.5),
            otc_text.animate.set_color(COLOR_MAIN),
            otc_label.animate.set_color(COLOR_MUTED),
            run_time=0.35,
            rate_func=rate_functions.ease_in_sine
        )
        self.wait(0.4)
        # (Total elapsed: 3.0s)

        # --- BEAT 2: The Gate / Door Appears (3s - 6s) ---
        # Voiceover: "What changes is what sits in front of it."

        # Security Gate / Door Barrier icon
        gate_box = RoundedRectangle(
            width=3.8, height=1.9, corner_radius=0.15,
            color=COLOR_ACCENT, stroke_width=4.5, fill_color=COLOR_BG, fill_opacity=0.92
        ).move_to(recap_icons.get_center())
        
        # Gate barrier bars
        gate_posts = VGroup(
            Line(gate_box.get_top() + LEFT * 1.5, gate_box.get_bottom() + LEFT * 1.5, color=COLOR_ACCENT, stroke_width=4),
            Line(gate_box.get_top() + RIGHT * 1.5, gate_box.get_bottom() + RIGHT * 1.5, color=COLOR_ACCENT, stroke_width=4),
        )
        
        # Center lock/shield emblem
        gate_shield_body = RoundedRectangle(width=0.75, height=0.65, corner_radius=0.1, color=COLOR_ACCENT, fill_color=COLOR_BG, fill_opacity=1, stroke_width=3)
        gate_shield_shackle = Arc(radius=0.24, angle=PI, color=COLOR_ACCENT, stroke_width=4).next_to(gate_shield_body, UP, buff=0)
        gate_lock = VGroup(gate_shield_body, gate_shield_shackle).move_to(gate_box.get_center())
        
        gate_label = Text("SECURITY GATE", font=FONT, font_size=22, color=COLOR_ACCENT, weight=BOLD).next_to(gate_box, UP, buff=0.18)
        gate_group = VGroup(gate_box, gate_posts, gate_lock, gate_label)

        # Gate slam/appearance in front of the recap icons
        gate_impact = gate_box.copy().set_stroke(width=2)

        self.play(
            FadeIn(gate_group, scale=1.4),
            run_time=0.5,
            rate_func=rate_functions.ease_in_expo
        )
        self.play(
            gate_impact.animate.scale(1.25).set_opacity(0),
            run_time=0.5,
            rate_func=rate_functions.ease_out_cubic
        )
        
        # Glow pulse on the gate
        self.play(
            gate_box.animate.set_stroke(width=6),
            gate_lock.animate.scale(1.1),
            run_time=0.5,
            rate_func=rate_functions.ease_out_sine
        )
        self.play(
            gate_box.animate.set_stroke(width=4.5),
            gate_lock.animate.scale(1 / 1.1),
            run_time=0.5,
            rate_func=rate_functions.ease_in_sine
        )
        self.wait(1.0)
        # (Total elapsed: 6.0s)

        # --- BEAT 3: Hold (6s - 8s) ---
        self.wait(2.0)
        # (Total elapsed: 8.0s / 192 frames)


SameMechanism = Shot020_SameMechanism


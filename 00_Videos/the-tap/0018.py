from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = "#CBD5E1"     # High-contrast technical slate for mobile readability
COLOR_INERT = "#64748B"     # Spent / inactive slate
COLOR_ACCENT = "#00E5FF"    # Tracr Cyan
COLOR_FIELD = "#0284C7"     # Electric cyan-blue for field lines
COLOR_COPPER = "#F59E0B"    # Copper / warm amber for the antenna coil
COLOR_GOLD = "#F59E0B"      # Warm amber/gold for subtle paid glow bloom
COLOR_WARM_LIGHT = "#FEF08A"# Soft warm light highlight
COLOR_RED_STRIKE = "#EF4444"# Bold diagnostic red for strike-throughs
COLOR_BG = BLACK


class Shot018_CardRecap(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0018: Card Recap - Start To Finish
        # (9.0 Seconds / 216 Frames @ 24fps)
        # =====================================================================

        # ---------------------------------------------------------------------
        # --- BEAT 1: The Entire Card Architecture (0.0s - 2.4s) ---
        # Voiceover: "And that's the entire card, start to finish."
        # ---------------------------------------------------------------------

        # Top Header
        header_title = Text("CARD ARCHITECTURE", font=FONT, font_size=24, color=COLOR_MAIN, weight=BOLD)
        header_sub = Text("COMPLETE PASSIVE CIRCUIT", font=FONT, font_size=15, color=COLOR_MUTED, weight=BOLD)
        header_group = VGroup(header_title, header_sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.55)

        # 1. The Card Chassis
        card_w, card_h = 6.4, 3.8
        card_chassis = RoundedRectangle(
            width=card_w, height=card_h, corner_radius=0.25,
            color=COLOR_MAIN, stroke_width=3.5, fill_color=COLOR_BG, fill_opacity=0.95
        )

        # 2. Multi-turn Copper Loop Antenna Coil
        # 3 concentric perimeter loops embedded in the card substrate
        coil_loops = VGroup(*[
            RoundedRectangle(
                width=card_w - (0.4 + i * 0.22),
                height=card_h - (0.4 + i * 0.22),
                corner_radius=0.20 - (i * 0.03),
                color=COLOR_COPPER,
                stroke_width=2.5,
                stroke_opacity=0.85
            )
            for i in range(3)
        ])

        # 3. Secure Element Microchip Module (Left side, standard EMV layout)
        chip_x = -1.85
        chip_bezel = RoundedRectangle(
            width=1.35, height=1.1, corner_radius=0.1,
            color=COLOR_MAIN, stroke_width=2.8, fill_color="#0F172A", fill_opacity=1
        ).shift(RIGHT * chip_x)

        # Contact pad dividing lines
        h_line = Line(chip_bezel.get_left(), chip_bezel.get_right(), color="#64748B", stroke_width=2)
        v_line1 = Line(chip_bezel.get_top() + LEFT * 0.22, chip_bezel.get_bottom() + LEFT * 0.22, color="#64748B", stroke_width=2)
        v_line2 = Line(chip_bezel.get_top() + RIGHT * 0.22, chip_bezel.get_bottom() + RIGHT * 0.22, color="#64748B", stroke_width=2)
        chip_pads = VGroup(h_line, v_line1, v_line2)

        # Inner silicon cryptographic core
        chip_core = RoundedRectangle(
            width=0.42, height=0.42, corner_radius=0.06,
            color=COLOR_ACCENT, fill_color=COLOR_ACCENT, fill_opacity=0.35, stroke_width=2.5
        ).move_to(chip_bezel.get_center())

        chip_tag = Text("SECURE CHIP", font=FONT, font_size=15, color=COLOR_ACCENT, weight=BOLD).next_to(chip_bezel, DOWN, buff=0.18)
        chip_group = VGroup(chip_bezel, chip_pads, chip_core, chip_tag)

        # Antenna feed traces leading into the chip module
        trace_top = Line(chip_bezel.get_top() + LEFT * 0.3, chip_bezel.get_top() + LEFT * 0.3 + UP * 0.9 + RIGHT * 0.8, color=COLOR_COPPER, stroke_width=2.5)
        trace_bot = Line(chip_bezel.get_bottom() + LEFT * 0.3, chip_bezel.get_bottom() + LEFT * 0.3 + DOWN * 0.9 + RIGHT * 0.8, color=COLOR_COPPER, stroke_width=2.5)
        feed_traces = VGroup(trace_top, trace_bot)

        # Coil label on the right
        coil_tag = Text("PERIMETER COIL", font=FONT, font_size=15, color=COLOR_COPPER, weight=BOLD).move_to(RIGHT * 1.6 + UP * 1.35)

        card_complete = VGroup(card_chassis, coil_loops, feed_traces, chip_group, coil_tag).shift(DOWN * 0.3)

        # Initial establish
        self.add(header_group, card_complete)
        self.wait(0.3)

        # Current Surge / Scanline Animation ("Start to finish" pulse)
        # Pulse traces around the coil and converges directly into the chip core
        pulse_flash = coil_loops[0].copy().set_color(COLOR_ACCENT).set_stroke(width=5.5)
        core_flash = chip_core.copy().set_color(WHITE).set_fill(COLOR_ACCENT, opacity=0.9)
        core_ripple = Circle(radius=0.25, color=COLOR_ACCENT, stroke_width=4).move_to(chip_core.get_center())

        self.play(
            ShowPassingFlash(pulse_flash, run_time=1.1, time_width=0.4),
            chip_core.animate.set_fill(COLOR_ACCENT, opacity=0.85).set_stroke(width=3.5),
            run_time=1.1,
            rate_func=rate_functions.ease_out_sine
        )
        self.play(
            core_ripple.animate.scale(3.2).set_opacity(0),
            chip_core.animate.set_fill(COLOR_ACCENT, opacity=0.35).set_stroke(width=2.5),
            run_time=0.6,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(0.4)
        # (Total elapsed: 2.4s / 58 frames)

        # ---------------------------------------------------------------------
        # --- BEAT 2: The Three Negatives (2.4s - 6.0s) ---
        # Voiceover: "No battery, no transmitter, no real number ever sent —"
        # ---------------------------------------------------------------------

        # Card scales down smoothly and docks at the top
        card_docked = card_complete.copy()
        
        self.play(
            header_group.animate.shift(UP * 0.3).set_opacity(0),
            card_complete.animate.scale(0.52).to_edge(UP, buff=0.35),
            run_time=0.6,
            rate_func=rate_functions.ease_in_out_cubic
        )

        # 3 Diagnostic Pillar Modules
        col_w, col_h = 3.7, 3.4
        box_y = -1.45

        # --- Pillar 1: NO BATTERY (Left: x = -4.1) ---
        col1_bg = RoundedRectangle(
            width=col_w, height=col_h, corner_radius=0.18,
            color="#334155", stroke_width=2.2, fill_color=COLOR_BG, fill_opacity=0.95
        ).move_to(LEFT * 4.1 + UP * box_y)

        # Battery icon
        bat_body = RoundedRectangle(width=1.3, height=0.72, corner_radius=0.08, color=COLOR_MAIN, stroke_width=2.8)
        bat_nub = RoundedRectangle(width=0.14, height=0.32, corner_radius=0.03, color=COLOR_MAIN, stroke_width=2.2).next_to(bat_body, RIGHT, buff=0.06)
        bat_bars = VGroup(*[
            Rectangle(width=0.22, height=0.5, color=COLOR_INERT, fill_color=COLOR_INERT, fill_opacity=0.6, stroke_width=0)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.1).move_to(bat_body.get_center())
        battery_icon = VGroup(bat_body, bat_nub, bat_bars).move_to(col1_bg.get_center() + UP * 0.75)

        bat_strike = Line(
            bat_body.get_corner(DL) + DL * 0.16,
            bat_body.get_corner(UR) + UR * 0.16,
            color=COLOR_RED_STRIKE, stroke_width=4.5
        )

        col1_title = Text("NO BATTERY", font=FONT, font_size=21, color=COLOR_MAIN, weight=BOLD).next_to(battery_icon, DOWN, buff=0.32)
        col1_fact = Text("PASSIVE INDUCTION", font=FONT, font_size=14, color=COLOR_ACCENT, weight=BOLD).next_to(col1_title, DOWN, buff=0.14)
        col1_sub = Text("powered by field", font=FONT, font_size=14, color=COLOR_MUTED).next_to(col1_fact, DOWN, buff=0.1)
        col1_group = VGroup(col1_bg, battery_icon, bat_strike, col1_title, col1_fact, col1_sub)

        # --- Pillar 2: NO TRANSMITTER (Center: x = 0) ---
        col2_bg = RoundedRectangle(
            width=col_w, height=col_h, corner_radius=0.18,
            color="#334155", stroke_width=2.2, fill_color=COLOR_BG, fill_opacity=0.95
        ).move_to(UP * box_y)

        # Antenna broadcast icon
        ant_mast = Line(DOWN * 0.35, UP * 0.35, color=COLOR_MAIN, stroke_width=3)
        ant_tip = Dot(ant_mast.get_top(), radius=0.08, color=COLOR_MAIN)
        ant_arc_l1 = Arc(radius=0.28, angle=PI/2, start_angle=3*PI/4, color=COLOR_MAIN, stroke_width=2.5).next_to(ant_tip, LEFT, buff=0.1)
        ant_arc_l2 = Arc(radius=0.48, angle=PI/2, start_angle=3*PI/4, color=COLOR_MAIN, stroke_width=2.5).next_to(ant_tip, LEFT, buff=0.1)
        ant_arc_r1 = Arc(radius=0.28, angle=PI/2, start_angle=-PI/4, color=COLOR_MAIN, stroke_width=2.5).next_to(ant_tip, RIGHT, buff=0.1)
        ant_arc_r2 = Arc(radius=0.48, angle=PI/2, start_angle=-PI/4, color=COLOR_MAIN, stroke_width=2.5).next_to(ant_tip, RIGHT, buff=0.1)
        antenna_icon = VGroup(ant_mast, ant_tip, ant_arc_l1, ant_arc_l2, ant_arc_r1, ant_arc_r2).move_to(col2_bg.get_center() + UP * 0.75)

        ant_strike = Line(
            antenna_icon.get_corner(DL) + DL * 0.12,
            antenna_icon.get_corner(UR) + UR * 0.12,
            color=COLOR_RED_STRIKE, stroke_width=4.5
        )

        col2_title = Text("NO TRANSMITTER", font=FONT, font_size=21, color=COLOR_MAIN, weight=BOLD).next_to(antenna_icon, DOWN, buff=0.32)
        col2_fact = Text("LOAD MODULATION", font=FONT, font_size=14, color=COLOR_ACCENT, weight=BOLD).next_to(col2_title, DOWN, buff=0.14)
        col2_sub = Text("ripples reader field", font=FONT, font_size=14, color=COLOR_MUTED).next_to(col2_fact, DOWN, buff=0.1)
        col2_group = VGroup(col2_bg, antenna_icon, ant_strike, col2_title, col2_fact, col2_sub)

        # --- Pillar 3: NO REAL NUMBER (Right: x = +4.1) ---
        col3_bg = RoundedRectangle(
            width=col_w, height=col_h, corner_radius=0.18,
            color="#334155", stroke_width=2.2, fill_color=COLOR_BG, fill_opacity=0.95
        ).move_to(RIGHT * 4.1 + UP * box_y)

        # Card number / PAN blocks (scaled to sit comfortably within the box)
        pan_blocks = VGroup(*[
            RoundedRectangle(width=0.16, height=0.24, corner_radius=0.04, color=COLOR_MAIN, fill_color=COLOR_MAIN, fill_opacity=0.9)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.06)
        pan_row = VGroup(*[pan_blocks.copy() for _ in range(3)]).arrange(RIGHT, buff=0.18)
        pan_icon = pan_row.move_to(col3_bg.get_center() + UP * 0.75)

        pan_strike = Line(
            pan_icon.get_corner(DL) + DL * 0.12,
            pan_icon.get_corner(UR) + UR * 0.12,
            color=COLOR_RED_STRIKE, stroke_width=4.5
        )

        col3_title = Text("NO REAL NUMBER", font=FONT, font_size=21, color=COLOR_MAIN, weight=BOLD).next_to(pan_icon, DOWN, buff=0.32)
        col3_fact = Text("ONE-TIME CODE", font=FONT, font_size=14, color=COLOR_ACCENT, weight=BOLD).next_to(col3_title, DOWN, buff=0.14)
        col3_sub = Text("counter + secret key", font=FONT, font_size=14, color=COLOR_MUTED).next_to(col3_fact, DOWN, buff=0.1)
        col3_group = VGroup(col3_bg, pan_icon, pan_strike, col3_title, col3_fact, col3_sub)

        # Pop-in cadence matching voiceover
        # 1. "No battery," (VO ~2.4s - 3.4s)
        self.play(
            FadeIn(col1_group, shift=UP * 0.25, scale=1.05),
            run_time=0.55,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.25)

        # 2. "no transmitter," (VO ~3.5s - 4.5s)
        self.play(
            FadeIn(col2_group, shift=UP * 0.25, scale=1.05),
            run_time=0.55,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.25)

        # 3. "no real number ever sent —" (VO ~4.6s - 5.8s)
        self.play(
            FadeIn(col3_group, shift=UP * 0.25, scale=1.05),
            run_time=0.55,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.85)
        # (Total elapsed: 6.0s / 144 frames)

        # ---------------------------------------------------------------------
        # --- BEAT 3: And It Still Pays For Your Coffee (6.0s - 9.0s) ---
        # Voiceover: "— and it still pays for your coffee."
        # (Note: Strictly DO NOT show "Payment Successful" text here!)
        # ---------------------------------------------------------------------

        all_recap_elements = VGroup(card_complete, col1_group, col2_group, col3_group)

        # 1. Elegant Ceramic Coffee Cup Assembly (Proper solid layering)
        saucer_y = 1.05

        # Saucer (base rim + inner well)
        saucer_rim = Ellipse(
            width=3.7, height=0.48, color=COLOR_MAIN, stroke_width=3.5,
            fill_color="#0B0F19", fill_opacity=1
        ).move_to(DOWN * saucer_y)
        saucer_inner = Ellipse(
            width=2.4, height=0.18, color="#475569", stroke_width=1.5
        ).move_to(DOWN * saucer_y)
        saucer = VGroup(saucer_rim, saucer_inner)

        # Cup Handle (Smooth bezier curve attached behind cup body)
        handle = CubicBezier(
            RIGHT * 1.25 + UP * 0.12,
            RIGHT * 2.15 + UP * 0.2,
            RIGHT * 2.15 + DOWN * 0.68,
            RIGHT * 0.95 + DOWN * 0.62,
            color=COLOR_MAIN, stroke_width=3.5
        )

        # Solid Cup Body (sitting neatly on the saucer)
        cup_body = Polygon(
            LEFT * 1.32 + UP * 0.24,
            RIGHT * 1.32 + UP * 0.24,
            RIGHT * 0.82 + DOWN * 0.92,
            LEFT * 0.82 + DOWN * 0.92,
            color=COLOR_MAIN, stroke_width=3.5,
            fill_color="#0B0F19", fill_opacity=1
        )

        # Top Rim & Hot Coffee Liquid
        cup_rim = Ellipse(
            width=2.64, height=0.46, color=COLOR_MAIN, stroke_width=3.5,
            fill_color="#1E293B", fill_opacity=1
        ).move_to(UP * 0.24)

        coffee_liquid = Ellipse(
            width=2.45, height=0.38, color="#2D1810", stroke_width=1.5,
            fill_color="#3E2723", fill_opacity=1
        ).move_to(UP * 0.22)

        # Crema heart swirl (nested cleanly inside the coffee liquid ellipse)
        crema_swirl = Arc(
            radius=0.22, angle=1.35 * PI, start_angle=0.15,
            color="#D7CCC8", stroke_width=2.0
        ).move_to(UP * 0.22 + LEFT * 0.12)

        # Rising Steam Trails (Graceful S-curves)
        steam1 = CubicBezier(
            LEFT * 0.45 + UP * 0.52,
            LEFT * 0.75 + UP * 1.15,
            LEFT * 0.25 + UP * 1.65,
            LEFT * 0.55 + UP * 2.25,
            color=COLOR_MUTED, stroke_width=2.5
        ).set_stroke(opacity=0.6)

        steam2 = CubicBezier(
            ORIGIN + UP * 0.52,
            RIGHT * 0.35 + UP * 1.2,
            LEFT * 0.25 + UP * 1.8,
            RIGHT * 0.1 + UP * 2.45,
            color=COLOR_MUTED, stroke_width=2.5
        ).set_stroke(opacity=0.75)

        steam3 = CubicBezier(
            RIGHT * 0.5 + UP * 0.52,
            RIGHT * 0.2 + UP * 1.15,
            RIGHT * 0.7 + UP * 1.7,
            RIGHT * 0.4 + UP * 2.35,
            color=COLOR_MUTED, stroke_width=2.5
        ).set_stroke(opacity=0.55)

        steam_group = VGroup(steam1, steam2, steam3)

        coffee_cup = VGroup(
            saucer, handle, cup_body, cup_rim, coffee_liquid, crema_swirl
        )

        # 2. Warm Amber Light Bloom ("Paid" glow, subtle warm light bloom)
        bloom_core = Ellipse(
            width=4.8, height=3.6, color=COLOR_GOLD,
            fill_color=COLOR_GOLD, fill_opacity=0.22, stroke_width=0
        ).move_to(coffee_cup.get_center() + DOWN * 0.1)

        bloom_mid = Ellipse(
            width=7.2, height=5.0, color=COLOR_GOLD,
            fill_color=COLOR_GOLD, fill_opacity=0.12, stroke_width=0
        ).move_to(coffee_cup.get_center() + DOWN * 0.1)

        bloom_outer = Ellipse(
            width=9.6, height=6.4, color="#D97706",
            fill_color="#D97706", fill_opacity=0.06, stroke_width=0
        ).move_to(coffee_cup.get_center() + DOWN * 0.1)

        bloom_group = VGroup(bloom_outer, bloom_mid, bloom_core)

        # 3. Transaction Settled Status Badge (Discreet verification, NO "Payment Successful")
        badge_box = RoundedRectangle(
            width=4.8, height=0.75, corner_radius=0.15,
            color=COLOR_GOLD, stroke_width=2.2, fill_color="#0B0F19", fill_opacity=0.95
        ).move_to(DOWN * 1.85)

        badge_left = Text("COFFEE // $4.50", font=FONT, font_size=19, color=COLOR_MAIN, weight=BOLD)
        badge_dot = Dot(radius=0.06, color=COLOR_GOLD)
        badge_right = Text("SETTLED", font=FONT, font_size=16, color=COLOR_GOLD, weight=BOLD)

        badge_content = VGroup(badge_left, badge_dot, badge_right).arrange(RIGHT, buff=0.28).move_to(badge_box.get_center())
        badge_group = VGroup(badge_box, badge_content)

        # Smooth transition into the coffee cup (0.45s)
        self.play(
            FadeOut(all_recap_elements, scale=0.9),
            FadeIn(coffee_cup, scale=1.08),
            FadeIn(steam_group),
            run_time=0.45,
            rate_func=rate_functions.ease_out_cubic
        )

        # The Warm Light Bloom ignites ("subtle paid glow")
        self.play(
            FadeIn(bloom_group, scale=0.85),
            cup_rim.animate.set_stroke(color=COLOR_WARM_LIGHT),
            saucer_rim.animate.set_stroke(color=COLOR_GOLD),
            handle.animate.set_stroke(color=COLOR_WARM_LIGHT),
            FadeIn(badge_group, shift=UP * 0.15),
            steam1.animate.shift(UP * 0.3).set_stroke(opacity=0.25),
            steam2.animate.shift(UP * 0.35).set_stroke(opacity=0.35),
            steam3.animate.shift(UP * 0.28).set_stroke(opacity=0.2),
            run_time=0.85,
            rate_func=rate_functions.ease_out_sine
        )

        # Final hold through frame 216 (exactly 9.0s)
        self.wait(1.575)


CardRecap = Shot018_CardRecap

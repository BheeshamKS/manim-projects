from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"

COLOR_MAIN = WHITE
COLOR_MUTED = "#CBD5E1"  # Clean high-contrast slate for mobile readability
COLOR_SLATE = "#64748B"  # Muted technical slate
COLOR_ACCENT = "#00E5FF" # Tracr Cyan
COLOR_BG = BLACK


class Shot013_014_HandshakeCliffhanger(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0013: Handshake Cliffhanger (0.0s - 14.2s / 340 frames @ 24fps)
        # =====================================================================

        # --- BEAT 1: The Handshake Recap & Demotion (0.0s - 3.8s) ---
        # Voiceover: "That's the conversation. Short, scripted, computer-fast."
        
        # 1. 2D recap of the 4 pulses from the Blender handshake
        reader_node = Text("READER", font=FONT, font_size=32, color=COLOR_MAIN, weight=BOLD)
        card_node = Text("CARD", font=FONT, font_size=32, color=COLOR_MAIN, weight=BOLD)
        nodes = VGroup(reader_node, card_node).arrange(RIGHT, buff=4.4)
        
        arrows = VGroup()
        for i in range(4):
            if i % 2 == 0:
                start = reader_node.get_right() + RIGHT * 0.2
                end = card_node.get_left() + LEFT * 0.2
            else:
                start = card_node.get_left() + LEFT * 0.2
                end = reader_node.get_right() + RIGHT * 0.2
                
            y_offset = UP * (0.6 - i * 0.4)
            arrow = Line(start + y_offset, end + y_offset, color=COLOR_MAIN, stroke_width=4).add_tip(tip_length=0.18)
            arrows.add(arrow)

        handshake_timeline = VGroup(nodes, arrows)
        
        # Continuity entrance from Blender
        self.play(FadeIn(handshake_timeline), run_time=1.0)
        self.wait(1.0)
        
        # Demote to top edge ("That's the conversation. Short, scripted, computer-fast.")
        self.play(
            handshake_timeline.animate.scale(0.68).to_edge(UP, buff=0.45).set_color(COLOR_MUTED),
            run_time=1.8,
            rate_func=rate_functions.ease_in_out_sine
        )
        # (Total elapsed: 3.8s)

        # --- BEAT 2: The Card & Payload Question (3.8s - 8.6s) ---
        # Voiceover: "But conversation alone doesn't explain the part that actually matters: what does the card say, exactly?"
        
        card_rect = RoundedRectangle(width=6.2, height=3.9, corner_radius=0.22, color=COLOR_MAIN, stroke_width=3.5)
        
        # Realistic EMV chip element on the card
        chip_body = RoundedRectangle(
            width=0.9, height=0.75, corner_radius=0.08,
            color="#94A3B8", stroke_width=2.0, fill_color="#1E293B", fill_opacity=0.8
        )
        chip_lines = VGroup(
            Line(chip_body.get_left(), chip_body.get_right(), color="#94A3B8", stroke_width=1.5),
            Line(chip_body.get_top(), chip_body.get_bottom(), color="#94A3B8", stroke_width=1.5),
            Line(chip_body.get_left() + UP * 0.2, chip_body.get_right() + UP * 0.2, color="#94A3B8", stroke_width=1.2),
            Line(chip_body.get_left() + DOWN * 0.2, chip_body.get_right() + DOWN * 0.2, color="#94A3B8", stroke_width=1.2)
        )
        chip = VGroup(chip_body, chip_lines).move_to(card_rect.get_corner(UL) + RIGHT * 0.95 + DOWN * 0.95)
        
        # Contactless waves symbol on card corner
        contactless_icon = VGroup(*[
            Arc(radius=r, angle=PI/2, start_angle=-PI/4, color="#94A3B8", stroke_width=2.5)
            for r in [0.15, 0.28, 0.41]
        ]).move_to(card_rect.get_corner(UR) + LEFT * 0.75 + DOWN * 0.75)
        
        card_base = VGroup(card_rect, chip, contactless_icon)
        
        # Question label: "WHAT DOES IT SAY?"
        say_label = Text("WHAT DOES IT SAY?", font=FONT, font_size=26, color=COLOR_MUTED, weight=BOLD)
        say_label.move_to(card_rect.get_center() + DOWN * 0.35)
        
        self.play(FadeIn(card_base, shift=UP * 0.25), Write(say_label), run_time=1.6)
        self.wait(3.2)
        # (Total elapsed: 8.6s)

        # --- BEAT 3: Card Number Revealed (8.6s - 14.2s) ---
        # Voiceover: "Because it's not saying your card number."
        
        # 16-digit placeholder blocks (4 chunks of 4), matching Shot 15's real_number asset
        digit_chunks = VGroup()
        for _ in range(4):
            chunk = VGroup(*[
                RoundedRectangle(width=0.22, height=0.33, corner_radius=0.06, color=COLOR_MAIN, fill_opacity=1)
                for _ in range(4)
            ]).arrange(RIGHT, buff=0.1)
            digit_chunks.add(chunk)
            
        digit_chunks.arrange(RIGHT, buff=0.3).move_to(card_rect.get_center() + DOWN * 0.2)
        
        # Positioned cleanly below card outline to avoid collision with the question mark
        num_label = Text("CARD NUMBER (16 DIGITS)", font=FONT, font_size=22, color=COLOR_MUTED, weight=BOLD)
        num_label.next_to(card_rect, DOWN, buff=0.35)
        
        # Large cliffhanger question mark in Tracr cyan
        question = Text("?", font=FONT, font_size=160, color=COLOR_ACCENT, weight=BOLD)
        question.move_to(digit_chunks.get_center())
        question_bg = Circle(radius=1.1, color=BLACK, fill_opacity=0.9, stroke_width=0).move_to(question)
        question_group = VGroup(question_bg, question)
        
        self.play(
            FadeOut(say_label),
            FadeIn(digit_chunks, shift=UP * 0.15),
            FadeIn(num_label),
            run_time=1.4
        )
        self.play(FadeIn(question_group, scale=0.6), run_time=0.4)
        self.play(
            question.animate.scale(1.15),
            run_time=0.3,
            rate_func=rate_functions.ease_out_back
        )
        self.play(
            question.animate.scale(1/1.15),
            run_time=0.3,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(3.2)
        # (Total elapsed: 14.2s)


        # =====================================================================
        # SHOT 0014: One-Time Code - It Doesn't (14.2s - 22.0s / 188 frames @ 24fps)
        # =====================================================================

        # --- BEAT 4: The Misconception - "Over the air, right? Just without the swipe?" (14.2s - 18.5s) ---
        # Voiceover: "Tapping sends your card number over the air, right? Just without the swipe?"
        
        full_card = VGroup(card_base, num_label)
        
        # 1. Reader terminal on far left (contactless POS terminal styling)
        reader_box = RoundedRectangle(
            width=2.1, height=4.2, corner_radius=0.22,
            color=COLOR_MAIN, stroke_width=3.5,
            fill_color="#0F172A", fill_opacity=0.5
        )
        reader_sensor = Circle(radius=0.65, color=COLOR_ACCENT, stroke_width=2.5)
        reader_sensor_core = Dot(radius=0.1, color=COLOR_ACCENT)
        reader_target = VGroup(reader_sensor, reader_sensor_core).move_to(reader_box.get_center() + UP * 0.55)
        reader_title = Text("READER", font=FONT, font_size=24, color=COLOR_MAIN, weight=BOLD).next_to(reader_target, DOWN, buff=0.6)
        reader_device = VGroup(reader_box, reader_target, reader_title).shift(LEFT * 4.6)
        
        # 2. Myth question headings at top
        air_title = Text("OVER THE AIR?", font=FONT, font_size=32, color=COLOR_ACCENT, weight=BOLD).shift(UP * 2.4)
        swipe_sub = Text("JUST WITHOUT THE SWIPE?", font=FONT, font_size=20, color=COLOR_MUTED, weight=BOLD).next_to(air_title, DOWN, buff=0.18)
        myth_headers = VGroup(air_title, swipe_sub)
        
        # 3. NFC wave arcs radiating through the air gap
        wave_arcs = VGroup(*[
            Arc(radius=r, angle=PI*0.62, start_angle=PI - PI*0.31, color=COLOR_ACCENT, stroke_width=sw, stroke_opacity=op)
            for r, sw, op in [(1.1, 4.0, 0.9), (1.8, 3.2, 0.65), (2.5, 2.5, 0.4), (3.2, 2.0, 0.22)]
        ]).shift(RIGHT * 1.6 + DOWN * 0.2)
        
        # Re-stage scene into Card vs Reader with clear open air gap
        self.play(
            FadeOut(handshake_timeline, run_time=0.4),
            FadeOut(question_group, scale=0.8, run_time=0.4),
            FadeOut(num_label, run_time=0.4),
            full_card.animate.scale(0.70).shift(RIGHT * 4.0),
            FadeIn(reader_device, shift=RIGHT * 0.3),
            FadeIn(myth_headers, shift=DOWN * 0.15),
            run_time=1.0
        )
        
        # The 16 digits lift off and float across the air gap toward the reader
        target_center = LEFT * 0.4 + DOWN * 0.2
        self.play(
            digit_chunks.animate.scale(1.05).move_to(target_center).set_color(COLOR_ACCENT),
            FadeIn(wave_arcs, shift=LEFT * 0.35),
            run_time=1.5,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(1.8)
        # (Total elapsed: 18.5s)

        # --- BEAT 5: The Dramatic Negation - "It doesn't." (18.5s - 20.6s) ---
        # Voiceover: "It doesn't."
        
        # Massive bold "X" stamping over the air transmission
        cross = Text("X", font=FONT, font_size=230, color=COLOR_ACCENT, weight=BOLD)
        cross_bg = Circle(radius=1.35, color=BLACK, fill_opacity=0.94, stroke_color=COLOR_ACCENT, stroke_width=3.5)
        cross_group = VGroup(cross_bg, cross.move_to(cross_bg.get_center())).move_to(target_center)
        
        # Impact shockwave
        shockwave = Circle(radius=0.4, color=COLOR_ACCENT, stroke_width=6).move_to(target_center)
        
        # Verdict text
        verdict = Text("IT DOESN'T.", font=FONT, font_size=32, color=COLOR_ACCENT, weight=BOLD)
        verdict.next_to(cross_group, DOWN, buff=0.42)
        
        # WHAM! The slam
        self.play(
            FadeIn(cross_group, scale=2.2),
            Create(shockwave),
            FadeOut(myth_headers, shift=UP * 0.2),
            # Airborne digits get severed, turn slate gray and drop
            digit_chunks.animate.set_color(COLOR_SLATE).shift(DOWN * 0.45).set_opacity(0.2),
            # Wireless wave arcs fizzle into dead slate and dissipate
            wave_arcs.animate.set_color(COLOR_SLATE).set_stroke(width=1, opacity=0),
            run_time=0.25,
            rate_func=rate_functions.ease_in_expo
        )
        
        # Impact shockwave expands and dissipates, X punches
        self.play(
            shockwave.animate.scale(5.0).set_stroke(width=1, opacity=0),
            cross.animate.scale(1.15),
            FadeIn(verdict, shift=UP * 0.15),
            run_time=0.35,
            rate_func=rate_functions.ease_out_cubic
        )
        self.play(
            cross.animate.scale(1/1.15),
            run_time=0.2,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1.3)
        # (Total elapsed: 20.6s)

        # --- BEAT 6: Hard Cut to Black (20.6s - 22.0s) ---
        # Sharp punctuation beat before Shot 15 starts ("The real number sits locked inside...")
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.1
        )
        self.wait(1.3)
        # (Total elapsed: 22.0s / 528 frames @ 24fps)


HandshakeCliffhanger = Shot013_014_HandshakeCliffhanger
Shot013_HandshakeCliffhanger = Shot013_014_HandshakeCliffhanger
Shot014_OneTimeCodeItDoesnt = Shot013_014_HandshakeCliffhanger
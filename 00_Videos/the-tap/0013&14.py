from manim import *

class HandshakeCliffhanger(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        FONT = "JetBrains Mono"
        
        COLOR_MAIN = WHITE
        COLOR_MUTED = DARK_GRAY
        COLOR_ACCENT = "#00E5FF" # Tracr Cyan

        # =====================================================================
        # SHOT 0013: Handshake Cliffhanger
        # =====================================================================

        # --- BEAT 1: The Handshake Recap & Demotion (0s - 4s) ---
        # Voiceover: "That's the conversation. Short, scripted, computer-fast."
        
        # 1. Create a sleek 2D recap of the 4 pulses from the Blender shot
        reader_node = Text("READER", font=FONT, font_size=24, color=COLOR_MAIN)
        card_node = Text("CARD", font=FONT, font_size=24, color=COLOR_MAIN)
        nodes = VGroup(reader_node, card_node).arrange(RIGHT, buff=4)
        
        # Draw 4 exchange arrows to represent the completed conversation
        arrows = VGroup()
        for i in range(4):
            # Avoid comparing NumPy arrays directly (like direction == RIGHT)
            # Instead, check if the index is even (Reader -> Card) or odd (Card -> Reader)
            if i % 2 == 0:
                start = reader_node.get_right() + RIGHT * 0.2
                end = card_node.get_left() + LEFT * 0.2
            else:
                start = card_node.get_left() + LEFT * 0.2
                end = reader_node.get_right() + RIGHT * 0.2
                
            y_offset = UP * (0.6 - i * 0.4) # Stack them vertically
            
            arrow = Line(start + y_offset, end + y_offset, color=COLOR_MAIN).add_tip(tip_length=0.15)
            arrows.add(arrow)

        handshake_timeline = VGroup(nodes, arrows)
        
        # We cut straight from Blender, so it fades in quickly to establish continuity
        self.play(FadeIn(handshake_timeline), run_time=1)
        self.wait(1)
        
        # "But conversation alone doesn't explain..." -> Demote it
        self.play(
            handshake_timeline.animate.scale(0.5).to_edge(UP, buff=0.5).set_color(COLOR_MUTED),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        # (Total elapsed: 4s)

        # --- BEAT 2: The Card Number (4s - 7s) ---
        # Voiceover: "...what does the card say, exactly? Because it's not saying your card number."
        
        # 1. Create the simplified card icon (Increased size to comfortably fit the digits)
        card = RoundedRectangle(width=6.5, height=4.1, corner_radius=0.2, color=COLOR_MAIN, stroke_width=4)
        
        # 2. Create the 16-digit placeholder blocks (4 chunks of 4, slightly scaled down to fit)
        digit_chunks = VGroup()
        for _ in range(4):
            chunk = VGroup(*[
                RoundedRectangle(width=0.2, height=0.3, corner_radius=0.05, color=COLOR_MAIN, fill_opacity=1)
                for _ in range(4)
            ]).arrange(RIGHT, buff=0.1)
            digit_chunks.add(chunk)
            
        digit_chunks.arrange(RIGHT, buff=0.3).move_to(card.get_center())
        card_icon = VGroup(card, digit_chunks)

        # Fade in the card in the center of the frame
        self.play(FadeIn(card_icon, shift=UP * 0.3), run_time=1.5)
        self.wait(1.5)
        # (Total elapsed: 7s)

        # --- BEAT 3: The Cliffhanger Question Mark (7s - 14s) ---
        
        # Create a massive question mark in the Tracr cyan accent color
        question = Text("?", font=FONT, font_size=180, color=COLOR_ACCENT)
        question.move_to(card_icon.get_center())
        
        # Add a subtle dark background to the question mark so it pops off the white digits
        question_bg = Circle(radius=1.2, color=BLACK, fill_opacity=0.8, stroke_width=0).move_to(question)
        question_group = VGroup(question_bg, question)

        # Pop it in and give it a single, sharp pulse
        self.play(FadeIn(question_group, scale=0.5), run_time=0.4)
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
        
        # Hold on the question mark while VO sets up the trap
        # Voiceover: "Tapping sends your card number over the air, right? Just without the swipe?"
        self.wait(6.0) 
        # (Total elapsed: 14s)


        # =====================================================================
        # SHOT 0014: One-Time Code - It Doesn't
        # =====================================================================
        
        # --- BEAT 4: The Transformation (14s - 16s) ---
        # Voiceover: "It doesn't."
        
        # Create the bold "X"
        cross = Text("X", font=FONT, font_size=240, color=COLOR_ACCENT, weight=BOLD)
        cross.move_to(card_icon.get_center())
        
        # The sharp transformation
        self.play(
            Transform(question, cross),
            question_bg.animate.scale(1.2), # Expand the black background slightly to accommodate the massive X
            run_time=0.2, 
            rate_func=rate_functions.ease_out_expo
        )
        # Give it a tiny, aggressive punch effect
        self.play(
            question.animate.scale(1.15), 
            run_time=0.1
        )
        self.play(
            question.animate.scale(1/1.15), 
            run_time=0.15
        )
        
        # Quick hold to let the "X" burn into their retinas
        # Using exactly 1.55s here to make this beat a perfect 2.0s
        self.wait(1.55)
        
        # --- BEAT 5: The Hard Cut to Black (16s - 20s) ---
        # (A punctuation beat before the next sequence)
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.1 # Very fast fade to mimic a hard cut
        )
        
        # Hold on pure black
        # Using exactly 3.9s here to make this final beat exactly 4.0s
        self.wait(3.9) 
        # (Total elapsed: 20s / 480 frames)
from manim import *

class Shot008_JargonReliefLoadModulation(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        FONT = "JetBrains Mono"
        
        COLOR_MAIN = WHITE
        COLOR_MUTED = "#CBD5E1"  # Crisp light technical slate for mobile readability
        COLOR_ACCENT = "#00E5FF" # Tracr Cyan for the rope jerks

        # --- BEAT 1: Term Display (0s - 3s) ---
        # Voiceover: "That's called load modulation."
        
        # 1. Create the scary jargon term front and center
        jargon_text = Text("Load Modulation", font=FONT, font_size=68, color=COLOR_MAIN, weight=BOLD)
        
        # Write it in confidently
        self.play(Write(jargon_text), run_time=1.5)
        self.wait(1.5) # Let it linger (Total elapsed: 3s)

        # --- BEAT 2: De-emphasis (3s - 5s) ---
        # Voiceover: "Same rule applies: forget the term, keep the picture."
        
        # 2. Visually demote the term (Scale 0.50 & bright slate for phone clarity)
        self.play(
            jargon_text.animate.scale(0.50).to_corner(UL, buff=0.6).set_color(COLOR_MUTED),
            run_time=2
        ) 
        # (Total elapsed: 5s)

        # --- BEAT 3: Metaphor Fade In (5s - 6s) ---
        # Voiceover: "The card isn't shouting."
        
        # Helper function to generate clean, scalable stick figures
        def create_stick_figure(label_str, color=COLOR_MAIN):
            head = Circle(radius=0.32, color=color, stroke_width=4.5)
            body = Line(ORIGIN, DOWN*1.1, color=color, stroke_width=4.5).next_to(head, DOWN, buff=0)
            arms = Line(LEFT*0.65, RIGHT*0.65, color=color, stroke_width=4.5).move_to(body.get_center() + UP*0.2)
            leg_l = Line(body.get_bottom(), body.get_bottom() + DOWN*0.85 + LEFT*0.4, color=color, stroke_width=4.5)
            leg_r = Line(body.get_bottom(), body.get_bottom() + DOWN*0.85 + RIGHT*0.4, color=color, stroke_width=4.5)
            
            person = VGroup(head, body, arms, leg_l, leg_r)
            label = Text(label_str, font=FONT, font_size=32, color=COLOR_MAIN, weight=BOLD)
            label.next_to(person, DOWN, buff=0.45)
            
            # Return the full group, plus a direct reference to the arms for anchoring the rope
            return VGroup(person, label), arms

        # Instantiate the two figures
        reader_group, reader_arms = create_stick_figure("READER")
        card_group, card_arms = create_stick_figure("CARD")
        
        reader_group.shift(LEFT * 3)
        card_group.shift(RIGHT * 3)
        
        # --- THE ROPE MECHANICS ---
        tension = ValueTracker(0.0) # 0.0 = Drooping/Relaxed, 1.0 = Pulled Taut
        
        def update_rope():
            start = reader_arms.get_right()
            end = card_arms.get_left()
            t = tension.get_value()
            
            # When tension is 0, it droops down by 0.8 units. When tension is 1, droop is 0.
            droop = 0.8 * (1 - t) 
            
            # Create a smooth, dynamic bezier curve that straightens out
            mid = (start + end) / 2 + DOWN * droop
            rope = VMobject()
            rope.set_points_as_corners([start, mid, end])
            rope.make_smooth()
            
            # Flash cyan when pulled tight
            if t > 0.5:
                rope.set_color(COLOR_ACCENT)
                rope.set_stroke(width=5.5 + 2.5*t) # Gets thicker when snapped
            else:
                rope.set_color(COLOR_MAIN)
                rope.set_stroke(width=4.5)
                
            return rope
            
        rope = always_redraw(update_rope)

        # Fade them in
        self.play(
            FadeIn(reader_group, shift=UP*0.2), 
            FadeIn(card_group, shift=UP*0.2),
            Create(rope),
            run_time=1
        )
        # (Total elapsed: 6s)

        # --- BEAT 4: The Tugging Pattern (6s - 12s) ---
        # Voiceover: "It's tugging on a rope the reader's already holding, in a pattern."
        
        def tug_rope():
            # Snap back
            self.play(
                card_group.animate.shift(RIGHT * 0.4),
                tension.animate.set_value(1.0),
                run_time=0.15,
                rate_func=rate_functions.ease_out_sine
            )
            # Hold the tension
            self.wait(0.1)
            # Relax forward
            self.play(
                card_group.animate.shift(LEFT * 0.4),
                tension.animate.set_value(0.0),
                run_time=0.15,
                rate_func=rate_functions.ease_in_sine
            )
            
        self.wait(0.5) # (Total elapsed: 6.5s)
        
        # Animate a rhythmic pattern (Tug ... Tug, Tug ... Tug)
        tug_rope()      # (6.9s)
        self.wait(0.4)  # (7.3s)
        
        tug_rope()      # (7.7s)
        self.wait(0.1)  # (7.8s)
        tug_rope()      # (8.2s)
        
        self.wait(0.6)  # (8.8s)
        
        tug_rope()      # (9.2s)
        
        # Hold for the final beats to reach exactly 12 seconds (288 frames)
        self.wait(2.8)


JargonReliefLoadModulation = Shot008_JargonReliefLoadModulation
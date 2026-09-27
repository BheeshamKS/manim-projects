from manim import *

class TokenSegmentation(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = "#000000"
         
        # Colorblind-safe palette (6 distinct colors)
        cb_colors = ["#4477AA", "#EE6677", "#228833", "#AA3377", "#66CCEE", "#BBBBBB"]
        token_ids = ["8144", "264", "33894", "922", "51692", "13"]

        # --- 1. Constructing the Prompt Text ---
        # By writing it as one single continuous string, we fix ALL kerning and alignment issues.
        # The font renderer places everything perfectly.
        full_text = "Write_a_poem_about_silicon."
        
        prompt_text = Text(full_text, font="Monospace", color=WHITE)
        prompt_text.move_to(UP * 0.5)

        # --- 2. Defining Token Slices ---
        # Text() mobjects are basically lists of individual character mobjects. 
        # We slice them to grab exactly the characters belonging to each token.
        token_slices = [
            prompt_text[0:5],   # Write
            prompt_text[5:7],   # _a
            prompt_text[7:12],  # _poem
            prompt_text[12:18], # _about
            prompt_text[18:26], # _silicon
            prompt_text[26:27]  # .
        ]

        # --- 3. Constructing Brackets and IDs ---
        brackets = VGroup()
        id_labels = VGroup()
        
        for t_mob, color, t_id in zip(token_slices, cb_colors, token_ids):
            # Brace maps exactly to the native width of the characters
            bracket = Brace(t_mob, direction=DOWN, buff=0.1)
            bracket.set_color(color)
            brackets.add(bracket)
            
            # Create MathTex IDs and center them below their respective bracket
            label = MathTex(t_id).scale(0.8)
            label.set_color(color)
            label.next_to(bracket, DOWN, buff=0.2)
            id_labels.add(label)

        # =========================================
        # --- Master Timeline (18.5s Total) -------
        # =========================================
        target_duration = 18.5
        elapsed_time = 0.0

        # A. The full prompt appears on screen (1.5s)
        self.play(FadeIn(prompt_text, shift=UP*0.2), run_time=1.5)
        self.wait(1.0)
        elapsed_time += 2.5

        # B. Color-coded brackets grow from center sequentially
        for bracket in brackets:
            self.play(GrowFromCenter(bracket), run_time=0.2)
            elapsed_time += 0.2
            
        self.wait(1.0) # Hold before IDs appear
        elapsed_time += 1.0

        # C. Token IDs fade in sequentially with 0.15s delay between each
        for i, label in enumerate(id_labels):
            self.play(FadeIn(label, shift=UP*0.1), run_time=0.2)
            elapsed_time += 0.2
            
            # 0.15s delay applied between the end of one fade and the start of the next
            if i < len(id_labels) - 1:
                self.wait(0.15)
                elapsed_time += 0.15
                
        self.wait(2.0) # Tension hold before the pulse
        elapsed_time += 2.0

        # D. "silicon" flashes and its ID pulses (1.5s)
        # token_slices[4] and id_labels[4] correspond to the 5th token ("_silicon")
        self.play(
            Indicate(token_slices[4], color=YELLOW),
            Indicate(id_labels[4], color=YELLOW, scale_factor=1.3),
            run_time=1.5
        )
        elapsed_time += 1.5

        # E. Final Hold
        # Subtract the elapsed animations from the 18.5s target to get our remaining wait time
        remaining_time = target_duration - elapsed_time
        self.wait(max(0, remaining_time)) 
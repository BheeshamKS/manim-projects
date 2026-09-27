from manim import *
import numpy as np

class NoAntenna(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        FONT = "JetBrains Mono"
        
        COLOR_MAIN = WHITE
        COLOR_MUTED = DARK_GRAY  # Deep gray for the dissolved/failed state
        
        # --- BEAT 1: Establish the Diagram (0s - 4s) ---
        # Voiceover: "Now the card's awake. But it has no antenna broadcasting outward..."
        
        # 1. The Reader (Left side)
        reader_box = Rectangle(width=1.5, height=5, color=COLOR_MAIN, stroke_width=4)
        reader_text = Text("READER", font=FONT, font_size=24, color=COLOR_MAIN).rotate(PI/2)
        reader = VGroup(reader_box, reader_text).shift(LEFT * 5)
        
        # 2. The Card & Coil (Right side, simplified from shot 0003)
        card_outline = RoundedRectangle(width=4, height=2.5, corner_radius=0.15, color=COLOR_MAIN, stroke_width=4)
        static_coil = VGroup(*[
            RoundedRectangle(width=w, height=h, corner_radius=0.1, color=COLOR_MUTED, stroke_width=2)
            for w, h in zip(np.arange(3.0, 3.8, 0.3), np.arange(1.5, 2.3, 0.3))
        ])
        card = VGroup(card_outline, static_coil).shift(RIGHT * 3.5)
        
        # Fade them in statically
        self.play(FadeIn(reader), FadeIn(card), run_time=1.5)
        self.wait(2.5) # (Total elapsed: 4s)

        # --- BEAT 2: The Fizzling Arrow Gag (4s - 8s) ---
        # Voiceover: "...no way to transmit a signal of its own."
        
        # We use a DashedLine with a tip to look like an outgoing wireless signal
        # It intentionally falls short of the reader to sell the "failure"
        signal_arrow = DashedLine(
            start=card.get_left() + LEFT * 0.2,
            end=card.get_left() + LEFT * 4.5, # Stops before hitting the reader
            color=COLOR_MAIN,
            stroke_width=6,
            dashed_ratio=0.6
        ).add_tip(tip_length=0.3)
        
        # 1. The attempt: It shoots out confidently
        self.play(Create(signal_arrow), run_time=1, rate_func=rate_functions.ease_out_sine)
        
        # 2. The struggle: It hesitates and wiggles slightly
        self.play(Wiggle(signal_arrow, rotation_angle=0.03, scale_value=1.05), run_time=1)
        
        # 3. The fizzle: Color drains to gray, it sags downward, and dissolves away
        self.play(
            signal_arrow.animate.set_color(COLOR_MUTED).set_opacity(0).shift(DOWN * 0.8),
            run_time=2,
            rate_func=rate_functions.ease_in_sine
        )
        # (Total elapsed: 8s)

        # --- BEAT 3: The Question Hold (8s - 11s) ---
        # Voiceover: "So how does it talk back?"
        
        # Crisp, simple question mark centered above the card
        question_mark = Text("?", font=FONT, font_size=72, color=COLOR_MAIN)
        question_mark.next_to(card, UP, buff=0.6)
        
        # Pops in gently
        self.play(FadeIn(question_mark, shift=UP * 0.3), run_time=1)
        
        # Hold for the final beats
        self.wait(2) # (Total elapsed: 11s / 264 frames)
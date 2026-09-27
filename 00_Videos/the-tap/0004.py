from manim import *

class JargonRelief(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        FONT = "JetBrains Mono"
        
        COLOR_MAIN = WHITE
        COLOR_MUTED = GRAY       # A soft gray to keep the captions subdued
        COLOR_ACCENT = "#00E5FF" # Tracr Cyan, matching the previous shot

        # --- BEAT 1: Term Display (0s - 3s) ---
        
        # 1. Create the scary jargon term front and center
        jargon_text = Text("Inductive Coupling", font=FONT, font_size=64, color=COLOR_MAIN)
        
        # Write it in confidently
        self.play(Write(jargon_text), run_time=1.5)
        self.wait(1.5) # Let it linger just long enough to read (Total elapsed: 3s)

        # --- BEAT 2: De-emphasis (3s - 5s) ---
        
        # 2. Visually demote the term (The Jargon Relief move)
        # We shrink it, turn it a muted color, and shove it out of the way to the top left
        self.play(
            jargon_text.animate.scale(0.35).to_corner(UL).set_color(COLOR_MUTED),
            run_time=2
        ) 
        # (Total elapsed: 5s)

        # --- BEAT 3: Icons and Captions (5s - 9s) ---
        
        # 1. Create two simplified coil icons (just 3 concentric circles each)
        left_coil = VGroup(*[Circle(radius=r, color=COLOR_MAIN, stroke_width=3) for r in [0.3, 0.5, 0.7]])
        right_coil = VGroup(*[Circle(radius=r, color=COLOR_MAIN, stroke_width=3) for r in [0.3, 0.5, 0.7]])
        
        left_coil.shift(LEFT * 3)
        right_coil.shift(RIGHT * 3)
        
        # 2. Create the simplified captions beneath them
        left_caption = Text("makes a field", font=FONT, font_size=24, color=COLOR_MUTED)
        left_caption.next_to(left_coil, DOWN, buff=0.75)
        
        right_caption = Text("steals a sliver of it", font=FONT, font_size=24, color=COLOR_MUTED)
        right_caption.next_to(right_coil, DOWN, buff=0.75)
        
        # Animate them in
        self.play(FadeIn(left_coil), FadeIn(right_coil), run_time=1)
        self.play(Write(left_caption), Write(right_caption), run_time=1)
        self.wait(2) # (Total elapsed: 9s)

        # --- BEAT 4: Transfer Animation (9s - 13s) ---
        
        # 1. Draw the energy-transfer arrow connecting the two coils
        transfer_arrow = CurvedArrow(
            left_coil.get_right() + RIGHT * 0.2, 
            right_coil.get_left() + LEFT * 0.2, 
            angle=-PI/3, 
            color=COLOR_ACCENT,
            stroke_width=4
        )
        self.play(Create(transfer_arrow), run_time=1)
        
        # 2. Animate a "pulse" of energy travelling along the arrow
        pulse = Dot(color=WHITE, radius=0.08)
        self.play(MoveAlongPath(pulse, transfer_arrow), run_time=1, rate_func=linear)
        self.play(FadeOut(pulse, run_time=0.1))
        
        # 3. Loop the pulse one more time for emphasis
        pulse2 = Dot(color=WHITE, radius=0.08)
        self.play(MoveAlongPath(pulse2, transfer_arrow), run_time=1, rate_func=linear)
        self.play(FadeOut(pulse2, run_time=0.1))
        
        self.wait(0.8) # (Total elapsed: 13s / ~312 frames)
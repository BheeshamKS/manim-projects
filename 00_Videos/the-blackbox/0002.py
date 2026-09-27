from manim import *

class PromptBlackBox(Scene):
    def construct(self):
        # --- Configuration ---
        config.background_color = "#000000" 
        fps = config.frame_rate 

        # --- Text Setup ---
        prompt_text = Text(
            "Write a poem about silicon",
            font="Monospace", 
            color=WHITE,
            stroke_width=0 
        )
        prompt_text.move_to(ORIGIN)

        # --- Black Box Setup (Visible Version) ---
        # Dark grey fill and stroke so it physically stands out against the black background
        black_box = Rectangle(
            width=prompt_text.width + 1.0, 
            height=prompt_text.height + 0.6,
            fill_color="#1A1A1A",     
            fill_opacity=0.90,        # Obscures text heavily but leaves it faintly visible
            stroke_color="#333333",   
            stroke_width=4
        )
        black_box.move_to(prompt_text)

        # =========================================
        # --- Timing Logic (Strictly 15 Seconds) --
        # =========================================
        typewriter_time = 6.0
        slam_time = 0.3
        tension_hold = 2.0
        final_hold = 48 / fps # Dynamically calculates 48 frames into seconds
        
        # Calculates the exact padding needed before the slam to hit 15.0s total
        wait_before_slam = 15.0 - (typewriter_time + slam_time + tension_hold + final_hold)

        # =========================================
        # --- Animation Sequence ---
        # =========================================

        # 1. Typewriter reveal 
        self.play(Write(prompt_text), run_time=typewriter_time, rate_func=linear)
        
        # 2. Wait for the precise voiceover cue
        self.wait(max(0, wait_before_slam))

        # 3. Rectangle Slam (FadeIn with UP shift, 0.3s)
        self.play(
            FadeIn(black_box, shift=UP),
            run_time=slam_time,
            rate_func=rate_functions.ease_out_sine
        )

        # 4. Tension hold for 2 seconds
        self.wait(tension_hold)

        # 5. Final Frame Hold (48 frames) before cut
        self.wait(final_hold)
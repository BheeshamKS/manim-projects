from manim import *

# Target: exactly 10.0 seconds @ 24 FPS (240 frames)

class SyscallScene(Scene):
    def construct(self):
        
        # --------------------------------------------------
        # tracr Boilerplate & Styling
        # --------------------------------------------------
        
        BG = "#000000"
        WHITE = "#E8F1FF"
        MUTED = "#7C8DA6"
        GREEN = "#4DDD70"
        MONO = "JetBrains Mono"

        self.camera.background_color = BG 

        # --------------------------------------------------
        # Static Layout Construction
        # --------------------------------------------------
        
        title = Text("SYSCALL", font=MONO, font_size=72, color=WHITE)
        
        subtitle = Text("a message from a program to the operating system", font=MONO, font_size=28, color=MUTED)
        
        punchline = Text("Python says: you finish it.", font=MONO, font_size=22, color=GREEN)

        # Arrange them vertically, centered on screen
        text_group = VGroup(title, subtitle, punchline).arrange(DOWN, buff=0.5)
        text_group.move_to(ORIGIN)

        # --------------------------------------------------
        # Animation Timeline (Total: 10.0s)
        # --------------------------------------------------

        # 1. Initial hold while voiceover starts: "If you want to sound smart at lunch..."
        self.wait(3.5)

        # 2. Write Title (1.0s) + Stagger (0.3s)
        self.play(Write(title), run_time=1.0)
        self.wait(0.3)

        # 3. Write Subtitle (1.0s) + Stagger (0.3s)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(0.3)

        # 4. Write Punchline (1.0s)
        self.play(Write(punchline), run_time=1.0)

        # 5. Hold on screen after all text has appeared
        self.wait(1.5)

        # 6. Fade to black transition 
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(punchline),
            run_time=1.4
        )

        # --------------------------------------------------
        # Total duration breakdown:
        # Initial wait: 3.5s
        # Title write: 1.0s
        # Pause: 0.3s
        # Subtitle write: 1.0s
        # Pause: 0.3s
        # Punchline write: 1.0s
        # Hold: 1.5s
        # Fade out: 1.4s
        # = 10.0 seconds exactly (240 frames @ 24 FPS)
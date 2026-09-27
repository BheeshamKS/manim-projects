from manim import *
import numpy as np

# --- GLOBAL CONFIGURATION & STYLES ---
FONT = "JetBrains Mono"
COLOR_MAIN = WHITE
COLOR_MUTED = DARK_GRAY
COLOR_ACCENT = "#00E5FF" # Tracr Cyan


class Shot015_TheVault(Scene):
    def construct(self):
        # =====================================================================
        # SHOT 0015: The Vault and The Substitute Number (15 Seconds / 360 Frames)
        # =====================================================================

        # --- BEAT 1: The Vault Seal (0s - 5s) ---
        # Voiceover: "The real number sits locked inside the chip and never leaves."
        
        # 1. Recreate the Real Number (carrying over its exact size/position from Shot 14)
        real_number = VGroup()
        for _ in range(4):
            chunk = VGroup(*[
                RoundedRectangle(width=0.2, height=0.3, corner_radius=0.05, color=COLOR_MAIN, fill_opacity=1)
                for _ in range(4)
            ]).arrange(RIGHT, buff=0.1)
            real_number.add(chunk)
        real_number.arrange(RIGHT, buff=0.3)

        # Starts perfectly centered
        self.play(FadeIn(real_number), run_time=1)
        self.wait(1)

        # 2. Create the Vault (Properly scaled up on the left side)
        vault_box = RoundedRectangle(width=4.0, height=3.5, corner_radius=0.2, color=COLOR_MAIN, stroke_width=4)
        vault_inner = RoundedRectangle(width=3.6, height=3.1, corner_radius=0.1, color=COLOR_MUTED, stroke_width=2)
        vault_open = VGroup(vault_box, vault_inner).shift(LEFT * 3.5)

        self.play(FadeIn(vault_open), run_time=1)
        
        # 3. Slide real number into the vault and scale it down so it physically fits inside
        self.play(
            real_number.animate.move_to(vault_open.get_center()).scale(0.45),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # 4. "Seal" the vault with a heavy door and padlock
        vault_door = RoundedRectangle(width=3.8, height=3.3, corner_radius=0.15, color=BLACK, fill_opacity=1, stroke_color=COLOR_MAIN, stroke_width=4)
        vault_door.move_to(vault_open)
        
        # Add a combination dial to sell the "safe" aesthetic
        dial_outer = Circle(radius=0.6, color=COLOR_MAIN, stroke_width=4).move_to(vault_door)
        dial_inner = Circle(radius=0.4, color=COLOR_MAIN, stroke_width=2).move_to(vault_door)
        dial_ticks = VGroup(*[
            Line(UP*0.4, UP*0.6, color=COLOR_MAIN, stroke_width=2).rotate(i * PI/4) 
            for i in range(8)
        ]).move_to(vault_door)
        door_group = VGroup(vault_door, dial_outer, dial_inner, dial_ticks)
        
        # Lock Graphic
        lock_body = RoundedRectangle(width=0.6, height=0.5, corner_radius=0.1, color=COLOR_MAIN, fill_opacity=1)
        lock_shackle = Arc(radius=0.2, angle=PI, color=COLOR_MAIN, stroke_width=6).next_to(lock_body, UP, buff=0)
        padlock = VGroup(lock_body, lock_shackle).next_to(vault_open, UP, buff=0.2)
        
        self.play(
            FadeIn(door_group),
            FadeIn(padlock, shift=DOWN*0.5),
            run_time=0.5
        )
        # (Total elapsed: 5s)

        # --- BEAT 2: The Substitute Number (5s - 9s) ---
        # Voiceover: "In its place, the card sends a substitute number..."
        
        # Create visually distinct substitute number (Dashed outlines, not filled)
        substitute_number = VGroup()
        for _ in range(4):
            chunk = VGroup(*[
                DashedVMobject(
                    RoundedRectangle(width=0.2, height=0.3, corner_radius=0.05, color=COLOR_MAIN, stroke_width=3, fill_opacity=0),
                    num_dashes=8
                )
                for _ in range(4)
            ]).arrange(RIGHT, buff=0.1)
            substitute_number.add(chunk)
            
        # Position cleanly on the right half of the screen
        substitute_number.arrange(RIGHT, buff=0.3).shift(RIGHT * 3.5 + UP * 1.0)
        substitute_number.scale(0.8) # Scaled down slightly to balance with the vault

        self.play(FadeIn(substitute_number, shift=UP * 0.3), run_time=1.5)
        self.wait(2.5)
        # (Total elapsed: 9s)

        # --- BEAT 3: The One-Time Code Stamp (9s - 13s) ---
        # Voiceover: "...and something new alongside it: a one-time code, generated fresh, for this tap..."
        
        # Stamp graphic
        stamp_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.15, color=COLOR_ACCENT, stroke_width=6)
        stamp_text = Text("OTC", font=FONT, font_size=36, color=COLOR_ACCENT, weight=BOLD)
        stamp_glyph = VGroup(stamp_box, stamp_text.move_to(stamp_box.get_center()))
        stamp_glyph.next_to(substitute_number, DOWN, buff=1.0)

        # The aggressive "thunk" stamp animation
        self.play(
            FadeIn(stamp_glyph, scale=3.0),
            run_time=0.4,
            rate_func=rate_functions.ease_in_expo
        )
        # Flash / Impact ripple
        impact = stamp_box.copy().set_stroke(width=2)
        self.play(
            impact.animate.scale(1.5).set_opacity(0),
            stamp_glyph.animate.set_color(COLOR_MAIN), # Cools off to white after impact
            run_time=0.6
        )
        
        self.wait(3.0)
        # (Total elapsed: 13s)

        # --- BEAT 4: The Hold (13s - 15s) ---
        # Voiceover: "...and this tap only."
        self.wait(2.0)
        # (Total elapsed: 15s / 360 frames)
from manim import *
import numpy as np

class Shot005_PowerBudget(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        FONT = "JetBrains Mono"
        
        COLOR_MAIN = WHITE
        COLOR_MUTED = "#CBD5E1"  # Crisp light technical slate for mobile readability
        COLOR_FIELD = "#0284C7"  # Electric cyan-blue for incoming field lines
        COLOR_ACCENT = "#00E5FF" # Tracr Cyan
        COLOR_STRIKE = "#FF3366" # Punchy red for the "no battery" slash

        # --- BEAT 1: The Centered Schematic Setup (0s - 1.5s) ---
        # Voiceover: "That current is the card's entire power budget."

        # Centered, detailed chip
        chip_outline = RoundedRectangle(width=2.5, height=2.5, corner_radius=0.2, color=COLOR_MAIN, stroke_width=4)
        chip_core = RoundedRectangle(width=1.2, height=1.2, corner_radius=0.1, color="#94A3B8", stroke_width=3)
        
        # Draw sleek circuit traces radiating from the core to the edges
        traces = VGroup(
            Line(chip_core.get_top(), chip_outline.get_top(), color="#64748B", stroke_width=2.5),
            Line(chip_core.get_bottom(), chip_outline.get_bottom(), color="#64748B", stroke_width=2.5),
            Line(chip_core.get_left(), chip_outline.get_left(), color="#64748B", stroke_width=2.5),
            Line(chip_core.get_right(), chip_outline.get_right(), color="#64748B", stroke_width=2.5)
        )
        chip = VGroup(chip_outline, chip_core, traces)
        
        self.play(Create(chip), run_time=1.5)

        # --- BEAT 2: Not Stored. Not Charged. (1.5s - 3.5s) ---
        # Voiceover: "Not stored. Not charged."

        # Create a sleek "Stored Power" HUD element above the chip
        battery_body = RoundedRectangle(width=1.1, height=0.55, corner_radius=0.1, color=COLOR_MAIN, stroke_width=3.5)
        battery_tip = Rectangle(width=0.14, height=0.22, color=COLOR_MAIN).next_to(battery_body, RIGHT, buff=0)
        battery = VGroup(battery_body, battery_tip)
        
        status_text = Text("STORED POWER", font=FONT, font_size=30, color=COLOR_MAIN, weight=BOLD)
        
        battery_group = VGroup(battery, status_text).arrange(DOWN, buff=0.25)
        battery_group.next_to(chip, UP, buff=0.7)

        # Bring it in
        self.play(FadeIn(battery_group, shift=UP*0.4), run_time=0.5)
        
        # The "No Power" strike
        strike = Line(battery_group.get_corner(DL) + DL*0.2, battery_group.get_corner(UR) + UR*0.2, color=COLOR_STRIKE, stroke_width=7)
        self.play(Create(strike), run_time=0.4)
        self.wait(0.4)
        
        # Quickly fade out the entire concept of stored power
        self.play(
            battery_group.animate.set_opacity(0),
            strike.animate.set_opacity(0),
            run_time=0.5
        )

        # --- BEAT 3: The Borrowed Wave & Glow (3.5s - 9s) ---
        # Voiceover: "Borrowed, for the length of the tap, and nothing more."

        # Visually represent the "borrowed" energy hitting the chip from the side
        field_lines = VGroup(*[
            Arc(radius=r, angle=PI/2, start_angle=-PI/4, color=COLOR_FIELD, stroke_width=5)
            for r in np.arange(1.5, 4.5, 0.6)
        ]).shift(LEFT * 4)

        # Create the active cyan glow for the chip
        glow_core = chip_core.copy().set_color(COLOR_ACCENT).set_stroke(width=6)
        glow_outline = chip_outline.copy().set_color(COLOR_ACCENT).set_stroke(width=6)
        glow_group = VGroup(glow_core, glow_outline)
        
        # The label - boosted for phone clarity with cyan accent on "borrowed"
        label = Text("borrowed, not stored", font=FONT, font_size=36, color=COLOR_MAIN, weight=BOLD, t2c={"borrowed": COLOR_ACCENT})
        label.next_to(chip, DOWN, buff=0.75)

        # Animate the field sliding in, striking the chip, and igniting the glow
        self.play(
            FadeIn(field_lines, shift=RIGHT),
            FadeIn(glow_group),
            Write(label),
            run_time=1.2
        )

        # Add updaters to keep the scene dynamically pulsating until the cut
        def pulse_glow(mob, dt):
            mob.time += dt
            # Sine wave oscillating the chip's glow opacity
            mob.set_stroke(opacity=0.5 + 0.5 * np.sin(5 * mob.time))
            
        glow_core.time = 0
        glow_outline.time = 0
        glow_core.add_updater(pulse_glow)
        glow_outline.add_updater(pulse_glow)

        def update_field(mob, dt):
            mob.time += dt
            for i, arc in enumerate(mob):
                # Oscillating the incoming magnetic field lines
                opacity = 0.35 + 0.35 * np.sin(4 * mob.time - i)
                arc.set_stroke(opacity=opacity)
                
        field_lines.time = 0
        field_lines.add_updater(update_field)

        # Hold for the remainder of the exactly 9 seconds (216 frames)
        self.wait(4.5)


PowerBudget = Shot005_PowerBudget
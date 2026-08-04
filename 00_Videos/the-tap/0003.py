from manim import *
import numpy as np

class InductiveCoupling(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        # Note: Ensure you have "JetBrains Mono" installed on your system. 
        # If Manim can't find it, it will default to a standard sans-serif.
        FONT = "JetBrains Mono"
        
        COLOR_WHITE = WHITE
        COLOR_MUTED = BLUE_E  # Deep, muted blue for the magnetic field
        COLOR_ACCENT = "#00E5FF" # Tracr's technical cyan/teal accent

        # --- BEAT 1: Reader & Field Establish (0s - 4s) ---
        
        # 1. Create the Reader
        reader_box = Rectangle(width=1.5, height=5, color=COLOR_WHITE, stroke_width=4)
        reader_text = Text("READER", font=FONT, font_size=24, color=COLOR_WHITE).rotate(PI/2)
        reader = VGroup(reader_box, reader_text).shift(LEFT * 5)
        
        self.play(FadeIn(reader), run_time=1)

        # 2. Create the Oscillating Magnetic Field
        # We create concentric arcs that pulse in opacity to simulate an invisible, oscillating wave
        arcs = VGroup(*[
            Arc(radius=r, angle=PI, start_angle=-PI/2, color=COLOR_MUTED, stroke_width=6)
            for r in np.arange(1, 8, 1)
        ]).shift(LEFT * 4.25) # Position at the right edge of the reader box

        # Custom updater to make the field pulse smoothly over time
        def update_field(mob, dt):
            mob.time += dt
            for i, arc in enumerate(mob):
                # Sine wave function to pulse opacity based on time and distance (i)
                opacity = 0.15 + 0.15 * np.sin(4 * mob.time - i)
                arc.set_stroke(opacity=opacity)

        arcs.time = 0
        arcs.add_updater(update_field)

        self.play(FadeIn(arcs), run_time=1)
        self.wait(2) # Hold to establish the oscillation (Total elapsed: 4s)

        # --- BEAT 2: Label Writes In (4s - 7s) ---
        
        freq_label = Text("13.56 MHz", font=FONT, font_size=24, color=COLOR_WHITE)
        freq_label.next_to(reader, DOWN, buff=0.5)
        
        self.play(Write(freq_label), run_time=1)
        self.wait(2) # (Total elapsed: 7s)

        # --- BEAT 3: Card Enters & Coil Activates (7s - 13s) ---
        
        # 1. Create the Card and static Coil
        card_outline = RoundedRectangle(width=4, height=2.5, corner_radius=0.15, color=COLOR_WHITE, stroke_width=4)
        
        # Create a 3-loop coil inside the card using slightly smaller rounded rectangles
        static_coil = VGroup(*[
            RoundedRectangle(width=w, height=h, corner_radius=0.1, color=DARK_GRAY, stroke_width=2)
            for w, h in zip(np.arange(3.0, 3.8, 0.3), np.arange(1.5, 2.3, 0.3))
        ])
        
        card = VGroup(card_outline, static_coil).shift(RIGHT * 8) # Start completely off-screen right
        
        # Animate the card sliding into the field
        # It lands exactly in the middle of the pulsating arcs
        self.play(card.animate.shift(LEFT * 5.5), run_time=3) 

        # 2. Induce Current (The "Aha" Moment)
        # Highlight the coil to the Cyan accent color
        self.play(static_coil.animate.set_color(COLOR_ACCENT).set_stroke(width=3), run_time=1)

        # 3. Create the Current Flow Indicator (Moving electrons/pulses)
        # We use a path exactly on the inner coil and animate dots moving along it
        current_path = RoundedRectangle(width=3.0, height=1.5, corner_radius=0.1).move_to(card.get_center())
        current_pulses = VGroup(*[Dot(color=COLOR_ACCENT, radius=0.06) for _ in range(6)])

        # Updater to move the dots seamlessly around the loop
        def create_pulse_updater(offset):
            def updater(mob, dt):
                t = (mob.time + offset) % 1.0 # Keep t between 0 and 1
                mob.move_to(current_path.point_from_proportion(t))
                mob.time += dt * 0.4 # Speed of the current
            return updater

        for i, pulse in enumerate(current_pulses):
            pulse.time = 0
            pulse.add_updater(create_pulse_updater(i / len(current_pulses)))

        self.play(FadeIn(current_pulses), run_time=1)
        self.wait(1) # (Total elapsed: 13s)

        # --- BEAT 4: The Hold (13s - 19s) ---
        
        # The updaters for the field oscillation and the current flow will continue running automatically.
        # We just hold the scene for the final 6 seconds to let the voiceover finish.
        self.wait(6) # (Total elapsed: 19s / ~456 frames) 
from manim import *
import numpy as np

class Shot007_LoadModulation(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        FONT = "JetBrains Mono"
        
        COLOR_MAIN = WHITE
        COLOR_MUTED = "#CBD5E1"   # Crisp light technical slate for mobile readability
        COLOR_FIELD = "#0284C7"   # Bright electric cyan-blue for field lines
        COLOR_ACCENT = "#00E5FF"  # Tracr Cyan for the data/ripple

        # --- BEAT 1: The Setup (0s - 5s) ---
        # Voiceover: "It doesn't send anything. It changes something."
        
        # 1. Reader & Label (Scaled and spaced cleanly for phone)
        reader_box = Rectangle(width=1.1, height=3.6, color=COLOR_MAIN, stroke_width=4)
        reader_text = Text("READER", font=FONT, font_size=28, color=COLOR_MAIN, weight=BOLD).rotate(PI/2)
        reader = VGroup(reader_box, reader_text).shift(LEFT * 5 + UP * 1.2)
        
        freq_label = Text("13.56 MHz", font=FONT, font_size=24, color=COLOR_ACCENT, weight=BOLD)
        freq_label.next_to(reader, DOWN, buff=0.3)

        # 2. Card & Coil
        card_outline = RoundedRectangle(width=3.2, height=2.0, corner_radius=0.15, color=COLOR_MAIN, stroke_width=4)
        static_coil = VGroup(*[
            RoundedRectangle(width=w, height=h, corner_radius=0.1, color="#94A3B8", stroke_width=2.5)
            for w, h in zip(np.arange(2.2, 3.1, 0.3), np.arange(1.0, 1.9, 0.3))
        ])
        card = VGroup(card_outline, static_coil).shift(RIGHT * 4.2 + UP * 1.2)

        # 3. Oscilloscope / Waveform Readout (Optimized thickness and labels for phone)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1, 1, 0.5],
            x_length=10.0, 
            y_length=1.3,
            axis_config={"color": "#64748B", "stroke_width": 2.5},
            tips=False
        ).shift(DOWN * 2.4)
        
        readout_label = Text("READER FIELD SENSOR", font=FONT, font_size=26, color=COLOR_MAIN, weight=BOLD)
        readout_label.next_to(axes, DOWN, buff=0.35)

        # 4. The Magnetic Field Arcs
        arcs = VGroup(*[
            Arc(radius=r, angle=PI, start_angle=-PI/2, color=COLOR_FIELD, stroke_width=6)
            for r in np.arange(1, 9.0, 1)
        ]).move_to(reader.get_right(), aligned_edge=LEFT)

        # Draw static elements instantly (since we cut from shot 0006)
        self.add(reader, freq_label, card, axes, readout_label)

        # --- THE MATHEMATICS OF THE RIPPLE ---
        time_tracker = ValueTracker(0)

        # This function acts as the "Load State" of the card.
        def envelope(t):
            if t < 5.0:
                return 1.0
            
            # Simple binary pulse pattern (simulating digital data transmission)
            bit_idx = int(t * 4)
            bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]
            if bits[bit_idx % len(bits)] == 1:
                return 0.35 # The card pulls power, dropping the amplitude (The Ripple!)
            return 1.0

        # --- UPDATERS (The Engine) ---

        # 1. Waveform Trace Updater (Thicker stroke for crisp mobile view)
        trace = always_redraw(lambda: axes.plot(
            lambda x: envelope(time_tracker.get_value() - (10 - x)) * 0.6 * np.sin(20 * (time_tracker.get_value() - (10 - x))),
            color=COLOR_ACCENT,
            stroke_width=3.5
        ))
        
        self.play(FadeIn(arcs), Create(trace), run_time=1)

        # 2. Card Coil Updater (Flashes cyan EXACTLY when load is pulled)
        def coil_updater(mob):
            env = envelope(time_tracker.get_value())
            if env < 1.0: # If amplitude drops, the card is actively pulling load
                mob.set_color(COLOR_ACCENT).set_stroke(width=3.5, opacity=1.0)
            else:
                mob.set_color("#94A3B8").set_stroke(width=2.5, opacity=0.7)
        
        static_coil.add_updater(coil_updater)

        # 3. Field Arcs Updater (Distorts the outer field EXACTLY when load is pulled)
        def arcs_updater(mob):
            t = time_tracker.get_value()
            env = envelope(t)
            for i, arc in enumerate(mob):
                base_opacity = 0.28 + 0.22 * np.sin(4 * t - i)
                
                # If we are modulating and this is an outer arc (near the card)
                if i >= 4 and env < 1.0:
                    # The distortion / ripple effect in the air
                    arc.set_stroke(color=COLOR_ACCENT, opacity=base_opacity + 0.45, width=7)
                else:
                    # Clean oscillation
                    arc.set_stroke(color=COLOR_FIELD, opacity=base_opacity, width=5)
                    
        arcs.add_updater(arcs_updater)

        # --- ANIMATION TIMELINE ---
        
        # BEAT 1: Clean State (1s to 5s)
        self.play(time_tracker.animate.set_value(5.0), run_time=4, rate_func=linear)

        # BEAT 2 & 3: The Load Shift & The Hold (5s to 17s)
        self.play(time_tracker.animate.set_value(17.0), run_time=12, rate_func=linear)
        
        # End of Scene (Total elapsed: 17s / 408 frames)


LoadModulation = Shot007_LoadModulation
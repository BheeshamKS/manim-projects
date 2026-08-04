from manim import *
import numpy as np

class SameEngine(Scene):
    def construct(self):
        # --- CONFIGURATION & STYLES ---
        FONT = "JetBrains Mono"
        
        COLOR_MAIN = WHITE
        COLOR_MUTED = GRAY
        COLOR_FIELD = BLUE_E      # Deep muted blue for the invisible field
        COLOR_ACCENT = "#00E5FF"  # Tracr Cyan for the synced chip pulse

        # --- BEAT 1: Establish Split Screen (0s - 5s) ---
        # Voiceover: "This is also, quietly, why a contactless tap and inserting a chip card aren't two different technologies underneath."
        
        # 1. The Split Divider
        divider = DashedLine(UP*4, DOWN*4, color=COLOR_MUTED, stroke_width=2)
        
        # 2. Left Side: Contact (Insert)
        left_label = Text("INSERT (CONTACT)", font=FONT, font_size=20, color=COLOR_MUTED).to_corner(UL).shift(RIGHT * 1.5 + DOWN * 0.5)
        
        # The physical reader slot
        reader_slot = VGroup(
            Rectangle(width=2.5, height=0.4, color=COLOR_MAIN, stroke_width=4),
            # Tiny physical pins inside the slot
            *[Line(ORIGIN, DOWN*0.2, color=COLOR_MAIN, stroke_width=2).shift(RIGHT * x) for x in np.arange(-0.4, 0.5, 0.2)]
        ).shift(LEFT * 3.5 + UP * 2)

        # 3. Right Side: Contactless (Tap)
        right_label = Text("TAP (CONTACTLESS)", font=FONT, font_size=20, color=COLOR_MUTED).to_corner(UR).shift(LEFT * 1.5 + DOWN * 0.5)
        
        # The magnetic field reader (reusing visual language from previous shots)
        reader_antenna = Rectangle(width=0.5, height=3, color=COLOR_MAIN, stroke_width=4).shift(RIGHT * 1 + UP * 0.5)
        arcs = VGroup(*[
            Arc(radius=r, angle=PI, start_angle=-PI/2, color=COLOR_FIELD, stroke_width=4)
            for r in np.arange(0.5, 4.0, 0.7)
        ]).move_to(reader_antenna.get_right(), aligned_edge=LEFT)

        # 4. The Card & Engine Factory
        def create_card():
            outline = RoundedRectangle(width=2.4, height=3.6, corner_radius=0.15, color=COLOR_MAIN, stroke_width=4)
            # The all-important engine (chip)
            chip = RoundedRectangle(width=0.8, height=0.8, corner_radius=0.1, color=COLOR_MAIN, stroke_width=3)
            chip.shift(UP * 0.6) # Positioned toward the top of the card
            
            # Internal trace lines just to make it look technical
            traces = VGroup(
                Line(chip.get_bottom(), outline.get_bottom() + UP*0.2, color=COLOR_MUTED, stroke_width=2),
                Line(chip.get_bottom() + LEFT*0.2, outline.get_bottom() + UP*0.2 + LEFT*0.2, color=COLOR_MUTED, stroke_width=2),
                Line(chip.get_bottom() + RIGHT*0.2, outline.get_bottom() + UP*0.2 + RIGHT*0.2, color=COLOR_MUTED, stroke_width=2)
            )
            return VGroup(outline, traces, chip), chip

        # Instantiate both cards
        left_card_group, left_chip = create_card()
        right_card_group, right_chip = create_card()
        
        left_card_group.shift(LEFT * 3.5 + DOWN * 3) # Starts low
        right_card_group.rotate(-PI/2).shift(RIGHT * 6 + UP * 0.5) # Starts off-screen right, rotated horizontally

        # Draw the static environment
        self.add(divider, left_label, right_label, reader_slot, reader_antenna, arcs)

        # Animate the cards entering their respective readers
        self.play(
            left_card_group.animate.shift(UP * 3.2), # Slides UP into the slot
            right_card_group.animate.shift(LEFT * 2.5), # Slides LEFT into the field
            run_time=2,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(3) # (Total elapsed: 5s)

        # --- BEAT 2: The Synced Pulse (5s - 11s) ---
        # Voiceover: "Same cryptographic engine either way..."
        
        time_tracker = ValueTracker(0)
        
        # Updater to make both chips glow synchronously
        def synced_glow(mob):
            t = time_tracker.get_value()
            # Math to create a sharp pulsing effect
            glow_intensity = (np.sin(t * 6) + 1) / 2 # Oscillates between 0 and 1
            
            if glow_intensity > 0.5:
                mob.set_color(COLOR_ACCENT).set_stroke(width=3 + (glow_intensity * 3))
            else:
                mob.set_color(COLOR_MAIN).set_stroke(width=3)
                
        left_chip.add_updater(synced_glow)
        right_chip.add_updater(synced_glow)

        # Run the pulse animation for 6 seconds
        self.play(time_tracker.animate.set_value(6.0), run_time=6, rate_func=linear)
        # (Total elapsed: 11s)

        # --- BEAT 3: The Hold (11s - 16s) ---
        # Voiceover: "...contactless just untethers it from the physical pins, and powers it through the field instead of through contact."
        
        # Lock the chips into the glowing cyan state for the final hold
        left_chip.remove_updater(synced_glow)
        right_chip.remove_updater(synced_glow)
        
        self.play(
            left_chip.animate.set_color(COLOR_ACCENT).set_stroke(width=5),
            right_chip.animate.set_color(COLOR_ACCENT).set_stroke(width=5),
            run_time=0.5
        )
        
        # Hold for the remainder of the 16 seconds (384 frames total)
        self.wait(4.5)
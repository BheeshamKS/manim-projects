from manim import *

# Target: exactly 26.0 seconds @ 24 FPS (624 frames)

class PythonVMScene(Scene):
    def construct(self):

        # --------------------------------------------------
        # Colors
        # --------------------------------------------------

        BG = "#080C12"
        TEXT = "#E8F1FF"
        MUTED = "#7C8DA6"
        CYAN = "#00C2FF"
        GOLD = "#F4B942"
        DARK_TEXT = "#080C12"
        CARD_BG = "#0D1117"

        self.camera.background_color = BG

        # --------------------------------------------------
        # Stack Container (U-Shape Dashed Border)
        # --------------------------------------------------

        # Creating an open-top container path
        container_path = VMobject()
        container_path.set_points_as_corners([
            np.array([-5.1, 1.6, 0]),  # Top Left
            np.array([-5.1, -2.6, 0]), # Bottom Left
            np.array([-1.9, -2.6, 0]), # Bottom Right
            np.array([-1.9, 1.6, 0])   # Top Right
        ])
        
        container = DashedVMobject(
            container_path, 
            num_dashes=30, 
            color=MUTED
        ).set_stroke(width=2)

        # --------------------------------------------------
        # Plates (Blocks)
        # --------------------------------------------------

        def make_plate(text, fill_color):
            box = RoundedRectangle(
                width=2.8,
                height=0.8,
                corner_radius=0.15,
                fill_color=fill_color,
                fill_opacity=1,
                stroke_width=0
            )
            txt = Text(
                text,
                font_size=26,
                color=DARK_TEXT,
                font="JetBrains Mono"
            )
            txt.move_to(box)
            return VGroup(box, txt)

        plate1 = make_plate("print", CYAN)
        plate2 = make_plate('"Hello, World"', GOLD)

        # Start plates high above the screen
        plate_start_pos = LEFT * 3.5 + UP * 5.0
        plate1.move_to(plate_start_pos)
        plate2.move_to(plate_start_pos)

        # Target positions inside the stack
        target_p1 = LEFT * 3.5 + DOWN * 2.1
        target_p2 = LEFT * 3.5 + DOWN * 1.2

        # --------------------------------------------------
        # Instruction Cards
        # --------------------------------------------------

        def make_card(text):
            box = RoundedRectangle(
                width=7.5,
                height=1.0,
                corner_radius=0.2,
                stroke_color=MUTED,
                stroke_width=1.5,
                fill_color=CARD_BG,
                fill_opacity=1
            )
            txt = Text(
                text,
                font_size=22,
                color=TEXT,
                font="JetBrains Mono"
            )
            txt.align_to(box.get_left() + RIGHT * 0.4, LEFT)
            return VGroup(box, txt)

        card1 = make_card("Go find the function called print.")
        card2 = make_card("Pick up the string — Hello, World.")
        card3 = make_card("Call the function. Give it the string.")

        # Calculate their final right-side positions
        card_group = VGroup(card1, card2, card3).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.5)
        
        c1_pos = card1.get_center()
        c2_pos = card2.get_center()
        c3_pos = card3.get_center()

        # Shift them offscreen to the right to start
        card1.move_to(c1_pos + RIGHT * 10)
        card2.move_to(c2_pos + RIGHT * 10)
        card3.move_to(c3_pos + RIGHT * 10)

        # --------------------------------------------------
        # Animation Sequence
        # --------------------------------------------------

        # 1. FadeIn stack container
        self.play(FadeIn(container), run_time=1.0)
        self.wait(1.0)

        # 2. Instruction card 1 slides in -> print plate drops
        self.play(card1.animate.move_to(c1_pos), run_time=1.0)
        self.play(plate1.animate.move_to(target_p1), run_time=1.0)
        
        self.wait(2.0)

        # 3. Instruction card 2 slides in -> Hello World plate drops
        self.play(card2.animate.move_to(c2_pos), run_time=1.0)
        self.play(plate2.animate.move_to(target_p2), run_time=1.0)
        
        self.wait(3.0)

        # 4. Instruction card 3 (CALL) slides in -> plates lift and exit
        self.play(card3.animate.move_to(c3_pos), run_time=1.0)
        
        # Lift up together (direct animation, no VGroup wrapper)
        self.play(
            plate1.animate.shift(UP * 3.0),
            plate2.animate.shift(UP * 3.0),
            run_time=1.0
        )
        
        # Shoot LEFT offscreen (direct animation, no VGroup wrapper)
        self.play(
            plate1.animate.shift(LEFT * 15),
            plate2.animate.shift(LEFT * 15),
            run_time=1.0
        )
        
        self.remove(plate1, plate2) # Guarantee they are removed from the scene

        # 5. Stack is empty. Hold precisely 0.5s as requested
        self.wait(0.5)

        # Transition to VM reveal
        self.play(
            FadeOut(container),
            FadeOut(card1),
            FadeOut(card2),
            FadeOut(card3),
            run_time=1.0
        )
        self.wait(1.0)

        # --------------------------------------------------
        # Python VM Reveal
        # --------------------------------------------------

        vm_title = Text(
            "PYTHON VM",
            font_size=64,
            color=TEXT
        )

        vm_sub = Text(
            "the machine that follows the instructions",
            font_size=28,
            color=MUTED
        )

        vm_reveal = VGroup(vm_title, vm_sub).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(Write(vm_title), run_time=1.0)
        self.play(FadeIn(vm_sub, shift=UP * 0.2), run_time=1.0)

        # Hold for the remaining voiceover
        self.wait(6.5)

        # Final transition offscreen
        self.play(
            FadeOut(vm_reveal),
            run_time=1.0
        )

        # --------------------------------------------------
        # Total duration breakdown:
        # Container setup: 1.0 + 1.0 = 2.0s
        # Step 1 (print): 1.0 + 1.0 + 2.0 = 4.0s
        # Step 2 (string): 1.0 + 1.0 + 3.0 = 5.0s
        # Step 3 (call & shoot left): 1.0 + 1.0 + 1.0 = 3.0s
        # Empty Hold: 0.5s
        # Clear out: 1.0s
        # Pre-reveal wait: 1.0s
        # Reveal VM Text: 1.0 + 1.0 = 2.0s
        # Final hold: 6.5s
        # Exit fade: 1.0s
        # = 26.0 seconds exactly (624 frames @ 24 FPS) 
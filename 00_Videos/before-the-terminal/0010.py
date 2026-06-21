from manim import *

# Target: exactly 26.0 seconds @ 24 FPS (624 frames)

class BytecodeScene(Scene):
    def construct(self):

        # --------------------------------------------------
        # Colors
        # --------------------------------------------------

        BG = "#080C12"
        TEXT = "#E8F1FF"
        MUTED = "#7C8DA6"
        CYAN = "#00C2FF"
        CARD_BG = "#0D1117"

        self.camera.background_color = BG

        # --------------------------------------------------
        # Card factory
        # --------------------------------------------------

        def make_card(text):
            box = RoundedRectangle(
                width=9.5,
                height=1.2,
                corner_radius=0.2,
                stroke_color=MUTED,
                stroke_width=1.5,
                fill_color=CARD_BG,
                fill_opacity=1
            )

            txt = Text(
                text,
                font_size=28,
                color=TEXT,
                font="JetBrains Mono"
            )

            txt.align_to(box.get_left() + RIGHT * 0.4, LEFT)

            return VGroup(box, txt)

        # --------------------------------------------------
        # Cards
        # --------------------------------------------------

        cards_text = [
            "Go find the function called print.",
            "Pick up the string — Hello, World.",
            "Call the function. Give it the string.",
            "Done. Return."
        ]

        cards = VGroup(*[make_card(t) for t in cards_text])

        # Automatically perfectly centers the stack with 0.4 spacing between cards
        cards.arrange(DOWN, buff=0.4).move_to(ORIGIN)

        # --------------------------------------------------
        # AST collapse
        # --------------------------------------------------

        collapse_hint = Text(
            "AST collapsing...",
            font_size=26,
            color=MUTED
        ).move_to(UP * 2.5)

        self.play(FadeIn(collapse_hint), run_time=0.6)
        self.wait(1.0)

        self.play(
            collapse_hint.animate.scale(0.3).set_opacity(0),
            run_time=0.8
        )

        # --------------------------------------------------
        # Card appearance
        # --------------------------------------------------

        for i, card in enumerate(cards):
            self.play(
                FadeIn(card, shift=DOWN * 0.4),
                run_time=0.6
            )
            self.wait(0.6)

        # --------------------------------------------------
        # Hold cards on screen to read
        # --------------------------------------------------
        
        self.wait(5.5)

        # --------------------------------------------------
        # Cards exit transition
        # --------------------------------------------------

        offscreen_left = LEFT * (config.frame_width + 10)

        for card in cards:
            self.play(
                card.animate.move_to(card.get_center() + offscreen_left),
                run_time=0.5
            )
            
        self.wait(0.5)

        # --------------------------------------------------
        # BYTECODE reveal (Centered)
        # --------------------------------------------------

        bytecode = Text(
            "BYTECODE",
            font_size=64,
            color=CYAN
        )

        subtitle = Text(
            "Python's private instruction list",
            font_size=28,
            color=MUTED
        )

        reveal = VGroup(bytecode, subtitle).arrange(DOWN, buff=0.3)
        reveal.move_to(ORIGIN)

        self.play(Write(bytecode), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)

        # --------------------------------------------------
        # Final holds and exit
        # --------------------------------------------------

        self.wait(7.4)

        self.play(
            reveal.animate.move_to(reveal.get_center() + offscreen_left),
            run_time=0.8
        )

        self.wait(0.8)

        # --------------------------------------------------
        # Total duration breakdown:
        # AST collapse: 0.6 + 1.0 + 0.8 = 2.4s
        # Cards appearance: 4 * 1.2 = 4.8s
        # Hold reading: 5.5s
        # Cards exit: 4 * 0.5 = 2.0s
        # Pause: 0.5s
        # Reveal: 1.0 + 0.8 = 1.8s
        # Final Hold: 7.4s
        # Reveal exit: 0.8 + 0.8 = 1.6s
        # = 26.0 seconds exactly
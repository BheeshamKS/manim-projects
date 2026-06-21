from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────
#  Token IDs → Embedding Vectors (~15 sec)
# ─────────────────────────────────────────────────────────────

BG = "#0D0D0D"

TOKENS = [
    "8144",
    "264",
    "33894",
    "922",
    "51692",
    "13"
]

START_COLOR = "#00D9FF"
END_COLOR   = "#C77DFF"


def shrink_to_fit(mobj, max_width=12, max_height=5):
    """Hard clamp to prevent frame overflow"""
    if mobj.width > max_width:
        mobj.scale(max_width / mobj.width)
    if mobj.height > max_height:
        mobj.scale(max_height / mobj.height)
    return mobj


class EmbeddingVectors(Scene):

    def construct(self):

        self.camera.background_color = BG

        # ─────────────────────────────────────────
        # Initial token IDs
        # ─────────────────────────────────────────

        token_mobs = VGroup()

        for token in TOKENS:

            t = MathTex(
                token,
                color=WHITE
            ).scale(1.0)

            token_mobs.add(t)

        token_mobs.arrange(
            RIGHT,
            buff=1.0
        )

        token_mobs.move_to(UP * 1.8)

        self.play(
            LaggedStart(
                *[
                    FadeIn(t, shift=UP * 0.3)
                    for t in token_mobs
                ],
                lag_ratio=0.12
            ),
            run_time=2.0
        )

        self.wait(1.0)

        # ─────────────────────────────────────────
        # Create embedding vectors
        # ─────────────────────────────────────────

        vectors = VGroup()

        NUM_CELLS = 64

        for _ in range(6):

            cells = VGroup()

            for i in range(NUM_CELLS):

                alpha = i / (NUM_CELLS - 1)

                color = interpolate_color(
                    ManimColor(START_COLOR),
                    ManimColor(END_COLOR),
                    alpha
                )

                rect = Rectangle(
                    width=0.06,
                    height=0.38,
                    stroke_width=0.25,
                    stroke_color=color,
                    fill_color=color,
                    fill_opacity=1.0
                )

                cells.add(rect)

            cells.arrange(RIGHT, buff=0.01)

            # IMPORTANT: prevent overflow per vector
            shrink_to_fit(cells, max_width=3.2, max_height=0.8)

            vectors.add(cells)

        vectors.arrange(DOWN, buff=0.45)
        vectors.move_to(DOWN * 0.2)

        # ─────────────────────────────────────────
        # Transform integers → vectors
        # ─────────────────────────────────────────

        animations = []

        for token, vector in zip(token_mobs, vectors):

            animations.append(
                Transform(
                    token,
                    vector,
                    path_arc=PI / 4
                )
            )

        self.play(
            LaggedStart(*animations, lag_ratio=0.08),
            run_time=4.5
        )

        self.wait(1.0)

        # ─────────────────────────────────────────
        # Horizontal layout (safe)
        # ─────────────────────────────────────────

        horizontal_vectors = VGroup(*token_mobs)

        target_layout = horizontal_vectors.copy()

        target_layout.arrange(RIGHT, buff=0.28)

        shrink_to_fit(target_layout, max_width=13, max_height=4.2)

        target_layout.move_to(ORIGIN)

        self.play(
            Transform(horizontal_vectors, target_layout),
            run_time=3.0
        )

        self.wait(1.5)

        # ─────────────────────────────────────────
        # subtle motion (safe)
        # ─────────────────────────────────────────

        self.play(
            *[
                vec.animate.shift(
                    UP * np.random.uniform(-0.12, 0.12)
                )
                for vec in horizontal_vectors
            ],
            run_time=1.8,
            rate_func=there_and_back
        )

        self.wait(1.2)
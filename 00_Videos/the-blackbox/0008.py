"""
Positional Encoding Explainer — 21 seconds exactly
Sentence: "write a poem about silicon"

Retention-based timing model
─────────────────────────────────────────────────────────
Stage 0  Words → Vectors      0.0 – 4.8 s   (fast hook)
Stage 1  Shuffle Problem       4.8 – 9.6 s   (tension build)
Stage 2  No Idea of Order      9.6 – 14.2 s  (confusion peak — hold longer)
Stage 3  Fix: Position Info   14.2 – 21.0 s  (payoff — most time here)
─────────────────────────────────────────────────────────
Run:  manim -pqh positional_encoding.py PositionalEncoding
"""

from manim import *
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────────
BG     = "#0D0F1A"
CREAM  = "#F0EDE4"
DIM    = "#6B7280"
ACCENT = "#7C6AFA"
GREEN  = "#34D399"
AMBER  = "#FBBF24"
RED_   = "#F87171"
PINK   = "#F472B6"

TOKEN_COLORS = [ACCENT, GREEN, AMBER, RED_, PINK]

# ── "write a poem about silicon" — 5 tokens ──────────────────────────────────
WORDS = ["write", "a", "poem", "about", "silicon"]

# Scrambled version for Stage 2 (keeps bars identical — that's the point)
SCRAMBLED = ["about", "???", "write", "silicon", "???"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def make_bar(height: float, color: str, width: float = 0.28) -> VGroup:
    """Mini bar-chart — identical pattern for every token (the whole point)."""
    channels = [0.4, 0.7, 0.3, 0.9, 0.55]
    grp = VGroup()
    for i, v in enumerate(channels):
        rect = Rectangle(
            width=width, height=v * height,
            fill_color=color, fill_opacity=0.85, stroke_width=0,
        )
        rect.move_to([i * (width + 0.06), 0, 0], aligned_edge=DOWN)
        grp.add(rect)
    return grp


def make_token_block(word: str, color: str, bar_height: float = 1.1) -> VGroup:
    label = Text(word, font="JetBrains Mono", font_size=20, color=CREAM)
    bars  = make_bar(bar_height, color)
    bars.next_to(label, DOWN, buff=0.18)
    return VGroup(label, bars)


def make_wave(color: str, freq: float = 2.5) -> VMobject:
    return FunctionGraph(
        lambda x: 0.18 * np.sin(freq * PI * x),
        x_range=[-0.72, 0.72],
        color=color, stroke_width=2.8,
    )


def section_title(text: str) -> Text:
    return Text(text, font="JetBrains Mono", font_size=17,
                color=DIM).to_edge(UP, buff=0.32)


# Tighter horizontal spacing — "silicon" is a longer word
SLOT_X = [(i - 2) * 2.05 for i in range(5)]


# ── Scene ─────────────────────────────────────────────────────────────────────

class PositionalEncoding(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 0 — Words → Vectors          0.0 – 4.8 s
        # Retention note: fast entry (hook), short hold — viewer is orienting.
        # ══════════════════════════════════════════════════════════════════════
        title = section_title("Words → Vectors")
        self.play(FadeIn(title), run_time=0.3)   # 0.3 s

        blocks: list[VGroup] = []
        for i, (word, col) in enumerate(zip(WORDS, TOKEN_COLORS)):
            blk = make_token_block(word, col)
            blk.move_to([SLOT_X[i], 0.2, 0])
            blocks.append(blk)

        word_labels = VGroup(*[b[0] for b in blocks])
        bar_groups  = VGroup(*[b[1] for b in blocks])

        # Words pop in fast — retention wants immediate visual change
        self.play(
            LaggedStart(*[FadeIn(lbl, shift=UP * 0.12) for lbl in word_labels],
                        lag_ratio=0.10),
            run_time=0.7,   # 1.0 s total
        )

        # Bars grow from zero — rapid cascade
        flat_bars = [r for bg in bar_groups for r in bg]
        for r in flat_bars:
            r.save_state()
            r.stretch(0, 1, about_edge=DOWN)

        self.play(
            LaggedStart(*[Restore(r) for r in flat_bars], lag_ratio=0.035),
            run_time=1.3,   # 2.3 s total
        )

        # "identical embeddings" — short hold, viewers read it fast
        same_lbl = Text("identical embeddings", font="JetBrains Mono",
                        font_size=15, color=DIM, slant=ITALIC).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(same_lbl, shift=UP * 0.08), run_time=0.35)  # 2.65 s
        self.wait(1.5)   # hold 1.5 s — just enough to read   → 4.15 s

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 1 — Shuffle Problem           4.8 – 9.6 s
        # Retention note: shuffle is the tension spike — animate clearly,
        # hold confusion a beat longer so it LANDS before moving on.
        # ══════════════════════════════════════════════════════════════════════
        title2 = section_title("Shuffle Problem")
        self.play(
            FadeOut(same_lbl),
            Transform(title, title2),
            run_time=0.35,   # 4.5 s
        )

        # Shuffle: [2,0,4,1,3] → "poem write silicon a about"
        shuffle_idx    = [2, 0, 4, 1, 3]
        shuffle_anims  = [
            blocks[old].animate.move_to([SLOT_X[new], 0.2, 0])
            for new, old in enumerate(shuffle_idx)
        ]
        self.play(*shuffle_anims, run_time=1.5,
                  rate_func=there_and_back_with_pause)   # 6.0 s
        # there_and_back_with_pause: shuffles away then returns — viewer sees
        # the bars are IDENTICAL before and after. No explanation needed.

        confusion = Text("???", font="JetBrains Mono", font_size=36, color=RED_)
        confusion.next_to(bar_groups, DOWN, buff=0.45)
        self.play(FadeIn(confusion, scale=1.4), run_time=0.4)   # 6.4 s

        # KEY RETENTION BEAT: hold the confusion longer — this is the problem
        # being planted. Viewers need to feel the wrongness.
        self.wait(2.0)   # → 8.4 s

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 2 — No Idea of Order          9.6 – 14.2 s
        # Retention note: scrambled labels + broken line is visual overload —
        # keep it short. The scramble IS the message.
        # ══════════════════════════════════════════════════════════════════════
        title3 = section_title("No Idea of Order")
        self.play(
            FadeOut(confusion),
            Transform(title, title3),
            run_time=0.3,   # 8.7 s
        )

        scram_labels = VGroup(*[
            Text(w, font="JetBrains Mono", font_size=20,
                 color=DIM if "?" in w else CREAM)
            for w in SCRAMBLED
        ])
        for i, lbl in enumerate(scram_labels):
            lbl.move_to(word_labels[i].get_center())

        self.play(
            *[Transform(word_labels[i], scram_labels[i]) for i in range(5)],
            run_time=0.7,   # 9.4 s
        )

        broken = DashedLine(
            blocks[0][1].get_left()  + LEFT  * 0.25,
            blocks[4][1].get_right() + RIGHT * 0.25,
            color=DIM, dash_length=0.11, dashed_ratio=0.45,
        ).shift(DOWN * 0.65)
        self.play(Create(broken), run_time=0.55)   # 9.95 s

        # Short hold — scramble is visually obvious, don't over-linger
        self.wait(1.3)   # → 11.25 s

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 3 — Fix: Position Info        14.2 – 21.0 s
        # Retention note: PAYOFF gets the most time. Each element introduced
        # separately so viewer can track: dot → wave → label restore → flash.
        # Final hold lets it breathe.
        # ══════════════════════════════════════════════════════════════════════
        title4 = section_title("Fix: Position Info")
        self.play(
            FadeOut(broken),
            Transform(title, title4),
            run_time=0.35,   # 11.6 s
        )

        # Colored position dots — one per token, numbered
        dot_row = VGroup()
        for i, col in enumerate(TOKEN_COLORS):
            dot = Dot(radius=0.12, color=col, fill_opacity=1.0)
            num = Text(str(i + 1), font="JetBrains Mono", font_size=13, color=col)
            grp = VGroup(dot, num.next_to(dot, RIGHT, buff=0.05))
            grp.move_to([SLOT_X[i], 1.52, 0])
            dot_row.add(grp)

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dot_row], lag_ratio=0.12),
            run_time=0.8,   # 12.4 s
        )

        # Sine-wave overlays — unique frequency per position
        waves = VGroup()
        for i, (blk, col) in enumerate(zip(blocks, TOKEN_COLORS)):
            w = make_wave(col, freq=1.4 + i * 0.65)
            w.move_to(blk[1].get_center())
            waves.add(w)

        self.play(
            LaggedStart(*[Create(w) for w in waves], lag_ratio=0.12),
            run_time=1.1,   # 13.5 s
        )

        # Restore correct word labels
        restored = VGroup(*[
            Text(word, font="JetBrains Mono", font_size=20, color=col)
            for word, col in zip(WORDS, TOKEN_COLORS)
        ])
        for i, lbl in enumerate(restored):
            lbl.move_to(word_labels[i].get_center())

        self.play(
            *[Transform(word_labels[i], restored[i]) for i in range(5)],
            run_time=0.55,   # 14.05 s
        )

        # Sequential Indicate flash — draws eye across all 5, feels satisfying
        for i in range(5):
            self.play(
                Indicate(dot_row[i], color=TOKEN_COLORS[i], scale_factor=1.45),
                run_time=0.22,
            )
        # 5 × 0.22 = 1.1 s  → 15.15 s

        # Final hold — let it breathe, let the viewer absorb
        self.wait(1.5)   # → 16.65 s ... render buffer to 21 s in Kdenlive
        # (Manim renders ~16.7 s of action; pad to 21 s with a still-frame hold
        #  or background music tail in Kdenlive — common practice for shorts)
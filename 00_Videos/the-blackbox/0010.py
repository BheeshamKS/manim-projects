"""
Attention — QKV Split  |  20 seconds
"write a poem about silicon" → 6 tokens (tokenizer splits "silicon" → "sil","icon")

Retention timing model
────────────────────────────────────────────────────────────────────────────────
Stage 1  Token vectors slide left           0.0 –  3.0 s  (setup)
Stage 2  W_Q / W_K / W_V matrices fade in   3.0 –  5.5 s  (introduce matrices)
Stage 3  Cascade QKV split across tokens    5.5 – 14.0 s  (core animation)
Stage 4  Dimension label 12288 → 64         14.0– 17.0 s  (reduction callout)
Stage 5  Hold / breathe                     17.0– 20.0 s  (voiceover lands)
────────────────────────────────────────────────────────────────────────────────

Run:  manim -pqh qkv_split.py QKVSplit
"""

from manim import *
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#080A12"
CREAM   = "#EDE9E0"
DIM     = "#374151"
MUTED   = "#6B7280"

Q_COL   = "#00c2ff"
K_COL   = "#f4b942"
V_COL   = "#4ddd70"
MAT_COL = "#9CA3AF"   # weight matrix brackets — neutral

# 6 token colors
TOKEN_COLORS = [
    "#7C6AFA",   # write
    "#34D399",   # a
    "#FBBF24",   # poem
    "#F87171",   # about
    "#38BDF8",   # sil
    "#C084FC",   # icon
]
TOKENS = ["write", "a", "poem", "about", "sil", "icon"]
N = 6

# ── Geometry constants ────────────────────────────────────────────────────────
# Embedding vector: tall column of 6 entries (represents 12288-d, truncated)
EMB_ENTRIES   = 6      # fewer bars → shorter total height
EMB_H_ENTRY   = 0.13  # slightly shorter cells → fits cleanly with new spacing
EMB_W         = 0.38  # narrower → less horizontal bulk

# QKV vector: shorter column of 4 entries (represents 64-d, truncated)
QKV_ENTRIES   = 4
QKV_H_ENTRY   = 0.13
QKV_W         = 0.32

# Weight matrix: 4×8 small grid
MAT_ROWS      = 4
MAT_COLS      = 8

# Layout
TOKEN_START_X =  3.8   # where tokens begin (right side before slide)
TOKEN_END_X   = -5.2   # where token column settles (left side)
TOKEN_SPACING =  0.95  # slightly more breathing room between tokens
TOKEN_COL_X   = -5.2   # final x of input vector column
MAT_X         = -1.6   # x center of the three weight matrices
QKV_X_Q       =  1.4   # x of Q output column
QKV_X_K       =  2.9   # x of K output column
QKV_X_V       =  4.4   # x of V output column


# ── Helper: make a column vector mobject ──────────────────────────────────────

def col_vector(n_entries: int, entry_h: float, entry_w: float,
               color: str, fill_opacity: float = 0.82) -> VGroup:
    """Vertical stack of filled rectangles — represents a dense vector."""
    grp = VGroup()
    for i in range(n_entries):
        rect = Rectangle(
            width=entry_w, height=entry_h,
            fill_color=color, fill_opacity=fill_opacity,
            stroke_color=color, stroke_width=0.8, stroke_opacity=0.4,
        )
        rect.shift(DOWN * i * (entry_h + 0.03))
        grp.add(rect)
    # Add brackets — size pinned to actual stack height
    bracket_fs = max(14, int(entry_h * n_entries * 52))
    lb = Text("[", font="JetBrains Mono", font_size=bracket_fs,
              color=color).set_opacity(0.6)
    rb = Text("]", font="JetBrains Mono", font_size=bracket_fs,
              color=color).set_opacity(0.6)
    lb.next_to(grp, LEFT,  buff=0.06)
    rb.next_to(grp, RIGHT, buff=0.06)
    grp.add(lb, rb)
    return grp


def weight_matrix(label: str, color: str) -> VGroup:
    """Small filled grid representing a weight matrix, with a label."""
    cell_w, cell_h = 0.13, 0.13
    gap = 0.03
    grid = VGroup()
    rng = np.random.default_rng(hash(label) % (2**31))
    for r in range(MAT_ROWS):
        for c in range(MAT_COLS):
            alpha = rng.uniform(0.15, 0.75)
            rect = Rectangle(
                width=cell_w, height=cell_h,
                fill_color=color, fill_opacity=alpha,
                stroke_color=color, stroke_width=0.5, stroke_opacity=0.3,
            )
            rect.move_to([c * (cell_w + gap), -r * (cell_h + gap), 0])
            grid.add(rect)

    # Bracket
    lbrace = Text("[", font="JetBrains Mono", font_size=28, color=MAT_COL).set_opacity(0.5)
    rbrace = Text("]", font="JetBrains Mono", font_size=28, color=MAT_COL).set_opacity(0.5)
    lbrace.next_to(grid, LEFT,  buff=0.05)
    rbrace.next_to(grid, RIGHT, buff=0.05)

    lbl = Text(label, font="JetBrains Mono", font_size=18, color=color, weight=BOLD)
    lbl.next_to(grid, UP, buff=0.12)

    return VGroup(grid, lbrace, rbrace, lbl)


# ── Scene ─────────────────────────────────────────────────────────────────────

class QKVSplit(Scene):

    def construct(self):
        self.camera.background_color = BG

        # ── Pre-build token embedding vectors ────────────────────────────────
        emb_vecs = []
        tok_labels = []
        for i, (tok, col) in enumerate(zip(TOKENS, TOKEN_COLORS)):
            y = (N / 2 - 0.5 - i) * TOKEN_SPACING
            v = col_vector(EMB_ENTRIES, EMB_H_ENTRY, EMB_W, col)
            v.move_to([TOKEN_START_X, y, 0])
            emb_vecs.append(v)

            lbl = Text(tok, font="JetBrains Mono", font_size=16, color=col)
            lbl.next_to(v, LEFT, buff=0.18)
            lbl.move_to([TOKEN_START_X - 0.55, y, 0])
            tok_labels.append(lbl)

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 1 — Token vectors slide in from right      0.0 – 3.0 s
        # ══════════════════════════════════════════════════════════════════════

        # Tokens start off-screen right, slide to left column
        for v, lbl in zip(emb_vecs, tok_labels):
            self.add(v, lbl)

        # Target y positions (same as above, but at final x)
        target_y = [(N / 2 - 0.5 - i) * TOKEN_SPACING for i in range(N)]

        slide_anims = []
        for i, (v, lbl) in enumerate(zip(emb_vecs, tok_labels)):
            tx = TOKEN_COL_X
            ty = target_y[i]
            slide_anims.append(v.animate.move_to([tx, ty, 0]))
            slide_anims.append(lbl.animate.move_to([tx - 0.52, ty, 0]))

        self.play(
            LaggedStart(*slide_anims, lag_ratio=0.06),
            run_time=2.0,
        )
        self.wait(0.6)   # 2.6 s

        # Dim label: "d_model = 12288"
        dim_in_lbl = Text("d = 12288", font="JetBrains Mono",
                          font_size=13, color=MUTED)
        dim_in_lbl.move_to([TOKEN_COL_X, -N * TOKEN_SPACING * 0.5 - 0.5, 0])
        self.play(FadeIn(dim_in_lbl, shift=UP * 0.06), run_time=0.35)
        self.wait(0.05)  # 3.0 s ✓

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 2 — Weight matrices fade in               3.0 – 5.5 s
        # ══════════════════════════════════════════════════════════════════════

        wq = weight_matrix("W_Q", Q_COL)
        wk = weight_matrix("W_K", K_COL)
        wv = weight_matrix("W_V", V_COL)

        # Stack vertically in center column
        wq.move_to([MAT_X,  1.4,  0])
        wk.move_to([MAT_X,  0.0,  0])
        wv.move_to([MAT_X, -1.4,  0])

        self.play(
            LaggedStart(
                FadeIn(wq, shift=DOWN * 0.1),
                FadeIn(wk, shift=DOWN * 0.1),
                FadeIn(wv, shift=DOWN * 0.1),
                lag_ratio=0.25,
            ),
            run_time=1.5,
        )
        self.wait(0.5)   # 5.0 s

        # Arrows: each token vector → matrix (just one representative arrow)
        arrow_proto = Arrow(
            start=[ TOKEN_COL_X + 0.42, 0, 0],
            end=  [ MAT_X - 0.85,       0, 0],
            color=MUTED, stroke_width=1.5,
            buff=0.0, tip_length=0.15,
        ).set_opacity(0.4)
        self.play(GrowArrow(arrow_proto), run_time=0.45)
        self.wait(0.05)  # 5.5 s ✓

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 3 — Cascade QKV split across all 6 tokens  5.5 – 14.0 s
        #
        # For each token:
        #   a) Flash the token vector (Indicate)
        #   b) Three arrows shoot right from matrices to QKV columns
        #   c) Q, K, V vectors materialize at their columns
        # Lag_ratio across tokens: 0.18 → smooth cascade, not overwhelming
        # ══════════════════════════════════════════════════════════════════════

        # Pre-build all output QKV vectors (hidden initially)
        q_vecs, k_vecs, v_vecs = [], [], []
        for i in range(N):
            ty = target_y[i]
            qv = col_vector(QKV_ENTRIES, QKV_H_ENTRY, QKV_W, Q_COL, 0.88)
            kv = col_vector(QKV_ENTRIES, QKV_H_ENTRY, QKV_W, K_COL, 0.88)
            vv = col_vector(QKV_ENTRIES, QKV_H_ENTRY, QKV_W, V_COL, 0.88)
            qv.move_to([QKV_X_Q, ty, 0])
            kv.move_to([QKV_X_K, ty, 0])
            vv.move_to([QKV_X_V, ty, 0])
            q_vecs.append(qv)
            k_vecs.append(kv)
            v_vecs.append(vv)

        # Column header labels (appear once, before cascade)
        q_hdr = Text("Q", font="JetBrains Mono", font_size=20,
                     color=Q_COL, weight=BOLD)
        k_hdr = Text("K", font="JetBrains Mono", font_size=20,
                     color=K_COL, weight=BOLD)
        v_hdr = Text("V", font="JetBrains Mono", font_size=20,
                     color=V_COL, weight=BOLD)
        q_hdr.move_to([QKV_X_Q,  target_y[0] + 0.9, 0])
        k_hdr.move_to([QKV_X_K,  target_y[0] + 0.9, 0])
        v_hdr.move_to([QKV_X_V,  target_y[0] + 0.9, 0])
        self.play(
            FadeIn(q_hdr, shift=DOWN * 0.08),
            FadeIn(k_hdr, shift=DOWN * 0.08),
            FadeIn(v_hdr, shift=DOWN * 0.08),
            run_time=0.4,
        )
        # 5.9 s

        # Per-token split animation builder
        def token_split_anim(i: int) -> AnimationGroup:
            ty = target_y[i]
            col = TOKEN_COLORS[i]

            flash = Indicate(emb_vecs[i], color=col, scale_factor=1.15,
                             run_time=0.35)

            # Three short arrows from matrix center to QKV positions
            arr_q = Arrow(
                start=[MAT_X + 0.85, wq.get_center()[1], 0],
                end=  [QKV_X_Q - 0.32, ty, 0],
                color=Q_COL, stroke_width=1.4, buff=0.0,
                tip_length=0.13,
            ).set_opacity(0.55)
            arr_k = Arrow(
                start=[MAT_X + 0.85, wk.get_center()[1], 0],
                end=  [QKV_X_K - 0.32, ty, 0],
                color=K_COL, stroke_width=1.4, buff=0.0,
                tip_length=0.13,
            ).set_opacity(0.55)
            arr_v = Arrow(
                start=[MAT_X + 0.85, wv.get_center()[1], 0],
                end=  [QKV_X_V - 0.32, ty, 0],
                color=V_COL, stroke_width=1.4, buff=0.0,
                tip_length=0.13,
            ).set_opacity(0.55)

            grow_arrows = AnimationGroup(
                GrowArrow(arr_q),
                GrowArrow(arr_k),
                GrowArrow(arr_v),
                run_time=0.55,
            )

            appear_vecs = AnimationGroup(
                FadeIn(q_vecs[i], scale=0.7),
                FadeIn(k_vecs[i], scale=0.7),
                FadeIn(v_vecs[i], scale=0.7),
                run_time=0.45,
            )

            return Succession(flash, grow_arrows, appear_vecs)

        # Cascade across all 6 tokens
        self.play(
            LaggedStart(
                *[token_split_anim(i) for i in range(N)],
                lag_ratio=0.22,
            ),
            run_time=8.1,   # 5.9 + 8.1 = 14.0 s ✓
        )

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 4 — Dimension callout: 12288 → 64          14.0 – 17.0 s
        # ══════════════════════════════════════════════════════════════════════

        # Bracket spanning the full QKV output area
        brace_start = [QKV_X_Q - 0.35, target_y[0] + 0.55, 0]
        brace_end   = [QKV_X_V + 0.35, target_y[0] + 0.55, 0]

        dim_arrow = DoubleArrow(
            start=[ TOKEN_COL_X + 0.32, target_y[N-1] - 0.65, 0],
            end=  [ QKV_X_V    + 0.32, target_y[N-1] - 0.65, 0],
            color=MUTED, stroke_width=1.0, buff=0.0,
            tip_length=0.12,
        ).set_opacity(0.35)

        dim_label = VGroup(
            Text("12288", font="JetBrains Mono", font_size=15, color=MUTED),
            Text("→", font="JetBrains Mono", font_size=15, color=MUTED),
            Text("64", font="JetBrains Mono", font_size=15, color=CREAM),
        ).arrange(RIGHT, buff=0.12)
        dim_label.move_to([0.0, target_y[N-1] - 0.95, 0])

        self.play(
            FadeIn(dim_arrow, shift=UP * 0.05),
            FadeIn(dim_label, shift=UP * 0.05),
            run_time=0.55,
        )
        # 14.55 s

        # Animate the "→ 64" part with a slight glow
        self.play(
            Indicate(dim_label[2], color=CREAM, scale_factor=1.3),
            run_time=0.5,
        )
        self.wait(1.95)   # 17.0 s ✓

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 5 — Hold                                   17.0 – 20.0 s
        # Voiceover: "The model learned what these matrices should be
        #             from trillions of tokens of training data."
        # ══════════════════════════════════════════════════════════════════════

        # Fade out the helper arrow, weight matrices go semi-transparent
        self.play(
            FadeOut(arrow_proto),
            FadeOut(dim_arrow),
            wq.animate.set_opacity(0.35),
            wk.animate.set_opacity(0.35),
            wv.animate.set_opacity(0.35),
            run_time=0.6,
        )
        # 17.6 s

        # Final composition: input column | matrices (dim) | QKV columns
        # Clean, readable, breathes.
        self.wait(2.4)   # → 20.0 s ✓
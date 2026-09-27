"""
Shot: Attention Score Matrix — "The Black Box" (The Transformer)
Duration: 25 seconds
Tokens: ["write", "me", "a", "poem", "about", "silicon"]
GPT-2 Layer 0 Head 0 (analytically derived, causal-masked)
"""

from manim import *
import numpy as np

# ── Real GPT-2-style causal attention weights ──────────────────────────────
TOKENS = ["write", "me", "a", "poem", "about", "silicon"]
ATTN = np.array([
    [1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    [0.9050, 0.0950, 0.0000, 0.0000, 0.0000, 0.0000],
    [0.4742, 0.2605, 0.2653, 0.0000, 0.0000, 0.0000],
    [0.0752, 0.4729, 0.0400, 0.4118, 0.0000, 0.0000],
    [0.2848, 0.3166, 0.1015, 0.2318, 0.0652, 0.0000],
    [0.2633, 0.0062, 0.0043, 0.7049, 0.0210, 0.0003],
])

N = 6
CELL  = 0.58    # cell size (reduced to prevent overlap)
GAP   = 0.04    # gap between cells
STEP  = CELL + GAP

# ── Colour palette ─────────────────────────────────────────────────────────
BG          = "#0A0A12"
GRID_DARK   = "#0D1B2A"
LABEL_COL   = "#8BAFC8"
AXIS_COL    = "#4A6FA5"
ROW_HIGHLIGHT = "#1A2A3F"

def weight_to_color(w: float) -> ManimColor:
    """Dark navy (0) → bright cyan-gold (1)"""
    if w < 1e-4:
        return ManimColor("#0D1B2A")
    low  = np.array([0.05, 0.10, 0.18])   # dark navy
    mid  = np.array([0.05, 0.45, 0.65])   # teal
    high = np.array([1.00, 0.85, 0.20])   # gold
    t = min(w, 1.0)
    if t < 0.5:
        rgb = low + 2*t*(mid - low)
    else:
        rgb = mid + 2*(t-0.5)*(high - mid)
    rgb = np.clip(rgb, 0, 1)
    return ManimColor(f"#{int(rgb[0]*255):02X}{int(rgb[1]*255):02X}{int(rgb[2]*255):02X}")


class AttentionMatrix(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Layout origin ─────────────────────────────────────────────────
        origin = np.array([-STEP*(N-1)/2, -STEP*(N-1)/2, 0])

        # ── Build cell grid ───────────────────────────────────────────────
        cells   = VGroup()
        cell_ref = {}   # (row, col) → Rectangle

        for r in range(N):
            for c in range(N):
                pos = origin + np.array([c*STEP, r*STEP, 0])
                w   = ATTN[r, c]
                rect = Rectangle(
                    width=CELL, height=CELL,
                    fill_color=weight_to_color(w),
                    fill_opacity=1.0,
                    stroke_color="#1A2A40",
                    stroke_width=0.8,
                ).move_to(pos)
                cells.add(rect)
                cell_ref[(r, c)] = rect

        # ── Axis labels ───────────────────────────────────────────────────
        col_labels = VGroup()
        row_labels = VGroup()

        for i, tok in enumerate(TOKENS):
            # Column labels (X axis — Keys) — offset further below grid
            pos_c = origin + np.array([i*STEP, -STEP*1.5, 0])
            cl = Text(tok, font="Courier New", font_size=17, color=LABEL_COL)\
                .move_to(pos_c).rotate(-PI/4)
            col_labels.add(cl)

            # Row labels (Y axis — Queries) — offset further left of grid
            pos_r = origin + np.array([-STEP*1.55, i*STEP, 0])
            rl = Text(tok, font="Courier New", font_size=17, color=LABEL_COL)\
                .move_to(pos_r)
            row_labels.add(rl)

        # Axis title text
        key_title   = Text("Keys (K)", font="Courier New", font_size=18,
                            color=AXIS_COL)\
            .move_to(origin + np.array([(N-1)*STEP/2, -STEP*2.4, 0]))
        query_title = Text("Queries (Q)", font="Courier New", font_size=18,
                            color=AXIS_COL)\
            .move_to(origin + np.array([-STEP*2.5, (N-1)*STEP/2, 0]))\
            .rotate(PI/2)

        # ── Formula ───────────────────────────────────────────────────────
        formula = MathTex(
            r"\text{Attention} = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{64}}\right)",
            font_size=32,
            color=WHITE,
        ).to_edge(UP, buff=0.45)
        formula.set_opacity(0)

        # ── "silicon" row highlight background ────────────────────────────
        row5_bg = Rectangle(
            width=N*STEP - GAP + 0.1,
            height=CELL + 0.1,
            fill_color=ROW_HIGHLIGHT,
            fill_opacity=0.0,
            stroke_opacity=0.0,
        ).move_to(origin + np.array([(N-1)*STEP/2, 5*STEP, 0]))

        # ── Row label "silicon" highlight ring ────────────────────────────
        silicon_ring = SurroundingRectangle(
            row_labels[5], color=YELLOW_C, buff=0.06, stroke_width=2
        ).set_opacity(0)

        # ═══════════════════════════════════════════════════════════════════
        # ANIMATION SEQUENCE  —  total ≈ 25 s
        # ═══════════════════════════════════════════════════════════════════

        # 0.0–2.0s  — Axis labels fade in
        self.play(
            FadeIn(col_labels, lag_ratio=0.12),
            FadeIn(row_labels, lag_ratio=0.12),
            FadeIn(key_title),
            FadeIn(query_title),
            run_time=2.0,
        )

        # 2.0–2.8s — brief pause before grid appears
        self.wait(0.8)

        # 2.8–8.0s  — Grid cells materialise row by row (bottom → top)
        # 6 rows × 0.7s each = 4.2s  (slower, more dramatic)
        for r in range(N):
            row_cells = VGroup(*[cell_ref[(r, c)] for c in range(N)])
            self.play(FadeIn(row_cells, lag_ratio=0.10), run_time=0.7)

        # 8.0–9.2s  — Row 5 ("silicon") highlights
        self.play(
            row5_bg.animate.set_fill(opacity=0.18).set_stroke(
                color="#3A6A9A", opacity=0.6, width=1.5
            ),
            row_labels[5].animate.set_color(YELLOW_C),
            silicon_ring.animate.set_opacity(1),
            run_time=1.2,
        )

        # 9.2–13.2s — Silicon row cells flash left-to-right (3.0s total)
        SILICON_ROW = 5
        flash_anims = []
        for c in range(N):
            w = ATTN[SILICON_ROW, c]
            cell = cell_ref[(SILICON_ROW, c)]
            scale = 1.0 + 0.35 * w
            flash_anims.append(
                Succession(
                    cell.animate(rate_func=there_and_back, run_time=0.55)
                        .scale(scale)
                        .set_stroke(color=YELLOW_C, width=3 * w + 0.5),
                )
            )

        self.play(LaggedStart(*flash_anims, lag_ratio=0.30), run_time=3.0)

        # 13.2–14.5s  — Highlight two hottest cells
        highlight_cells = [
            cell_ref[(5, 3)],   # poem — 0.705
            cell_ref[(5, 0)],   # write — 0.263
        ]
        col_highlight_labels = [col_labels[3], col_labels[0]]

        self.play(
            *[cell.animate.set_stroke(color=WHITE, width=3.5)
              for cell in highlight_cells],
            *[lbl.animate.set_color(WHITE)
              for lbl in col_highlight_labels],
            run_time=1.3,
        )

        # 14.5–15.5s — Weight annotations appear
        ann_poem  = Text("0.70", font="Courier New", font_size=15, color=WHITE)\
            .move_to(cell_ref[(5, 3)].get_center())
        ann_write = Text("0.26", font="Courier New", font_size=15, color=WHITE)\
            .move_to(cell_ref[(5, 0)].get_center())

        self.play(
            FadeIn(ann_poem, scale=1.4),
            FadeIn(ann_write, scale=1.4),
            run_time=0.8,
        )

        # 15.5–16.5s — Hold before formula
        self.wait(1.0)

        # 16.5–18.5s — Formula fades in
        self.play(
            formula.animate.set_opacity(1),
            run_time=2.0,
        )

        # 18.5–19.5s — Formula glow pulse
        self.play(formula.animate.set_color(YELLOW_C), run_time=0.5)
        self.play(formula.animate.set_color(WHITE),    run_time=0.5)

        # 20.0–25.0s — Final hold
        self.wait(7.7)


if __name__ == "__main__":
    # Render: manim -pqh attention_matrix.py AttentionMatrix
    pass
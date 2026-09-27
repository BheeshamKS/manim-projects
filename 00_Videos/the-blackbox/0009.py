"""
Positional Encoding — "The Fingerprint Merge"  |  12 seconds
Sentence: "write a poem about silicon"

Retention-based timing model
────────────────────────────────────────────────────────────────────
Stage 1  [embedding] + [position]     0.0 – 2.5 s   (setup — fast)
Stage 2  Tiny waves appear above bars 2.5 – 5.5 s   (subtle, not dominant)
Stage 3  Wave compresses into bar     5.5 – 8.5 s   (merge — satisfying)
Stage 4  Snap to perfect ordered row  8.5 – 12.0 s  (AHA — most time here)
────────────────────────────────────────────────────────────────────

Run:  manim -pqh position_fingerprint.py PositionFingerprint
Voiceover: sync in Kdenlive / Premiere
"""

from manim import *
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#080A12"
CREAM   = "#EDE9E0"
DIM     = "#4B5563"
MUTED   = "#374151"

# Per-token accent colors — each token owns a color, carries it through all stages
TOKEN_COLORS = [
    "#7C6AFA",   # write  — violet
    "#34D399",   # a      — emerald
    "#FBBF24",   # poem   — amber
    "#F87171",   # about  — rose
    "#38BDF8",   # silicon — sky
]

WORDS = ["write", "a", "poem", "about", "silicon"]
N     = len(WORDS)

# Horizontal slot positions — tighter spacing, "silicon" is long
SLOT_X = [(i - 2) * 2.15 for i in range(N)]
BAR_Y  = -0.5    # y-center of the bar group
WAVE_Y = BAR_Y + 1.05  # waves float just above bars


# ── Bar geometry: fixed channel pattern (identical across all tokens) ──────────
CHANNELS   = [0.38, 0.72, 0.28, 0.88, 0.52]   # same for every token
BAR_W      = 0.26
BAR_SPACING= 0.07
BAR_H_MAX  = 1.0


def make_bars(color: str, opacity: float = 0.88) -> VGroup:
    grp = VGroup()
    for i, v in enumerate(CHANNELS):
        r = Rectangle(
            width=BAR_W,
            height=v * BAR_H_MAX,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0,
        )
        r.move_to([i * (BAR_W + BAR_SPACING), 0, 0], aligned_edge=DOWN)
        grp.add(r)
    return grp


def make_wave(color: str, freq: float) -> VMobject:
    """Tiny sine wave — deliberately small so it doesn't dominate."""
    return FunctionGraph(
        lambda x: 0.13 * np.sin(freq * PI * x),
        x_range=[-0.68, 0.68],
        color=color,
        stroke_width=2.2,
        stroke_opacity=0.75,
    )


def make_label(word: str, color: str, size: int = 19) -> Text:
    return Text(word, font="JetBrains Mono", font_size=size, color=color)


# ── Wave frequencies — distinct per position (low-to-high left-to-right) ─────
WAVE_FREQS = [1.2, 1.9, 2.7, 3.6, 4.6]


# ── Scene ─────────────────────────────────────────────────────────────────────

class PositionFingerprint(Scene):

    def construct(self):
        self.camera.background_color = BG

        # ──────────────────────────────────────────────────────────────────────
        # Pre-build all objects so we reference them cleanly across stages
        # ──────────────────────────────────────────────────────────────────────

        labels   = []   # word labels
        bar_grps = []   # VGroup of 5 channel rects each
        waves    = []   # sine wave per token

        for i, (word, col) in enumerate(zip(WORDS, TOKEN_COLORS)):
            lbl = make_label(word, col)
            lbl.move_to([SLOT_X[i], BAR_Y + BAR_H_MAX * 0.7 + 0.55, 0])
            labels.append(lbl)

            bars = make_bars(col)
            bars.move_to([SLOT_X[i], BAR_Y, 0])
            bar_grps.append(bars)

            w = make_wave(col, WAVE_FREQS[i])
            w.move_to([SLOT_X[i], WAVE_Y, 0])
            waves.append(w)

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 1 — [embedding] + [position]       0.0 – 2.5 s
        # Fast setup. Two-line formula fades in, then bars materialize below it.
        # ══════════════════════════════════════════════════════════════════════

        # Formula: show the concept before the visuals
        formula = Text(
            "[embedding]  +  [position]",
            font="JetBrains Mono",
            font_size=22,
            color=DIM,
        ).to_edge(UP, buff=0.38)

        plus_highlight = Text("+", font="JetBrains Mono",
                              font_size=22, color=CREAM)
        plus_highlight.move_to(formula.get_center())   # rough center — cosmetic only

        self.play(FadeIn(formula, shift=DOWN * 0.1), run_time=0.45)
        self.wait(0.3)   # 0.75 s

        # Word labels pop in fast (staggered)
        self.play(
            LaggedStart(*[FadeIn(lbl, shift=UP * 0.1) for lbl in labels],
                        lag_ratio=0.09),
            run_time=0.65,   # 1.4 s
        )

        # Bars grow from zero — cascade
        for bg in bar_grps:
            for r in bg:
                r.save_state()
                r.stretch(0, 1, about_edge=DOWN)

        flat_bars = [r for bg in bar_grps for r in bg]
        self.play(
            LaggedStart(*[Restore(r) for r in flat_bars], lag_ratio=0.03),
            run_time=0.9,   # 2.3 s
        )
        self.wait(0.2)   # 2.5 s ✓

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 2 — Tiny waves appear above each bar   2.5 – 5.5 s
        # Waves are the "position fingerprint". Keep them quiet — supporting
        # cast, not the main character yet.
        # ══════════════════════════════════════════════════════════════════════

        # Dim the formula — not the focus now
        self.play(formula.animate.set_opacity(0.25), run_time=0.3)   # 2.8 s

        # Waves grow in one by one — staggered so each is individually noticed
        self.play(
            LaggedStart(*[Create(w) for w in waves], lag_ratio=0.18),
            run_time=1.4,   # 4.2 s
        )

        # Small label above the wave row — "position fingerprint"
        fp_label = Text("position fingerprint", font="JetBrains Mono",
                        font_size=13, color=DIM, slant=ITALIC)
        fp_label.move_to([0, WAVE_Y + 0.42, 0])
        self.play(FadeIn(fp_label, shift=UP * 0.06), run_time=0.4)   # 4.6 s
        self.wait(0.9)   # 5.5 s ✓

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 3 — Wave compresses into bar           5.5 – 8.5 s
        # The wave "falls into" the bar. Bar color shifts slightly to signal
        # the merge — a tint toward white/brighter. Clean and fast.
        # ══════════════════════════════════════════════════════════════════════

        self.play(FadeOut(fp_label), run_time=0.25)   # 5.75 s

        # For each token: wave moves down into bar, bar brightens
        merge_anims = []
        for i, (w, bg, col) in enumerate(zip(waves, bar_grps, TOKEN_COLORS)):
            # Wave slides down into bar center
            merge_anims.append(
                w.animate.move_to(bg.get_center()).set_opacity(0)
            )

        self.play(
            *merge_anims,
            run_time=1.0,   # 6.75 s
        )

        # Bar color brightens — interpolate each token color toward white
        # by changing fill_color to a lighter version
        BRIGHT = {
            TOKEN_COLORS[0]: "#A89BFB",
            TOKEN_COLORS[1]: "#6EE7B7",
            TOKEN_COLORS[2]: "#FDE68A",
            TOKEN_COLORS[3]: "#FCA5A5",
            TOKEN_COLORS[4]: "#7DD3FC",
        }
        brighten_anims = []
        for bg, col in zip(bar_grps, TOKEN_COLORS):
            for r in bg:
                brighten_anims.append(
                    r.animate.set_fill(BRIGHT[col], opacity=1.0)
                )

        self.play(*brighten_anims, run_time=0.7)   # 7.45 s
        self.wait(0.8)   # 8.25 s ✓  (slight extra hold before snap)

        # ══════════════════════════════════════════════════════════════════════
        # STAGE 4 — SNAP TO PERFECT ORDERED ROW       8.5 – 12.0 s
        #
        # THIS IS THE AHA MOMENT.
        # Everything — labels + bars — snaps into a clean, evenly-spaced
        # horizontal sequence. No fanfare. Just crisp alignment.
        # The viewer's brain reads: ORDER. SEQUENCE. UNDERSTOOD.
        #
        # Hold it. Let it breathe. That's the point.
        # ══════════════════════════════════════════════════════════════════════

        # Final perfectly-ordered positions — tighter, more geometric
        FINAL_X  = [(i - 2) * 2.1 for i in range(N)]
        FINAL_BY  = -0.35     # bars snap slightly higher (cleaner composition)
        FINAL_LY  = FINAL_BY + BAR_H_MAX * 0.7 + 0.58

        snap_anims = []
        for i in range(N):
            snap_anims.append(
                bar_grps[i].animate.move_to([FINAL_X[i], FINAL_BY, 0])
            )
            snap_anims.append(
                labels[i].animate.move_to([FINAL_X[i], FINAL_LY, 0])
            )

        # Also restore formula to full opacity — it's the "answer" now
        snap_anims.append(formula.animate.set_opacity(0.9))

        self.play(
            *snap_anims,
            run_time=0.55,   # snap is fast — that's the point
            rate_func=rush_into,   # accelerates in, stops cleanly
        )
        # 8.8 s

        # Sequence indicator: small numbered dots below bars
        seq_dots = VGroup()
        for i, col in enumerate(TOKEN_COLORS):
            dot = Dot(radius=0.09, color=col, fill_opacity=1)
            num = Text(str(i + 1), font="JetBrains Mono",
                       font_size=12, color=col)
            pair = VGroup(dot, num.next_to(dot, RIGHT, buff=0.04))
            pair.move_to([FINAL_X[i], FINAL_BY - 0.78, 0])
            seq_dots.add(pair)

        # Dots appear in order — left to right — reinforcing SEQUENCE
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in seq_dots], lag_ratio=0.14),
            run_time=0.8,   # 9.6 s
        )

        # Thin horizontal line connecting all dots — the "sequence" is explicit
        seq_line = Line(
            seq_dots[0].get_center(),
            seq_dots[-1].get_center(),
            color=DIM, stroke_width=1.2, stroke_opacity=0.45,
        )
        self.play(Create(seq_line), run_time=0.45)   # 10.05 s

        # Final hold — this is where the voiceover lands
        # "Order isn't built into Transformers. We have to inject it ourselves."
        self.wait(1.95)   # → 12.0 s ✓
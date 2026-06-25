from manim import *
from pathlib import Path

BG    = "#000000"
WHITE = "#E8F1FF"
MUTED = "#7C8DA6"
MONO  = "JetBrains Mono"

ACCENT_BLUE   = "#4FC3F7"   # VS Code blue
ACCENT_YELLOW = "#FFD54F"   # Python yellow
ACCENT_MUTED  = "#7C8DA6"   # arrow / arc color

# Absolute path so Manim finds assets regardless of CWD when invoked
ASSETS = str(Path(__file__).parent.parent.parent / "01_Assets" / "Images")


# Brand colors — hardcoded because SVGMobject cannot restore per-path
# colors from SVGs that use currentColor or have no fill attributes.
VSCODE_BLUE  = "#007ACC"
PY_BLUE      = "#3776AB"
PY_YELLOW    = "#FFD43B"


def color_vscode(svg: SVGMobject) -> SVGMobject:
    """VS Code icon: single flat blue."""
    svg.set_fill(VSCODE_BLUE, opacity=1)
    svg.set_stroke(color=VSCODE_BLUE, width=0)
    return svg


def color_python(svg: SVGMobject) -> SVGMobject:
    """
    Python icon: two interlocked snakes — top snake blue, bottom snake yellow.
    SVGMobject splits the SVG into submobjects in document order.
    Submobject 0 = blue snake body, submobject 1 = yellow snake body.
    If the split differs, both halves will at least be visible.
    """
    submobs = svg.submobjects
    if len(submobs) >= 2:
        submobs[0].set_fill(PY_BLUE,   opacity=1).set_stroke(width=0)
        submobs[1].set_fill(PY_YELLOW, opacity=1).set_stroke(width=0)
    else:
        # Fallback: single-path SVG — use dominant blue
        svg.set_fill(PY_BLUE, opacity=1).set_stroke(width=0)
    return svg


class Shot0005_5(Scene):
    def construct(self):
        self.camera.background_color = BG

        FW = config.frame_width
        FH = config.frame_height

        # ── Icons ────────────────────────────────────────────────────────────
        ICON_H = 1.4

        vscode_icon = SVGMobject(str(Path(ASSETS) / "vs-code.svg"))
        vscode_icon.set_height(ICON_H)
        color_vscode(vscode_icon)

        python_icon = SVGMobject(str(Path(ASSETS) / "python.svg"))
        python_icon.set_height(ICON_H)
        color_python(python_icon)

        # file-py: drawn in black — recolor to WHITE so it shows on dark BG
        file_icon = SVGMobject(str(Path(ASSETS) / "file-py.svg"))
        file_icon.set_height(ICON_H * 0.85)
        file_icon.set_fill(WHITE, opacity=1)
        file_icon.set_stroke(color=WHITE, width=0)

        # Horizontal positions: vscode left, file center, python right
        vscode_icon.move_to(LEFT  * (FW * 0.28))
        file_icon.move_to(  ORIGIN              )
        python_icon.move_to(RIGHT * (FW * 0.28))

        # ── Labels ───────────────────────────────────────────────────────────
        LABEL_FS   = 22
        OVERSAMPLE = 3

        def crisp(txt, color=MUTED):
            t = Text(txt, font=MONO, font_size=LABEL_FS * OVERSAMPLE, color=color)
            t.scale(1 / OVERSAMPLE)
            return t

        lbl_vscode = crisp("VS Code", WHITE)
        lbl_file   = crisp("script.py", MUTED)
        lbl_python = crisp("Python 3.11", WHITE)

        LABEL_GAP = 0.22
        lbl_vscode.next_to(vscode_icon, DOWN, buff=LABEL_GAP)
        lbl_file.next_to(file_icon,     DOWN, buff=LABEL_GAP)
        lbl_python.next_to(python_icon, DOWN, buff=LABEL_GAP)

        # ── Arrow: VSCode → file (solid, "takes the file") ───────────────────
        arrow_vscode_file = Arrow(
            start = vscode_icon.get_right() + RIGHT * 0.1,
            end   = file_icon.get_left()    + LEFT  * 0.1,
            buff             = 0,
            stroke_width     = 2.5,
            color            = ACCENT_BLUE,
            tip_length       = 0.18,
            max_stroke_width_to_length_ratio = 999,
        )

        # ── Dashed arc: VSCode → Python (search path, "finds Python") ────────
        vs_right = vscode_icon.get_right()
        py_left  = python_icon.get_left()

        _arc_base = CubicBezier(
            vs_right + RIGHT * 0.15,
            vs_right + RIGHT * 0.15 + UP * 1.4,
            py_left  + LEFT  * 0.15 + UP * 1.4,
            py_left  + LEFT  * 0.15,
            color        = ACCENT_YELLOW,
            stroke_width = 2.2,
        )
        search_arc = DashedVMobject(_arc_base, num_dashes=18, dashed_ratio=0.55)
        search_arc.set_color(ACCENT_YELLOW)

        # Tiny arrowhead landing on Python icon
        arc_tip = Arrow(
            start = py_left + LEFT  * 0.3 + UP * 0.2,
            end   = py_left + LEFT  * 0.05,
            buff             = 0,
            stroke_width     = 2.2,
            color            = ACCENT_YELLOW,
            tip_length       = 0.16,
            max_stroke_width_to_length_ratio = 999,
        )

        # ── Static layout done — now animate ─────────────────────────────────

        # Beat 1 (0.0–1.0): VS Code fades in
        self.play(
            FadeIn(vscode_icon, shift=UP * 0.15),
            FadeIn(lbl_vscode,  shift=UP * 0.10),
            run_time=0.7,
        )
        self.wait(0.3)

        # Beat 2 (1.0–2.4): file appears, arrow draws
        self.play(
            FadeIn(file_icon, shift=UP * 0.12),
            FadeIn(lbl_file,  shift=UP * 0.08),
            run_time=0.5,
        )
        self.play(
            GrowArrow(arrow_vscode_file),
            run_time=0.7,
        )
        self.wait(0.2)

        # Beat 3 (2.4–4.2): Python appears, dashed arc draws
        self.play(
            FadeIn(python_icon, shift=UP * 0.15),
            FadeIn(lbl_python,  shift=UP * 0.10),
            run_time=0.6,
        )
        self.play(
            Create(search_arc),
            run_time=0.9,
        )
        self.play(
            GrowArrow(arc_tip),
            run_time=0.25,
        )

        # Beat 4 (4.2–5.0): hold
        self.wait(0.9)
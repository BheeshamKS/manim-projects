from manim import *
from pathlib import Path

BG    = "#000000"
WHITE = "#E8F1FF"
MUTED = "#7C8DA6"
MONO  = "JetBrains Mono"

PY_BLUE   = "#3776AB"
PY_YELLOW = "#FFD43B"

ASSETS = str(Path(__file__).parent.parent.parent / "01_Assets" / "Images")

OVERSAMPLE = 3

def crisp(txt, fs=20, color=WHITE):
    t = Text(txt, font=MONO, font_size=fs * OVERSAMPLE, color=color)
    t.scale(1 / OVERSAMPLE)
    return t


class Shot0006_5(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Python icon — two-tone
        py = SVGMobject(str(Path(ASSETS) / "python.svg"))
        py.set_height(2.2)
        submobs = py.submobjects
        if len(submobs) >= 2:
            submobs[0].set_fill(PY_BLUE,   opacity=1).set_stroke(width=0)
            submobs[1].set_fill(PY_YELLOW, opacity=1).set_stroke(width=0)
        else:
            py.set_fill(PY_BLUE, opacity=1).set_stroke(width=0)

        py.move_to(ORIGIN)

        label = crisp("Python 3.11", fs=22, color=MUTED)
        label.next_to(py, DOWN, buff=0.28)

        # Pulse ring — starts small, expands and fades
        ring = Circle(radius=0.1, color=PY_YELLOW, stroke_width=2.5, fill_opacity=0)
        ring.move_to(py.get_center())

        # ── animate ──────────────────────────────────────────────────────────

        # icon + label fade in from slight drop
        self.play(
            FadeIn(py,    shift=UP * 0.18),
            FadeIn(label, shift=UP * 0.10),
            run_time=0.7,
        )
        self.wait(0.2)

        # two pulse rings — "waking up"
        for _ in range(2):
            pulse = ring.copy()
            self.add(pulse)
            self.play(
                pulse.animate.scale(9).set_stroke(opacity=0),
                run_time=0.75,
                rate_func=rush_from,
            )
            self.remove(pulse)

        self.wait(0.5)
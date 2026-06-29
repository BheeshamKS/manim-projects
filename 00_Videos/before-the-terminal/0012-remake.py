from manim import *
from pathlib import Path

# ── tracr identity ────────────────────────────────────────────────────────────
BG    = "#000000"
WHITE = "#E8F1FF"
MUTED = "#7C8DA6"
CYAN  = "#4FC3F7"
GOLD  = "#FFD54F"
MONO  = "JetBrains Mono"

WIN_COLOR   = "#0078D4"
APPLE_COLOR = "#FFFFFF"
ARCH_COLOR  = "#1793D1"
PY_COLOR_1  = "#3776AB"
PY_COLOR_2  = "#FFD43B"

# ── asset paths ───────────────────────────────────────────────────────────────
_ASSETS   = Path(__file__).resolve().parent.parent.parent / "01_Assets" / "Images"
WIN_SVG   = str(_ASSETS / "windows-11.svg")
APPLE_SVG = str(_ASSETS / "apple.svg")
ARCH_SVG  = str(_ASSETS / "arch-linux.svg")
PY_SVG    = str(_ASSETS / "python.svg")

# ── helpers ───────────────────────────────────────────────────────────────────
OVERSAMPLE = 4

def crisp(txt, size, color=WHITE, font=MONO):
    t = Text(txt, font=font, font_size=size * OVERSAMPLE, color=color)
    t.scale(1 / OVERSAMPLE)
    return t


class Shot0012(Scene):
    def construct(self):
        self.camera.background_color = BG

        FW = config.frame_width
        FH = config.frame_height

        # ═══════════════════════════════════════════════════════════════════════
        # BEAT 1  (0–8s)
        # Three OS logos reveal one by one, then hold.
        # VO: "You're probably on Windows, Mac, or Linux."
        # ═══════════════════════════════════════════════════════════════════════
        LOGO_H = 1.6

        win   = SVGMobject(WIN_SVG).set_color(WIN_COLOR).set_height(LOGO_H)
        apple = SVGMobject(APPLE_SVG).set_color(APPLE_COLOR).set_height(LOGO_H)
        arch  = SVGMobject(ARCH_SVG).set_color(ARCH_COLOR).set_height(LOGO_H)

        os_row = VGroup(win, apple, arch)
        os_row.arrange(RIGHT, buff=1.4)
        os_row.move_to(ORIGIN)

        # reveal each logo — 1.2s each = 3.6s
        for logo in os_row:
            self.play(DrawBorderThenFill(logo), run_time=1.2, rate_func=smooth)

        self.wait(3.2)   # hold so VO lands — total ~6.8s

        # ═══════════════════════════════════════════════════════════════════════
        # BEAT 2  (8–14s)
        # Logos shrink + rise. Python logo fades in below.
        # Labels appear. Hold.
        # VO: "The OS is the one actually in charge. Python just works for it."
        # ═══════════════════════════════════════════════════════════════════════
        LOGO_H_SMALL = 0.9
        OS_Y         =  FH * 0.24
        PY_Y         = -FH * 0.24

        py_logo = SVGMobject(PY_SVG)
        if len(py_logo.submobjects) >= 2:
            py_logo.submobjects[0].set_color(PY_COLOR_1)
            py_logo.submobjects[1].set_color(PY_COLOR_2)
        else:
            py_logo.set_color(PY_COLOR_1)
        py_logo.set_height(LOGO_H_SMALL)
        py_logo.move_to([0, PY_Y, 0])
        py_logo.set_opacity(0)

        os_label = crisp("OS", 22, color=MUTED)
        py_label = crisp("Python", 22, color=MUTED)

        # logos rise and shrink
        self.play(
            os_row.animate.scale(LOGO_H_SMALL / LOGO_H).move_to([0, OS_Y, 0]),
            run_time=1.0, rate_func=smooth,
        )
        os_label.next_to(os_row, UP, buff=0.2)
        self.play(FadeIn(os_label, shift=DOWN * 0.12), run_time=0.4)

        # Python rises up into frame
        self.play(
            py_logo.animate.set_opacity(1),
            run_time=1.0, rate_func=smooth,
        )
        py_label.next_to(py_logo, DOWN, buff=0.2)
        self.play(FadeIn(py_label, shift=UP * 0.12), run_time=0.4)

        self.wait(2.2)   # hold — total beat ~5s, running ~12s

        # ═══════════════════════════════════════════════════════════════════════
        # BEAT 3  (14–21s)
        # Cyan arrow grows from Python up to OS.
        # Message text fades in beside arrow. Hold.
        # VO: "So when print finishes, it sends a message up.
        #      OS. Take this string — Hello, World — and write it to the terminal."
        # ═══════════════════════════════════════════════════════════════════════
        up_arrow = Arrow(
            start=py_logo.get_top()   + UP   * 0.18,
            end=os_row.get_bottom()   + DOWN * 0.18,
            color=CYAN,
            stroke_width=3.5,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )

        msg = crisp('"Take this string. Write it."', 20, color=WHITE)
        msg.next_to(up_arrow, RIGHT, buff=0.28)

        self.play(Create(up_arrow), run_time=1.2, rate_func=smooth)
        self.play(FadeIn(msg, shift=LEFT * 0.15), run_time=0.6)
        self.wait(4.2)   # hold — +1s on message beat

        # ═══════════════════════════════════════════════════════════════════════
        # BEAT 4  (21–30s)
        # Swap: arrow + msg fade, new gold arrow goes DOWN to terminal rect.
        # Terminal rect draws in. "Hello, World" types out. Hold.
        # VO: "The OS gets the message. It finds the terminal window inside VS Code.
        #      And it starts sending characters."
        # ═══════════════════════════════════════════════════════════════════════
        term_rect = RoundedRectangle(
            corner_radius=0.12,
            width=4.0,
            height=1.1,
            color=MUTED,
            stroke_width=1.5,
            fill_color=ManimColor.from_hex("#0D1117"),
            fill_opacity=1,
        )
        term_label = crisp("terminal", 18, color=MUTED)
        term_label.move_to(term_rect.get_center())
        term_rect.next_to(os_row, DOWN, buff=2.4)
        term_label.move_to(term_rect.get_center())

        down_arrow = Arrow(
            start=os_row.get_bottom() + DOWN * 0.18,
            end=term_rect.get_top()   + UP   * 0.12,
            color=GOLD,
            stroke_width=3.5,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            FadeOut(up_arrow),
            FadeOut(msg),
            FadeOut(py_logo),
            FadeOut(py_label),
            run_time=0.5,
        )

        self.play(Create(term_rect), run_time=0.6)
        self.play(FadeIn(term_label, shift=UP * 0.1), run_time=0.3)
        self.play(Create(down_arrow), run_time=1.0, rate_func=smooth)
        self.wait(2.0)   # hold — let terminal land before typing

        # type out Hello, World
        chars = "Hello, World"
        typed = crisp(chars, 22, color=CYAN)
        typed.move_to(term_rect.get_center())

        self.play(FadeOut(term_label), run_time=0.2)
        self.play(
            AddTextLetterByLetter(typed, time_per_char=0.28),
            run_time=len(chars) * 0.28,
        )
    
        self.wait(1.5) 

        # ── Outro: staggered fadeout — manim's LaggedStart signature ─────────
        # All remaining mobjects dissolve outward one by one, ~2.5s total
        self.play(
            LaggedStart(
                FadeOut(typed,      shift=DOWN * 0.2),
                FadeOut(term_rect,  shift=DOWN * 0.2),
                FadeOut(down_arrow, shift=DOWN * 0.2),
                FadeOut(os_row,     shift=UP   * 0.2),
                FadeOut(os_label,   shift=UP   * 0.2),
                lag_ratio=0.25,
            ),
            run_time=2.5,
            rate_func=smooth,
        )

        self.wait(0.3)
from manim import *
from pathlib import Path

BG    = "#000000"
WHITE = "#E8F1FF"
MUTED = "#7C8DA6"
MONO  = "JetBrains Mono"

VSCODE_BLUE = "#007ACC"
DIM         = "#2A2F3A"
ACCENT      = "#4FC3F7"

OVERSAMPLE = 3

# Script: 00_Videos/before-the-terminal/0006.5.py
# Asset:  01_Assets/Images/vs-code.svg
VSCODE_SVG = str(Path(__file__).parent.parent.parent / "01_Assets" / "Images" / "vs-code.svg")


def crisp(text, font_size, color=WHITE, **kwargs):
    """Oversample then scale — fixes Pango sub-pixel glyph spacing."""
    t = Text(text, font=MONO, font_size=font_size * OVERSAMPLE, color=color, **kwargs)
    t.scale(1 / OVERSAMPLE)
    return t


class Shot0006_5(Scene):
    """
    Shot 0006.5 — 'Before The Terminal'
    Voiceover: 'VS Code just saves you the trouble. The button is not magic. It's a shortcut.'

    Layout: button LEFT ——arrow——> terminal RIGHT, verdict below centre.
    """

    def construct(self):
        self.camera.background_color = BG

        FW = config.frame_width
        FH = config.frame_height

        # ── 1. BUILD STATIC LAYOUT ────────────────────────────────────────────

        # VS Code button — left side
        vscode_icon = SVGMobject(VSCODE_SVG)
        vscode_icon.set_color(VSCODE_BLUE)
        vscode_icon.scale(0.32)

        btn_label = crisp("Run Python File", font_size=22, color=WHITE)
        btn_label.next_to(vscode_icon, RIGHT, buff=0.18)

        btn_group = VGroup(vscode_icon, btn_label)

        btn_bg = SurroundingRectangle(
            btn_group,
            buff=0.28,
            color=VSCODE_BLUE,
            fill_color=DIM,
            fill_opacity=1,
            corner_radius=0.12,
            stroke_width=1.8,
        )

        button = VGroup(btn_bg, btn_group)
        button.move_to(LEFT * (FW * 0.22))

        # Terminal command — right side
        cmd_text = crisp("python hello.py", font_size=30, color=ACCENT)
        prompt   = crisp("$ ", font_size=30, color=MUTED)
        prompt.next_to(cmd_text, LEFT, buff=0.06)
        terminal_line = VGroup(prompt, cmd_text)

        term_bg = SurroundingRectangle(
            terminal_line,
            buff=0.22,
            color=MUTED,
            fill_color="#0D1117",
            fill_opacity=1,
            corner_radius=0.08,
            stroke_width=1.2,
        )
        terminal_block = VGroup(term_bg, terminal_line)
        terminal_block.move_to(RIGHT * (FW * 0.22))

        # Arrow: button right → terminal left
        arrow = Arrow(
            start=btn_bg.get_right() + RIGHT * 0.05,
            end=term_bg.get_left()   + LEFT  * 0.05,
            color=ACCENT,
            buff=0.1,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.18,
        )

        # Verdict — below centre
        verdict_1 = crisp("not magic.", font_size=26, color=MUTED)
        verdict_2 = crisp("a shortcut.", font_size=26, color=WHITE)
        verdict_group = VGroup(verdict_1, verdict_2).arrange(RIGHT, buff=0.25)
        verdict_group.move_to(DOWN * 2.2)

        # ── 2. ANIMATE ────────────────────────────────────────────────────────

        self.play(FadeIn(button), run_time=0.6)
        self.wait(0.4)

        self.play(GrowArrow(arrow), run_time=0.55, rate_func=smooth)
        self.play(FadeIn(terminal_block), run_time=0.5)
        self.wait(0.5)

        # Button dims — it's the shortcut, not the star
        self.play(
            btn_bg.animate.set_stroke(color=MUTED, width=1.2).set_fill(opacity=0.4),
            vscode_icon.animate.set_opacity(0.4),
            btn_label.animate.set_opacity(0.45),
            run_time=0.6,
        )

        self.play(Write(verdict_1), run_time=0.55, rate_func=smooth)
        self.play(Write(verdict_2), run_time=0.55, rate_func=smooth)
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(button, arrow, terminal_block, verdict_group)),
            run_time=0.5,
        )
from manim import *

# ══════════════════════════════════════════════════════════════════
#  BPE Tokenization Explainer  — ~73 seconds
# ══════════════════════════════════════════════════════════════════

MONO   = "JetBrainsMono Nerd Font"
ACCENT = "#00D9FF"
GREEN  = "#39FF14"
YELLOW = "#FFD700"
RED    = "#FF6B6B"
PURPLE = "#C77DFF"
BG     = "#0D0D0D"

PHOTO_COLOR    = "#00FF41"
LITH_COLOR     = "#CC6600"
OGRAPHY_COLOR  = "#00FF41"

FS = 58


def mono(s, color=WHITE, size=FS):
    return Text(s, font=MONO, font_size=size, color=color)


class BytePairEncoding(MovingCameraScene):

    def construct(self):

        self.camera.background_color = BG

        # cinematic opening pause
        self.wait(2.0)

        self._silicon_section()       # ~20s
        self._photo_section()         # ~22s
        self._vocab_section()         # ~12s
        self._array_section()         # ~19s

    # ─────────────────────────────────────────────────────────────
    #  PART 1 — silicon
    # ─────────────────────────────────────────────────────────────
    def _silicon_section(self):

        word = mono("silicon")
        word.move_to(ORIGIN)

        self.play(
            FadeIn(word, scale=0.85),
            run_time=1.6
        )

        self.wait(2.0)

        # split into sil / icon
        sil  = mono("sil", color=ACCENT)
        icon = mono("icon", color=YELLOW)

        sil.move_to(LEFT * 2.2)
        icon.move_to(RIGHT * 1.9)

        self.play(
            TransformMatchingShapes(
                word,
                VGroup(sil, icon)
            ),
            run_time=2.4
        )

        self.wait(1.5)

        box_sil  = SurroundingRectangle(sil, color=ACCENT, buff=0.18)
        box_icon = SurroundingRectangle(icon, color=YELLOW, buff=0.18)

        self.play(
            Create(box_sil),
            Create(box_icon),
            run_time=1.2
        )

        self.wait(1.0)

        # IDs
        id_sil = mono(
            "35904",
            color=GREEN,
            size=26
        ).next_to(box_sil, DOWN, buff=0.22)

        id_icon = mono(
            "1965",
            color=GREEN,
            size=26
        ).next_to(box_icon, DOWN, buff=0.22)

        self.play(
            FadeIn(id_sil, shift=DOWN * 0.25),
            FadeIn(id_icon, shift=DOWN * 0.25),
            run_time=1.2
        )

        self.wait(2.0)

        # underscore enters
        underscore = mono("_", color=RED)

        underscore.next_to(box_sil, LEFT, buff=0.05)
        underscore.shift(LEFT * 3.5)

        self.play(
            underscore.animate.next_to(
                box_sil,
                LEFT,
                buff=0.05
            ),
            run_time=2.0
        )

        self.wait(1.5)

        # merge
        merged = mono("[_silicon]", color=WHITE)
        merged.move_to(ORIGIN)

        merged_id = mono(
            "51692",
            color=GREEN,
            size=30
        )

        merged_id.next_to(
            merged,
            DOWN,
            buff=0.28
        )

        self.play(
            TransformMatchingShapes(
                VGroup(
                    underscore,
                    sil,
                    box_sil,
                    icon,
                    box_icon
                ),
                merged
            ),

            TransformMatchingShapes(
                VGroup(id_sil, id_icon),
                merged_id
            ),

            run_time=2.5
        )

        self.wait(1.5)

        self.play(
            Flash(
                merged_id,
                color=GREEN,
                flash_radius=0.55
            ),
            run_time=0.8
        )

        self.wait(2.5)

        # clear
        self.play(
            FadeOut(merged),
            FadeOut(merged_id),
            run_time=1.0
        )

        self.wait(1.2)

    # ─────────────────────────────────────────────────────────────
    #  PART 2 — photolithography
    # ─────────────────────────────────────────────────────────────
    def _photo_section(self):

        word = mono(
            "photolithography",
            size=46
        )

        word.move_to(ORIGIN)

        self.play(
            FadeIn(word, shift=UP * 0.2),
            run_time=1.4
        )

        self.wait(2.0)

        # fragments
        frag_photo = mono(
            "photo",
            color=PHOTO_COLOR,
            size=46
        )

        frag_lith = mono(
            "lith",
            color=LITH_COLOR,
            size=46
        )

        frag_ography = mono(
            "ography",
            color=OGRAPHY_COLOR,
            size=46
        )

        frag_photo.move_to(LEFT * 4.0)
        frag_lith.move_to(ORIGIN)
        frag_ography.move_to(RIGHT * 4.2)

        self.play(
            TransformMatchingShapes(
                word,
                VGroup(
                    frag_photo,
                    frag_lith,
                    frag_ography
                )
            ),
            run_time=3.0
        )

        self.wait(1.8)

        # boxes
        box_p = SurroundingRectangle(
            frag_photo,
            color=PHOTO_COLOR,
            buff=0.18
        )

        box_l = SurroundingRectangle(
            frag_lith,
            color=LITH_COLOR,
            buff=0.18
        )

        box_o = SurroundingRectangle(
            frag_ography,
            color=OGRAPHY_COLOR,
            buff=0.18
        )

        self.play(
            Create(box_p),
            Create(box_l),
            Create(box_o),
            run_time=1.4
        )

        self.wait(1.0)

        # IDs
        id_p = mono(
            "4604",
            color=PHOTO_COLOR,
            size=24
        ).next_to(box_p, DOWN, buff=0.2)

        id_l = mono(
            "48218",
            color=LITH_COLOR,
            size=24
        ).next_to(box_l, DOWN, buff=0.2)

        id_o = mono(
            "5814",
            color=OGRAPHY_COLOR,
            size=24
        ).next_to(box_o, DOWN, buff=0.2)

        self.play(
            FadeIn(id_p, shift=DOWN * 0.2),
            run_time=1.0
        )

        self.wait(1.3)

        self.play(
            FadeIn(id_l, shift=DOWN * 0.2),
            run_time=1.0
        )

        self.wait(1.5)

        self.play(
            FadeIn(id_o, shift=DOWN * 0.2),
            run_time=1.0
        )

        self.wait(3.0)

        self.play(
            FadeOut(
                VGroup(
                    frag_photo,
                    frag_lith,
                    frag_ography,
                    box_p,
                    box_l,
                    box_o,
                    id_p,
                    id_l,
                    id_o
                )
            ),
            run_time=1.2
        )

        self.wait(1.5)

    # ─────────────────────────────────────────────────────────────
    #  PART 3 — vocab scaling
    # ─────────────────────────────────────────────────────────────
    def _vocab_section(self):

        gpt2_lbl = mono(
            "GPT-2",
            size=36
        )

        gpt2_num = mono(
            "(50,257)",
            size=36,
            color=ACCENT
        )

        gpt2 = VGroup(
            gpt2_lbl,
            gpt2_num
        ).arrange(
            RIGHT,
            buff=0.2
        )

        gpt2.move_to(LEFT * 3.2)

        self.play(
            FadeIn(gpt2, shift=UP * 0.25),
            run_time=1.0
        )

        self.wait(1.5)

        arrow = Arrow(
            gpt2.get_right() + RIGHT * 0.15,
            gpt2.get_right() + RIGHT * 2.8,
            color=WHITE,
            stroke_width=3,
            buff=0
        )

        self.play(
            GrowArrow(arrow),
            run_time=1.2
        )

        self.wait(0.8)

        gpt4_lbl = mono(
            "GPT-4",
            size=36
        )

        gpt4_lbl.next_to(
            arrow.get_end(),
            RIGHT,
            buff=0.2
        )

        self.play(
            FadeIn(gpt4_lbl),
            run_time=0.8
        )

        self.wait(0.5)

        tracker = ValueTracker(50257)

        gpt4_num = always_redraw(
            lambda: mono(
                f"({int(tracker.get_value()):,})",
                size=36,
                color=YELLOW
            ).next_to(
                gpt4_lbl,
                RIGHT,
                buff=0.2
            )
        )

        self.add(gpt4_num)

        self.play(
            tracker.animate.set_value(100258),
            run_time=5.5,
            rate_func=linear
        )

        self.wait(2.5)

        vocab_grp = VGroup(
            gpt2,
            arrow,
            gpt4_lbl,
            gpt4_num
        )

        self.play(
            FadeOut(vocab_grp),
            run_time=1.0
        )

        self.wait(1.0)

    # ─────────────────────────────────────────────────────────────
    #  PART 4 — token segmentation
    # ─────────────────────────────────────────────────────────────
    def _array_section(self):

        cb_colors = [
            "#4477AA",
            "#EE6677",
            "#228833",
            "#AA3377",
            "#66CCEE",
            "#BBBBBB"
        ]

        token_ids = [
            "8144",
            "264",
            "33894",
            "922",
            "51692",
            "13"
        ]

        full_text = "Write_a_poem_about_silicon."

        prompt_text = Text(
            full_text,
            font="Monospace",
            color=WHITE
        )

        prompt_text.move_to(UP * 0.5)

        token_slices = [
            prompt_text[0:5],
            prompt_text[5:7],
            prompt_text[7:12],
            prompt_text[12:18],
            prompt_text[18:26],
            prompt_text[26:27],
        ]

        brackets = VGroup()
        id_labels = VGroup()

        for t_mob, color, t_id in zip(
            token_slices,
            cb_colors,
            token_ids
        ):

            bracket = Brace(
                t_mob,
                direction=DOWN,
                buff=0.1
            )

            bracket.set_color(color)
            brackets.add(bracket)

            label = MathTex(t_id).scale(0.8)

            label.set_color(color)
            label.next_to(
                bracket,
                DOWN,
                buff=0.2
            )

            id_labels.add(label)

        # prompt
        self.play(
            FadeIn(prompt_text, shift=UP * 0.2),
            run_time=2.0
        )

        self.wait(1.5)

        # brackets
        for bracket in brackets:

            self.play(
                GrowFromCenter(bracket),
                run_time=0.6
            )

            self.wait(0.35)

        self.wait(1.5)

        # IDs
        for i, label in enumerate(id_labels):

            self.play(
                FadeIn(label, shift=UP * 0.1),
                run_time=0.6
            )

            if i < len(id_labels) - 1:
                self.wait(0.45)

        self.wait(3.0)

        # highlight silicon token
        self.play(
            Indicate(
                token_slices[4],
                color=YELLOW
            ),

            Indicate(
                id_labels[4],
                color=YELLOW,
                scale_factor=1.3
            ),

            run_time=2.0
        )

        self.wait(4.0)
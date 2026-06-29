from manim import *


# 600 frames @ 24 FPS = exactly 25.0 seconds


class ASTConstruction(Scene):
    def construct(self):

        # --------------------------------------------------
        # Colors
        # --------------------------------------------------

        BG    = "#000000"
        TEXT  = "#F0F4FF"
        MUTED = "#6B7A99"
        CYAN  = "#00E5FF"
        PINK  = "#FF2D95"
        GOLD  = "#FFB800"
        LIME  = "#39FF14"
        MONO  = "JetBrains Mono"

        self.camera.background_color = BG

        # --------------------------------------------------
        # Box factory (outline only)
        # --------------------------------------------------

        def make_box(text, width, height=0.65, color=MUTED, sw=1.5):
            rect = RoundedRectangle(
                corner_radius=0.12, width=width, height=height,
                stroke_color=color, stroke_width=sw,
                fill_opacity=0,
            )
            label = Text(text, font=MONO, font_size=24, color=TEXT)
            label.move_to(rect)
            return VGroup(rect, label)

        # --------------------------------------------------
        # Build boxes
        # --------------------------------------------------

        box_print = make_box("print", 2.4, sw=2.5)
        box_lp    = make_box("(", 0.7)
        box_hello = make_box('"Hello, World"', 4.6, sw=2.5)
        box_rp    = make_box(")", 0.7)

        boxes = VGroup(box_print, box_lp, box_hello, box_rp)
        boxes.arrange(RIGHT, buff=0.2)
        boxes.move_to(ORIGIN).shift(DOWN * 1.0)

        # --------------------------------------------------
        # Role labels (appear above boxes)
        # --------------------------------------------------

        func_label = Text(
            "function", font=MONO, font_size=22, color=CYAN,
        )
        func_label.next_to(box_print, UP, buff=0.2)
        func_label.set_opacity(0)

        arg_label = Text(
            "argument", font=MONO, font_size=22, color=GOLD,
        )
        arg_label.next_to(box_hello, UP, buff=0.2)
        arg_label.set_opacity(0)

        # --------------------------------------------------
        # Connection lines (boxes → role labels)
        # --------------------------------------------------

        line_func = Line(
            box_print.get_top(), func_label.get_bottom(),
            color=CYAN, stroke_width=2.5,
        )
        line_func.set_opacity(0)

        line_arg = Line(
            box_hello.get_top(), arg_label.get_bottom(),
            color=GOLD, stroke_width=2.5,
        )
        line_arg.set_opacity(0)

        # --------------------------------------------------
        # Tree structure (above roles)
        # --------------------------------------------------

        def make_tree_node(text, color, width=2.6, height=0.6):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.1,
                stroke_color=color, stroke_width=2.5,
                fill_opacity=0,
            )
            txt = Text(text, font=MONO, font_size=22, color=TEXT)
            txt.move_to(rect)
            return VGroup(rect, txt)

        call_node = make_tree_node("Call", LIME, width=2.4)
        call_node.move_to(UP * 1.4)
        call_node.set_opacity(0)

        # Lines from role labels to Call
        line_func_call = Line(
            func_label.get_top(), call_node.get_bottom(),
            color=CYAN, stroke_width=2.5,
        )
        line_func_call.set_opacity(0)

        line_arg_call = Line(
            arg_label.get_top(), call_node.get_bottom(),
            color=GOLD, stroke_width=2.5,
        )
        line_arg_call.set_opacity(0)

        tree_group = VGroup(
            call_node, line_func_call, line_arg_call,
            func_label, arg_label,
            line_func, line_arg,
        )

        # ==========================================================
        # TIMELINE  (25.0 seconds)
        # ==========================================================

        # --- Act 1: Boxes appear (0.0 - 3.0s) ---
        # "But boxes alone are not enough."

        self.play(
            LaggedStart(
                *[FadeIn(b, shift=UP * 0.12) for b in boxes],
                lag_ratio=0.12,
            ),
            run_time=1.8,
        )
        self.wait(1.2)

        # --- Act 2: Isolation (3.0 - 6.0s) ---
        # "Python still doesn't know what they mean together."

        for b in boxes:
            self.play(
                Indicate(b, color=MUTED, scale_factor=1.04),
                run_time=0.35,
            )
            self.wait(0.15)
        self.wait(0.8)

        # --- Act 3: Roles emerge (6.0 - 10.0s) ---
        # "Now Python takes those boxes and works out how they
        #  relate to each other."

        # print lights up cyan + function label
        self.play(
            box_print[0].animate.set_stroke(color=CYAN, width=3.0),
            run_time=0.5,
        )

        self.play(
            line_func.animate.set_opacity(0.6),
            FadeIn(func_label, shift=DOWN * 0.08),
            run_time=0.8,
        )
        self.wait(0.2)

        # hello lights up gold + argument label
        self.play(
            box_hello[0].animate.set_stroke(color=GOLD, width=3.0),
            run_time=0.5,
        )

        self.play(
            line_arg.animate.set_opacity(0.6),
            FadeIn(arg_label, shift=DOWN * 0.08),
            run_time=0.8,
        )
        self.wait(0.2)

        # Pause — let the relationship sink in
        self.play(
            Indicate(VGroup(box_print, func_label), color=CYAN, scale_factor=1.03),
            Indicate(VGroup(box_hello, arg_label), color=GOLD, scale_factor=1.03),
            run_time=0.6,
        )
        self.wait(0.4)

        # --- Act 4: Tree grows (10.0 - 16.0s) ---
        # "`print` is a function. Someone is calling it."
        # "`Hello, World` is what's being passed to it."
        # "So Python draws a map. A tree."

        self.play(
            line_func_call.animate.set_opacity(0.7),
            line_arg_call.animate.set_opacity(0.7),
            run_time=0.8,
        )

        self.play(
            call_node.animate.set_opacity(1),
            run_time=0.8,
        )

        # Call node pulse — the "aha" moment
        self.play(
            call_node[0].animate.set_stroke(width=3.5),
            call_node.animate.scale(1.08),
            run_time=0.5,
            rate_func=there_and_back,
        )
        self.wait(0.4)

        # Paren boxes dim — they're now just syntax
        self.play(
            box_lp.animate.set_opacity(0.35),
            box_rp.animate.set_opacity(0.35),
            run_time=0.5,
        )
        self.wait(1.2)

        # --- Act 5: Each box finds its place (15.5 - 20.0s) ---
        # "Each box finds its place."

        self.play(
            Indicate(VGroup(box_print, func_label), color=CYAN, scale_factor=1.04),
            run_time=0.4,
        )
        self.wait(0.15)
        self.play(
            Indicate(VGroup(box_hello, arg_label), color=GOLD, scale_factor=1.04),
            run_time=0.4,
        )
        self.wait(0.15)
        self.play(
            Indicate(call_node, color=LIME, scale_factor=1.06),
            run_time=0.5,
        )
        self.wait(0.3)

        # Slight tighten — everything breathes into alignment
        self.play(
            tree_group.animate.shift(DOWN * 0.1),
            boxes.animate.shift(UP * 0.08),
            run_time=0.8,
        )
        self.wait(1.2)

        # --- Act 6: Hold (20.0 - 25.0s) ---
        self.wait(5.0)

from manim import *

# 672 frames @ 24 FPS = exactly 28.0 seconds

class ASTTreeScene(Scene):
    def construct(self):

        # --------------------------------------------------
        # Colors
        # --------------------------------------------------

        BG = "#000000"
        TEXT = "#E8F1FF"
        MUTED = "#7C8DA6"
        CYAN = "#00C2FF" 
        GOLD = "#F4B942"
        GREEN = "#4DDD70"

        self.camera.background_color = BG

        # --------------------------------------------------
        # Node helper
        # --------------------------------------------------

        def make_node(text, border_color, width=None):

            if width is None:
                width = max(2.8, len(text) * 0.15)

            rect = RoundedRectangle(
                width=width,
                height=0.75,
                corner_radius=0.15,
                stroke_color=border_color,
                stroke_width=2.5,
                fill_opacity=0,
            )

            txt = Text(
                text,
                font_size=24,
                color=TEXT,
            )

            txt.move_to(rect)

            return VGroup(rect, txt)

        # --------------------------------------------------
        # Tree nodes
        # --------------------------------------------------

        program = make_node("Program", MUTED, width=3.0)
        expression = make_node("Expression", MUTED, width=3.2)
        call = make_node("Call", CYAN, width=2.5)

        name_node = make_node(
            "Name: print",
            CYAN,
            width=3.8,
        )

        string_node = make_node(
            'String: "Hello, World"',
            GOLD,
            width=5.8,
        )

        # --------------------------------------------------
        # Layout (no overlap)
        # --------------------------------------------------

        program.move_to(UP * 2.0)

        expression.move_to(UP * 0.4)

        call.move_to(DOWN * 0.8)

        name_node.move_to(LEFT * 3.8 + DOWN * 2.8)

        string_node.move_to(RIGHT * 4.2 + DOWN * 2.8)

        # --------------------------------------------------
        # Connections
        # --------------------------------------------------

        def connect(parent, child):
            return Line(
                parent.get_bottom(),
                child.get_top(),
                color=MUTED,
                stroke_width=2,
            )

        l1 = connect(program, expression)
        l2 = connect(expression, call)
        l3 = connect(call, name_node)
        l4 = connect(call, string_node)

        # --------------------------------------------------
        # Tree build
        # --------------------------------------------------

        self.play(
            FadeIn(program),
            run_time=2.0,
        )

        self.play(
            Create(l1),
            FadeIn(expression),
            run_time=2.5,
        )

        self.play(
            Create(l2),
            FadeIn(call),
            run_time=3.0,
        )

        self.play(
            Create(l3),
            FadeIn(name_node),
            run_time=3.0,
        )

        self.play(
            Create(l4),
            FadeIn(string_node),
            run_time=3.0,
        )

        # --------------------------------------------------
        # Tree complete hold 
        # (Tree build ends at 13.5s. We wait 8.0s so the next 
        # animation finishes exactly at the 23.0s mark)
        # --------------------------------------------------
        
        self.wait(8.0)

        # --------------------------------------------------
        # Transition everything out (Ends at 23.0s)
        # --------------------------------------------------

        tree_group = VGroup(
            program,
            expression,
            call,
            name_node,
            string_node,
            l1,
            l2,
            l3,
            l4,
        )

        self.play(
            tree_group.animate.scale(0.1).move_to(ORIGIN),
            run_time=1.5,
        )
        
        # This completely deletes the tiny speck so it doesn't overlap the text
        self.remove(tree_group)

        # --------------------------------------------------
        # AST reveal (Starts exactly at 23.0s)
        # --------------------------------------------------

        ast_title = Text(
            "AST",
            font_size=60,
            color=TEXT,
        )

        ast_sub = Text(
            "Abstract Syntax Tree",
            font_size=28,
            color=MUTED,
        )

        ast_tag = Text(
            "it's a map",
            font_size=24,
            color=GREEN,
        )

        ast_group = VGroup(
            ast_title,
            ast_sub,
            ast_tag,
        ).arrange(
            DOWN,
            buff=0.25,
        )

        ast_group.move_to(ORIGIN)

        self.play(
            Write(ast_title),
            run_time=1.0,
        )

        self.play(
            Write(ast_sub),
            run_time=1.0,
        )

        self.play(
            Write(ast_tag),
            run_time=0.8,
        )

        self.wait(2.2)

        # --------------------------------------------------
        # Total duration:
        # Build: 13.5s
        # Hold: 8.0s
        # Transition out: 1.5s
        # --- (Everything clears exactly at the 23.0 seconds mark) ---
        # AST Reveal: 2.8s
        # Final Hold: 2.2s
        # = 28.0 seconds total
        # = 672 frames @ 24 FPS
from manim import *

class FlashAttention(MovingCameraScene):
    def construct(self):
        # ---------------------------------------------------------
        # 1. The Trivial 6x6 Attention Matrix
        # ---------------------------------------------------------
        # Create a 6x6 grid of squares
        small_grid = VGroup(*[
            VGroup(*[Square(side_length=0.5).set_stroke(width=2, color=BLUE_A).set_fill(BLUE_E, opacity=0.8) for _ in range(6)])
            .arrange(RIGHT, buff=0)
            for _ in range(6)
        ]).arrange(DOWN, buff=0)
        
        self.play(FadeIn(small_grid), run_time=1.5)
        self.wait(1.5)

        # ---------------------------------------------------------
        # 2. Scaling Out to the Massive Grid (Memory Strain)
        # ---------------------------------------------------------
        # We use a 32x32 grid to visually represent the 100k x 100k matrix
        dense_grid = VGroup(*[
            VGroup(*[Square(side_length=0.15).set_stroke(width=0.5, color=DARK_GRAY).set_fill(RED_E, opacity=0.9) for _ in range(32)])
            .arrange(RIGHT, buff=0)
            for _ in range(32)
        ]).arrange(DOWN, buff=0)
        
        dense_grid.move_to(ORIGIN)

        # Pull the camera back and swap the grids
        self.play(
            self.camera.frame.animate.scale(2.5),
            FadeOut(small_grid),
            FadeIn(dense_grid),
            run_time=2.5
        )

        # Add text indicating the O(n^2) problem
        strain_text = Text("100,000 x 100,000 Matrix", color=RED_A).scale(1.5)
        strain_sub = Text("O(n²) Memory Strain", color=RED).scale(1.2)
        text_group = VGroup(strain_text, strain_sub).arrange(DOWN, buff=0.3)
        text_group.next_to(dense_grid, UP, buff=0.8)

        self.play(Write(text_group), run_time=1.5)
        self.wait(2)

        # ---------------------------------------------------------
        # 3. FlashAttention & SRAM Tiling
        # ---------------------------------------------------------
        # Update text
        flash_text = Text("FlashAttention: SRAM Tiling", color=BLUE_B).scale(1.5).move_to(text_group)
        
        # Drop down strict white grid lines to divide into 4x4 macro-tiles (each containing 8x8 squares)
        tile_lines = VGroup()
        step = dense_grid.width / 4
        start_x = dense_grid.get_left()[0]
        start_y = dense_grid.get_top()[1]

        for i in range(5):
            # Vertical lines
            v_line = Line(
                start=np.array([start_x + i*step, dense_grid.get_top()[1], 0]),
                end=np.array([start_x + i*step, dense_grid.get_bottom()[1], 0]),
                color=WHITE, stroke_width=6
            )
            # Horizontal lines
            h_line = Line(
                start=np.array([dense_grid.get_left()[0], start_y - i*step, 0]),
                end=np.array([dense_grid.get_right()[0], start_y - i*step, 0]),
                color=WHITE, stroke_width=6
            )
            tile_lines.add(v_line, h_line)

        self.play(
            FadeOut(text_group),
            FadeIn(flash_text),
            Create(tile_lines),
            run_time=2
        )

        # ---------------------------------------------------------
        # 4. Block-by-Block Computation
        # ---------------------------------------------------------
        # Zoom camera in slightly on the top-left section to show the optimization
        self.play(
            self.camera.frame.animate.scale(0.6).move_to(dense_grid.get_corner(UL) + RIGHT*step*1.2 + DOWN*step*1.2),
            run_time=2
        )

        # Iterate through the 16 tiles (4 rows, 4 columns)
        for row in range(4):
            for col in range(4):
                # Gather the exact squares that make up the current tile
                tile_squares = VGroup()
                for r in range(row * 8, (row + 1) * 8):
                    for c in range(col * 8, (col + 1) * 8):
                        tile_squares.add(dense_grid[r][c])

                # Create a surrounding highlight rectangle
                box = SurroundingRectangle(tile_squares, color=YELLOW, buff=0.02, stroke_width=8)

                # Speeds up slightly as it goes to signify rapid parallel/tiled processing
                anim_time = max(0.15, 0.4 - (row * 4 + col) * 0.015)

                self.play(Create(box), run_time=anim_time)
                # Cool the active block back down to blue
                self.play(
                    tile_squares.animate.set_fill(BLUE_E, opacity=0.9),
                    FadeOut(box),
                    run_time=anim_time
                )

        # ---------------------------------------------------------
        # 5. Final Pull-back
        # ---------------------------------------------------------
        # Zoom back out to reveal the fully computed, stable matrix
        self.play(
            self.camera.frame.animate.scale(1 / 0.6).move_to(ORIGIN),
            run_time=2.5
        )
        self.wait(2)
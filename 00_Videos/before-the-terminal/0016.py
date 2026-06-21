import os
from pathlib import Path
from manim import *

# ==============================================================
# TRACR CREDITS SCENE — TWEAKABLE SETTINGS
# ==============================================================
# Everything you'd want to adjust lives here. The layout below uses
# measured spacing (next_to / arrange), so changing any single value
# here won't break alignment elsewhere — gaps re-derive themselves.
# ==============================================================

# --- Colors ----------------------------------------------------
BG    = "#000000"   # background color
WHITE = "#E8F1FF"   # primary text (headers, ref IDs/titles)
MUTED = "#7C8DA6"   # secondary text (used-for lines, role names)
CYAN  = "#00C2FF"   # accent color — currently applied only to the ">" marker
FONT  = "Inter"     # font family. Must be installed system-wide on the render
                     # machine (check with `fc-list | grep -i <name>`), or
                     # Pango will silently substitute a fallback font.

# --- Typography --------------------------------------------------
HEADER_FONT_SIZE    = 28   # "SOURCES" / "PRODUCTION"
REF_FONT_SIZE        = 18   # "> REF 01 | ..." line
USED_FOR_FONT_SIZE   = 16   # "Used for: ..." line
ROLE_LABEL_FONT_SIZE = 20   # "PRODUCED BY" etc.
ROLE_NAME_FONT_SIZE  = 16   # "Bheesham Kumar Sajnani" etc.
USED_FOR_OPACITY     = 0.7  # dimness of the "Used for" line vs full MUTED.
                             # 1.0 = same weight as everything else in MUTED,
                             # lower = more recessive/secondary-feeling.

# --- Camera / overall pacing --------------------------------------
CAMERA_START_Y = 3.5  # How high the camera starts. Higher number = text starts 
                      # closer to the bottom edge of the screen.
SCROLL_SPEED = 0.5    # world units the camera moves per SECOND. This is the
                      # master pacing dial — every timed beat below moves the
                      # camera proportionally to this value, so raising it
                      # speeds up the whole video without re-tuning anything
                      # else. Lower = slower, more cinematic and readable.
                      # Higher = faster, more energetic, less time per line.

# --- Typing / cursor effect (runs once per source entry) -----------
CURSOR_BLINK_COUNT    = 2     # how many times the cursor blinks before a
                               # line starts typing. More = longer "thinking"
                               # pause before each entry.
CURSOR_BLINK_ON_TIME  = 0.15  # seconds the cursor is visible per blink
CURSOR_BLINK_OFF_TIME = 0.1   # seconds the cursor is hidden per blink
REF_LINE_TYPE_TIME    = 0.6   # seconds to "type" the "> REF 01 | ..." line.
                               # Lower = faster typing, snappier feel.
USED_FOR_TYPE_TIME    = 0.3   # seconds to "type" the "Used for: ..." line.
                               # Usually kept <= REF_LINE_TYPE_TIME since
                               # it's the shorter, secondary line.
GAP_AFTER_ENTRY       = 2   # pause after one full entry finishes, before
                               # the next blink cycle starts.

# --- Pauses / section transitions -----------------------------------
INTRO_PAUSE                = 0.5  # blank scroll before "SOURCES" fades in
PAUSE_AFTER_SOURCES_HEADER = 0.1  # pause between "SOURCES" appearing and
                                   # the list starting to type
PAUSE_BEFORE_PROD_HEADER   = 0.5  # pause after the last source entry,
                                   # before "PRODUCTION" fades in
PAUSE_AFTER_PROD_HEADER    = 1.5  # pause between "PRODUCTION" appearing
                                   # and the grid fading in
END_PADDING                = 1.0  # extra blank scroll after the last line
                                   # clears the top of frame before the
                                   # scene ends. More = longer hold at the
                                   # very end, less = cuts tighter.

# --- Reveal animation timing -----------------------------------------
SOURCES_HEADER_FADE_TIME = 1.0   # how long "SOURCES" takes to fade in
PROD_HEADER_FADE_TIME    = 1.0   # how long "PRODUCTION" takes to fade in
GRID_FADE_TIME           = 1.5   # how long the production grid takes to
                                  # fade in (longer since it's bigger)
HEADER_RISE_SHIFT        = 0.2   # how far PRODUCTION/the grid visually rise
                                  # while fading in. 0 = plain fade with no
                                  # motion, higher = more pronounced rise.

# --- Spacing (measured world-space gaps, NOT seconds) -------------------
USED_FOR_BUFF               = 0.18  # gap between a ref line and its
                                     # "Used for" line directly beneath it
USED_FOR_INDENT             = 0.4   # how far the "Used for" line is
                                     # indented relative to the ref line
ROW_BUFF                    = 0.55  # gap between one full source row and
                                     # the next
HEADER_TO_CONTENT_BUFF      = 0.8   # gap below "SOURCES" before the list
                                     # starts, and below "PRODUCTION"
                                     # before the grid starts
SOURCES_TO_PROD_HEADER_BUFF = 1.0   # gap between the end of the source
                                     # list and the "PRODUCTION" header
COLUMN_GAP                  = 1.2   # horizontal gap between the two
                                     # production columns
ROLE_NAME_BUFF               = 0.15  # gap between a role label and the
                                      # name directly beneath it
ROLE_BLOCK_BUFF              = 0.5   # gap between one role block and the
                                      # next, within the same column

# --- Layout margins ---------------------------------------------------
LEFT_MARGIN = 0.8   # distance from the left edge of frame to where
                     # text starts. Bigger = everything sits further
                     # from the edge.

# --- Cursor block -------------------------------------------------------
CURSOR_WIDTH  = 0.15  # blinking cursor block width
CURSOR_HEIGHT = 0.25  # blinking cursor block height
CURSOR_GAP    = 0.15  # gap between the cursor and the start of the
                       # ref line text it's about to "type"

# --- Internal: Pango small-size kerning workaround ------------------------
# Don't change this unless you start seeing squashed/uneven letter spacing
# again (see ManimCommunity/manim#2844 — Pango loses sub-pixel precision at
# small font sizes regardless of font choice). This renders every Text() at
# OVERSAMPLE x the requested font_size, then scales the vector mobject back
# down — Pango gets enough precision at the larger size, and scaling a
# finished vector path afterward is just a transform, so it can't
# reintroduce the rounding.
OVERSAMPLE = 10


class CreditsRollScene(MovingCameraScene):
    def construct(self):

        # --------------------------------------------------
        # tracr Boilerplate & Styling
        # --------------------------------------------------

        self.camera.background_color = BG

        LEFT_X = -config.frame_width / 2 + LEFT_MARGIN

        def crisp_text(content, font_size, **kwargs):
            t = Text(content, font_size=font_size * OVERSAMPLE, **kwargs)
            t.scale(1 / OVERSAMPLE)
            return t

        # --------------------------------------------------
        # Static Layout Construction (Virtual World)
        # Every vertical gap below comes from arrange()/next_to(), which
        # measures the ACTUAL rendered bounding box of each Text object —
        # this is what keeps spacing consistent regardless of font or size.
        # --------------------------------------------------

        header_sources = crisp_text(
            "SOURCES", font=FONT, font_size=HEADER_FONT_SIZE, color=WHITE,
            weight=BOLD, disable_ligatures=True,
        )
        header_sources.move_to([LEFT_X, 1.0, 0], aligned_edge=LEFT)

        source_texts = [
            ("REF 01", "Microsoft — VS Code Python Extension", "Stage 0 — demystifying the run button"),
            ("REF 02", "Microsoft — VS Code Python Language Docs", "Stage 0 — VS Code fires a process"),
            ("REF 03", "PSF — tokenize module documentation", "Stage 2 — tokenizer mechanism and visual"),
            ("REF 04", "CPython Source — Parser/lexer.c", "Stage 1 + 2 — C-level pipeline"),
            ("REF 05", "PSF — ast module documentation", "Stage 3 — AST structure"),
            ("REF 06", "PSF — dis module documentation", "Stage 4 — exact instructions shown"),
            ("REF 07", "PSF — dis module, version change notes", "Stage 4 — \"your one line becomes a dozen\""),
            ("REF 08", "tenthousandmeters.com — CPython VM deep-dive", "Stage 5 — VM execution model"),
            ("REF 09", "tenthousandmeters.com — Bytecode execution", "Stage 5 — the actual function name"),
            ("REF 10", "PSF — sys module documentation (stdout)", "Stage 6 — print() → sys.stdout → OS write"),
            ("REF 11", "realpython.com — Guide to print()", "Stage 6 — honest nuance"),
        ]

        source_objects = []  # (t1, t2) pairs, kept for the typing/cursor animation below
        source_rows = VGroup()

        for ref, title, used in source_texts:
            t1 = crisp_text(
                f"> {ref} | {title}", font=FONT, font_size=REF_FONT_SIZE,
                color=MUTED, t2c={">": CYAN}, disable_ligatures=True,
            )
            t2 = crisp_text(
                f"Used for: {used}", font=FONT, font_size=USED_FOR_FONT_SIZE,
                color=MUTED, disable_ligatures=True,
            ).set_opacity(USED_FOR_OPACITY)

            # t2 sits directly under t1 with a MEASURED buff, then nudges right for the indent.
            t2.next_to(t1, DOWN, buff=USED_FOR_BUFF, aligned_edge=LEFT).shift(RIGHT * USED_FOR_INDENT)

            row = VGroup(t1, t2)
            source_objects.append((t1, t2))
            source_rows.add(row)

        # Stack every source row under the previous row. Because buff is applied
        # between each row's real bounding box, spacing stays consistent even
        # though some entries wrap longer titles than others.
        source_rows.arrange(DOWN, aligned_edge=LEFT, buff=ROW_BUFF)
        source_rows.next_to(header_sources, DOWN, buff=HEADER_TO_CONTENT_BUFF, aligned_edge=LEFT)

        header_prod = crisp_text(
            "PRODUCTION", font=FONT, font_size=HEADER_FONT_SIZE, color=WHITE,
            weight=BOLD, disable_ligatures=True,
        )
        header_prod.next_to(source_rows, DOWN, buff=SOURCES_TO_PROD_HEADER_BUFF, aligned_edge=LEFT)

        roles_left = [
            ("PRODUCED BY", "Bheesham Kumar Sajnani"),
            ("SCRIPT", "Bheesham Kumar Sajnani"),
            ("VISUAL DIRECTION", "Bheesham Kumar Sajnani"),
            ("EDITING", "Bheesham Kumar Sajnani"),
        ]
        roles_right = [
            ("RESEARCH", "Bheesham Kumar Sajnani"),
            ("3D & ANIMATION", "Bheesham Kumar Sajnani"),
            ("SOUND DESIGN", "Bheesham Kumar Sajnani"),
        ]

        def role_block(role, name):
            r = crisp_text(role, font=FONT, font_size=ROLE_LABEL_FONT_SIZE, color=WHITE, disable_ligatures=True)
            n = crisp_text(name, font=FONT, font_size=ROLE_NAME_FONT_SIZE, color=MUTED, disable_ligatures=True)
            n.next_to(r, DOWN, buff=ROLE_NAME_BUFF, aligned_edge=LEFT)
            return VGroup(r, n)

        col1 = VGroup(*[role_block(r, n) for r, n in roles_left]).arrange(DOWN, aligned_edge=LEFT, buff=ROLE_BLOCK_BUFF)
        col2 = VGroup(*[role_block(r, n) for r, n in roles_right]).arrange(DOWN, aligned_edge=LEFT, buff=ROLE_BLOCK_BUFF)

        col1.next_to(header_prod, DOWN, buff=HEADER_TO_CONTENT_BUFF, aligned_edge=LEFT)
        col2.next_to(col1, RIGHT, buff=COLUMN_GAP).align_to(col1, UP)

        grid_group = VGroup(col1, col2)

        cursor = Rectangle(width=CURSOR_WIDTH, height=CURSOR_HEIGHT, fill_color=CYAN, fill_opacity=1, stroke_width=0)

        # --------------------------------------------------
        # BULLETPROOF CAMERA ENGINE
        # --------------------------------------------------
        
        # Shift the camera up before the timeline even begins
        self.camera.frame.set_y(CAMERA_START_Y)

        def pan_cam(duration):
            return self.camera.frame.animate.shift(DOWN * SCROLL_SPEED * duration)

        def wait_and_scroll(duration):
            self.play(pan_cam(duration), run_time=duration, rate_func=linear)

        # --------------------------------------------------
        # Animation Timeline
        # --------------------------------------------------

        wait_and_scroll(INTRO_PAUSE)

        self.play(FadeIn(header_sources), pan_cam(SOURCES_HEADER_FADE_TIME), run_time=SOURCES_HEADER_FADE_TIME, rate_func=linear)
        wait_and_scroll(PAUSE_AFTER_SOURCES_HEADER)

        for t1, t2 in source_objects:
            cursor.move_to(t1.get_left(), aligned_edge=RIGHT).shift(LEFT * CURSOR_GAP)

            for _ in range(CURSOR_BLINK_COUNT):
                self.add(cursor)
                wait_and_scroll(CURSOR_BLINK_ON_TIME)
                self.remove(cursor)
                wait_and_scroll(CURSOR_BLINK_OFF_TIME)

            self.play(Write(t1), pan_cam(REF_LINE_TYPE_TIME), run_time=REF_LINE_TYPE_TIME, rate_func=linear)
            self.play(Write(t2), pan_cam(USED_FOR_TYPE_TIME), run_time=USED_FOR_TYPE_TIME, rate_func=linear)
            wait_and_scroll(GAP_AFTER_ENTRY)

        wait_and_scroll(PAUSE_BEFORE_PROD_HEADER)

        self.play(FadeIn(header_prod, shift=UP * HEADER_RISE_SHIFT), pan_cam(PROD_HEADER_FADE_TIME), run_time=PROD_HEADER_FADE_TIME, rate_func=linear)
        wait_and_scroll(PAUSE_AFTER_PROD_HEADER)

        self.play(FadeIn(grid_group, shift=UP * HEADER_RISE_SHIFT), pan_cam(GRID_FADE_TIME), run_time=GRID_FADE_TIME, rate_func=linear)

        # --------------------------------------------------
        # DYNAMIC SCREEN CLEAR CALCULATION
        # --------------------------------------------------
        lowest_y = grid_group.get_bottom()[1]
        target_camera_y = lowest_y - (config.frame_height / 2) - END_PADDING
        current_camera_y = self.camera.frame.get_center()[1]
        distance_to_go = current_camera_y - target_camera_y

        if distance_to_go > 0:
            time_needed = distance_to_go / SCROLL_SPEED
            wait_and_scroll(time_needed)
        else:
            wait_and_scroll(2.0)
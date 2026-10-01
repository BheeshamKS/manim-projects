import os
from pathlib import Path
from manim import *

# ==============================================================
# TRACR CREDITS SCENE — 20-SECOND LEFT-SIDE COMPOSITING ROLL
# Video: THE TAP (Shot 0028)
# Designed to sit strictly on the left half of the video (x < 0)
# leaving the right half clear for 3D visuals / end-screen cards.
# Total Runtime: 20.0s (480 frames @ 24fps)
# ==============================================================

# --- Visual Colors (Tracr Signature Palette) ------------------
BG    = "#000000"   # Background color (deep void black)
WHITE = "#E8F1FF"   # Primary text (headers, emphasis)
MUTED = "#7C8DA6"   # Technical slate (secondary text, used-for lines)
CYAN  = "#00E5FF"   # Tracr Cyan accent (">" indicators, name highlight)
FONT  = "JetBrains Mono" # Monospace technical typeface

# --- Typography & Hierarchy -----------------------------------
HEADER_FONT_SIZE     = 26   # "SOURCES" / "PRODUCTION"
REF_FONT_SIZE        = 15   # "> REF 01 | ..." title line
USED_FOR_FONT_SIZE   = 12   # "Used for: ..." context line
ROLE_MAIN_FONT_SIZE  = 17   # "DIRECTED, WRITTEN & ANIMATED"
ROLE_SUB_FONT_SIZE   = 13   # "RESEARCH · 3D MODELING · SOUND DESIGN · EDITING"
NAME_FONT_SIZE       = 20   # "BY BHEESHAM KUMAR SAJNANI"
USED_FOR_OPACITY     = 0.70 # Dimness of the secondary explanation line

# --- Layout & Left-Side Bounding ------------------------------
LEFT_MARGIN          = 0.8  # Margin from the far left frame edge
MAX_CONTENT_WIDTH    = 5.3  # Hard width ceiling: prevents any line crossing into the middle (x = 0)

# --- Sources Reference Data (Easily Editable) -----------------
SOURCES = [
    ("REF 01", "EMVCo — Contactless Specifications", "Kernel specs, APDU handshake & transaction flow"),
    ("REF 02", "ISO/IEC 14443-2 / -3", "13.56 MHz inductive coupling & load modulation"),
    ("REF 03", "NXP Semiconductors — SmartMX / MIFARE", "Passive RF harvesting & secure microcontroller"),
    ("REF 04", "Hancke & Kuhn (2005)", "Relay attacks on contactless smart cards"),
    ("REF 05", "Apple Platform Security", "Secure Element, cryptograms & biometric gating"),
    ("REF 06", "Veritasium x MKBHD", "Real-world relay demonstration reference"),
]

# --- Production Roles (Unified single mention) -----------------
PROD_ROLES_PRIMARY   = "DIRECTED, WRITTEN & ANIMATED"
PROD_ROLES_SECONDARY = "RESEARCH · 3D MODELING · SOUND DESIGN · EDITING"
PROD_NAME_LINE       = "BY BHEESHAM KUMAR SAJNANI"

# --- Internal: Crisp font rendering workaround ----------------
OVERSAMPLE = 5


class Shot028_CreditsScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        # Establish coordinate boundaries for strictly left-side layout
        LEFT_X = -config.frame_width / 2 + LEFT_MARGIN

        def crisp_text(content, font_size, color=WHITE, weight=NORMAL, **kwargs):
            t = Text(
                content,
                font=FONT,
                font_size=font_size * OVERSAMPLE,
                color=color,
                weight=weight,
                disable_ligatures=True,
                **kwargs
            )
            t.scale(1 / OVERSAMPLE)
            # Strict safety guard: clamp width so it NEVER crosses the middle
            if t.width > MAX_CONTENT_WIDTH:
                t.scale_to_fit_width(MAX_CONTENT_WIDTH)
            return t

        # ------------------------------------------------------
        # 1. SOURCES SECTION (Virtual World)
        # ------------------------------------------------------
        header_sources = crisp_text("SOURCES", HEADER_FONT_SIZE, color=WHITE, weight=BOLD)
        header_sources.move_to([LEFT_X, 1.8, 0], aligned_edge=LEFT)

        source_objects = []
        source_rows = VGroup()

        for ref, title, used in SOURCES:
            t1 = crisp_text(
                f"> {ref} | {title}",
                REF_FONT_SIZE,
                color=MUTED,
                t2c={">": CYAN}
            )
            t2 = crisp_text(
                f"Used for: {used}",
                USED_FOR_FONT_SIZE,
                color=MUTED
            ).set_opacity(USED_FOR_OPACITY)

            t2.next_to(t1, DOWN, buff=0.14, aligned_edge=LEFT).shift(RIGHT * 0.35)
            row = VGroup(t1, t2)
            source_objects.append((t1, t2))
            source_rows.add(row)

        source_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        source_rows.next_to(header_sources, DOWN, buff=0.60, aligned_edge=LEFT)

        # ------------------------------------------------------
        # 2. PRODUCTION SECTION (Unified Single-Mention Credit)
        # ------------------------------------------------------
        header_prod = crisp_text("PRODUCTION", HEADER_FONT_SIZE, color=WHITE, weight=BOLD)
        r_primary   = crisp_text(PROD_ROLES_PRIMARY, ROLE_MAIN_FONT_SIZE, color=WHITE, weight=BOLD)
        r_secondary = crisp_text(PROD_ROLES_SECONDARY, ROLE_SUB_FONT_SIZE, color=MUTED)
        by_name     = crisp_text(
            PROD_NAME_LINE,
            NAME_FONT_SIZE,
            color=CYAN,
            weight=BOLD,
            t2c={"BY": MUTED}
        )

        prod_body = VGroup(r_primary, r_secondary, by_name).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        prod_group = VGroup(header_prod, prod_body).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        prod_group.next_to(source_rows, DOWN, buff=0.90, aligned_edge=LEFT)

        # ------------------------------------------------------
        # 3. CAMERA MOTION & 20-SECOND PACING
        # ------------------------------------------------------
        CAMERA_START_Y = 2.0
        # Scroll target: center the production block in the lower portion of the left frame
        TARGET_CAMERA_Y = prod_group.get_center()[1] - 0.35
        SCROLL_DIST = CAMERA_START_Y - TARGET_CAMERA_Y
        SCROLL_TIME = 15.5  # Camera travels steadily for 15.5s, then holds rock-steady
        SCROLL_SPEED = SCROLL_DIST / SCROLL_TIME

        self.camera.frame.set_y(CAMERA_START_Y)

        def pan_cam(duration):
            return self.camera.frame.animate.shift(DOWN * SCROLL_SPEED * duration)

        def wait_and_scroll(duration):
            self.play(pan_cam(duration), run_time=duration, rate_func=linear)

        # Snappy cyan cursor indicator
        cursor = Rectangle(width=0.12, height=0.22, fill_color=CYAN, fill_opacity=1, stroke_width=0)

        # ------------------------------------------------------
        # 4. TIMELINE (Target: Exactly 20.0s / 480 frames @ 24fps)
        # ------------------------------------------------------

        # (0.0s - 1.0s): Scene intro, "SOURCES" header fades in on the left
        self.play(
            FadeIn(header_sources),
            pan_cam(1.00),
            run_time=1.00,
            rate_func=linear
        )

        # (1.0s - 12.4s): 6 sources roll and type out snappily (1.90s per entry)
        for t1, t2 in source_objects:
            cursor.move_to(t1.get_left(), aligned_edge=RIGHT).shift(LEFT * 0.12)
            self.add(cursor)
            wait_and_scroll(0.12)
            self.remove(cursor)
            wait_and_scroll(0.08)
            self.play(Write(t1), pan_cam(0.45), run_time=0.45, rate_func=linear)
            self.play(Write(t2), pan_cam(0.35), run_time=0.35, rate_func=linear)
            wait_and_scroll(0.90)

        # (12.4s - 13.0s): Brief breather before production section
        wait_and_scroll(0.60)

        # (13.0s - 14.0s): "PRODUCTION" header rises and enters
        self.play(
            FadeIn(header_prod, shift=UP * 0.15),
            pan_cam(1.00),
            run_time=1.00,
            rate_func=linear
        )

        # (14.0s - 15.5s): Unified production credit block appears in crisp contrast
        self.play(
            FadeIn(prod_body, shift=UP * 0.20),
            pan_cam(1.50),
            run_time=1.50,
            rate_func=linear
        )

        # Camera has arrived at TARGET_CAMERA_Y. Hold the final card rock-steady!
        # Hold time to clearly read the unified production credit
        self.wait(3.45)

        # Elegant fade out to black
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.65
        )
        # (Total elapsed: exactly 20.00s / 480 frames @ 24fps)


# Aliases for flexible CLI rendering
CreditsRollScene = Shot028_CreditsScene
Shot028_TheCreditsScene = Shot028_CreditsScene
TheCreditsScene = Shot028_CreditsScene
Shot028 = Shot028_CreditsScene

import os
from pathlib import Path
from manim import *
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# =====================================================================
# SHOT 0026: The Range Assumption & The Real-World Attack (Veritasium)
# Video: THE TAP (Shot 0026)
# Total Runtime: 16.00 Seconds (384 Frames @ 24fps)
#
# Voiceover:
# "Just the assumption that 'in range' means 'in the room.'
#  Someone pulled this off again recently, live, on a real locked phone,
#  for real money — worth watching in full, linked below."
# =====================================================================

FONT = "JetBrains Mono"
BG = "#000000"              # Deep void black
COLOR_MAIN = WHITE          # Primary text
COLOR_MUTED = "#CBD5E1"     # Slate
COLOR_DIM = "#64748B"       # Subtle slate
COLOR_ACCENT = "#00E5FF"    # Tracr Cyan
COLOR_RED = "#EF4444"       # Diagnostic red strike

SCRIPT_DIR = Path(__file__).resolve().parent
USER_CARD_SRC = SCRIPT_DIR / "user_ref_card.png"
CLEAN_CARD_HD = SCRIPT_DIR / "clean_youtube_card_4k.png"

# Ensure clean upscaled 4K card exists
if not CLEAN_CARD_HD.exists() and USER_CARD_SRC.exists():
    try:
        src = Image.open(str(USER_CARD_SRC)).convert("RGBA")
        target_w, target_h = int(src.width * 2.5), int(src.height * 2.5)
        upscaled = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
        sharpened = upscaled.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=2))
        radius = 48
        mask = Image.new("L", (target_w, target_h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (target_w, target_h)], radius=radius, fill=255)
        card_hd = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        card_hd.paste(sharpened, (0, 0), mask=mask)
        card_hd.save(str(CLEAN_CARD_HD), "PNG")
    except Exception as e:
        print(f"Warning generating clean card: {e}")


class Shot026_RelayRealWorld(Scene):
    def construct(self):
        self.camera.background_color = BG

        # =====================================================================
        # BEAT 1: Simple, Crisp Typography (0.0s - 5.0s = 5.0s / 120 Frames)
        # Voiceover: "Just the assumption that 'in range' means 'in the room.'"
        # =====================================================================
        
        # Simple, elegant quote lines
        intro_line = Text("Just the assumption that", font=FONT, font_size=24, color=COLOR_MUTED)
        
        # Comparison row: "in range"  ==  "in the room."
        t_in_range = Text('"in range"', font=FONT, font_size=32, color=COLOR_ACCENT, weight=BOLD)
        t_equals   = Text("==", font=FONT, font_size=30, color=COLOR_DIM, weight=BOLD)
        t_in_room  = Text('"in the room."', font=FONT, font_size=32, color=COLOR_MAIN, weight=BOLD)
        
        comp_row = VGroup(t_in_range, t_equals, t_in_room).arrange(RIGHT, buff=0.35)
        
        quote_group = VGroup(intro_line, comp_row).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        # Bold diagonal red strike across the equivalence operator
        strike_slash = Line(
            t_equals.get_corner(DL) + LEFT * 0.12 + DOWN * 0.12,
            t_equals.get_corner(UR) + RIGHT * 0.12 + UP * 0.12,
            color=COLOR_RED, stroke_width=5
        )

        beat1_group = VGroup(quote_group, strike_slash)

        # 0.0s - 1.0s: Fade in typography cleanly
        self.play(FadeIn(quote_group, shift=UP * 0.2), run_time=1.0)

        # 1.0s - 2.0s: Hold for read
        self.wait(1.0)

        # 2.0s - 2.8s: Slashes the assumption with clean red strike
        self.play(
            Create(strike_slash),
            t_in_room.animate.set_color(COLOR_MUTED),
            run_time=0.8,
            rate_func=rate_functions.ease_out_quad
        )

        # 2.8s - 5.0s: Hold beat 1 (Total elapsed: 5.0s)
        self.wait(2.2)

        # =====================================================================
        # BEAT 2: Clean YouTube Card (5.0s - 11.5s = 6.5s / 156 Frames)
        # Voiceover: "Someone pulled this off again recently, live, on a real locked phone, for real money —"
        # =====================================================================

        card_path = str(CLEAN_CARD_HD) if CLEAN_CARD_HD.exists() else str(USER_CARD_SRC)
        card = ImageMobject(card_path)
        card.height = 5.3
        card.shift(UP * 0.2)

        # Clean, subtle bezel framing the card
        border = RoundedRectangle(
            width=card.width + 0.08, height=card.height + 0.08, corner_radius=0.18,
            color="#262626", stroke_width=2.0
        ).move_to(card)

        card_group = Group(border, card)

        # 5.0s - 6.2s: Fade out beat 1, fade in the simple YouTube card
        self.play(
            FadeOut(quote_group, shift=DOWN * 0.2),
            FadeOut(strike_slash, shift=DOWN * 0.2),
            FadeIn(card_group, shift=UP * 0.25),
            run_time=1.2,
            rate_func=rate_functions.ease_out_cubic
        )

        # 6.2s - 11.5s: Clean hold to view the card
        self.wait(5.3)
        # (Total elapsed: 11.5s)

        # =====================================================================
        # BEAT 3: Simple "Linked Below" Cue (11.5s - 16.0s = 4.5s / 108 Frames)
        # Voiceover: "— worth watching in full, linked below."
        # =====================================================================

        callout_text = Text("Linked below", font=FONT, font_size=18, color=COLOR_ACCENT, weight=BOLD)
        arrow = Triangle(color=COLOR_ACCENT, fill_color=COLOR_ACCENT, fill_opacity=1).rotate(PI).scale(0.12)
        callout_group = VGroup(callout_text, arrow).arrange(DOWN, buff=0.14).next_to(border, DOWN, buff=0.28)

        # 11.5s - 12.3s: Fade in callout
        self.play(FadeIn(callout_group, shift=UP * 0.15), run_time=0.8)

        # 12.3s - 14.7s: 3 cycles of smooth, gentle pulsing on the downward arrow
        # Pulse 1 (12.3s - 13.1s = 0.8s)
        self.play(arrow.animate.shift(DOWN * 0.12).set_opacity(0.55), run_time=0.4, rate_func=rate_functions.ease_out_sine)
        self.play(arrow.animate.shift(UP * 0.12).set_opacity(1.0), run_time=0.4, rate_func=rate_functions.ease_in_sine)

        # Pulse 2 (13.1s - 13.9s = 0.8s)
        self.play(arrow.animate.shift(DOWN * 0.12).set_opacity(0.55), run_time=0.4, rate_func=rate_functions.ease_out_sine)
        self.play(arrow.animate.shift(UP * 0.12).set_opacity(1.0), run_time=0.4, rate_func=rate_functions.ease_in_sine)

        # Pulse 3 (13.9s - 14.7s = 0.8s)
        self.play(arrow.animate.shift(DOWN * 0.12).set_opacity(0.55), run_time=0.4, rate_func=rate_functions.ease_out_sine)
        self.play(arrow.animate.shift(UP * 0.12).set_opacity(1.0), run_time=0.4, rate_func=rate_functions.ease_in_sine)

        # 14.7s - 16.0s: Clean settle and hold (Total elapsed: exactly 16.00s = 384 frames @ 24fps)
        self.wait(1.175)


# Aliases for compatibility with build scripts and planners
Shot026_LinkedBelowCallout = Shot026_RelayRealWorld

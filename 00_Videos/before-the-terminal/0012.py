import os
from pathlib import Path
from manim import *

# Target: exactly 20.0 seconds @ 24 FPS (480 frames)

class OSDivideScene(Scene):
    def construct(self):
        
        # --------------------------------------------------
        # Dynamic Asset Path Resolution
        # --------------------------------------------------
        SCRIPT_DIR = Path(__file__).resolve().parent
        ROOT_DIR = SCRIPT_DIR.parent.parent
        ASSET_DIR = ROOT_DIR / "01_Assets" / "Images"

        # --------------------------------------------------
        # tracr Boilerplate & Styling
        # --------------------------------------------------
        
        BG = "#0C0A10"  # OS background
        BG_PY = "#080C12" # Python background
        WHITE = "#E8F1FF"
        MUTED = "#7C8DA6"
        CYAN = "#00C2FF"
        BLOCK_BG = "#101722"
        MONO = "JetBrains Mono"

        FW = config.frame_width
        FH = config.frame_height

        self.camera.background_color = BG 

        # --------------------------------------------------
        # Static Layout Construction
        # --------------------------------------------------
        
        # 1. Backgrounds & Divider
        top_bg = Rectangle(
            width=FW, height=FH / 2,
            fill_color=BG_PY, fill_opacity=1, stroke_width=0
        ).to_edge(UP, buff=0)

        divider = Line(LEFT * (FW/2), RIGHT * (FW/2), color=MUTED, stroke_width=2)
        divider_glow = Line(LEFT * (FW/2), RIGHT * (FW/2), color=CYAN, stroke_width=8, stroke_opacity=0)

        # 2. Main Zone Label (Python)
        py_icon = SVGMobject(str(ASSET_DIR / "python.svg"))
        py_icon.set_style(fill_opacity=1, stroke_width=0)
        
        # Force colors onto the paths in case the SVG uses CSS styling that Manim ignores
        if len(py_icon) == 2:
            py_icon[0].set_color("#3776AB") # Python Blue
            py_icon[1].set_color("#FFD43B") # Python Yellow
        elif len(py_icon) > 0:
            py_icon.set_color("#FFD43B") # Fallback to solid yellow to guarantee visibility
            
        py_icon.scale_to_fit_height(0.45)
        py_txt = Text("PYTHON", font=MONO, font_size=28, color=MUTED)
        
        py_row = VGroup(py_icon, py_txt).arrange(RIGHT, buff=0.3).to_corner(UL, buff=0.6)
        
        # 3. Ecosystem SVGs (Perfect Grid Alignment)
        def create_os_logo(filename, name, override_color=None):
            icon = SVGMobject(str(ASSET_DIR / filename))
            icon.set_style(fill_opacity=1, stroke_width=0)
            if override_color:
                icon.set_color(override_color)
            icon.scale_to_fit_height(0.35)
            txt = Text(name, font=MONO, font_size=20, color=MUTED)
            return icon, txt

        win_icon, win_txt = create_os_logo("windows-11.svg", "Windows")
        mac_icon, mac_txt = create_os_logo("apple.svg", "macOS", WHITE)
        arch_icon, arch_txt = create_os_logo("arch-linux.svg", "Linux")

        icons = VGroup(win_icon, mac_icon, arch_icon)
        texts = VGroup(win_txt, mac_txt, arch_txt)

        # Arrange icons vertically and force them to share an exact center X-axis
        icons.arrange(DOWN, buff=0.5)
        icon_center_x = icons.get_center()[0]
        for icon in icons:
            icon.set_x(icon_center_x)

        # Lock all text elements to a strict left-aligned column next to the icons
        max_icon_right = max([i.get_right()[0] for i in icons])
        for icon, txt in zip(icons, texts):
            txt.set_y(icon.get_y())
            txt.set_x(max_icon_right + 0.3, direction=LEFT)

        logo_stack = VGroup(icons, texts)
        logo_stack.to_edge(LEFT, buff=0.8).shift(DOWN * 2) 

        # 4. Message Packet Components
        block_box = RoundedRectangle(
            width=5.2, height=1.2, corner_radius=0.15, 
            fill_color=BLOCK_BG, fill_opacity=1, 
            stroke_color=MUTED, stroke_width=1.5
        )
        header_line = Line(
            block_box.get_corner(UL) + DOWN * 0.3, 
            block_box.get_corner(UR) + DOWN * 0.3, 
            color=MUTED, stroke_width=1
        ).set_opacity(0.5)
        led = Dot(color=CYAN, radius=0.06).move_to(block_box.get_corner(UL) + RIGHT * 0.25 + DOWN * 0.15)
        payload_text = Text("write: Hello, World", font=MONO, font_size=24, color=WHITE).move_to(block_box).shift(DOWN * 0.1)

        packet_items = [block_box, header_line, led, payload_text]
        
        # Position exactly in the vertical middle of the Python zone (Y = +2.0)
        for item in packet_items:
            item.shift(UP * 2.0) 
        
        # Shockwave
        shockwave = Circle(radius=0.1, color=CYAN, stroke_width=4).move_to(ORIGIN)

        # --------------------------------------------------
        # Animation Timeline (Total: 20.0s)
        # --------------------------------------------------

        # 1. Base Setup (0.0s - 1.0s)
        self.play(
            FadeIn(top_bg), FadeIn(py_row), 
            Create(divider), Create(divider_glow),
            run_time=1.0
        )

        self.wait(3.0)

        # 2. Packet forms (4.0s - 5.0s)
        self.play(
            DrawBorderThenFill(block_box), Create(header_line),
            FadeIn(led, scale=0.5), Write(payload_text),
            run_time=1.0
        )

        # Hold (5.0s - 11.0s)
        self.wait(6.0)

        # 3. Windows, Mac, and Arch ALL appear simultaneously (11.0s - 12.0s)
        self.play(
            FadeIn(logo_stack, shift=RIGHT * 0.2),
            run_time=1.0
        )

        self.wait(2.0)

        # 4. The Drop and Crossing (14.0s - 16.0s)
        # Drops use constant mathematical velocity to maintain exact pacing.
        # Total distance is exactly 4.0 units (from Y=+2.0 to Y=-2.0)
        
        # Part A: Drop to boundary (2.0 units down in 1.0s)
        self.play(
            *[item.animate(rate_func=linear).shift(DOWN * 2.0) for item in packet_items],
            run_time=1.0
        )

        self.add(shockwave)
        
        # Part B: Packet pushes through line (0.6 units down in 0.3s)
        self.play(
            block_box.animate(rate_func=linear).shift(DOWN * 0.6).set_stroke(color=CYAN),
            header_line.animate(rate_func=linear).shift(DOWN * 0.6),
            led.animate(rate_func=linear).shift(DOWN * 0.6).set_color("#4DDD70"),
            payload_text.animate(rate_func=linear).shift(DOWN * 0.6),
            
            divider.animate(rate_func=linear).set_color(CYAN).set_stroke(width=3),
            divider_glow.animate(rate_func=linear).set_stroke(opacity=0.6),
            shockwave.animate(rate_func=linear).scale(60).set_opacity(0),
            run_time=0.3
        )

        # Part C: Finishes drop to exact center of OS zone (1.4 units down in 0.7s)
        self.play(
            *[item.animate(rate_func=linear).shift(DOWN * 1.4) for item in packet_items],
            divider.animate(rate_func=linear).set_color(MUTED).set_stroke(width=2),
            divider_glow.animate(rate_func=linear).set_stroke(opacity=0),
            run_time=0.7
        )

        # 5. Hold landed exactly in center (16.0s - 17.0s)
        self.wait(1.0)

        # 6. Clean fade out of Python layer (17.0s - 18.5s)
        self.play(
            FadeOut(top_bg), FadeOut(py_row), FadeOut(divider),
            run_time=1.5
        )

        # 7. Final hold (18.5s - 20.0s)
        self.wait(1.5)
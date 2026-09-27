#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path("/mnt/SSD_Storage/manim-projects/00_Videos/the-tap")
MANIM_BIN = Path("/mnt/SSD_Storage/manim-projects/.venv/bin/manim")
FINAL_OUT_DIR = BASE_DIR / "final_4k_renders"
FINAL_OUT_DIR.mkdir(exist_ok=True)

SHOTS = [
    ("0003.py", "Shot003_InductiveCoupling", "0003_InductiveCoupling.mp4"),
    ("0004.py", "Shot004_JargonRelief", "0004_JargonRelief.mp4"),
    ("0005.py", "Shot005_PowerBudget", "0005_PowerBudget.mp4"),
    ("0006.py", "Shot006_NoAntenna", "0006_NoAntenna.mp4"),
    ("0007.py", "Shot007_LoadModulation", "0007_LoadModulation.mp4"),
    ("0008.py", "Shot008_JargonReliefLoadModulation", "0008_JargonReliefLoadModulation.mp4"),
    ("0009.py", "Shot009_SameEngine", "0009_SameEngine.mp4"),
    ("0013&14.py", "Shot013_014_HandshakeCliffhanger", "0013_0014_HandshakeCliffhanger.mp4"),
    ("0015.py", "Shot015_TheVault", "0015_TheVault.mp4"),
    ("0016.py", "Shot016_SecretKey", "0016_SecretKey.mp4"),
    ("0017.py", "Shot017_AlreadySpent", "0017_AlreadySpent.mp4"),
    ("0020.py", "Shot020_SameMechanism", "0020_SameMechanism.mp4"),
    ("0021.py", "Shot021_ArchitectureSplit", "0021_ArchitectureSplit.mp4"),
    ("0023.py", "Shot023_PhoneAsksFirst", "0023_PhoneAsksFirst.mp4"),
]

def render_shot(script_file, scene_name, output_name):
    final_dest = FINAL_OUT_DIR / output_name
    print(f"\n=======================================================")
    print(f"Rendering: {scene_name} from {script_file} -> {output_name}")
    print(f"=======================================================")
    
    cmd = [
        str(MANIM_BIN),
        "render",
        str(script_file),
        scene_name,
        "-o",
        output_name
    ]
    
    res = subprocess.run(cmd, cwd=str(BASE_DIR))
    if res.returncode != 0:
        print(f"ERROR rendering {scene_name}!", file=sys.stderr)
        return False
        
    # Locate the rendered output file
    # Manim places it in media/videos/<script_stem>/2160p24/<output_name>
    script_stem = Path(script_file).stem
    candidates = list((BASE_DIR / "media" / "videos" / script_stem / "2160p24").glob(f"*{output_name}*"))
    if not candidates:
        # Check recursively in media/videos/
        candidates = list((BASE_DIR / "media" / "videos").rglob(output_name))
        
    if candidates and candidates[0].exists():
        src_path = candidates[0]
        shutil.copy2(src_path, final_dest)
        print(f"SUCCESS: Rendered & copied to {final_dest} ({final_dest.stat().st_size / (1024*1024):.2f} MB)")
        return True
    else:
        print(f"WARNING: Output file {output_name} not found in candidates: {candidates}", file=sys.stderr)
        return False

def main():
    print(f"Starting fresh 4K 24fps Batch Render of all {len(SHOTS)} shots...")
    successes = []
    failures = []
    
    for script_file, scene_name, output_name in SHOTS:
        ok = render_shot(script_file, scene_name, output_name)
        if ok:
            successes.append(output_name)
        else:
            failures.append(output_name)
            
        # Clean partial movie files after each shot to keep disk usage lean
        if (BASE_DIR / "media").exists():
            for partial_dir in (BASE_DIR / "media").rglob("partial_movie_files"):
                if partial_dir.is_dir():
                    shutil.rmtree(partial_dir, ignore_errors=True)
            
    print("\n-------------------------------------------------------")
    print(f"Batch Render Completed: {len(successes)}/{len(SHOTS)} successful.")
    if failures:
        print(f"Failures: {failures}", file=sys.stderr)
    
    # Final cleanup of media/ temp directory
    print("\nCleaning up temporary media directory...")
    if (BASE_DIR / "media").exists():
        shutil.rmtree(BASE_DIR / "media", ignore_errors=True)
            
    print(f"Cleanup done! All final 4K renders saved to: {FINAL_OUT_DIR}")

if __name__ == "__main__":
    main()

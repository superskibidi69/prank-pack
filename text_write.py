import os
from pathlib import Path

# ---------- CONFIG ----------
num_files = 100
letter = "thank you for helping me test\n"
repeat_count = 800

# ---------- DETECT DESKTOP ----------
def get_desktop():
    home = Path.home()

    # Linux XDG desktop
    xdg = os.environ.get("XDG_DESKTOP_DIR")
    if xdg:
        path = Path(os.path.expandvars(xdg))
        if path.exists():
            return path

    # common desktop folder names
    for name in ["Desktop", "Escritorio", "Bureau", "桌面"]:
        path = home / name
        if path.exists():
            return path

    # fallback to home if nothing found
    return home

desktop = get_desktop()

# ---------- CREATE TXT FILES ----------
for i in range(num_files):
    file_path = desktop / f"file{i}.txt"
    file_path.write_text(letter * repeat_count)

print(f"{num_files} txt files created on your desktop at {desktop}")

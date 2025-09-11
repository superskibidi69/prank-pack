import os
from pathlib import Path
import sys

# ---------- CONFIG ----------
num_files = 100
letter = "thank you for helping me test\n"
repeat_count = 1000000

# ---------- DETECT DESKTOP ----------
def get_desktop():
    home = Path.home()

    if sys.platform.startswith("win"):
        try:
            import ctypes
            from ctypes import wintypes
            CSIDL_DESKTOPDIRECTORY = 0x10
            SHGFP_TYPE_CURRENT = 0
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOPDIRECTORY, 0, SHGFP_TYPE_CURRENT, buf)
            path = Path(buf.value)
            if path.exists():
                return path
        except Exception:
            pass
    else:
        # macOS/Linux
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

    # fallback
    return home

desktop = get_desktop()

# ---------- CREATE TXT FILES ----------
for i in range(num_files):
    file_path = desktop / f"file{i}.txt"
    file_path.write_text(letter * repeat_count)

# ---------- OPTIONAL CONFIRMATION ----------
if sys.platform.startswith("win"):
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, f"{num_files} txt files created on your desktop!", "Done", 0)
else:
    print(f"{num_files} txt files created on your desktop at {desktop}")

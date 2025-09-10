import os
from pathlib import Path

# ---------- CONFIG ----------
num_files = 10
letter = "thank you for helping me test"
repeat_count = 100

# ---------- DETECT DESKTOP ----------
home = Path.home()
desktop = None

# try common desktop names
for name in ["Desktop", "Escritorio", "Bureau", "桌面"]:
    path = home / name
    if path.exists():
        desktop = path
        break

# fallback to home if desktop not found
if desktop is None:
    desktop = home

# ---------- CREATE TXT FILES ----------
for i in range(num_files):
    file_path = desktop / f"file{i}.txt"
    file_path.write_text(letter * repeat_count)

print(f"{num_files} txt files created on your desktop at {desktop}")

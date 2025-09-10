import subprocess
import sys

# your script to package
script_name = "text_write.py"

# ---------- CHECK AND INSTALL PYINSTALLER ----------
try:
    import PyInstaller
    print("PyInstaller already installed.")
except ModuleNotFoundError:
    print("PyInstaller not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])

# ---------- BUILD EXE ----------
print(f"Building executable for {script_name} ...")
subprocess.check_call([
    sys.executable,
    "-m", "PyInstaller",
    "--onefile",
    "--noconsole",
    script_name
])

print("Done! Check the 'dist' folder for your executable.")

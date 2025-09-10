import subprocess, sys, os

script_name = "duck_spawner.py"
app_name = "DuckApp"

# check PyInstaller
try:
    import PyInstaller
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])

# ---------- BUILD ONEFILE EXECUTABLE ----------
print("Building single-file executable...")
subprocess.check_call([
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", app_name,
    "--add-data", "duck.webp:.",
    "--add-data", "duck1.webp:.",
    script_name
])

# # ---------- BUILD MAC APP BUNDLE ----------
# print("Building macOS app bundle...")
# subprocess.check_call([
#     sys.executable, "-m", "PyInstaller",
#     "--windowed",
#     "--name", app_name,
#     "--add-data", "duck.webp:.",
#     "--add-data", "duck1.webp:.",
#     "--osx-bundle-identifier", "com.example.duckapp",
#     script_name
# ])

print("Done! Check 'dist' folder for executables and app bundle.")

import subprocess, sys, os

script_name = "duck_spawner.py"
app_name = "DuckApp"

# check PyInstaller
try:
    import PyInstaller
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])

choice = input("Build macOS app bundle? (y/n): ").strip().lower()

if choice == "y":
    print("Building macOS app bundle...")
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--windowed",
        "--name", app_name,
        "--add-data", "duck.webp:.",
        "--add-data", "duck1.webp:.",
        "--osx-bundle-identifier", f"com.example.{app_name.lower()}",
        script_name
    ])

    bundle_path = f"dist/{app_name}.app"
    dmg_name = f"{app_name}.dmg"

    if os.path.exists(bundle_path):
        print("Creating DMG...")
        subprocess.check_call([
            "hdiutil", "create",
            "-volname", app_name,
            "-srcfolder", bundle_path,
            "-ov", "-format", "UDZO",
            dmg_name
        ])
        print(f"DMG created: {dmg_name}")
    else:
        print("Error: App bundle not found, cannot create DMG.")

else:
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

print("Done! Check 'dist' folder for output.")

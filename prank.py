from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox,
    QScrollArea, QFrame, QDialog, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys, random, time, os
from threading import Thread, Event
from playsound import playsound

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def play_fart():
    try:
        if window.audio_enabled:
            playsound(resource_path("fart.mp3"), block=False)
    except:
        pass

class FakeLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fake Login")
        self.setStyleSheet("background-color:#0d0d0d; color:#00ff99; font-family:Courier;")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.fake_login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def fake_login(self):
        username = self.username_input.text()
        # password is masked automatically
        self.username_input.clear()
        self.password_input.clear()
        QMessageBox.critical(self, "Login Failed", f"❌ Wrong username or password for '{username}'!")
        play_fart()

class PrankApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("QWidget { background-color: #0d0d0d; color: #00ff99; font-family: Courier; }")
        self.stop_event = Event()
        self.running_buttons = set()
        self.audio_enabled = True

        layout = QVBoxLayout()
        self.label = QLabel("Select a prank to deploy:")
        layout.addWidget(self.label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QFrame()
        self.scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(self.scroll_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        self.pranks = {
            "Matrix Rain": self.matrix_rain,
            "Self Destruct": self.self_destruct,
            "System Scan": self.fake_scan,
            "Error Popup": self.error_popup,
            "Fake Update": self.fake_update,
            "Blue Screen": self.fake_bsod,
            "Typing Virus": self.typing_virus_safe,
            "Rickroll Loader": self.rickroll_loader,
            "AI Takeover": self.ai_takeover,
            "Hacker Trace": self.hacker_trace,
            "Quantum Boot": self.quantum_boot,
            "Emoji Storm": self.emoji_storm,
            "Glitch Text": self.glitch_text,
            "Terminal Flood": self.terminal_flood,
            "System Rewind": self.system_rewind,
            "404 Reality Not Found": self.reality_not_found,
            "Color Flash": self.color_flash,
            "Fake Login": self.fake_login,
            "Infinite Loops": self.infinite_loops,
            "Confetti Blast": self.confetti_blast,
            "Screen Shake": self.screen_shake,
            "Fake Virus Warning": self.fake_virus_warning,
            "Rapid Hacking Logs": self.rapid_hacking_logs,
            "Simulated Crashes": self.simulated_crashes,
            "NPM Install": self.npm
        }

        for name, func in self.pranks.items():
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, b=btn, f=func: self.run_prank(b, f))
            btn.setCursor(Qt.PointingHandCursor)
            self.scroll_layout.addWidget(btn)

        panic_btn = QPushButton("🛑 PANIC BUTTON")
        panic_btn.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px;")
        panic_btn.setCursor(Qt.PointingHandCursor)
        panic_btn.clicked.connect(self.panic_reset)
        layout.addWidget(panic_btn)

        audio_btn = QPushButton("🔊 Fart Sounds: ON")
        audio_btn.setCursor(Qt.PointingHandCursor)
        audio_btn.setCheckable(True)
        audio_btn.setChecked(True)
        audio_btn.clicked.connect(lambda: self.toggle_audio(audio_btn))
        layout.addWidget(audio_btn)

        self.setLayout(layout)

    def toggle_audio(self, btn):
        self.audio_enabled = not self.audio_enabled
        btn.setText(f"🔊 Fart Sounds: {'ON' if self.audio_enabled else 'OFF'}")

    def run_prank(self, button, prank_func):
        if button in self.running_buttons: return
        self.running_buttons.add(button)
        button.setEnabled(False)
        Thread(target=self._prank_wrapper, args=(button, prank_func), daemon=True).start()

    def _prank_wrapper(self, button, prank_func):
        try:
            prank_func()
        finally:
            button.setEnabled(True)
            self.running_buttons.discard(button)

    def panic_reset(self):
        self.stop_event.set()
        self.label.setText("🛑 All pranks halted.")
        time.sleep(0.2)
        self.stop_event.clear()

    # ---------------- Pranks ----------------
    def matrix_rain(self):
        chars = "01ㄱㄴㅏㅓㅗㅜ█▓▒░"
        for _ in range(50):
            if self.stop_event.is_set(): return
            rain = "".join(random.choice(chars) for _ in range(80))
            self.label.setText(rain)
            self.label.setStyleSheet(f"color: #{random.randint(0,0x00FF00):06x}; background-color: black; font-family: Courier;")
            time.sleep(0.02)
        self.label.setText("Select a prank to deploy:")
        play_fart()

    def self_destruct(self):
        for i in range(10,0,-1):
            if self.stop_event.is_set(): return
            self.label.setText(f"⚠️ SYSTEM SELF-DESTRUCT IN {i} ⚠️")
            self.label.setStyleSheet(f"color: #{random.randint(0xFF0000,0xFF5555):06x}; background-color: black; font-family: Courier;")
            time.sleep(0.4)
        self.label.setText("💥 Just kidding 😎")
        play_fart()

    def fake_scan(self):
        steps = ["🔍 Scanning bootloader...", "🔍 Analyzing memory...", "⚠️ Anomaly detected!", "✅ Simulation complete."]
        for msg in steps:
            if self.stop_event.is_set(): return
            self.label.setText(msg)
            time.sleep(1)
        self.label.setText("Select a prank to deploy:")
        play_fart()

    def error_popup(self):
        if self.stop_event.is_set(): return
        code = random.randint(1000,9999)
        for _ in range(2):
            QMessageBox.critical(self, "Critical Error", f"Malware Signature #{code} activated!\nSystem lockdown initiated.")
            if self.stop_event.is_set(): return
        play_fart()

    def fake_update(self):
        for i in range(0,101,10):
            if self.stop_event.is_set(): return
            self.label.setText(f"🔄 Installing Update... {i}%")
            time.sleep(0.25)
        self.label.setText("✅ Update complete. Welcome to Windows 98.")
        play_fart()

    def fake_bsod(self):
        if self.stop_event.is_set(): return
        QMessageBox.critical(self, "System Failure", "💀 A fatal exception has occurred.\nPress any key to continue...")
        play_fart()

    def typing_virus_safe(self):
        for i in range(1,10):
            if self.stop_event.is_set(): return
            self.label.setText("🧠 Injecting thoughts...\n" + ("I am inside your system. "*i))
            time.sleep(0.2)
        self.label.setText("Select a prank to deploy:")
        play_fart()

    def rickroll_loader(self):
        self.label.setText("🎵 Loading Rick Astley...")
        time.sleep(1)
        self.label.setText("Never gonna give you up...")
        time.sleep(1)
        self.label.setText("🎶 You've been Rickrolled.")
        play_fart()

    def ai_takeover(self):
        self.label.setText("🤖 AI Core Activation...")
        time.sleep(0.3)
        self.label.setText("🧠 Overriding user privileges...")
        time.sleep(0.3)
        self.label.setText("👁️ Surveillance mode enabled...")
        time.sleep(0.3)
        self.label.setText("✅ You're still in control.")
        play_fart()

    def hacker_trace(self):
        self.label.setText("🕵️ Tracing hacker IP...")
        time.sleep(0.3)
        self.label.setText("🌐 Locating signal...")
        time.sleep(0.3)
        self.label.setText("📍 Hacker found: 127.0.0.1")
        time.sleep(0.3)
        self.label.setText("✅ You are the hacker.")
        play_fart()

    def quantum_boot(self):
        self.label.setText("⚛️ Booting Quantum OS...")
        time.sleep(0.3)
        self.label.setText("🌀 Entangling kernel modules...")
        time.sleep(0.3)
        self.label.setText("✅ Quantum boot complete.")
        play_fart()

    def emoji_storm(self):
        for _ in range(20):
            if self.stop_event.is_set(): return
            storm = "".join(random.choice("😎🤖💥🔥💀👻🧠🛸🧨☠️") for _ in range(50))
            self.label.setText(storm)
            self.label.setStyleSheet(f"color: #{random.randint(0,0xFFFFFF):06x}; background-color: black; font-family: Courier;")
            time.sleep(0.08)
        self.label.setText("🌪️ Emoji storm passed.")
        play_fart()

    def glitch_text(self):
        for _ in range(30):
            if self.stop_event.is_set(): return
            glitch = "".join(random.choice("█▓▒░@#$%&!?") for _ in range(50))
            self.label.setText(glitch)
            self.label.setStyleSheet(f"color: #{random.randint(0,0xFFFFFF):06x}; background-color: black; font-family: Courier;")
            time.sleep(0.04)
        self.label.setText("🧬 Glitch resolved.")
        play_fart()

    def terminal_flood(self):
        for i in range(1,21):
            if self.stop_event.is_set(): return
            self.label.setText(f"💻 Terminal line {i}: echo 'Hello World!'")
            time.sleep(0.15)
        self.label.setText("✅ Flood complete.")
        play_fart()

    def system_rewind(self):
        self.label.setText("⏪ Rewinding system state...")
        time.sleep(0.3)
        self.label.setText("⏳ Restoring previous session...")
        time.sleep(0.3)
        self.label.setText("✅ System restored to 1998.")
        play_fart()

    def reality_not_found(self):
        self.label.setText("🔍 Searching for reality...")
        time.sleep(0.3)
        self.label.setText("❌ Reality not found.")
        time.sleep(0.3)
        self.label.setText("✅ Simulation resumed.")
        play_fart()

    def color_flash(self):
        for _ in range(25):
            if self.stop_event.is_set(): return
            self.setStyleSheet(f"QWidget {{ background-color: #{random.randint(0,0xFFFFFF):06x}; color: #{random.randint(0,0x00FF00):06x}; font-family:Courier; }}")
            time.sleep(0.08)
        self.setStyleSheet("QWidget { background-color: #0d0d0d; color: #00ff99; font-family: Courier; }")
        play_fart()

    def fake_login(self):
        dlg = FakeLoginDialog()
        dlg.exec_()
        play_fart()

    def infinite_loops(self):
        self.label.setText("♾️ Spawning infinite loops...")
        for i in range(1, 21):
            if self.stop_event.is_set(): return
            self.label.setText(f"Loop {i} initiated...")
            time.sleep(0.12)
        self.label.setText("✅ All loops terminated (fake).")
        play_fart()

    def confetti_blast(self):
        for _ in range(25):
            if self.stop_event.is_set(): return
            confetti = "".join(random.choice("🎉✨💥🌈🎊") for _ in range(30))
            self.label.setText(confetti)
            time.sleep(0.08)
        self.label.setText("🎊 Confetti settled.")
        play_fart()

    def screen_shake(self):
        original_pos = self.pos()
        for _ in range(120):
            if self.stop_event.is_set(): return
            dx, dy = random.randint(-15,15), random.randint(-15,15)
            self.move(original_pos.x()+dx, original_pos.y()+dy)
            time.sleep(0.03)
        self.move(original_pos)
        play_fart()

    def fake_virus_warning(self):
        for _ in range(3):
            if self.stop_event.is_set(): return
            QMessageBox.warning(self, "VIRUS ALERT", "🚨 VIRUS DETECTED! SYSTEM COMPROMISED! 🚨")
            time.sleep(0.5)
        play_fart()

    def rapid_hacking_logs(self):
        for i in range(1,31):
            if self.stop_event.is_set(): return
            log = f"HACKER LOG {i}: access granted {random.randint(1000,9999)}"
            self.label.setText(log)
            time.sleep(0.04)
        self.label.setText("✅ Logs complete.")
        play_fart()

    def simulated_crashes(self):
        for i in range(1,4):
            if self.stop_event.is_set(): return
            QMessageBox.critical(self, "CRASH", f"Fatal error {random.randint(100,999)} occurred!")
            time.sleep(0.3)
        play_fart()

    def npm(self):
        packages = ["express", "axios", "cors", "dotenv",
                    "webpack", "MongoDB", "jest", "nextjs", "node-fetch","discordjs", "wrangler"]
        for pkg in packages:
            if self.stop_event.is_set(): return
            bar_len = 22
            bar = ["."] * bar_len
            self.label.setText(f"{pkg} [{' '.join(bar)}] 0%")
            time.sleep(0.36)
            for i in range(bar_len):
                if self.stop_event.is_set(): return
                bar[i] = random.choice(["/", "\\", "█"])
                time.sleep(random.uniform(0.03,0.08))
                percent = int((i+1)/bar_len*100)
                self.label.setText(f"{pkg} [{' '.join(bar)}] {percent}%")
            self.label.setText(f"{pkg} [{' '.join(bar)}] installed")
            time.sleep(0.15)
        self.label.setText("Added 253 packages, found 𝟬 vulnerabilities.")
        play_fart()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Prank Control Panel")
    window = PrankApp()
    window.setWindowTitle("Prank Control Panel")
    window.setWindowIcon(QIcon(resource_path("icon.ico")))
    window.show()
    sys.exit(app.exec_())

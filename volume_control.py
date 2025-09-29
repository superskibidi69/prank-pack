import sys, os, random, time, subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def set_volume_mac(vol):
    vol = max(0, min(100, vol))
    subprocess.Popen(
        ["osascript", "-e", f"set volume output volume {vol}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def play_meme(sound_file):
    subprocess.Popen(["afplay", sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class ClickVolume(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enterprise-grade volume control")
        self.setGeometry(500, 300, 400, 200)

        layout = QVBoxLayout()
        self.info = QLabel("Click anywhere fast to stay loud", self)
        self.info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info)

        self.display = QLabel("Volume: 0%", self)
        self.display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.display)

        self.setLayout(layout)

        self.clicks = 0
        self.volume = 0
        self.last_click = time.time()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_volume)
        self.timer.start(1000)

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_window)
        self.move_timer.start(40)

        self.meme_timer = QTimer()
        self.meme_timer.timeout.connect(self.play_random_meme)
        self.meme_timer.start(1000)
        self.next_meme = random.randint(10, 20)
        self.meme_elapsed = 0

        self.sounds = [
            resource_path("1.wav"),
            resource_path("2.wav")
        ]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicks += 1
            self.last_click = time.time()

    def update_volume(self):
        now = time.time()
        if now - self.last_click > 5:
            self.volume = max(0, self.volume - 1)
        else:
            cps = self.clicks
            self.volume = min(100, cps * 10)
        self.clicks = 0

        set_volume_mac(self.volume)
        self.display.setText(f"volume: {self.volume}%")
        self.meme_elapsed += 1

    def play_random_meme(self):
        if self.meme_elapsed >= self.next_meme:
            sound_file = random.choice(self.sounds)
            play_meme(sound_file)
            self.meme_elapsed = 0
            self.next_meme = random.randint(10, 20)

    def move_window(self):
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        new_x = max(0, min(self.x() + dx, 1440 - self.width()))
        new_y = max(0, min(self.y() + dy, 900 - self.height()))
        self.move(new_x, new_y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ClickVolume()
    win.show()
    sys.exit(app.exec_())

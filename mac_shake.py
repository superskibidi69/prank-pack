import sys, random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer

class Shaky(QWidget):
    def __init__(self, x, y, w=220, h=180):
        super().__init__()
        self.setGeometry(x, y, w, h)
        self.setStyleSheet(
            "QWidget { background-color: #0d0d0d; color: #00ff99; font-family: Courier; }"
        )
        self.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.screen_shake)
        self.timer.start(17)
    def screen_shake(self):
        dx, dy = random.randint(-12, 12), random.randint(-12, 12)
        self.move(self.x() + dx, self.y() + dy)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Shakey Shakey (Makey Makey reference)")

    windows = []
    for i in range(5):
        x, y = 300 + i * 50, 300 + i * 50
        win = Shaky(x, y)
        # win.setWindowTitle(f"Shakey {i+1}")
        windows.append(win)

    sys.exit(app.exec_())

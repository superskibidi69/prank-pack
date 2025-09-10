from PyQt5 import QtWidgets, QtCore
import sys
import tempfile
import os
from shutil import copyfile
import pyttsx3
from playsound import playsound

class TTSApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.audio_file = None
        self.init_ui()
        self.engine = pyttsx3.init()

    def init_ui(self):
        self.setWindowTitle("TTS API GUI (Local)")
        self.setGeometry(100, 100, 400, 250)

        self.layout = QtWidgets.QVBoxLayout()

        self.text_input = QtWidgets.QTextEdit(self)
        self.layout.addWidget(self.text_input)

        self.voice_label = QtWidgets.QLabel("Voice ID (for GUI only):", self)
        self.layout.addWidget(self.voice_label)

        self.voice_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.voice_input)

        self.btn_layout = QtWidgets.QHBoxLayout()

        self.speak_btn = QtWidgets.QPushButton("Speak & Play", self)
        self.speak_btn.clicked.connect(self.send_tts)
        self.btn_layout.addWidget(self.speak_btn)

        self.download_btn = QtWidgets.QPushButton("Download", self)
        self.download_btn.clicked.connect(self.download_audio)
        self.download_btn.setEnabled(False)
        self.btn_layout.addWidget(self.download_btn)

        self.layout.addLayout(self.btn_layout)

        self.status_label = QtWidgets.QLabel("", self)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def send_tts(self):
        text = self.text_input.toPlainText()
        voice_id = self.voice_input.text()  # kept for GUI, not used
        if not text:
            self.status_label.setText("Enter text!")
            return

        self.status_label.setText("Generating audio locally...")
        QtWidgets.QApplication.processEvents()

        try:
            # generate temp WAV locally
            temp_fd, temp_path = tempfile.mkstemp(suffix=".wav")
            os.close(temp_fd)  # pyttsx3 writes file, so close fd

            self.engine.save_to_file(text, temp_path)
            self.engine.runAndWait()

            self.audio_file = temp_path
            playsound(self.audio_file)
            self.download_btn.setEnabled(True)
            self.status_label.setText("Played audio locally! You can download now.")
        except Exception as e:
            self.status_label.setText("Fail")

    def download_audio(self):
        if not self.audio_file:
            return
        options = QtWidgets.QFileDialog.Options()
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Audio",
            "output.wav",
            "WAV Files (*.wav)",
            options=options
        )
        if save_path:
            copyfile(self.audio_file, save_path)
            self.status_label.setText("Saved!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = TTSApp()
    gui.show()
    sys.exit(app.exec_())

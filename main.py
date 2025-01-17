import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class MP3Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP3 Player")
        self.setGeometry(300, 300, 400, 300)

        self.player = QMediaPlayer()
        self.playlist = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Выберите папку с музыкой")
        layout.addWidget(self.label)

        self.song_list = QListWidget()
        layout.addWidget(self.song_list)

        self.play_button = QPushButton("Пуск/Пауза")
        self.play_button.clicked.connect(self.toggle_play_pause)
        layout.addWidget(self.play_button)

        self.next_button = QPushButton("Следующий трек")
        self.next_button.clicked.connect(self.next_song)
        layout.addWidget(self.next_button)

        self.load_button = QPushButton("Загрузить папку")
        self.load_button.clicked.connect(self.load_folder)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку с музыкой")
        if folder_path:
            self.playlist.clear()
            self.song_list.clear()
            for file in os.listdir(folder_path):
                if file.endswith(".mp3"):
                    self.playlist.append(os.path.join(folder_path, file))
                    self.song_list.addItem(file)

    def toggle_play_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("Пуск")
        else:
            current_song = self.song_list.currentRow()
            if current_song >= 0:
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[current_song])))
                self.player.play()
                self.play_button.setText("Пауза")

    def next_song(self):
        current_index = self.song_list.currentRow()
        if current_index < len(self.playlist) - 1:
            self.song_list.setCurrentRow(current_index + 1)
            self.toggle_play_pause()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MP3Player()
    player.show()
    sys.exit(app.exec_())

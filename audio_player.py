from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class AudioPlayer:
    def __init__(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.LowLatency)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
    
    def set_media(self, file_path):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
    
    def play_audio(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

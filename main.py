import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QFileDialog, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer
from audio_player import AudioPlayer
from transcription_segment import TranscriptionSegment
from interactive_events import InteractiveWaveform
from save_transcription import save_transcription

class AudioTranscriber(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Penny's Audio Transcriber")
        self.setGeometry(100, 100, 1200, 800)
        self.setFocusPolicy(Qt.StrongFocus)
 
        self.audioPlayer = AudioPlayer() 
        self.audioWaveform = InteractiveWaveform(self.audioPlayer.mediaPlayer)
        self.audioFileLoaded = False
        self.setupUI()
        
    def setupUI(self):    
        openButton = QPushButton("Open Audio File")
        openButton.clicked.connect(self.open_file)

        self.timeDisplayButton = QPushButton("0.000 s")
        self.timeDisplayButton.setFixedSize(120, 30)  # Set the width and height
        self.timeFormat = 'seconds'
        self.timeDisplayButton.clicked.connect(self.toggle_time_format)

        self.playButton = QPushButton("Play", self)
        self.playButton.clicked.connect(self.toggle_play)
        
        speedButton1 = QPushButton("x1")
        speedButton1.clicked.connect(lambda: self.set_speed(1))
        speedButton2 = QPushButton("x2")
        speedButton2.clicked.connect(lambda: self.set_speed(2))
        speedButton4 = QPushButton("x4")
        speedButton4.clicked.connect(lambda: self.set_speed(4))
        
        self.transcriptLabel = QLabel("Transcript:")
        self.transcriptEdit = QTextEdit()
        
        saveButton = QPushButton("Save Transcription")
        saveButton.clicked.connect(self.save_transcription)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)
        
        self.audioPlayer.mediaPlayer.positionChanged.connect(self.position_changed)
        self.audioPlayer.mediaPlayer.durationChanged.connect(self.duration_changed)
        
        layout = QVBoxLayout()
        layout.addWidget(openButton)
        layout.addWidget(self.audioWaveform)
        layout.addWidget(self.slider)
        
        timeLayout = QHBoxLayout() 
        timeLayout.addWidget(self.timeDisplayButton)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(speedButton1)
        controlLayout.addWidget(speedButton2)
        controlLayout.addWidget(speedButton4)
        
        layout.addLayout(timeLayout)
        layout.addLayout(controlLayout)
        layout.addWidget(self.audioPlayer.videoWidget)
        layout.addWidget(self.transcriptLabel)
        layout.addWidget(self.transcriptEdit)
        layout.addWidget(saveButton)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        
    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.mp3)")
        if fileName != '':
            self.audioPlayer.set_media(fileName)
            self.audioWaveform.plot_waveform(fileName)
            self.audioFileLoaded = True
            self.playButton.setEnabled(True)
            self.playButton.setText("Play")
    
    def save_transcription(self):
        text = self.transcriptEdit.toPlainText()
        save_transcription(text)
    
    def set_position(self, position):
        self.audioPlayer.mediaPlayer.setPosition(position)
        
    def toggle_time_format(self):
        if self.timeFormat == 'seconds':
            self.timeFormat = 'minutes'
        else:
            self.timeFormat = 'seconds'
        self.update_time_display(self.last_position)

    def position_changed(self, position):
        self.slider.setValue(position)
        self.last_position = position
        duration = self.audioPlayer.mediaPlayer.duration()
        if duration > 0:
            self.audioWaveform.update_pin(position)
            self.update_time_display(position)
            
    def update_time_display(self, position):
        milliseconds = position % 1000
        seconds = position // 1000
        mins, secs = divmod(seconds, 60)

        if self.timeFormat == 'seconds':
            self.timeDisplayButton.setText(f"{seconds}.{milliseconds:03d} s")
        else:
            self.timeDisplayButton.setText(f"{mins:02}:{secs:02}.{milliseconds:03d}")

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.toggle_play()
        super().keyPressEvent(event)

    def toggle_play(self):
        if self.audioPlayer.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.audioPlayer.mediaPlayer.pause()
            self.playButton.setText("Play")
        else:
            self.audioPlayer.mediaPlayer.play()
            self.playButton.setText("Pause")
    
    def set_speed(self, speed):
        self.audioPlayer.mediaPlayer.setPlaybackRate(speed)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioTranscriber()
    window.show()
    sys.exit(app.exec_())
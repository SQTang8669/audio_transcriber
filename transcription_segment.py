from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class TranscriptionSegment:
    def __init__(self):
        self.segmentWidget = QWidget()
        layout = QVBoxLayout()
        self.segmentLabel = QLabel("Segment Transcription:")
        self.segmentEdit = QTextEdit()
        layout.addWidget(self.segmentLabel)
        layout.addWidget(self.segmentEdit)
        self.segmentWidget.setLayout(layout)

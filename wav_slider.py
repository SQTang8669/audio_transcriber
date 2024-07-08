from PyQt5.QtWidgets import QSlider, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

class CustomSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super(CustomSlider, self).__init__(orientation, parent)
        self.visibleStart = 25  # Percentage of the start of the visible area
        self.visibleEnd = 75  # Percentage of the end of the visible area

    def paintEvent(self, event):
        super(CustomSlider, self).paintEvent(event)

        # Painting the rectangle on the slider
        painter = QPainter(self)
        rect = QRect(self.width() * self.visibleStart / 100, 0,
                     self.width() * (self.visibleEnd - self.visibleStart) / 100, self.height())
        painter.setBrush(QColor(200, 200, 255, 150))  # Semi-transparent blue
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

    def set_visible_range(self, start_percentage, end_percentage):
        # Assuming you have logic here to update the slider's transparent square
        pass
import sys
import numpy as np
from pydub import AudioSegment
import pyqtgraph as pg

class AudioWaveform(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(AudioWaveform, self).__init__(*args, **kwargs)
        self.setBackground('w')
        self.showGrid(x=False, y=False)
        self.setLimits(xMin=0) 
        self.setMinimumHeight(200)
        self.getAxis('left').setVisible(False)
        self.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))

        self.getViewBox().setMouseMode(pg.ViewBox.RectMode)

        self.line = None
        self.vline = None
        self.duration = 0
        self.last_position = 0

        self.window_len = 10
        self.half_win = 5

    def plot_waveform(self, file_path):
        audio = AudioSegment.from_file(file_path)

        duration_of_silence = self.half_win * 1000
        silence = AudioSegment.silent(duration=duration_of_silence, frame_rate=audio.frame_rate)

        padded_audio = silence + audio

        samples = np.array(padded_audio.get_array_of_samples())
        self.duration = len(samples) / audio.frame_rate
        
        time_axis = np.linspace(0, self.duration, num=len(samples))

        self.clear()

        self.line = self.plot(time_axis, samples, pen=pg.mkPen(color=(214, 192, 222), width=0.5))

        self.setXRange(0, self.window_len)

        if self.vline:
            self.removeItem(self.vline)
        self.vline = pg.InfiniteLine(pos=self.half_win, angle=90, pen=pg.mkPen('k', width=2))
        self.addItem(self.vline)

    def update_pin(self, position):
        position /= 1000
        position += self.half_win

        start = max(0, position - self.window_len / 2)
        end = min(self.duration, start + self.window_len)
        self.setXRange(start, end, padding=0)

        center_of_display = (start + end) / 2
        self.vline.setPos(center_of_display)

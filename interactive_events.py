# interactive_waveform.py
from audio_waveform import AudioWaveform

class InteractiveWaveform(AudioWaveform):
    def __init__(self, mediaPlayer, *args, **kwargs):
        super(InteractiveWaveform, self).__init__(*args, **kwargs)
        self.mediaPlayer = mediaPlayer
        self.getViewBox().setMouseEnabled(x=False, y=False)
        # self.plotItem.vb.setMouseEnabled(x=False, y=False) 
        # self.setMouseEnabled(x=False, y=False)

    def mousePressEvent(self, event):
        self.setFocus()
        super(InteractiveWaveform, self).mousePressEvent(event)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        increment = 2000  # This is the 5 seconds increment/decrement
        if delta > 0:
            new_position = self.mediaPlayer.position() - increment
        else:
            new_position = self.mediaPlayer.position() + increment
        # Check for boundaries of the media position
        new_position = max(0, min(new_position, self.mediaPlayer.duration()))
        self.mediaPlayer.setPosition(new_position)
        event.accept()

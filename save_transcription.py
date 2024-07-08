from PyQt5.QtWidgets import QFileDialog

def save_transcription(text):
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getSaveFileName(None, "Save Transcription", "", "Text Files (*.txt);;All Files (*)", options=options)
    if fileName:
        with open(fileName, 'w') as file:
            file.write(text)

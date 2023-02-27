import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, QObject, pyqtSignal

from pytube import Stream, Playlist
import os
import math

class Worker(QObject):
    def __init__(self,app):
        super().__init__()
        self.app = app

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        self.app.download(self.app.textboxValue)
        self.app.textbox.setText("")
        self.finished.emit()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Youtube Mp4 Downloader'
        self.setWindowIcon(QIcon('logo.ico'))
        self.left = 1000
        self.top = 600
        self.width = 420
        self.height = 170
        
        self.setFixedSize(self.width, self.height)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(380, 40)

        self.button = QPushButton('Download', self)
        self.button.move(150, 80)
        self.button.clicked.connect(self.on_click)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(15, 130, 400, 25)
        self.progress.setValue(0)

        self.show()

    def on_click(self):
        self.textboxValue = self.textbox.text()
        if(self.textboxValue):
            self.thread = QThread()
            self.worker = Worker(app=self)

            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
        else:
            QMessageBox.question(self, 'Error',
                                 "You have to input a link", QMessageBox.Ok, QMessageBox.Ok)

    def on_progress(
        self, stream: Stream, chunk: bytes, bytes_remaining: int
    ) -> None:
        filesize =  stream.filesize
        bytes_received = filesize - bytes_remaining
        progress_value = math.trunc(float(bytes_received / filesize) * 100)
        self.progress.setValue(progress_value)

    def download(self, url):
        try:
            playlist = Playlist(url)
            if(playlist):
                for p_video in playlist.videos:
                    p_video.register_on_progress_callback(self.on_progress)
                    video = p_video.streams.get_highest_resolution()

                    desktop_location = os.path.expanduser("~/Desktop") + "/"
                    video.download(output_path='.', filename='temp.mp4')
                    #base, ext = os.path.splitext(out_file)

                    final_file = rf"{p_video.title}" + ".mp4"
                    invalid = '<>:"/\|?*'
                    for char in invalid:
                        final_file = final_file.replace(char, '')

                    os.rename("temp.mp4", desktop_location + final_file)

                    print(p_video.title + " has been successfully downloaded.")
            else:
                QMessageBox.question(self, 'Invalid Url',
                                    "The youtube link you have given is not valid.", QMessageBox.Ok, QMessageBox.Ok)

        except:
            error = sys.exc_info()[1]
            QMessageBox.question(self, 'Error',
                                str(error), QMessageBox.Ok, QMessageBox.Ok)
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

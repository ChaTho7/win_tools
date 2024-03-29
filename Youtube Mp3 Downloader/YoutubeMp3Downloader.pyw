import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

from pytube import YouTube
import os
import ffmpeg


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Youtube Mp3 Downloader"
        self.setWindowIcon(QIcon("logo.ico"))
        self.left = 1000
        self.top = 600
        self.width = 420
        self.height = 140

        self.setFixedSize(self.width, self.height)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(380, 40)

        self.button = QPushButton("Download", self)
        self.button.move(150, 80)

        self.svgWidget = QSvgWidget(self)
        self.svgWidget.load("status.svg")
        self.svgWidget.setGeometry(QRect(300, 80, 30, 30))

        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        if textboxValue:
            download(textboxValue, self)
        else:
            QMessageBox.question(
                self,
                "Error",
                "You have to input a link",
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
        self.textbox.setText("")


def download(url, self):
    try:
        yt = YouTube(url=url)
        if yt:
            audio = (
                yt.streams.get_by_itag(22)
                or yt.streams.get_by_itag(18)
                or yt.streams.get_audio_only()
            )
            desktop_location = os.path.expanduser("~/Desktop") + "/"
            audio.download(output_path=".", filename="temp.mp3")
            # base, ext = os.path.splitext(out_file)

            final_file = rf"{audio.title}" + ".mp3"
            invalid = '<>:"/\|?*'
            for char in invalid:
                final_file = final_file.replace(char, "")
            stream = ffmpeg.input("temp.mp3")
            stream = ffmpeg.output(
                stream, final_file, acodec="libmp3lame", audio_bitrate=192000
            )
            ffmpeg.run(stream)
            os.remove("temp.mp3")
            os.rename(final_file, desktop_location + final_file)

            QMessageBox.question(
                self,
                "Download Completed",
                yt.title + " has been successfully downloaded.",
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
        else:
            QMessageBox.question(
                self,
                "Invalid Url",
                "The youtube link you have given is not valid.",
                QMessageBox.Ok,
                QMessageBox.Ok,
            )

    except:
        error = sys.exc_info()[1]
        QMessageBox.question(self, "Error", str(error), QMessageBox.Ok, QMessageBox.Ok)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

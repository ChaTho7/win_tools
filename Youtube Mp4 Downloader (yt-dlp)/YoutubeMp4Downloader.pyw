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

import yt_dlp, os, sys


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Youtube Mp4 Downloader"
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


def progress_hook(d):
    print("--------------------------")
    print(d["status"])
    if d["status"] == "finished":
        print("Done downloading")
    if d["status"] == "downloading":
        print(d["filename"], d["_percent_str"], d["_eta_str"])


def download(url, self):
    try:
        outtmpl = ""
        video_title = ""
        null_device = open(os.devnull, "w")
        with yt_dlp.YoutubeDL(
            params={
                "noplaylist": True,
            }
        ) as ydl:
            stdout_orig = sys.stdout
            stderr_orig = sys.stderr

            sys.stdout = null_device
            sys.stderr = null_device

            info = ydl.extract_info(url, download=False)

            sys.stdout = stdout_orig
            sys.stderr = stderr_orig

            video_title = info.get("title")

            desktop_location = os.path.expanduser("~/Desktop")
            invalid = '<>:"/\|?*'
            for char in invalid:
                video_title = video_title.replace(char, "")

            outtmpl = f"{desktop_location}/{video_title}.%(ext)s"

        ydl_opts = {
            "format": f"bestvideo[height<=1080][ext=mp4]+bestaudio/best[height<=1080]/best",
            "outtmpl": outtmpl,
            "progress_hooks": [progress_hook],
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            stdout_orig = sys.stdout
            stderr_orig = sys.stderr

            sys.stdout = null_device
            sys.stderr = null_device

            ydl.download([url])

            sys.stdout = stdout_orig
            sys.stderr = stderr_orig

        null_device.close()
        QMessageBox.question(
            self,
            "Download Completed",
            video_title + " has been successfully downloaded.",
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

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QInputDialog,
    QCheckBox,
    QDialog,
    QVBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5.QtSvg import QSvgWidget

import yt_dlp, os, sys, edit_metadata, get_metadata


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

        self.button.clicked.connect(self.on_download_button_click)
        self.show()

    @pyqtSlot()
    def on_download_button_click(self):
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


class CheckboxDialog(QDialog):
    def __init__(self, parent=None):
        super(CheckboxDialog, self).__init__(parent)
        self.setWindowTitle("Thumbnail")
        self.height = 70

        layout = QVBoxLayout()

        self.checkbox = QCheckBox("Include Thumbnail")
        layout.addWidget(self.checkbox)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_clicked)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def apply_clicked(self):
        self.accept()

    def get_checkbox_state(self):
        return self.checkbox.isChecked()


def download(url, self):
    try:
        outtmpl = ""
        video_title = ""
        video_thumbnail_url = ""
        api_result = {}
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
            video_thumbnail_url = info["thumbnail"]

            desktop_location = os.path.expanduser("~/Desktop")
            video_title = fix_title(video_title)

            outtmpl = f"{desktop_location}/{video_title}.%(ext)s"

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": outtmpl,
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

        try:
            api_result = get_metadata.get_metadata_from_api(video_title)
        except:
            error = sys.exc_info()[1]
            QMessageBox.question(self, "Error", str(
                error), QMessageBox.Ok, QMessageBox.Ok)
            pass

        metadata_title = set_title_metadata(
            self, api_result.get("title", None))
        metadata_artist = set_artist_metadata(
            self, api_result.get("artist", None))
        is_add_thumbnial = set_thumbnail(self)

        metadata_result = edit_metadata.edit(
            f"{desktop_location}/{video_title}.mp3", metadata_title, metadata_artist, video_thumbnail_url if (is_add_thumbnial and video_thumbnail_url is not None) else None)

        if metadata_result is not None:
            QMessageBox.question(
                self,
                "Metadata",
                metadata_result,
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
    except:
        error = sys.exc_info()[1]
        QMessageBox.question(self, "Error", str(
            error), QMessageBox.Ok, QMessageBox.Ok)
        pass


def set_title_metadata(self, title_from_api):
    title, done = QInputDialog.getText(
        self, 'Title Input', 'Enter the title:', text=title_from_api)
    if done:
        return title
    else:
        return None


def set_artist_metadata(self, artist_from_api):
    artist, done = QInputDialog.getText(
        self, 'Artist Input', 'Enter the artist:', text=artist_from_api)
    if done:
        return artist
    else:
        return None


def set_thumbnail(self):
    dialog = CheckboxDialog(self)
    if dialog.exec_() == QDialog.Accepted:
        thumbnail_option = dialog.get_checkbox_state()
        return thumbnail_option
    return False


def fix_title(video_title):
    invalid_chars = '<>:"/\|?*'
    invalid_blocks = ["(Lyrics)",
                      "lyrics",
                      "(Lyric Video)",
                      "[Lyric Video]",
                      "Lyric Video",
                      "(Official Video)",
                      "[Official Video]",
                      "Official Video",
                      "(Official Lyric Video)",
                      "[Official Lyric Video]",
                      "Official Lyric Video",
                      "(Music Video)",
                      "[Music Video]",
                      "Music Video",
                      "NCS - Copyright Free Music",
                      "[NCS Release]"]

    for char in invalid_chars:
        video_title = video_title.replace(char, "")
    for block in invalid_blocks:
        video_title = video_title.replace(block, "")

    return str(video_title).strip()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

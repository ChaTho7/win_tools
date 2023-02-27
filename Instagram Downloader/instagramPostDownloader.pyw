import sys, os, shutil

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import instaloader
from instaloader.structures import Post

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Instagram Post Downloader'
        self.setWindowIcon(QIcon('logo.ico'))
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

        self.button = QPushButton('Download', self)
        self.button.move(150, 80)

        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        if(textboxValue):
            download(textboxValue, self)
        else:
            QMessageBox.question(self, 'Error',
                                 "You have to input a link", QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

def download(url, self):
    try:
        download_success = False

        instance = instaloader.Instaloader()
        instance.login(user="",passwd="") # cocaxot501

        post_code = url
        post = Post.from_shortcode(instance.context,post_code)

        desktop_location = os.path.expanduser("~/Desktop") + "/"
        instance.download_post(post,"temp")
        files = os.listdir("./temp")
        for file in files:
            base_name, extension = os.path.splitext(file)
            if extension == ".jpg" or extension == ".mp4":
                is_exists = os.path.exists(desktop_location + "Insta Downloads")
                if is_exists:
                    os.rename(os.path.abspath(os.getcwd()) + "\\temp\\" + file,desktop_location + "Insta Downloads/"+ file)
                else:
                    os.makedirs(desktop_location + "Insta Downloads")
                    os.rename(os.path.abspath(os.getcwd()) + "\\temp\\" + file,desktop_location + "Insta Downloads/"+ file)
        #shutil.rmtree("temp")

        download_success = True
        #if download_success:
        #
        #    QMessageBox.question(self, 'Download Completed',
        #                            "Post has been successfully downloaded.", QMessageBox.Ok, QMessageBox.Ok)
        #else:
        #    QMessageBox.question(self, 'Invalid Url',
        #                         "The youtube link you have given is not valid.", QMessageBox.Ok, QMessageBox.Ok)
    except:
        error = sys.exc_info()[1]
        QMessageBox.question(self, 'Error',
                             str(error), QMessageBox.Ok, QMessageBox.Ok)
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

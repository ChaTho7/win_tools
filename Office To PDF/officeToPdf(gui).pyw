import subprocess
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

files = os.listdir(".")
extensions = [".doc", ".docx", ".dot", ".dotx", ".docm", ".xls", ".xlsm",
              ".pptx", ".ppt", ".ppsx", ".ppsm", ".pps", ".pptm"]

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Office to PDF'
        self.setWindowIcon(QIcon('logo.ico'))
        self.left = 1000
        self.top = 600
        self.width = 300
        self.height = 80
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.button = QPushButton('Convert', self)
        self.button.move(100,25)

        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        trigger(self)

def convert_to_pdf(file, self):
    try:
        libre_office = 'C:/Program Files/LibreOffice/program/soffice.exe'
        destination_path = './pdfs'

        subprocess.run(
            '"{}" --convert-to pdf --outdir "{}" "{}"'
            .format(libre_office, destination_path, file,), shell=True)
    except:
        error = sys.exc_info()[1]
        QMessageBox.question(self, 'Error',
                             str(error), QMessageBox.Ok, QMessageBox.Ok)
        pass

def trigger(self):
    for file in files:
        base_name, extension = os.path.splitext(file)
        if extension in extensions:
            convert_to_pdf(file,self)

    QMessageBox.question(self, 'Office to PDF',
                                 "Converting Completed. ", QMessageBox.Ok)
    self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
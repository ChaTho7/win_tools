import subprocess
import os
import sys
import tkinter
from tkinter.filedialog import askopenfilenames
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

extensions = [".doc", ".docx", ".dot", ".dotx", ".docm", ".xls", ".xlsm",
              ".pptx", ".ppt", ".ppsx", ".ppsm", ".pps", ".pptm"]
tkinter.Tk().withdraw()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Office to PDF'
        self.setWindowIcon(QIcon('logo.ico'))
        self.left = 1000
        self.top = 600
        self.width = 300
        self.height = 80

        self.setFixedSize(self.width, self.height)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.button = QPushButton('Convert', self)
        self.button.move(100,25)

        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        trigger(self)

def convert_to_pdf(file_path, parent_path, self):
    try:
        libre_office = 'C:/Program Files/LibreOffice/program/soffice.exe'

        destination_path = f"{parent_path}/pdfFiles/"
        if(os.path.isdir(f"{parent_path}/pdfFiles/") != True):
            os.mkdir(f"{parent_path}/pdfFiles/")

        subprocess.run(
            '"{}" --convert-to pdf --outdir "{}" "{}"'
            .format(libre_office, destination_path, file_path), shell=True)
    except:
        error = sys.exc_info()[1]
        QMessageBox.question(self, 'Error',
                             str(error), QMessageBox.Ok, QMessageBox.Ok)
        pass

def trigger(self):
    file_paths = askopenfilenames()

    for file_path in file_paths:
        parent_path, file_name = os.path.split(file_path)
        base_name , extension = os.path.splitext(file_name)

        if extension in extensions:
            convert_to_pdf(file_path, parent_path, self)

    QMessageBox.question(self, 'Office to PDF',
                                 "Converting Completed. ", QMessageBox.Ok)
    self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
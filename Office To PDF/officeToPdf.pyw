import tkinter
from tkinter.filedialog import askopenfilenames
import subprocess
import os
import sys

mode = sys.argv[2]
extensions = [
    ".doc",
    ".docx",
    ".dot",
    ".dotx",
    ".docm",
    ".xls",
    ".xlsm",
    ".pptx",
    ".ppt",
    ".ppsx",
    ".ppsm",
    ".pps",
    ".pptm",
    ".rtf",
    ".pdf",
]

tkinter.Tk().withdraw()


def convert_to_pdf(file_path, parent_path):
    try:
        libre_office = "C:/Program Files/LibreOffice/program/soffice.exe"

        destination_path = f"{parent_path}/pdfFiles/"
        if os.path.isdir(f"{parent_path}/pdfFiles/") != True:
            os.mkdir(f"{parent_path}/pdfFiles/")

        subprocess.run(
            '"{}" --convert-to pdf --outdir "{}" "{}"'.format(
                libre_office, destination_path, file_path
            ),
            shell=True,
        )
    except:
        error = sys.exc_info()[1]
        print(str(error))
        pass


if mode == "file":
    file_path = sys.argv[1]

    parent_path, file_name = os.path.split(file_path)
    base_name, extension = os.path.splitext(file_name)

    convert_to_pdf(file_path, parent_path)
else:
    working_path = sys.argv[1]

    file_paths = askopenfilenames(initialdir=working_path)

    for file_path in file_paths:
        parent_path, file_name = os.path.split(file_path)
        base_name, extension = os.path.splitext(file_name)

        if extension in extensions:
            convert_to_pdf(file_path, parent_path)

tkinter.Tk().quit()

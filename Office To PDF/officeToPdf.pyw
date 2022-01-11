import subprocess
import os
import sys

files = os.listdir(".")
extensions = [".doc", ".docx", ".dot", ".dotx", ".docm", ".xls", ".xlsm",
              ".pptx", ".ppt", ".ppsx", ".ppsm", ".pps", ".pptm"]

def convert_to_pdf(file):
    try:
        libre_office = 'C:/Program Files/LibreOffice/program/soffice.exe'
        destination_path = './pdfs'

        subprocess.run(
            '"{}" --convert-to pdf --outdir "{}" "{}"'
            .format(libre_office, destination_path, file,), shell=True)
    except:
        error = sys.exc_info()[1]
        print(str(error))
        pass

for file in files:
    base_name, extension = os.path.splitext(file)
    if extension in extensions:
        convert_to_pdf(file)


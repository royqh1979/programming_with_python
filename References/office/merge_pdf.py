"""
A simple python script to merge all the pdf files in the directory where this script is located.

@author: Yuanyang Shao
"""

import PyPDF2
from easygraphics import dialog as dlg

import os
from pathlib import Path



def main():
    # find all the pdf files in current directory.
    dir_path = dlg.get_directory_name("请选择要转换的目录")

    path = Path(dir_path)
    pdfFM = PyPDF2.PdfFileMerger()
    open_files = []
    for entry in path.iterdir():
        if not entry.is_file():
            continue
        filename = str(path.absolute()) + os.sep + entry.name.lower()
        if filename.endswith(".pdf"):
            file = open(filename,'rb')
            pdfFM.append(file)

    # output the file.
    with open(dir_path + "\\Merged.pdf", 'wb') as write_out_file:
        pdfFM.write(write_out_file)

    for file in open_files:
        file.close()


if __name__ == '__main__':
    main()
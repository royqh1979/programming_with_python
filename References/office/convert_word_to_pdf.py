from comtypes.client import CreateObject,Constants
from easygraphics import dialog as dlg

import os
from pathlib import Path



app = CreateObject("Word.Application")
word_constants = Constants(app)

dir_path = dlg.get_directory_name("请选择要转换的目录")

path = Path(dir_path)

for entry in path.iterdir():
    if not entry.is_file():
        continue
    print()
    filename = str(path.absolute())+os.sep+entry.name.lower()
    if filename.endswith(".doc") or filename.endswith(".docx"):
        print(filename)
        newname = filename.replace(".docx",".pdf")
        newname = filename.replace(".doc",".pdf")
        presentation = app.Documents.Open(filename)
        presentation.SaveAs2(newname, word_constants.wdFormatPDF)
        presentation.Close()

app.Quit()
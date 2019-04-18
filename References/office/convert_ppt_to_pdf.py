from comtypes.client import CreateObject,Constants
from easygraphics import dialog as dlg

import os
from pathlib import Path



app = CreateObject("Powerpoint.Application")
pp_constants = Constants(app)

dir_path = dlg.get_directory_name("请选择要转换的目录")

path = Path(dir_path)

for entry in path.iterdir():
    if not entry.is_file():
        continue
    print()
    filename = str(path.absolute())+os.sep+entry.name.lower()
    if filename.endswith(".ppt") or filename.endswith(".pptx"):
        print(filename)
        newname = newname.replace(".pptx",".pdf")
        newname = filename.replace(".ppt",".pdf")
        presentation = app.Presentations.Open(filename)
        presentation.SaveAs(newname, pp_constants.ppSaveAsPDF)
        presentation.Close()

app.Quit()
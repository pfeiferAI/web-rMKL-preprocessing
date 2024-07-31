"""
This file is part of web-rMKL preprocessing.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__author__ = "Nicolas Kersten"
__license__ = 'GNU General Public License v3.0'

import os

ui_files = ["MainWindow", "LogDialog", "AboutDialog"]
qrc_file = "icons_and_img"

if __name__ == "__main__":
    for ui_element in ui_files:
        ui_file_path = os.path.join("../res", f"{ui_element}.ui")
        py_file_path = os.path.join("../preprocessing", f"{ui_element}.py")
        os.system("pyside6-uic -o %s %s" % (py_file_path, ui_file_path))
        with open(py_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if "import icons_and_img_rc" in line:
                lines[i] = "from preprocessing import icons_and_img_rc\n"
                break
        with open(py_file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"Converted {ui_element}.ui to {ui_element}.py")
    qrc_file_path = os.path.join("../res", f"{qrc_file}.qrc")
    py_file_path = os.path.join("../preprocessing", f"{qrc_file}.py")
    os.system(f"pyside6-rcc -o {py_file_path} {qrc_file_path}")
    print(f"Converted {qrc_file}.qrc to {qrc_file}.py")
    print("Done.")
    exit(0)

#!/bin/bash

ui_files=("MainWindow" "AboutDialog" "LogDialog")

if [ ! -d "../res" ] && [ ! -d "../src" ]; then
    echo "Please run this script from the project build directory."
    exit 1
fi

for ui_file in "${ui_files[@]}"; do
    ui_file_path="../res/$ui_file.ui"
    py_file_path="../preprocessing/${ui_file}.py"
    pyside6-uic -o "${py_file_path}" "${ui_file_path}"
    # replace resource import statement to make the file compatible with the package structure
    while IFS= read -r line; do
        if [[ "${line}" == *"import icons_and_img_rc"* ]]; then
            line="from preprocessing import icons_and_img_rc"
        fi
        echo "${line}" >> "${py_file_path}.tmp"
    done < "${py_file_path}"
    mv "${py_file_path}.tmp" "${py_file_path}"
    echo "Converted ${ui_file}"
done

pyside6-rcc -o "../preprocessing/icons_and_img_rc.py" "../res/icons_and_img.qrc"
echo "Converted icons_and_img.qrc"


echo "Done."
exit 0
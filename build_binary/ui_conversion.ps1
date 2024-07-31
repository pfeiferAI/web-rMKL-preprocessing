$ui_files = @("MainWindow", "AboutDialog", "LogDialog")

if (-not (Test-Path "../res") -and -not (Test-Path "../src")) {
    Write-Error "Please run this script from the project build directory."
    exit 1
}

foreach ($ui_file in $ui_files) {
    $ui_file_path = "../res/$ui_file.ui"
    $py_file_path = "../preprocessing/${ui_file}.py"
    pyside6-uic -o $py_file_path $ui_file_path
    # replace resource import statement to make the file compatible with the package structure
    Get-Content $py_file_path | ForEach-Object {
        if ($_ -like "*import icons_and_img_rc*") {
            $_ = "from preprocessing import icons_and_img_rc"
        }
        $_
    } | Set-Content "${py_file_path}.tmp"
    Move-Item -Force "${py_file_path}.tmp" $py_file_path # replace the original file
    Write-Output "Converted $ui_file"
}

pyside6-rcc -o "../preprocessing/icons_and_img_rc.py" "../res/icons_and_img.qrc"
Write-Output "Converted icons_and_img.qrc"

Write-Output "Done."
exit 0
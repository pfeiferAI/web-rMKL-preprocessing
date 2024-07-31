#!/bin/bash
# Build the binary for linux
# Usage: ./build_linux.sh [build_folder]
# Requirements: Pyinstaller, linuxApp.spec

# check directory argument
if [ -z "$1" ]
then
    echo "No build directory specified, cannot build"
    exit 1
fi

# create subdirectories for dist and build
mkdir -p "$1/dist"
mkdir -p "$1/build"

# build the app using pyinstaller
pyinstaller linuxApp.spec --distpath "$1/dist" --workpath "$1/build" --clean -y

# check if build was successful
if [ $? -eq 0 ]
    then
        echo "Build successful"
        exit 0
    else
        echo "Build failed"
        exit 1
fi
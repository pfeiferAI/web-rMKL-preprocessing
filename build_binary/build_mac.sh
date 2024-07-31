#!/bin/bash
# Build the binary for macOS
# Usage: ./build_mac.sh [build_folder] [-p] -> -p will trigger packaging the app into a dmg
# Requirements: Pyinstaller, create-dmg and macOS, macApp.spec
# Note: This script only creates the app and dmg for the target architecture (x86_64 or arm64)

# check directory argument
if [ -z "$1" ]
then
    echo "No build directory specified, cannot build"
    exit 1
fi

# check if packaging is requested
if [ -z "$2" ]
  then
      PACKAGE=true
  else
      PACKAGE=false
fi

# check if build directory exists
if [ ! -d "$1" ]
then
    echo "Build directory does not exist, creating it"
    mkdir "$1"
fi

# create subdirectories for dist and build
mkdir -p "$1/dist"
mkdir -p "$1/build"

# build the app using pyinstaller
pyinstaller macApp.spec --distpath "$1/dist" --workpath "$1/build" --clean -y

# check if build was successful
if [ $? -eq 0 ]
    then
        echo "Build successful"
    else
        echo "Build failed"
        exit 1
fi

# continue if packaging is requested
if [ "$PACKAGE" == false ]
    then
        exit 0
fi

# read the app name and the icon name from the spec file
APP_NAME=$(sed -n '/app = /,$p' macAPP.spec | grep 'name=' | tr -d ' ' | cut -d '=' -f 2 | tr -d "'" | tr -d ',')
APP_ICON=$(sed -n '/app = /,$p' macAPP.spec | grep 'icon=' | tr -d ' ' | cut -d '=' -f 2 | tr -d "'" | tr -d ',')

# run build_dmg.sh to package the app
./build_dmg.sh "$1/dist" "$APP_NAME" "$APP_ICON"
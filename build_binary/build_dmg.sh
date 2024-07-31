#!/bin/zsh
# Build a DMG for the Python distribution.
# The destination of the APP should be passed as the first argument.
# The name of the App should be passed as the second argument.
# The path to the icon file should be passed as the third argument.
# Check if output directory argument is provided
if [ -z "$1" ]
    then
        echo "Error: Output directory argument is missing"
        exit 1
fi
# Check if app name argument is provided
if [ -z "$2" ]
    then
        echo "Error: App name argument is missing"
        exit 1
fi
# Check if icon file argument is provided
if [ -z "$3" ]
    then
        echo "Error: Icon file argument is missing"
        exit 1
fi

# Store the basename of the App and the DMG path
APP_NAME=$(basename "$2" .app)
DMG_NAME="$1/$APP_NAME.dmg"

# Create a temporary directory to hold the DMG contents.
mkdir -p $1/dmg
rm -r $1/dmg/*
# Copy the Python distribution into the temporary directory.
cp -r "$1/$2" $1/dmg
# Check that the DMG doesn't already exist.
test -f "$$DMG_NAME" && rm "$$DMG_NAME"
# Create the DMG.
create-dmg \
  --volname "$APP_NAME" \
  --volicon "$3" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "$2" 175 120 \
  --hide-extension "$APP_NAME" \
  --app-drop-link 450 120 \
  "$DMG_NAME" \
  "$1/dmg/"
# Clean up.
rm -r $1/dmg
# Check if create-dmg ran successfully
if [ $? -eq 0 ]
    then
        echo "create-dmg ran successfully"
        exit 0
    else
        echo "create-dmg failed"
        exit 1
fi
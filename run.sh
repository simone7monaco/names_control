#!/bin/bash

abspath ()
{
case "${1}" in
    [./]*)
    local ABSPATH="$(cd ${1%/*}; pwd)/"
    echo "${ABSPATH/\/\///}"
    ;;
    *)
    echo "${PWD}/"
    ;;
esac
}

SCRIPT_DIR=`abspath ${0}`

streamlit run $SCRIPT_DIR/web_app.py


# To add an icon to your new application, you need to do the following:
# 
# Find or create a PNG that you want to be your icon.
# 
# Open the image in the Preview application – other graphics apps may also work.
# 
# Press command-a to select all and then command-c to copy it to the clipboard.
# 
# Select your application in the Finder and press command-i to Get Info window.
# 
# Click on the icon in the upper left corner of the info window to select it:
# 
# enter image description here
# 
# Paste the image from the clipboard which should change the icon.
# 
# enter image description here
# 
# You can also open up the Get Info window on other application, select it's icon, and copy it so you can paste it onto your new application. After you assign any icon, if you look in your .app directory, you should see a filename that starts with Icon.

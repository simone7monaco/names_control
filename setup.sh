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

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# PATH=$PATH:$CURRENTPATH

echo "Installing..."
# python -m pip install -r $SCRIPT_DIR/requirements.txt
# streamlit run $SCRIPT_DIR/web_app.py
mkdir -p /Applications/Controlla_Nomi.app/Contents/MacOS

cp $SCRIPT_DIR/run.sh /Applications/Controlla_Nomi.app/Contents/MacOS/Controlla_Nomi
chmod +x /Applications/Controlla_Nomi.app/Contents/MacOS/Controlla_Nomi
cp $SCRIPT_DIR/Controller.py /Applications/Controlla_Nomi.app/Contents/MacOS/Cotroller.py
cp $SCRIPT_DIR/hotwords.yaml /Applications/Controlla_Nomi.app/Contents/MacOS/

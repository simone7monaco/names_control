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
mkdir -p s/Applications/Controlla_Nomi.app/Contents/MacOS

cp run.sh /Applications/Controlla_Nomi.app/Contents/MacOS/Controlla_Nomi
chmod +x /Applications/Controlla_Nomi.app/Contents/MacOS/Controlla_Nomi
cp web_app.py /Applications/Controlla_Nomi.app/Contents/MacOS/
cp hotwords.yaml /Applications/Controlla_Nomi.app/Contents/MacOS/

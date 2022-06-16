#!/bin/bash
#Generate a desktop for cutrestick
BASEDIR=$(dirname $0)
if [[ $BASEDIR == "." ]]
then
	BASEDIR=$PWD
fi
cd $BASEDIR
DIR=${BASEDIR//\//\\/}
sed  -e "s/Exec=.*/Exec=$DIR\/cutrestick\.py/"  -e "s/Icon=.*/Icon=$DIR\/images\/joyOriginal\.jpg/" cutrestick.desktop > $HOME/.local/share/applications/cutrestick.desktop

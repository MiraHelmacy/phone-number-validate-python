#!/bin/sh

#local user directory for when the files are stored.
localDirectory="$HOME/.local/phone-number-validate"

#location where the link between the path and the local directory is
linkLocation="/usr/local/bin/phone-number-validate"

#make link in path
sudo rm $linkLocation && sudo ln -s "$localDirectory/phone-number-validate" $linkLocation || sudo ln -s "$localDirectory/phone-number-validate" $linkLocation

# make a directory for the files to go into
rm -rf $localDirectory && mkdir -p $localDirectory || mkdir -p $localDirectory

#add execute to phone-number-validate
chmod +x phone-number-validate

#copy files to the directory
cp README.md $localDirectory
cp LICENSE $localDirectory
cp phone-number-validate $localDirectory
cp -r validate $localDirectory
cp -r fileio $localDirectory


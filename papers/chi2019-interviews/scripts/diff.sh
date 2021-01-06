#!/bin/sh
#verify that there are exactly 2 inputs
if [ $# != 2 ]; then
   echo "Please provide the folders containing the original and the revised versions of the paper, respectively."
   echo "USAGE: ./diff.sh original_folder revised_folder"
   exit 0
fi

#check for arguments being directories and existing.
if [ ! -d "$1" -o ! -d "$2" ]; then
   echo "The specified arguments must be folders."
   echo "USAGE: ./diff.sh original_folder revised_folder"
   exit 0
fi

#add check for file already existing
#add check for file existing in the original location
if [ ! -f "$2"/Makefile ]; then
   echo "ERROR: Makefile does not exist."
   exit 0
fi

#add check for directory existing
if [ ! -d diff ]; then
   mkdir diff
fi

original=$1
revised=$2

%TODO: Handle case of diffing from repo.

cp -R "$revised"/* diff
rm diff/*.tex

echo "Ready to diff..."

for file in "$original"/*.tex 
do 
   filename=$(basename "$file")
   latexdiff "$original"/"$filename" "$revised"/"$filename" > diff/"$filename"
done

cd diff
make

#TODO rename PDF by adding diff at the end

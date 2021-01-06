#!/bin/sh
#Script to change the template files to paper-specific name.

#verify that there is only and exactly 1 input
if [ $# != 1 ]; then
   echo "Please provide the name of the paper."
   exit 0
fi

#verify file exists before renaming
if [ -f template.tex ]; then
   mv template.tex $1.tex
fi

if [ -f references_template.bib ]; then 
   mv references_template.bib references_"$1".bib
fi

#replace "template.tex" and "references_template.bib" in individual section tex files
sed -i '' 's/template/$1/g' *.tex

#replace "template.tex" and "references_template.bib" names in Makefile
sed -i '' 's/template/$1/g' Makefile

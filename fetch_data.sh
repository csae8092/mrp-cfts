#/bin/bash


rm -rf data
mkdir -p ./data/editions
mkdir -p ./data/indices
wget https://zenodo.org/record/6424734/files/oeaw-ministerratsprotokolle/mp-edition-data-v1.2.zip?download=1 -O dl.zip
unzip dl.zip
find -path "*TEI/*.xml" -exec cp -prv '{}' './data/editions' ';'
find -path "*ndices/*.xml" -exec cp -prv '{}' './data/indices' ';'
mv './data/indices/standOff.xml' './data/indices/listperson.xml'
rm -rf ./oeaw*
rm dl.zip
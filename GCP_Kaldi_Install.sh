#!/bin/bash
#Script to git and install kaldi on Google Cloud Platform linux instance


#Get number of available cpus
n=$(nproc --all) #will be used to speed up make

#Check if git installed
which git
[ $? -eq 0 ] || (echo "git not installed... \n Installing git..\n" && sudo apt-get update && sudo apt-get --assume-yes install git)

#Git Kaldi
git clone https://github.com/kaldi-asr/kaldi.git kaldi --origin upstream

#Install dependencies
sudo apt-get install --assume-yes g++ make automake autoconf bzip2 unzip sox libtool subversion zlib1g-dev

cd kaldi/tools
sudo ./extras/install_mkl.sh

make -j $n

cd ../src

./configure --shared

make depend -j $n

make -j $n

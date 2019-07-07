#!/bin/bash
#
#This code for preparing the OGI kids data for kaldi ASR training
#Should be run from s5 directory

set -e

if [ $# != 1 ]; then
	echo "Usage: ogi_data_prep.sh /path/to/ogi_data"
	exit 1;
fi

export LC_ALL=C #To make sure that the sorting of files will be performed in the same way as C++

OGIROOT=$1
ver=1,2,3 #The selected level of verification 
grads='5-10' #The selected grad range of children

trndir=data/train
tstdir=data/test
devdir=data/dev

mkdir -p $trndir $tstdir $devdir

. ./path.sh || exit 1; # for KALDI_ROOT

[ ! -d $OGIROOT/docs ] && echo "Error: the OGI directory must contains docs directory" && exit 1;

#Split speakers among test dev train in 3 sep files each contain list of speakers
#Write code in the shell to generate 3 dir data/train data/test data/dev and modify the below code to accept list of spekers 

touch $trndir/spkrs $tstdir/spkrs $devdir/spkrs

#Split speakers to train, test and dev by default 15% for test, 15% dev and 70% training
#Can be modified by passing optional --train_portion float, --test_portion float, --dev_portion float to the command

local/ogi_split_data.py $OGIROOT $trndir/spkrs $tstdir/spkrs $devdir/spkrs

for dir in $trndir $tstdir $devdir; do
    
    local/gen_text_utt2spkr.py $OGIROOT $dir/text $dir/utt2spk $dir/wav.scp -l $dir/spkrs -v $ver -g $grads

    #Sort Files
    sort -o $dir/text $dir/text
    sort -o $dir/utt2spk $dir/utt2spk
    sort -o $dir/wav.scp $dir/wav.scp

    utils/utt2spk_to_spk2utt.pl $dir/utt2spk > $dir/spk2utt

done

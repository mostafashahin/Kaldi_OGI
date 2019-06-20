#!/bin/bash

. ./cmd.sh
set -e # exit on error

#Call data preparation script with the path to the OGI data (must contains the docs disrectory)

local/ogi_data_prep.sh /media/mostafa/Windows/root/PhD/Datasets/OREGON_Kids_Corpus/

#Generate MFCC

for part in train test dev; do
    mfccdir=data/$part/mfcc
    mfcclog=exp/make_mfcc/$part
    mkdir -p $mfccdir $mfcclog
    steps/make_mfcc.sh --nj 4 --cmd "$train_cmd" data/$part $mfcclog $mfccdir
    steps/compute_cmvn_stats.sh data/$part $mfcclog $mfccdir
done

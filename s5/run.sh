#!/bin/bash

. ./cmd.sh
set -e # exit on error

#Call data preparation script with the path to the OGI data (must contains the docs disrectory)

local/ogi_data_prep.sh /media/mostafa/Windows/root/PhD/Datasets/OREGON_Kids_Corpus/

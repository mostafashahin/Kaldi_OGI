#!/bin/bash
#
#This code for preparing the data/local/dict dirictory of OGI kids data for kaldi ASR training
#Should be run from s5 directory

set -e

if [ $# != 1 ]; then
	echo "Usage: $(basename $0) /path/to/ogi_data"
        exit 1;
fi

#Make sure that srilm installed
echo $KALDI_ROOT/tools/srilm/bin/i686-m64
which ngram-count
[ $? -eq 0 ] || [ -d $KALDI_ROOT/tools/srilm/bin/i686-m64 ] && export PATH=$PATH:$KALDI_ROOT/tools/srilm/bin/i686-m64 || exit 1

OGIROOT=$1
langdir=`pwd`/data/lang
dir=`pwd`/data/local/lm_srilm

#TODO check existance of srilm, exit if not exist

#Check if dir exist, otherwise create it
[ -d $dir ] || mkdir -p $dir || exit 1

#TODO Do the same for spontenous data

#Get Text from scripted data
cat $OGIROOT/docs/all.map | gawk -F\" '{print $2}' | sed -E -e 's/([[:alnum:]]+)[,"\x27](\s)/\1\2/g' -e '/^$/d' | tr [:lower:] [:upper:] > $dir/scripted_txt.tmp

#Get unique set of OGI words, normalize the text by removing the /,/, /"/ or /'/ at the end of the word.  

cat $dir/scripted.txt | tr " " "\n" | sort -u > $dir/scripted_words.tmp


#Use ngram-count from srilm to generate bi gram LM from the list of scripted words

ngram-count -text $dir/scripted_txt.tmp -order 2 -lm $dir/bi.lm

#convert to fst format

arpa2fst --disambig-symbol=#0 --read-symbol-table=$langdir/words.txt $dir/bi.lm $langdir/G.fst

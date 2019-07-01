#!/bin/bash
#
#This code for preparing the data/local/dict dirictory of OGI kids data for kaldi ASR training
#Should be run from s5 directory

if [ $# != 1 ]; then
        echo "Usage: ogi_dict_prep.sh /path/to/ogi_data"
        exit 1;
fi

OGIROOT=$1
dir=`pwd`/data/local/dict

#Run wsj_prepare_dict.sh -- Rewrite it in python 
local/wsj_prepare_dict.sh || exit 1

#Check that all words are in the lexicon

#Get unique set of OGI words

cat $OGIROOT/docs/all.map | gawk -F\" '{print $2}' \
	| tr " " "\n" | sort -u | sed -E -e 's/([[:alnum:]]+)([,"\x27])$/\1/g' -e '/^$/d' | \
	tr [:lower:] [:upper:] > $dir/ogi-words.tmp

#Get unique set of cmu dict words
cat $dir/cmudict/cmudict.0.7a | sed '/^;;;/d' | gawk '{print $1}' | \
	sort -u > $dir/cmu-words.tmp

#Check if all exist in 
grep -owFf $dir/ogi-words.tmp $dir/cmu-words.tmp | grep -vwFf - $dir/ogi-words.tmp > $dir/missing-words.tmp

#Run pronunciation tool come with logios 
svn co http://svn.code.sf.net/p/cmusphinx/code/trunk/logios/ $dir/logios

perl $dir/logios/Tools/MakeDict/make_pronunciation.pl -tools $dir/logios/Tools/ -dictdir $dir -words missing-words.tmp -dict missing-words.dict

cat $dir/lexicon.txt $dir/missing-words.dict > $dir/lexicon.tmp
sort -u $dir/lexicon.tmp > $dir/lexicon.txt
#TODO merge with lexicon dict
#TODO do normalization step here and in prepare data to remoe ',' 

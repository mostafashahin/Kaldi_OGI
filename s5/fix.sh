#!/bin/bash
OGIROOT=/srv/scratch/z5173707/Dataset/OGI/
#spontaneous
sed -i 's/<long<bn>/<long><bn>/g' $OGIROOT/trans/spontaneous/08/0/ks80r/ks80rxx0.txt
sed -i 's/<ns./<ns>./g'  $OGIROOT/trans/spontaneous/09/3/ksk1e/ksk1exx0.txt
sed -i 's/\.\.//g' $OGIROOT/trans/spontaneous/09/3/ksk1e/ksk1exx0.txt
sed -i 's/<ln>>/<ln>/g' $OGIROOT/trans/spontaneous/08/1/ksj3y/ksj3yxx0.txt
sed -i 's/ sniff>/ <sniff>/g' $OGIROOT/trans/spontaneous/09/2/ks904/ks904xx0.txt
sed -i 's/<bs: no no>/<bs>/g' $OGIROOT/trans/spontaneous/01/2/ks105/ks105xx0.txt
sed -i 's/<bs: dave>/<bs>/g' $OGIROOT/trans/spontaneous/01/0/ks10i/ks10ixx0.txt
sed -i 's/<sing<bn>>/<sing><bn>/g' $OGIROOT/trans/spontaneous/00/3/ksb0i/ksb0ixx0.txt
sed -i 's/<sing<bn>/<sing><bn>/g' $OGIROOT/trans/spontaneous/01/2/ksc0h/ksc0hxx0.txt
sed -i 's/<bs./<bs>./g' $OGIROOT/trans/spontaneous/01/0/ksc3l/ksc3lxx0.txt
sed -i 's/<<bs>/<bs>/g' $OGIROOT/trans/spontaneous/04/2/ksf0p/ksf0pxx0.txt
sed -i 's/<ln>>/<ln>/g' $OGIROOT/trans/spontaneous/08/0/ks83w/ks83wxx0.txt
sed -i 's/\.//g' $OGIROOT/trans/spontaneous/01/0/ksc3l/ksc3lxx0.txt 
#scripted
grep -q ^8V $OGIROOT/docs/all.map; [ $? -eq 0 ] || echo 8V \"abnormal\" >> $OGIROOT/docs/all.map

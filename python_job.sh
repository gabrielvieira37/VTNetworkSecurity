#!/bin/sh
START=1
END=$1
hash_name=$(awk -F "=" '/hash_name/{print $2}' hash.ini)
rm received_times.json 2> /dev/null

for ((c=$START; c<=$END; c++))
do 
    echo "$c"
    python3 sender.py
    sleep 1
done


python3 plot_graphs.py  -n $hash_name
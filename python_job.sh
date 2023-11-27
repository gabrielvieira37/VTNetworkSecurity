#!/bin/sh
START=1
END=$1
# hash_name=$(awk -F "=" '/hash_name/{print $2}' hash.ini)
hash_name=$2

rm received_times.json 2> /dev/null

for ((c=$START; c<=$END; c++))
do 
    echo "$c"
    python3 sender.py -ha $hash_name
    sleep 1
done


python3 group_times.py  -n $hash_name
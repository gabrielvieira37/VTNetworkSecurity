#!/bin/sh
START=1
END=5

rm received_times.json 2> /dev/null

for ((c=$START; c<=$END; c++))
do 
    echo "$c"
    python3 sender.py
    sleep 1
done


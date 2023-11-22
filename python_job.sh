#!/bin/sh
START=1
END=5
for ((c=$START; c<=$END; c++))
do 
    echo "$c"
    python3 sender.py
    sleep 1
done


#!/bin/bash

echo "Running qmin lookup..."
echo "Resolver list: $1"
echo "Geographical location: $2"
mkdir -p results
for i in {0..99}; do 
    workers=2000
    out_file=results/$2-$i-$(date +"%Y-%m-%d-%H%M%S").csv
    ./multi-thread-qmin.py -r $1 -w $workers --geo $2 -i $i > $out_file
done


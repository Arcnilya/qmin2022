#!/bin/bash

today=$(date +%F)
wget -q https://dnsthought.nlnetlabs.nl/report.csv
mv report.csv qmin_adoption_over_time_$today.csv
wget -q https://dnsthought.nlnetlabs.nl/does_qnamemin/report.csv
mv report.csv does_qnamemin_$today.csv

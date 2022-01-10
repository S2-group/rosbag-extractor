#!/bin/bash

terms=$2
file=$1
username=$3
hash=$4

if [ $# -lt 4 ]; then # -lt -> '<'
	echo "Please, set up all the parameters:"
	echo "./extract.sh filename terms username hash"
	exit 0
fi

echo $terms

dir="./data/"$file

# if the file dir not exist then mkdir
if [ ! -d $dir ]; then
	mkdir -p $dir
fi

### search before 2015
date='<2015-01-01'
curl -u $username:$hash "https://api.github.com/search/repositories?q=$terms+created:$date" -o $dir"/"before_2015".json"
###

### Search by Month
year=2015
months=(01 02 03 04 05 06 07 08 09 10 11 12)
day=30

while [ $year -lt 2022 ]; do # -lt -> '<'
  for month in ${months[*]}; do # search for each month
    echo $month"/"$year
    echo "rest 60 seconds now"
    sleep 30

    # determine days of the month
    if [ $month -eq 02 ]; then # -eq -> '='
      day=28
    else
      if [ $month -lt 8 ]; then
        if [ $((month%2)) -eq 0 ]; then
          day=30
        else
          day=31
        fi
      else
        if [ $month -eq 08 ] || [ $month -eq 10 ] || [ $month -eq 12 ]; then
          day=31
        else
          day=30
        fi
      fi
    fi

    # search syntax: YYYY-MM-DD..YYYY-MM-DD
    date=$year"-"$month"-01"..$year"-"$month"-"$day
    # per_page default : 30
    # page default: 1
    curl -u $username:$hash "https://api.github.com/search/repositories?q=$terms+created:$date" -o $dir"/"$year"-"$month".json"
  done

  year=$((year+1))
done
###

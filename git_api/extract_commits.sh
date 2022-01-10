#!/bin/bash

terms=$2
file=$1
username=$3
hash=$4

# if parameter less than 6, then something is missing
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
date='<2010-01-01'
echo "before 2010"
curl -u $username:$hash "https://api.github.com/search/commits?q=$terms+committer-date:$date&per_page=100" -o $dir"/"before_2010".json"
###

### Search by Month
#start year
year=2010
months=(01 02 03 04 05 06 07 08 09 10 11 12)
day=30

count=0

# search for year until 2022
while [ $year -lt 2022 ]; do # -lt -> '<'
	for month in ${months[*]}; do # search for each month
	  i=1
		echo $month"/"$year
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

    # commit date between 01 - 15 of the month
    # search syntax: YYYY-MM-DD..YYYY-MM-DD

    echo "rest 30 seconds here"
    sleep 30
    ii=1  # start search from page 1
    date=$year"-"$month"-01"..$year"-"$month"-15"
    while [ $count -lt 700 ]; do
      curl -u $username:$hash "https://api.github.com/search/commits?q=$terms+committer-date:$date&per_page=100&page=$ii" -o $dir"/"$year"-"$month"-"$i".json"
      count=$((count+100))
      i=$((i+1))   # result file index
      ii=$((ii+1)) # page search no.
    done
    count=0

    echo "rest 30 seconds here"
    sleep 30
    ii=1  # start search from page 1
    date=$year"-"$month"-16"..$year"-"$month"-"$day
    while [ $count -lt 700 ]; do
      curl -u $username:$hash "https://api.github.com/search/commits?q=$terms+committer-date:$date&per_page=100&page=$ii" -o $dir"/"$year"-"$month"-"$i".json"
      count=$((count+100))
      i=$((i+1))   # result file index
      ii=$((ii+1)) # page search no.
    done
    count=0
  done

  year=$((year+1))
done
###
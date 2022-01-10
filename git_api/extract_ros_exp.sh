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

date='<2022-01-01'
### Search repo
echo "rosbag_experiment repos"
curl -u $username:$hash "https://api.github.com/search/repositories?q=$terms+created:$date" -o $dir"/"repos".json"

echo "rest 10 seconds now"
sleep 10

### Search commit
echo "rosbag_experiment commits"
curl -u $username:$hash "https://api.github.com/search/commits?q=$terms+committer-date:$date&per_page=100" -o $dir"/"commits".json"

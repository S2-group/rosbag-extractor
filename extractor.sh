#!/bin/bash

# ./extractor.sh ros2 2022-01-01 2022-01-02 ./file
ros_version=$1
start_time=$2
end_time=$3
file=$4
echo ">>>> Bag File Extractor <<<<"
if [ -z "$2" ]; then
    echo "Use the following command: ./extractor.sh <ros_version> [<start_time>] [<end_time>] <bag_file>"
else
    if [ -z "$4" ]; then
        if [ -z "$3" ]; then
            file=$2
        else
            file=$3
        fi
    fi
    case $ros_version in
        ros1)
            echo "Extracting ROS 1 Bag File"
            python3 ./src/extractor/ros1/extract_graph.py $file
            ;;
        ros2)
            echo "Extracting ROS 2 Bag File"
            cd ./src/extractor/ros2
            python3 ./main.py $file "${start_time}" "${end_time}"
            cd -
            ;;
        *)
            echo "ROS version is unknown"
            ;;
    esac
fi
echo ">>>>>>>>>>>>>><<<<<<<<<<<<<<<"
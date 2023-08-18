#!/bin/bash

# ./extractor.sh ros2 2022-01-01 2022-01-02 ./file
ros_version=$1
start_time=$2
end_time=$3
file=$4
filetype=$5

echo ">>>> Bag File Extractor <<<<"
if [ -z "$2" ]; then
    echo "Use the following command: ./extractor.sh <ros_version> [<start_time>] [<end_time>] <bag_file> <file_type>"
#  python3
elif [ -z "$3" ]; then
    echo "Filetype missing"
else
    if [ -z "$5" ]; then
        if [ -z "$4" ]; then
            file=$2
            filetype=$3
            start_time="start"
            end_time="end"
        fi
    fi

    case $ros_version in
        ros1)
            echo "Extracting ROS 1 Bag File"
            python3 ./src/extractor/ros1/extract_graph.py $file
            ;;
        ros2)
            echo "Extracting ROS 2 Bag File"
            if [ "$filetype" == "mcap" ]; then
              ls ${file}/*.mcap >& /dev/null
              if [ $? -eq 0 ]; then
                python3 ./src/extractor/ros2/main.py "${start_time}" "${end_time}" $file $filetype
              else
                echo "Wrong filetype"
              fi
            elif [ "$filetype" == "db3" ]; then
              ls ${file}/metadata.yaml >& /dev/null
              if [ $? -eq 0 ]; then
                python3 ./src/extractor/ros2/main.py "${start_time}" "${end_time}" $file $filetype
              else
                echo "Wrong filetype"
              fi
            else
              echo "Input the correct filetype. Valid filetypes in ROS2 are 'db3' and 'mcap'. "
            fi
            ;;
        *)
            echo "ROS version is unknown"
            ;;
    esac
fi
echo ">>>>>>>>>>>>>><<<<<<<<<<<<<<<"
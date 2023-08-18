# Automatic Extraction of Time-windowed ROS Computation Graphs from ROS Bag Files

This repository contains the replication package and dataset of our poster presented at the  Robot Software Architecture workshop ([RSA 2023](https://roboticsa.github.io/RoboticSA2023/)) co-located with the International Conference on Robotics and Automation [ICRA 2023](https://www.icra2023.org).

A two-pager about this project is available on Arxiv [here](https://arxiv.org/abs/2305.16405).

This study has been designed, developed, and reported by the following investigators:

- [Michel Albonico](https://michelalbonico.github.io/) (Federal University of Technology, Paraná - UTFPR)
- [Berry Chen](#) (Student@Vrije Universiteit Amsterdam)
- [Ivano Malavolta](https://www.ivanomalavolta.com) (Vrije Universiteit Amsterdam)

This project is about a tool to statically extract time-windowed computation graphs from [ROS bag files](http://wiki.ros.org/rosbag). Our approach is an alternative to dynamic extractors, such as the [rqt_graph](http://wiki.ros.org/rqt_graph) tool.

## The Approach
The following figure illustrates the 3-phases approach to extract the time-windowed computation graphs from the ROS bag files: 

* ***Rosbag Extraction***: in this phase, we read the ROS bag content data and store it in a tabular format (CSV file), which is broadly used for data conversion and analysis. Both, ROS 1 and ROS 2 bag formats are supported.
* ***Time-window Slicing***: in this phase, we select only the computation graph components within a time interval (time-window passed as a parameter), which benefits from the data that is already tabulated in the CSV file from phase 1
* ***Computation Graph Building***: finally, in this phase, we generate a computation graph compatible with RQT, 
which is a standard among ROS community.

<p align="center"><img src="./rosbag_extractor-hd.png" alt="Extracted Graph: Minimal Publisher" width="350" height="350"/></center></p>

## Repository Organization

```
./bagfiles/          - Contains samples of bag files and a list of all we found on GitHub.
./src/git_api/       - Contains the code used and documentation to crawl GitHub repositories.
./src/extractor/     - Contains the source code and documentation of the architecture extractor.
```

## Installation
Note that it is not necessary for our architecture extractor, which is independent of platforms. However, it requires a few dependencies, solved by the following commands:

```
$ pip3 install -r ./requirements.txt
$ sudo apt install graphviz
```
If the requirements list is/becomes broken, do not hesitate to pull request the necessary updates.

Then, just run the extraction script on a bag file: 
```
$ ./extractor.sh <ros_version> [<start_time> <end_time>] /path/file
```

##### Example

Here, we provide and example with a very simple ROS 2 bag file:
```
$ export root_dir='your project dir'
$ ./extractor.sh ros2 "2020-02-04 07:23:55" "2020-02-04 07:23:59" $root_dir/bagfiles/ros2/talker/
```

The expected result is the following image, which will be in the rosbag file directory:

<img src="./ros2_extraction.png" alt="Extracted Graph: Minimal Publisher" width="350"/>

# Improvements

The improvements are held in the [dev](https://github.com/S2-group/icra-ws-robotics-rosbag/tree/dev) branch.

# Extraction of Time-windowed ROS Computation Graphs from ROS Bag Files
...

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

The improvements are held in the [dev](https://github.com/S2-group/rosbag-extractor/tree/dev) branch.

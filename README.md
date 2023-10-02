# RosART - A ROS Static Architecture Extraction and Visualization Tool

## The Approach
The following figure illustrates the 3-phases approach to extract computation graphs from the ROS bag files: 

* ***Rosbag Extraction***: In this phase, the time-stamped data from the bagfile is extracted, encompassing records of nodes and topics’ activities. Subsequently, this data is organized into separate CSV files for each topic, ensuring ease of access for further analysis. Supported file formats include ``bag``(ROS1), ``db3``(ROS2) and ``mcap``(ROS2).
* ***Time-window Slicing***: in this phase, we select only the computation graph components within a time interval (time-window passed as a parameter), which benefits from the data that is already tabulated in the CSV file from phase 1
* ***Computation Graph Building***: finally, in this phase, we generate a computation graph compatible with RQT, 
which is a standard among ROS community.

<p align="center"><img src="./new-wrokflow.png" alt="New workflow" width="700"/></center></p>


## Repository Organization

```
./bagfiles/          - Contains samples of bag files and a list of all we found on GitHub.
./graphs/            - Contains the extracted computation graphs.
./metrics/           - Contains the metrics of each bag file after extraction.
./node_input/        - Contains the external inputs with architectural information.
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
$ python3 extractor.py [-h] <-v ROS_VERSION> [-s START_TIME] [-e END_TIME] <-f FILE_PATH> <-ft FILE_TYPE> [-i INPUT] [-ts TIME_SPACE]
```

##### Example

Here, we provide an example with a very simple ROS 2 bag file:
```
$ python3 extractor.py -v=ros2 -s=1 -e=3 -f=./bagfiles/ros2/talker -ft=db3 -i=./node_input/minimal_publisher.csv
```
By running this command, the tool extracts from the 1st second to the 3rd second of the bagfile, with information from the external input.

The expected result is the following image, which will be in the ``graphs/ros2`` directory:

<img src="./graphs/ros2/talker/talker_0.png" alt="Extracted Graph: Minimal Publisher" width="500"/>

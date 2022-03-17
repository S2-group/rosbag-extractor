# rosbag_project

Implementation of a tool for automatically extracting the computation graph of robotics systems out of mission logs. The project is based on ROS, the standard framework for implementing robotics software today. ROS provides also a standard format for logs collected at runtime, they are called bags. In this project you will develop a tool-based approach that, given as input a ROS bag, will automatically extract its software components (in terms of blocks, connections, and topics). In this project you will work on the ros bags available in this dataset about planetary exploration:  https://starslab.ca/enav-planetary-dataset/

## Requirements
Before running the graph extraction, you must install a basic ROS1 environment. Follow [this](http://wiki.ros.org/noetic/Installation/Ubuntu) tutorial.

In Ubuntu, after setting the apt-get souce, run the following command:

```
sudo apt-get install ...
```

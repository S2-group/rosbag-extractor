# rosbag_project

<!-- The project is based on ROS, the standard framework for implementing robotics software today. A tool-based approach is developed that, given as input a ROS bag, will automatically extract its software components (in terms of blocks, connections, and topics).  -->

In this project, we aim to design an architecture extractor with the existing information acquired from rosbags, which records the topic commands sent to the robot in a previous execution. Our approach is an alternative to dynamic extractors, such as native [rqt_graph](http://wiki.ros.org/rqt_graph) tool, which are not trivial to be executed since they require a running ROS environment. Then, our approach’s output is compared to the output of a dynamic execution with rqt graph tool over 242 bag files public available in GitHub. As a result, about 202 bagfiles’ architectures can be extracted correctly, where the extractor cannot performed properly on the rest of bagfiles due to the lack of information while recording.

The project consists of 3 phases：
1. ROS in general
2. Extracting information from ROS bags
3. Validation


## ROS in general
ROS documentation: http://wiki.ros.org
ROS tutorials : http://wiki.ros.org/ROS/Tutorials

There are 2 common used instructions in this project, namely [rosbag record] (http://wiki.ros.org/rosbag/Commandline) and [rqt_graph](http://wiki.ros.org/rqt_graph)


## Extracting information from ROS bags
By using python and its package [bagpy](https://jmscslgroup.github.io/bagpy/), messages stored in the bagfiles can be read and decoded. 


## Validation


## Result
By applying our static approach to the 242 bagfiles obtained from GitHub, it is found that most bagfiles can be extracted without any problem. Also, problems occurred within 49 bags where the main node `/rosout` is not recorded in the bag.  

Extraction result: Full list can be found [here](https://drive.google.com/file/d/16UHFbm1s-yIXtfGYNJD7NTrwlfN8zlXg/view)
<img src="extraction_result.png" width="600" align="center" alt="Extraction results">


<!-- ## Requirements
Before running the graph extraction, you must install a basic ROS1 environment. Follow [this](http://wiki.ros.org/noetic/Installation/Ubuntu) tutorial.

In Ubuntu, after setting the apt-get souce, run the following command:

```
sudo apt-get install ...
```
 -->

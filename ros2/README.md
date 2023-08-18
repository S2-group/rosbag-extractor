# ros_bsc_project

Similar to the [extraction in ROS1](https://github.com/BerryC-VU/rosbag_project), this project aims to design and develop a tool for the static extraction of the computation graph of ROS2 robotic systems. 

[This](https://github.com/BerryC-VU/ros_bsc_project/blob/master/ros2_bagfiles.xlsx) spreedsheet contains a list of bagfile used in this project.

### Run script

Three parameters are needed to run the extraction script for the bagfile: 
- path to file
- user-defined start time
- user-defined end time

```
python3 path_to_file start-time end-time
```

An example of running the extraction on [bagfile](https://github.com/BerryC-VU/ros_bsc_project/tree/master/rosbag2_2022_06_02-08_49_23):
```
python3 src/main.py rosbag2_2022_06_02-08_49_23 '2022-06-02 08:50:06' '2022-06-02 09:01:20'
```
The expected result as follow:
<img src="extracted_graph.png" width="500" align="center" alt="Extraction results">

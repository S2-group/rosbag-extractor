# Extracting ROS Communication Architecture Reconfiguration From ROS Bag Files

This repository contains the replication package and dataset of the paper submitted to RobotSoftwareArchitecture@ICRA 2023.

This study has been designed, developed, and reported by the following investigators:

- [Michel Albonico](https://michelalbonico.github.io/) (Federal University of Technology, Paraná - UTFPR)
- [Berry Chen](#) (Student@Vrije Universiteit Amsterdam)
- [Ivano Malavolta](https://www.ivanomalavolta.com) (Vrije Universiteit Amsterdam)

In this project, we aim to statically extract time-windowed architectural information from [ROS bag files](http://wiki.ros.org/rosbag). Our approach is an alternative to dynamic extractors, such as native [rqt_graph](http://wiki.ros.org/rqt_graph) tool.

## Repository Organization

```
src/git_api/       - Contains the code used and documentation to crawl GitHub repositories.
src/extractor/     - Contains the source code and documentation of the architecture extractor.
```

## Instalation
Note that it is not necessary for our architecture extractor, which is independent of platforms. However, it requires a few dependencies, solved by the following commands:

```
$ pip install -r ./requirements.txt
$ sudo apt install graphviz
```

Then, just run the extraction script on a bagfile: 
```
python3 extract_graph.py /path/file
```

Here, we provide and example with a very simple file **[argument time/misses bag]**:
```
python3 src/extract_graph.py ./turtlesim.bag
```

The expected result is the following image:

<img src="./screenshot.png" alt="Extracted Graph: Turtlesim" style="height: 350px; width:350px;"/>

## Public Bagfiles

- In [this](https://drive.google.com/drive/folders/1HwNHiVZJhChzVv4ZwMy9yN5gWYnwAsSi?usp=sharing) shared folder, you will find some bagfiles from our team experiments with ROS+SLAM.
- We have also used the [MET dataset](https://starslab.ca/enav-planetary-dataset/) for our tool validation. It contains huge bagfiles from a rover robot navigation.
- [This](#) spreadsheet contains all the public bagfiles we found on GitHub. 

## Extracting information from ROS bags
By using python and its package [bagpy](https://jmscslgroup.github.io/bagpy/), messages stored in the bagfiles can be read and decoded. Topics presented in the bagfile can be extracted by using `b.topic_table,` where `b` is a bagreader object. Then, we need first to check whether `rosout` is in the topic table or not. If not, the architecture information cannot be extracted with our approach. Otherwise, the information needed to generate a computational graph can be extracted, and [Graphviz](https://graphviz.org) is used to connect and visualize the graph.

## Validation
Comparing to the dynamic approach(rqt_graph), our static approach workds totally independent on ROS environment. Validation process are done by manually checking the graphs of each bagfiles in the validation set and compare the differences between two approaches' graphs.



<!--## Result
By applying our static approach to the 242 bagfiles obtained from GitHub, it is found that most bagfiles can be extracted without any problem. Also, problems occurred within 49 bags where the main node `/rosout` is not recorded in the bag.  

Extraction result: Full list can be found [here](https://drive.google.com/file/d/16UHFbm1s-yIXtfGYNJD7NTrwlfN8zlXg/view)
<img src="extraction_result.png" width="700" align="center" alt="Extraction results">

-->


<!-- ## Requirements
Before running the graph extraction, you must install a basic ROS1 environment. Follow [this](http://wiki.ros.org/noetic/Installation/Ubuntu) tutorial.

In Ubuntu, after setting the apt-get souce, run the following command:

```
sudo apt-get install ...
```
 -->

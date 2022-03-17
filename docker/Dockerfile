FROM ubuntu:18.04

# Install necessary prerequisites
RUN apt-get update
RUN apt-get install -y lsb-release gnupg python3-pip

# Workaround interactive tzdata update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install --yes tzdata
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

ENV HOME=/root
WORKDIR $HOME

# Adding ROS repos
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# Update APT package cache
RUN apt-get update
RUN apt-get install -y libgtest-dev

# Install necessary tools
RUN pip3 install -U rosdep rosinstall_generator vcstool
RUN pip3 install --upgrade setuptools

# Initialize rosdep
RUN rosdep init
RUN rosdep update

# Make workspace
RUN mkdir ros_catkin_ws
RUN cd ros_catkin_ws/

# Get sources for rospy noetic
RUN rosinstall_generator rospy --rosdistro noetic --deps --tar --repos python_qt_binding qt_gui_core rqt rqt_graph > noetic-desktop.rosinstall
RUN mkdir ./src
RUN vcs import --input noetic-desktop.rosinstall ./src

# Get sources for noetic
#RUN rosinstall_generator --rosdistro noetic --upstream-development --repos python_qt_binding qt_gui_core rqt > rqt.rosinstall
#RUN vcs import --input rqt.rosinstall ./src

# Install dependencies
RUN rosdep install --from-paths ./src --ignore-packages-from-source --rosdistro noetic -y

# Build all
RUN ./src/catkin/bin/catkin_make_isolated --install -DPYTHON_EXECUTABLE=/usr/bin/python3 -DCMAKE_BUILD_TYPE=Release

# Source necessary environment
RUN echo "source $HOME/install_isolated/setup.bash" >> $HOME/.bashrc

# Cleanup
RUN rm -rf build_isolated devel_isolated noetic-desktop.rosinstall ros_catkin_ws src

ENTRYPOINT bash

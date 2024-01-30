FROM osrf/ros:humble-desktop


# install ros package
RUN apt-get update && apt-get install -y \
      ros-${ROS_DISTRO}-demo-nodes-cpp \
      ros-${ROS_DISTRO}-demo-nodes-py && \
    rm -rf /var/lib/apt/lists/*





# RUN git clone https://github.com/icos-pit/agrorob_server 
COPY . .

RUN . /opt/ros/$ROS_DISTRO/setup.sh
# # # play ros bag
# CMD ["ros2", "bag", "play", "agrorob_server/bags/rosbag2_2023_11_30-09_27_02/rosbag2_2023_11_30-09_27_02_0.db3","--loop"]
CMD ["ros2", "bag", "play", "rosbag2_2023_11_30-09_27_02_0.db3","--loop"]



# ##
# ## Build part
# ##
# FROM rust:slim-buster as builder


# RUN echo "deb [trusted=yes] https://download.eclipse.org/zenoh/debian-repo/ /" | tee -a /etc/apt/sources.list > /dev/null \
#     apt update \
#     apt install zenoh-bridge-dds

# CMD [ "zenoh-bridge-dds" , "-m", "peer"]

 
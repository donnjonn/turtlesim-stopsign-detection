echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
source ../../../devel/setup.bash
gnome-terminal -x roscore
gnome-terminal -x rosrun turtlesim turtlesim_node
gnome-terminal -e "bash -c 'source ../../../devel/setup.bash;rosrun stop_sign_detection image_publisher.py; $SHELL'"
rosrun stop_sign_detection detection.py -c $1



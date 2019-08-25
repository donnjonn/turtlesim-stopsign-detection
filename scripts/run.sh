#!/bin/bash
c_hasc=0
classifier=""
while getopts 'mc:' OPTION; do
	case "$OPTION" in
		m)
			cd ../../..
			catkin_make
			cd src/turtlesim-stopsign-detection/scripts
			;;
		c)
			c_hasc=1
			classifier="$OPTARG"
			;;
		?)
			echo "script usage:"
	esac
done
if [ $c_hasc -ne 1 ]; then
	echo "Error: specify classifier"
	exit 1
fi
if [ "$classifier" !=  "haar" ] && [ "$classifier" != "lbp" ]; then
	echo "Error: only haar or lbp classifier supported"
	exit 1	
fi
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
source ../../../devel/setup.bash
gnome-terminal -x roscore
gnome-terminal -x rosrun turtlesim turtlesim_node
gnome-terminal -e "bash -c 'source ../../../devel/setup.bash;rosrun stop_sign_detection image_publisher.py; $SHELL'"
rosrun stop_sign_detection detection.py -c $classifier



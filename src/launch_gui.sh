#!/bin/bash -e

# Copyright 2021 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

# Simple workaround to get ROS Melodic to use python3 when launching the program using rosrun.

PACKAGE_PATH=$(rospack find gazebo_terrain)
cd $PACKAGE_PATH/scripts/
echo "Launching GUI"
python3 main.py
echo "Exiting GUI"

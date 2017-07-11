#!/bin/bash -e
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/inmoov-ros
# Additional copyright may be held by others, as reflected in the commit history.


# Script Preliminary Info
echo " "
echo "GAZEBO TERRAIN GENERATOR"
echo " "
echo "Note: This program assumes that you have already saved a square greyscale"
echo "      .png file in your Home/Pictures/ directory to use as your heightmap."
echo "      If you do not have your image located there, you need to move it   "
echo "      there before continuing."
echo " "

# Expected Location of Catkin Workspace Files (source directory, generally)
CATKIN_WS_SRC="/home/$USER/catkin_ws/src"

# Cleanup 'Temp' Directory
rm /$CATKIN_WS_SRC/gazebo_terrain/temp/*
touch placehold

# Get Image Name
echo "What is the name of your heightmap image? (the image name without .png):"
read YOURIMAGENAME
	
# Copy Image
cp ~/Pictures/$YOURIMAGENAME.png $CATKIN_WS_SRC/gazebo_terrain/temp

# Create Model Files
cd $CATKIN_WS_SRC/gazebo_terrain/temp
touch model.config model.sdf

# Resize Image
cd $CATKIN_WS_SRC/gazebo_terrain/
python image_resize.py "$YOURIMAGENAME"
echo " "
echo "Grayscale heightmap created"
echo " "

#  Write Data to Model Files
python model_config_gen.py
python model_sdf_gen.py "$YOURIMAGENAME"
echo "model.config and model.sdf created and written-out"
echo " "

# Create Model Directory
cd ~/.gazebo/models
mkdir $YOURIMAGENAME
cd $YOURIMAGENAME/
mkdir -p materials/textures/
echo "Model directory created"
echo " "

# Move these Files to the Correct Directory
mv $CATKIN_WS_SRC/gazebo_terrain/temp/model.config ~/.gazebo/models/$YOURIMAGENAME
mv $CATKIN_WS_SRC/gazebo_terrain/temp/model.sdf ~/.gazebo/models/$YOURIMAGENAME
mv $CATKIN_WS_SRC/gazebo_terrain/temp/$YOURIMAGENAME.png ~/.gazebo/models/$YOURIMAGENAME/materials/textures

echo "Program is finished; You should now be ready to test your heightmap in Gazebo."
echo " "

#EOF

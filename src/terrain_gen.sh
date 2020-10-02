#!/bin/bash -e
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.


# Load package directory:

PACKAGE_PATH=$(rospack find gazebo_terrain)


# Script Preliminary Info
echo " "
echo "GAZEBO TERRAIN GENERATOR"
echo " "
echo "Note: This program assumes that you have already saved a square greyscale"
echo "      .png file in your gazebo_terrain/pictures/ directory to use as your heightmap."
echo "      If you do not have your image located there, you need to move it   "
echo "      there before continuing."
echo " "


# Get Image Name
echo "What is the name of your heightmap image? (the image name without .png):"
read YOURIMAGENAME

# Create Model Directory
cd $PACKAGE_PATH/models/
mkdir $YOURIMAGENAME
cd $YOURIMAGENAME/
mkdir -p materials/textures/
mkdir $PACKAGE_PATH/launch/$YOURIMAGENAME/
echo " "
echo "Model directory created"
echo " "



# Model path
MODEL_PATH="${PACKAGE_PATH}/models/$YOURIMAGENAME"

# Create 'model.config' and 'model.sdf'
cd $MODEL_PATH
touch model.config model.sdf

# Copy image into model directory
cp $PACKAGE_PATH/pictures/$YOURIMAGENAME.png $MODEL_PATH/materials/textures

# Resize Image
cd $PACKAGE_PATH/scripts
python3 image_resize.py "$YOURIMAGENAME" "$MODEL_PATH/materials/textures"
echo "Heightmap copied and resized to Gazebo's requirements"
echo " "

#  Write Data to Model Files
#python3 model_config_gen.py "$MODEL_PATH"
#python3 model_sdf_gen.py "$MODEL_PATH" "$YOURIMAGENAME"
python3 model.py "$MODEL_PATH" "$YOURIMAGENAME"
echo "The model, world and launch are created and written. The program is finished; You should now be ready to test your heightmap in Gazebo."
echo " "
echo "To test your terrain in the gazebo world, run the following command:"
echo " "
echo "             roslaunch gazebo_terrain $YOURIMAGENAME""_world.launch          "
#EOF

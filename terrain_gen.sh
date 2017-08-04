#!/bin/bash -e
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
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

# Get static paths
RELATIVE_PATH="`dirname \"$0\"`"
ABSOLUTE_PATH="`( cd \"$RELATIVE_PATH\" && pwd )`"

# Get Image Name
echo "What is the name of your heightmap image? (the image name without .png):"
read YOURIMAGENAME

# Create Model Directory
cd /home/$USER/.gazebo/models
mkdir $YOURIMAGENAME
cd $YOURIMAGENAME/
mkdir -p materials/textures/
echo " "
echo "Model directory created"
echo " "

# Model path
MODEL_PATH="/home/$USER/.gazebo/models/$YOURIMAGENAME"

# Copy image into model directory# Create Model Files
cd $MODEL_PATH

# Create 'model.config' and 'model.sdf'
touch model.config model.sdf
cp /home/$USER/Pictures/$YOURIMAGENAME.png $MODEL_PATH/materials/textures

# Resize Image
cd $ABSOLUTE_PATH/gazeboterrain/
python image_resize.py "$YOURIMAGENAME" "$MODEL_PATH/materials/textures"
echo "Heightmap copied and resized to Gazebo's requirements"
echo " "

#  Write Data to Model Files
python model_config_gen.py "$MODEL_PATH"
python model_sdf_gen.py "$MODEL_PATH" "$YOURIMAGENAME"
echo "'model.config' and 'model.sdf' created and written. The program is finished; You should now be ready to test your heightmap in Gazebo."

#EOF

#!/bin/bash
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

#Get the Name of the Model Directory
echo "What is the name of the model directory you want to delete?:"
read MODELNAME

# Warning
echo " "
echo "Things to delete:"
echo " "
echo "  DIRECTORIES"
echo "    /home/$USER/.gazebo/models/$MODELNAME/materials/textures/"
echo "    /home/$USER/.gazebo/models/$MODELNAME/materials/"
echo "    /home/$USER/.gazebo/models/$MODELNAME/"
echo " "
echo "  FILES"
echo "    model.config"
echo "    model.sdf"
echo "    $MODELNAME.png"
echo " "

#Safety Feature
echo "Are you absolutely sure you want to delete this model? Once deleted, you will"
echo "NOT be able to recover it! (Y or n)"
read ANSWER

if [ $ANSWER = Y ]; then
    echo " "
else 
    exit
fi

# Interactively delete all files and directories
if [ -d /home/$USER/.gazebo/models/$MODELNAME ]; then
    rm -ri /home/$USER/.gazebo/models/$MODELNAME
fi

echo " "
echo "Program finished. Check to make sure the directory is gone."

#EOF

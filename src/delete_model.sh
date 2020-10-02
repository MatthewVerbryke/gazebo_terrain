#!/bin/bash
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

#Get the Name of the Model Directory
echo "What is the name of the model directory you want to delete?:"
read MODELNAME


PACKAGE_PATH=$(rospack find gazebo_terrain)


# Warning
echo " "
echo "Things to delete:"
echo " "
echo "  DIRECTORIES AND FILES"
echo "    $PACKAGE_PATH/models/$MODELNAME/"
echo "    $PACKAGE_PATH/worlds/$MODELNAME.world"
echo "    $PACKAGE_PATH/launch/$MODELNAME/"
echo " "

#Safety Feature
echo "Are you absolutely sure you want to delete this model? Once deleted, you will"
echo "NOT be able to recover it! (Y or n)"
read ANSWER

if [ $ANSWER = Y ] || [ $ANSWER = y ]; then
    echo " "
else 
    echo "Skipped"
    exit
fi

# Interactively delete all files and directories
if [ -d $PACKAGE_PATH/models/$MODELNAME ]; then
    rm -r $PACKAGE_PATH/models/$MODELNAME $PACKAGE_PATH/worlds/$MODELNAME.world $PACKAGE_PATH/launch/$MODELNAME/

else
	echo "Model not found"
	exit
fi

echo " "
echo "Program finished. Check to make sure the directory is gone."

#EOF

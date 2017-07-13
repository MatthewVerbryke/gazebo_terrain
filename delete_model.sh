#!/bin/bash
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

#Get the Name of the Model Directory
echo "What is the name of the model directory you want to delete?:"
read MODELNAME

#Safety Feature #2
echo "Are you absolutely sure you want to delete this model? Once deleted, you will"
echo "NOT be able to recover it! (Y or n)"
read ANSWER

if [ $ANSWER = Y ]; then
    echo " "
else 
    exit
fi

#Delete Files
cd ~/.gazebo/models/$MODELNAME

rm model.config
echo "..."

rm model.sdf
echo "..."

cd ~/.gazebo/models/$MODELNAME/materials/textures
rm $MODELNAME.png
echo "..."

echo "All files deleted; deleting directories"

cd ~/.gazebo/models/$MODELNAME/materials
rmdir textures
echo "..."

cd ~/.gazebo/models/$MODELNAME
rmdir materials
echo "..."

cd ~/.gazebo/models/
rmdir $MODELNAME
echo "..."

#EOF

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

if [ -d ~/.gazebo/models/$MODELNAME ] then;
    #Delete Files
    #rm -rf /home/$USER/.gazebo/models/$MODELNAME # forcibly delete with no prompts
    rm -ri /home/$USER/.gazebo/models/$MODELNAME # forcibly prompts user, requires interaction from user to delete each file and directory
    
    # what it should be getting rid of...
    #rm model.config
    #rm model.sdf
    #cd ~/.gazebo/models/$MODELNAME/materials/textures
    #rm $MODELNAME.png
    #echo "All files deleted; deleting directories"
    #cd ~/.gazebo/models/$MODELNAME/materials
    #rmdir textures
    #cd ~/.gazebo/models/$MODELNAME
    #rmdir materials
    #cd ~/.gazebo/models/
    #rmdir $MODELNAME
fi

echo "All done! :)"
#EOF

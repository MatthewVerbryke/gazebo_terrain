#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

import os
import sys
import string

# Get cwd
setdir = os.getcwd()

# Command line input
file_path = sys.argv[1]
img_name = sys.argv[2]

# Ask for desired dimensions and heights of the Gazebo model
size_x = raw_input('What would you like the dimensions of the square terrain area be (in meters)?:\n')
print (' ')
size_y = size_x
size_z = raw_input('What would you like to be the highest elevation of the terrain be (in meters)?:\n')
print(' ')

# Change to templates directory
os.chdir('templates')

# Read template file
template = open('sdf_temp.txt', 'r')
tempholdtext = template.read()
template.close()
sdftemplate = str(tempholdtext)

# Filling in content
sdfdata = str(sdftemplate)
sdfdata = sdfdata.replace( "$FILENAME$", img_name )
sdfdata = sdfdata.replace( "$SIZEX$", size_x )
sdfdata = sdfdata.replace( "$SIZEY$", size_y )
sdfdata = sdfdata.replace( "$SIZEZ$", size_z )
sdfcontent = str(sdfdata)

# Go to model directory
os.chdir(file_path)

# Open file
target = open('model.sdf', 'w')

# Write to model.sdf
target.write(sdfcontent)

# Close file
target.close()

# Change back directory
os.chdir(setdir)

#EOF

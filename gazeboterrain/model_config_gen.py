#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

import os
import sys
import string
from sys import argv

# Get cwd
setdir = os.getcwd()

# Command line input
file_path = sys.argv[1]

# Ask for configuration data
model_name = raw_input("Input the name of the model (displayed on the Gazebo insert menu):\n")
print (" ")
creator_name = raw_input("Input your name:\n")
print (" ")
email = raw_input("Input your email address:\n")
print (" ")
description = raw_input("Add a short description of the model:\n")
print (" ")

# Change to templates directory
os.chdir('templates')

# Read template file
template = open('config_temp.txt', 'r')
tempholdtext = template.read()
template.close()
configtemplate = str(tempholdtext)

# Fill in content
configdata = str(configtemplate)
configdata = configdata.replace( "$MODELNAME$", model_name )
configdata = configdata.replace( "$AUTHORNAME$", creator_name )
configdata = configdata.replace( "$EMAILADDRESS$", email )
configdata = configdata.replace( "$DESCRIPTION$", description )
configcontent = str(configdata)

# Go to model directory
os.chdir(file_path)

# Open file
target = open('model.config', 'w')

# Write to model.config
target.write(configcontent)

# Close file
target.close()

# Change back directory
os.chdir(setdir)

#EOF

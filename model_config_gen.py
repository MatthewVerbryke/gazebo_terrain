#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/inmoov-ros
# Additional copyright may be held by others, as reflected in the commit history.

import os
import sys
import string
from sys import argv

# Ask for Configuration Data
model_name = raw_input('Input the name of the model (displayed on the Gazebo insert menu):\n')
print (' ')
creator_name = raw_input('Input your name:\n')
print (' ')
email = raw_input('Input your email address:\n')
print (' ')
description = raw_input('Add a short description of the model:\n')
print (' ')

# Read Template File
template = open('config_temp.txt', 'r')
tempholdtext = template.read()
template.close()
configtemplate = str(tempholdtext)

# Fill in Content
configdata = str(configtemplate)
configdata = configdata.replace( "$MODELNAME$", model_name )
configdata = configdata.replace( "$AUTHORNAME$", creator_name )
configdata = configdata.replace( "$EMAILADDRESS$", email )
configdata = configdata.replace( "$DESCRIPTION$", description )
configcontent = str(configdata)

# Find and write to model.config
os.chdir("temp")
target = open('model.config', 'w')
target.write(configcontent)
target.close()

# Change Back Directory
os.chdir("/..")

#EOF

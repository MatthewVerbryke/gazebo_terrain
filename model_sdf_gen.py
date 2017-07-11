#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/inmoov-ros
# Additional copyright may be held by others, as reflected in the commit history.

import os
import sys
import string

#Asking for Model Information
img_name = sys.argv[1]
size_x = raw_input('What would you like the dimensions of the square terrain area be (in meters)?:\n')
print (' ')
size_y = size_x
size_z = raw_input('What would you like to be the highest elevation of the terrain be (in meters)?:\n')
print(' ')

#Read Template File
template = open('sdf_temp.txt', 'r')
tempholdtext = template.read()
template.close()
sdftemplate = str(tempholdtext)

#Filling in Content
sdfdata = str(sdftemplate)
sdfdata = sdfdata.replace( "$FILENAME$", img_name )
sdfdata = sdfdata.replace( "$SIZEX$", size_x )
sdfdata = sdfdata.replace( "$SIZEY$", size_y )
sdfdata = sdfdata.replace( "$SIZEZ$", size_z )
sdfcontent = str(sdfdata)

#Write to model.sdf
os.chdir("temp")
target = open('model.sdf', 'w')
target.write(sdfcontent)
target.close()

# Change Back Directory
os.chdir("/..")

#EOF

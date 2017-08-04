#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

import os
import string
import sys

class GenerateModelSDF():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()

        # Command line input
        self.file_path = sys.argv[1]
        self.img_name = sys.argv[2]

        # Ask for desired dimensions and heights of the Gazebo model
        self.size_x = raw_input('What would you like the dimensions of the square terrain area be (in meters)?:\n')
        print (' ')
        self.size_y = self.size_x
        self.size_z = raw_input('What would you like the highest elevation of the terrain be (in meters)?:\n')
        print(' ')
        
        # Run main program
        self.main()

    def read_sdf_template(self):
        try:
            
            # Open template
            template = open('sdf_temp.txt', 'r')
            
            # Read template
            temp_hold_text = template.read()
            sdf_template = str(temp_hold_text)
            
            return sdf_template
            
        finally:
            
            # Close template
            template.close()

    def write_sdf_file(self, sdf_template):
        try:

            # Filling in content
            sdf_template = sdf_template.replace( "$FILENAME$", self.img_name )
            sdf_template = sdf_template.replace( "$SIZEX$", self.size_x )
            sdf_template = sdf_template.replace( "$SIZEY$", self.size_y )
            sdf_template = sdf_template.replace( "$SIZEZ$", self.size_z )
            
            # Ensure results are a string
            sdf_content = str(sdf_template)

            # Open file
            target = open('model.sdf', 'w')

            # Write to model.sdf
            target.write(sdf_content)
            
        finally:

            # Close file
            target.close()
            
    def main(self):
        try:
            
            # Change to templates directory
            os.chdir('templates')
            
            # Read template file
            sdf_template = self.read_sdf_template()

            # Change to model directory
            os.chdir(self.file_path)
            
            # Write to model.sdf
            self.write_sdf_file(sdf_template)
            
        finally:

            # Change back directory
            os.chdir(self.setdir)


if __name__ == "__main__":
    GenerateModelSDF()
#EOF

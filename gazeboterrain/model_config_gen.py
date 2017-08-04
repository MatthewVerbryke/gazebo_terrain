#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

import os
import string
import sys
from sys import argv


class GenerateModelConfig():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()

        # Command line arguments
        self.file_path = sys.argv[1]

        # Ask for configuration data
        self.model_name = raw_input("Input the name of the model (displayed on the Gazebo insert menu):\n")
        print (" ")
        self.creator_name = raw_input("Input your name:\n")
        print (" ")
        self.email = raw_input("Input your email address:\n")
        print (" ")
        self.description = raw_input("Add a short description of the model:\n")
        print (" ")
        
        # Run main program
        self.main()
        
    def read_config_template(self):
        try:
            
            # Open template
            template = open('config_temp.txt', 'r')
            
            # Read template
            temp_hold_text = template.read()
            config_template = str(temp_hold_text)
            
            return config_template
            
        finally:
            
            # Close template
            template.close()
            
    def write_config_file(self, config_template):
        try:
            
            # Replace indicated values
            config_template = config_template.replace( "$MODELNAME$", self.model_name )
            config_template = config_template.replace( "$AUTHORNAME$", self.creator_name )
            config_template = config_template.replace( "$EMAILADDRESS$", self.email )
            config_template = config_template.replace( "$DESCRIPTION$", self.description )
            
            # Ensure results are a string
            config_content = str(config_template)
                    
            # Open config file
            target = open('model.config', 'w')

            # Write to config file
            target.write(config_content)

        finally:

            # Close file
            target.close()
            
    def main(self):
        try:
            
            # Change to templates directory
            os.chdir('templates')
            
            # Read template file
            config_template = self.read_config_template()

            # Change to model directory
            os.chdir(self.file_path)
            
            # Write to model.config
            self.write_config_file(config_template)

        finally:
            
            # Change back to cwd
            os.chdir(self.setdir)


if __name__ == "__main__":
    GenerateModelConfig()

#EOF

#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.


import os
import string
import sys


def read_template(temp_file_name):
    
    try:
        
        # Open template
        temp_file = open(temp_file_name, "r")
        
        # Read template
        temp_hold_text = temp_file.read()
        template = str(temp_hold_text)
        
        return template
            
    finally:
        
        # Close template
        temp_file.close()
        
def write_config_file(config_template):
    
    try:
        
        # Ask for configuration data
        model_name = raw_input("Input the name of the model (displayed on the Gazebo insert menu):\n")
        print (" ")
        creator_name = raw_input("Input your name:\n")
        print (" ")
        email = raw_input("Input your email address:\n")
        print (" ")
        description = raw_input("Add a short description of the model:\n")
        print (" ")
        
        # Replace indicated values
        config_template = config_template.replace( "$MODELNAME$", model_name )
        config_template = config_template.replace( "$AUTHORNAME$", creator_name )
        config_template = config_template.replace( "$EMAILADDRESS$", email )
        config_template = config_template.replace( "$DESCRIPTION$", description )
        
        # Ensure results are a string
        config_content = str(config_template)
        
        # Open config file
        target = open("model.config", "w")
        
        # Write to config file
        target.write(config_content)

    finally:
        
        # Close file
        target.close()
        
def write_sdf_file(img_name, sdf_template):
    
    try:
        
        # Ask for desired dimensions and heights of the Gazebo model
        size_x = raw_input("What would you like the dimensions of the square terrain area be (in meters)?:\n")
        print (" ")
        size_y = size_x
        size_z = raw_input("What would you like the highest elevation of the terrain be (in meters)?:\n")
        print(" ")
        
        # Filling in content
        sdf_template = sdf_template.replace( "$FILENAME$", img_name )
        sdf_template = sdf_template.replace( "$SIZEX$", size_x )
        sdf_template = sdf_template.replace( "$SIZEY$", size_y )
        sdf_template = sdf_template.replace( "$SIZEZ$", size_z )
            
        # Ensure results are a string
        sdf_content = str(sdf_template)

        # Open file
        target = open("model.sdf", "w")

        # Write to model.sdf
        target.write(sdf_content)
            
    finally:

        # Close file
        target.close()        
        
def main():
    
    try:
        
        # Get cwd
        setdir = os.getcwd()
        
        # Command line input
        file_path = sys.argv[1]
        img_name = sys.argv[2]
        
        # Change to templates directory
        os.chdir("templates")
        
        # Read template files
        config_template = read_template("config_temp.txt")
        sdf_template = read_template("sdf_temp.txt")
        
        # Change to model directory
        os.chdir(file_path)
        
        # Write to model.config
        write_config_file(config_template)        
        
        # Write to model.sdf
        write_sdf_file(img_name, sdf_template)
        
    finally:
        
        # Change back to cwd
        os.chdir(setdir)

        
main()        
        
        
        

#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.


import os
import string
import sys
import rospkg

rospack = rospkg.RosPack()
package_path = rospack.get_path('gazebo_terrain')

img_name = ""


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
    global img_name
    try:

        # Ask for configuration data
        model_name = img_name
        creator_name = input("Input your name:\n")
        print(" ")
        email = input("Input your email address:\n")
        print(" ")
        description = input("Add a short description of the model:\n")
        print(" ")

        # Replace indicated values
        config_template = config_template.replace("$MODELNAME$", model_name)
        config_template = config_template.replace("$AUTHORNAME$", creator_name)
        config_template = config_template.replace("$EMAILADDRESS$", email)
        config_template = config_template.replace("$DESCRIPTION$", description)

        # Ensure results are a string
        config_content = str(config_template)

        # Open config file
        target = open("model.config", "w")

        # Write to config file
        target.write(config_content)

    finally:

        # Close file
        target.close()


def write_sdf_file(img_name, sdf_template, world_template, name_world_launch_template, world_launch_template):
    try:

        # Ask for desired dimensions and heights of the Gazebo model
        size_x = input("What would you like the dimensions of the square terrain area be (in meters)?:\n")
        print(" ")
        size_y = size_x
        size_z = input("What would you like the highest elevation of the terrain be (in meters)?:\n")
        print(" ")

        # Filling in content
        sdf_template = sdf_template.replace("$FILENAME$", img_name)
        sdf_template = sdf_template.replace("$SIZEX$", size_x)
        sdf_template = sdf_template.replace("$SIZEY$", size_y)
        sdf_template = sdf_template.replace("$SIZEZ$", size_z)
        world_template = world_template.replace("$FILENAME$", img_name)
        name_world_launch_template = name_world_launch_template.replace("$FILENAME$", img_name)
        world_launch_template = world_launch_template.replace("$FILENAME$", img_name)

        # Ensure results are a string
        sdf_content = str(sdf_template)
        world_content = str(world_template)
        name_world_launch_content = str(name_world_launch_template)
        world_launch_content = str(world_launch_template)



        # Open file
        target = open("model.sdf", "w")
        target_world = open(r"%s" % (package_path + "/worlds/" + img_name + ".world"), "w")
        target_name_launch = open(r"%s" % (package_path + "/launch/" + img_name + "/" + img_name + "_world.launch"), "w")
        target_launch = open(r"%s" % (package_path + "/launch/" + img_name + "/" + img_name + ".launch"), "w")



        # Write to model.sdf
        target.write(sdf_content)
        target_world.write(world_content)
        target_name_launch.write(name_world_launch_content)
        target_launch.write(world_launch_content)

    finally:

        # Close file
        target.close()
        target_world.close()
        target_name_launch.close()
        target_launch.close()


def main():
    global img_name
    
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
        world_template = read_template("name_world_temp.txt")
        name_world_launch_template = read_template("name_world_launch_temp.txt")
        world_launch_template = read_template("world_launch_temp.txt")

        # Change to model directory
        os.chdir(file_path)

        # Write to model.config
        write_config_file(config_template)

        # Write to model.sdf
        write_sdf_file(img_name, sdf_template, world_template, name_world_launch_template, world_launch_template)

    finally:

        # Change back to cwd
        os.chdir(setdir)


main()        




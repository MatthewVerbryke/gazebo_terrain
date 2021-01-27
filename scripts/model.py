#!/usr/bin/env python

"""
  Functions and Class objects for generating terrain models in Gazebo.
  
  TODO: Move Gazebo world/launch file generation into its own module.

  Copyright 2017-2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""


import os
from shutil import copyfile
import string
import sys
import rospkg

from image_resize import rescale_and_resize_image


# Get gazebo model directory path
HOME_PATH = os.path.expanduser("~")
MODEL_PATH = HOME_PATH + "/.gazebo/models/"


class ModelInfo(object):
    """
    A class variable for storing gazebo terrain model information
    """
    
    def __init__(self):
        
        self.name = ""
        self.author = ""
        self.email = ""
        self.description = ""
        self.heightmap = ""
        self.resolution = 0
        self.side = 0.0
        self.range = 0.0
        
    def check_entries(self):
        """
        TODO
        """
        return True

def read_template(temp_file_name):
    """
    Read in and return a template file.
    """
    
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

def write_config_file(config_template, model_info):
    """
    Write the model infomation to the model config file.
    """
    
    try:
        
        # Replace indicated values
        config_template = config_template.replace("$MODELNAME$",
                                                  model_info.name)
        config_template = config_template.replace("$AUTHORNAME$",
                                                  model_info.author)
        config_template = config_template.replace("$EMAILADDRESS$",
                                                  model_info.email)
        config_template = config_template.replace("$DESCRIPTION$",
                                                  model_info.description)

        # Ensure results are a string
        config_content = str(config_template)

        # Open config file
        target = open("model.config", "w")

        # Write to config file
        target.write(config_content)

    finally:
        
        # Close file
        target.close()


def write_sdf_file(sdf_template, model_info):
    """
    Write the model infomation to the model SDF file.
    """
    
    try:
        
        # Filling in content
        heightmap_no_ext = os.path.splitext(model_info.heightmap)[0]
        sdf_template = sdf_template.replace("$MODELNAME$",
                                             model_info.name)
        sdf_template = sdf_template.replace("$FILENAME$", 
                                            heightmap_no_ext)
        sdf_template = sdf_template.replace("$SIZEX$",
                                            model_info.side)
        sdf_template = sdf_template.replace("$SIZEY$",
                                            model_info.side)
        sdf_template = sdf_template.replace("$SIZEZ$",
                                            model_info.range)
        # world_template = world_template.replace("$FILENAME$", img_name)
        # name_world_launch_template = name_world_launch_template.replace("$FILENAME$", img_name)
        # world_launch_template = world_launch_template.replace("$FILENAME$", img_name)

        # Ensure results are a string
        sdf_content = str(sdf_template)
        # world_content = str(world_template)
        # name_world_launch_content = str(name_world_launch_template)
        # world_launch_content = str(world_launch_template)

        # Open file
        target = open("model.sdf", "w")
        # target_world = open(r"%s" % (package_path + "/worlds/" + img_name + ".world"), "w")
        # target_name_launch = open(r"%s" % (package_path + "/launch/" + img_name + "/" + img_name + "_world.launch"), "w")
        # target_launch = open(r"%s" % (package_path + "/launch/" + img_name + "/" + img_name + ".launch"), "w")

        # Write to model.sdf
        target.write(sdf_content)
        # target_world.write(world_content)
        # target_name_launch.write(name_world_launch_content)
        # target_launch.write(world_launch_content)

    finally:
        
        # Close file
        target.close()
        # target_world.close()
        # target_name_launch.close()
        # target_launch.close()

def create_model(img_path, img_name, model_info):
    """
    Generate a gazebo terrain model using the given model information,
    heightmap, and template files.
    """
    
    # Get path to heightmap destination
    dest_path = MODEL_PATH + model_info.name + "/materials/textures/"

    # Get cwd
    setdir = os.getcwd()
    
    # Retrieve templates
    os.chdir("templates")
    config_template = read_template("config_temp.txt")
    sdf_template = read_template("sdf_temp.txt")
    #world_template = read_template("name_world_temp.txt")
    #name_world_launch_template = read_template("name_world_launch_temp.txt")
    #world_launch_template = read_template("world_launch_temp.txt")
    
    try:
        
        # Create directory structure
        model_dir = MODEL_PATH + model_info.name
        os.mkdir(model_dir)
        os.mkdir(model_dir + "/materials")
        os.mkdir(model_dir + "/materials/textures/")
        
        # Copy heightmap image to proper location
        os.chdir(img_path)
        copyfile(img_name, os.path.join(dest_path, img_name))

        # Write model files
        os.chdir(model_dir)
        write_config_file(config_template, model_info)
        write_sdf_file(sdf_template, model_info)
        #write_sdf_file(img_name, sdf_template, world_template, name_world_launch_template, world_launch_template)

        # Rescale/resize heightmap image
        os.chdir(dest_path)
        rescale_and_resize_image(img_name, model_info.resolution, True)
        
        return True
        
    finally:
        
        # Change back to cwd
        os.chdir(setdir)


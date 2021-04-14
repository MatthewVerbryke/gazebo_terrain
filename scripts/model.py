#!/usr/bin/env python

"""
  Functions and Class objects for generating terrain models in Gazebo.

  Copyright 2017-2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""


import math
import os
from shutil import copyfile
import string
import sys

from image_resize import rescale_and_resize_image
from template import read_text_file


class ModelInfo(object):
    """
    A class variable for storing gazebo terrain model information.
    """
    
    def __init__(self):
        
        # Model variables
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
        Handle common errors in field entered values for the current model
        """
        
        msg_out = []
        
        # Check that the numbers entered make sense
        if self.resolution <= 0:
            error = "Entered resolution must be 1x1 or higher"
            msg_out.append(error)
            
        # Check that image resolution is allowable by gazebo          
        else:
            img_check = math.log(self.resolution - 1)/math.log(2)
            if (img_check - int(img_check) == 0):
                pass
            else:
                error = "Entered resolution not allowed: must be an integer in the series: resolution = 2^n+1"
                msg_out.append(error)
            
        if self.side <= 0:
            error = "Terrain side lengths must be greater than 0.0 meters"
            msg_out.append(error)
        if self.range < 0:
            error = "Height range must be 0.0 meters or greater"
            msg_out.append(error)
            
        # Handle output
        if len(msg_out) == 0:
            return True, msg_out
        else:
            return False, msg_out

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
                                            str(model_info.side))
        sdf_template = sdf_template.replace("$SIZEY$",
                                            str(model_info.side))
        sdf_template = sdf_template.replace("$SIZEZ$",
                                            str(model_info.range))
            
        # Ensure results are a string
        sdf_content = str(sdf_template)
    
        # Open file
        target = open("model.sdf", "w")
            
        # Write to model.sdf
        target.write(sdf_content)

    
    finally:
        
        # Close file
        target.close()

def create_model(img_path, img_name, model_info):
    """
    Generate a gazebo terrain model using the given model information,
    heightmap, and template files.
    """
    
    model_dir = os.path.join(MODEL_PATH, model_info.name)

    # Get path to heightmap destination
    dest_path = os.path.join(model_dir, "materials/textures/")
    
    # Retrieve templates
    config_template = read_text_file("config_temp.txt")
    sdf_template = read_text_file("sdf_temp.txt")
    
    # Create directory structure
    model_dir = os.path.join(MODEL_PATH, model_info.name)
    os.mkdir(model_dir)
    os.mkdir(model_dir + "/materials")
    os.mkdir(model_dir + "/materials/textures/")
    
    # Copy heightmap image to proper location
    copyfile(os.path.join(img_path, img_name), os.path.join(dest_path, img_name))

    # Write model files
    os.chdir(model_dir)
    write_config_file(config_template, model_info)
    write_sdf_file(sdf_template, model_info)
    
    # Rescale/resize heightmap image
    rescale_and_resize_image(os.path.join(dest_path, img_name), model_info.resolution, True)
    return True

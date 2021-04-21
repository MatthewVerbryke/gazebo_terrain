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

from image_resize import rescale_and_resize_image
from template import read_text_file, write_file_to_dir


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


def fill_config_template(config_temp, model_info):
    """
    Write the model infomation to the model config file.
    """
        
    # Replace template values
    config_content = config_temp
    config_content = config_content.replace("$MODELNAME$",
                                            model_info.name)
    config_content = config_content.replace("$AUTHORNAME$",
                                            model_info.author)
    config_content = config_content.replace("$EMAILADDRESS$",
                                            model_info.email)
    config_content = config_content.replace("$DESCRIPTION$",
                                            model_info.description)
                                          
    return config_content

def fill_sdf_template(sdf_temp, model_info):
    """
    Write the model infomation to the model SDF file.
    """
    
    # Get heightmap name with no extension
    heightmap_no_ext = os.path.splitext(model_info.heightmap)[0]
    
    # Replace template values
    sdf_content = sdf_temp
    sdf_content = sdf_content.replace("$MODELNAME$",
                                      model_info.name)
    sdf_content = sdf_content.replace("$FILENAME$", 
                                       heightmap_no_ext)
    sdf_content = sdf_content.replace("$SIZEX$",
                                      str(model_info.side))
    sdf_content = sdf_content.replace("$SIZEY$",
                                      str(model_info.side))
    sdf_content = sdf_content.replace("$SIZEZ$",
                                      str(model_info.range))
                                        
    return sdf_content

def create_model(img_path, img_name, pkg_path, model_info):
    """
    Generate a gazebo terrain model using the given model information,
    heightmap, and template files.
    """

    # Relevant paths
    temp_path = os.path.join(pkg_path, "scripts/templates")
    model_path = os.path.join(pkg_path, "models")
            
    try:
        
        # Retrieve templates
        config_template = read_text_file(temp_path, "config_temp.txt")
        sdf_template = read_text_file(temp_path, "sdf_temp.txt")
        
        # Create directory structure for model
        model_dir = os.path.join(model_path, model_info.name)
        os.mkdir(model_dir)
        os.mkdir(model_dir + "/materials")
        os.mkdir(model_dir + "/materials/textures")
        
        # Get path to heightmap destination
        dest_path = os.path.join(model_dir, "materials/textures/")
        
        # Copy heightmap image to proper location
        copyfile(os.path.join(img_path, img_name), os.path.join(dest_path, img_name))

        # Fill information into templates
        config_content = fill_config_template(config_template, model_info)
        sdf_content = fill_sdf_template(sdf_template, model_info)
        
        # Write model files
        write_file_to_dir(model_dir, "model.config", config_content)
        write_file_to_dir(model_dir, "model.sdf", sdf_content)
        
        # Rescale/resize heightmap image
        rescale_and_resize_image(os.path.join(dest_path, img_name), model_info.resolution, True)
    
        return True
        
    except:
        
        return False

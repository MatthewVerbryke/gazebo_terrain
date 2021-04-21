#!/usr/bin/env python

"""
  Functions for generating Gazebo world and launch files for terrain
  models.

  Copyright 2017-2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""


import os

from template import read_text_file, write_file_to_dir


def fill_world_template(world_temp, model_info):
    """
    Write relevant information into the world file template.
    """

    # Replace template values
    world_content = world_temp
    world_content = world_content.replace("$FILENAME$", model_info.name)

    return world_content
    

def fill_launch_template(launch_temp, model_info):
    """
    Write relevant information into the launch file template.
    """

    # Replace template values
    launch_content = launch_temp
    launch_content = launch_content.replace("$FILENAME$", model_info.name)
    
    return launch_content

def create_gazebo_files(pkg_path, model_info):
    """
    Create a world and launch file to bringup the current terrain model 
    in a otherwise empty Gazebo world.
    """
    
    # Relevant paths
    temp_path = os.path.join(pkg_path, "scripts/templates")
    world_path = os.path.join(pkg_path, "worlds")
    launch_path = os.path.join(pkg_path, "launch")
    
    try:
    
        # Retrieve templates
        world_temp = read_text_file(temp_path, "world_temp.txt")
        launch_temp = read_text_file(temp_path, "launch_temp.txt")
        
        # Fill information into templates
        world_content = fill_world_template(world_temp, model_info)
        launch_content = fill_launch_template(launch_temp, model_info)
        
        # Create world file
        world_file_name = "{}.world".format(model_info.name)
        write_file_to_dir(world_path, world_file_name, world_content)
        
        # Create launch file
        launch_file_name = "{}.launch".format(model_info.name)
        write_file_to_dir(launch_path, launch_file_name, launch_content)
        
        return True

    except:
        
        return False

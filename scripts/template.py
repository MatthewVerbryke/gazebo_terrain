#!/usr/bin/env python

"""
  Function to retrieve the contents of a text file.

  Copyright 2017-2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""


import os


def read_text_file(dir_path, file_name):
    """
    Read and return the contents of a text file.
    """

    # Get cwd
    start_dir = os.getcwd()
    
    try:
        # Go to template directory
        os.chdir(dir_path)
        
        # Open template
        file_obj = open(file_name, "r")

        # Read template
        content_hold = file_obj.read()
        content = str(content_hold)

        return content

    finally:
        
        # Close template
        file_obj.close()
        
        # Return to starting directory
        os.chdir(start_dir)

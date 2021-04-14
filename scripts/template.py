#!/usr/bin/env python

"""
  Quick functions for reading and writing to files.

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
    cwd = os.getcwd()
    
    try:
        
        # Go to template directory
        os.chdir(dir_path)
        
        # Open and read template
        with open(file_name, "r") as target:
            content_hold = target.read()
            content = str(content_hold)
            
        return content

    finally:

        # Return to starting directory
        os.chdir(cwd)
        
def write_file_to_dir(dir_path, file_name, content):
    """
    Write content to a file in a designated directory.
    
    WARN: function overwrites any file with 'file_name' in the provided
    directory
    """
    
    # Get cwd
    cwd = os.getcwd()
    
    try:
        
        # Go to the destination directory
        os.chdir(dir_path)
        
        # Write the contents to the file
        with open(file_name, "w") as target:
            content_str = str(content)
            target.write(content_str)
            
    finally:
        
        # Return to starting directory
        os.chdir(cwd)
            

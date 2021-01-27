#!/usr/bin/env python

"""
  Functions for checking and rescaling/resizing heightmap images.

  Copyright 2017-2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""


import math
import os
import sys

from PIL import Image, ImageTk


def check_image_size(img_name, img_path):
    """
    Check to make sure the given image is square and has no channels in
    it.
    """
    
    try:
        
        # Open image
        img = Image.open(img_name)
        
        # Determine size of image
        width, height = img.size
        
        # Check if image is square
        if (width==height):
            is_square = True
        else:
            is_square = False
            
        # Check for channels in image
        img_list = list(img.getdata())
        img_max = max(img_list)
        if (type(img_max)==int):
            is_single_channel = True
        else:
            is_single_channel = False
            
        return is_square, is_single_channel
            
    finally:
        
        # Close image
        img.close()

def rescale_and_resize_image(img_name, img_size, save_img):
    """
    Convert image to 8-bit image of which is sized to the desired 
    resolution
    """
    
    try:
        
        # Open image
        img = Image.open(img_name)
        
        # Resize image
        img = img.resize((int(img_size), int(img_size)), Image.ANTIALIAS) 
        
        # Get data from image
        img_list = list(img.getdata())
        
        # Find minimum and maximum value pixels in the image
        img_max = max(img_list)
        img_min = min(img_list)
        
        # Determine factor to scale to a 8-bit image
        scale_factor = 255.0/(img_max - img_min)
        
        img_list_new = [0] * img_size * img_size
        
        # Rescale all pixels to the range 0 to 255 (in line with unit8 values)
        for i in range(0,img_size):
            for j in range(0,img_size):
                img_list_new[i*img_size + j] = int((img_list[i*img_size + j]-img_min)*scale_factor)
                if (img_list_new[i*img_size + j] > 255) or (img_list_new[i*img_size + j] < 0) or (img_list_new[i*img_size + j]-int(img_list_new[i*img_size + j]) != 0):
                    print("img_list_new[%d][%d] = %r" % (i,j,img_list_new[i*img_size + j]))
        
        img.putdata(img_list_new)
        
        # Convert to uint8 greyscale image
        img = img.convert('L')
        
        # Save image
        if save_img:
            img.save(img_name)
        else:
            ph = ImageTk.PhotoImage(img)
            return ph
        
    finally:
        
        # Close image
        img.close()

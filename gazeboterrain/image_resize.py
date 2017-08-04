#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.


import math
import os
import sys

import PIL
from PIL import Image


class ImageRescaleAndResize():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()

        # Command line arguments
        self.img_name = sys.argv[1] + ".png"
        self.img_path = sys.argv[2]

        # Get side length
        print("Gazebo requires that the image used for the heightmap be square and its")
        print("sides be 2^n+1 (n=1,2,3,...) pixels in size. As such, recomended sizes ")
        print("include 129 x 129, 257 x 257, 513 x 513.")
        print(" ")
        self.img_size = input("What side length should the final image have?:\n")

        allowed_size = False

        # Check Size
        while not allowed_size:
            img_check = math.log(self.img_size - 1)/math.log(2)
            if (img_check - int(img_check) == 0):
                allowed_size = True
            else:
                print(" ")
                print("This size is not allowed.")
                self.img_size = input("Try a different size:\n")
        
        # Run main program
        self.main()

    def rescale_and_resize(self, img_size):
        try:
            
            # Open image
            img = Image.open(self.img_name)

            # Resize image
            img = img.resize((int(img_size), int(img_size)), PIL.Image.ANTIALIAS) 

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
            img.save(self.img_name)
            
        finally:
            
            # Close image
            img.close()

    def main(self):
        try:
            
            # Change to image directory
            os.chdir(self.img_path)
            
            # Resize and rescale the image
            self.rescale_and_resize(self.img_size)
        
        finally:
            
            # Change back directory
            os.chdir(self.setdir)

            print(" ")


if __name__ == "__main__":
    ImageRescaleAndResize()
    
#EOF

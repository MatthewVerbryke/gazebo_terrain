#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/inmoov-ros
# Additional copyright may be held by others, as reflected in the commit history.


import math
import os
import PIL
import sys
from PIL import Image


# Necessary Inputs
img_name = sys.argv[1] + ".png"
print(' ')
print('Gazebo requires that the image used for the heightmap be square and its')
print('sides be 2^n+1 (n=1,2,3,...) pixels in size. As such, recomended sizes ')
print('include 129 x 129, 257 x 257, 513 x 513')
print(' ')
img_size = input('What side length should the final image have?:\n')

# Check Size
allowed_size = False

while allowed_size == False:
    img_check = math.log(img_size - 1)/math.log(2)
    if (img_check - int(img_check) == 0):
        allowed_size = True
    else:
        print('This size is not allowed.')
	img_size = input('Try a different size:\n')

# Find and open .png
os.chdir("temp")
img = Image.open(img_name)

# Resize Image
img = img.resize((int(img_size), int(img_size)), PIL.Image.ANTIALIAS) 

# Rescale All Pixels to the Range 0 to 255 (in line with unit8 values)
imglist2 = list(img.getdata())
maximg = max(imglist2)
minimg = min(imglist2)
scale_factor = 255.0/(maximg - minimg)
imglist3 = [0]*img_size*img_size

for i in range(0,img_size):
    for j in range(0,img_size):
        imglist3[i*img_size + j] = int((imglist2[i*img_size + j]-minimg)*scale_factor)
        if (imglist3[i*img_size + j] > 255) or (imglist3[i*img_size + j] < 0) or (imglist3[i*img_size + j]-int(imglist3[i*img_size + j]) != 0):
            print("imglist3[%d][%d] = %r" % (i,j,imglist3[i*img_size + j]))

img.putdata(imglist3)

# Convert to uint8 Greyscale Image
img = img.convert('L')

# Save and Close
img.save(img_name)
img.close()

# Change Back Directory
os.chdir("/..")

#EOF

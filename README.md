# Gazebo Terrain Model Generator

## Summary

This repository contains a simple python-based program that can generate a Gazebo terrain model from a greyscale PNG image input. The program creates the necessary files for the model based on user input, while also resizing and reformating the given heightmap image to ensure compatability with Gazebo. (Based on this [tutorial](https://github.com/AS4SR/general_info/wiki/Creating-Heightmaps-for-Gazebo))

## Requirements

The program requires the following to function:
* [Gazebo](http://gazebosim.org/)
* [Pillow](http://pillow.readthedocs.io/en/3.0.x/index.html)
* [python-resize-image](https://pypi.python.org/pypi/python-resize-image)

Tested on Ubuntu 16.04 LTS with Gazebo 7

## Instructions

### Installation

Clone the repsitory into your `home/$USER/catkin_ws/src/` directory

### Terrain Generation

Place your heightmap image into your `Pictures` directory before running the program so that it can be found. This image should be a greyscale PNG.

In the gazebo terrain directory, run the program with:

```
./terrain_gen.sh
```

When running the program, it will first ask you for the name of your image; make sure that this is the same as the image in the `Pictures` directory but without the ".png"! You will then be asked to enter various information needed to fill out the configuration files, such as the menu name for the model, size, and other parameters.

Once the program is finished generating the files, open up Gazebo to test out your model. The name that you selected for the model should appear on the `Insert` menu bar.

### Deleting Models

Also included in this repository is `delete_model.sh`, a script that can look into the Gazebo model directory and interactively delete the user-selected directory, if it exists. Be careful to not delete default Gazebo models or anything you want to keep when using this!

Run it with:

```
./delete_models.sh
```

## Notes

* I have managed to get up to 8km x 8km terrains to spawn without issue on my computer
* The image output should be an 8-bit greyscale image. Conversion from 16-bit to 8-bit images are confirmed to work, but it should work with larger grayscales (this still needs to be tested).

## License

This program is licensed under the BSD 3-clause license, as presented in the LICENSE file

Program is Copyright (c) University of Cincinnati


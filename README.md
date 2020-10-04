# Automatic Gazebo Terrain Model Generator

<img src="https://img.shields.io/badge/noetic-passing-green">

## Summary

This repository contains a simple python-based program that can generate a Gazebo terrain model from a greyscale PNG image input. The program creates the necessary files for the model based on user input, while also resizing and reformating the given heightmap image to ensure compatability with Gazebo. (Based on this [tutorial](https://github.com/AS4SR/general_info/wiki/Creating-Heightmaps-for-Gazebo)). Its advised to use a **SRTM30 Plus** image from the tutorial mentioned.

## Requirements

The program requires the following to function:
* [Gazebo](http://gazebosim.org/)
* [Pillow](http://pillow.readthedocs.io/en/3.0.x/index.html)
* [python-resize-image](https://pypi.python.org/pypi/python-resize-image)

Tested on **Ubuntu 20.04 LTS** with **ROS-Noetic** and **Gazebo 11**.

## Instructions

### Installation

* Clone the repository into your `~/$WORKSPACE/src/` directory.

* Run a `catkin_make` in your $WORKSPACE folder.

* Export the model paths in Gazebo:

        echo "export GAZEBO_MODEL_PATH=~/$WORKSPACE/src/gazebo_terrain/models" >> ~/.bashrc && exec bash


### Terrain Generation

Place your heightmap image into your `gazebo_terrain/pictures` directory before running the program so that it can be found. This image should be a greyscale PNG.

In order for this program to work:

  1. The PNG should be a greyscale image without any alpha channels (ideally an unsigned 8-bit image, but the code should be able to convert other bit-size images to the proper format).
  2. The height and width (in pixels) of the PNG must be equal.

To generate the terrain model, world and launch files:

        rosrun gazebo_terrain terrain_gen.sh


When running the program, it will first ask you for the name of your image; make sure that this is the same as the image in the `gazebo_terrain/pictures` directory but without the ".png"! You will then be asked to enter various information needed to fill out the configuration files, such as the size, and other parameters.

Once the program is finished generating the files, it will prompt a command to be run. For example, an image named "terrain_random.png" is present in the `gazebo_terrain/pictures` directory, so the command would be:


        roslaunch gazebo_terrain terrain_random_world.launch

Here is the output:

<img src="https://user-images.githubusercontent.com/45683974/94947425-407a6e80-04fb-11eb-860e-52164d57af1a.jpg" width="900" height="420">

### Deleting Models

Also included in this repository is `delete_model.sh`, a script that can look into the Gazebo model directory and interactively delete the user-selected directory, if it exists. Be careful to not delete default Gazebo models or anything you want to keep when using this!

Run it with:

        rosrun gazebo_terrain delete_model.sh

## Notes

* I have managed to get up to 8km x 8km terrains to spawn without issue on my computer
* The image output should be an 8-bit greyscale image. Conversion from 16-bit to 8-bit images are confirmed to work, but it should work with larger grayscales (this still needs to be tested).
* Based on [issues](http://answers.gazebosim.org/question/17984/heightmap-insertion-unsuccessful-with-gazebo-7/) [others](http://answers.gazebosim.org/question/16319/gazebo-700-crash-on-heightmap-insertion/) have been [having](https://github.com/MatthewVerbryke/gazebo_terrain/issues/1), it appears that you need Gazebo 7.9 or higher for heightmap insertion to work (may work with versions as low as 7.7).

## License

This program is licensed under the BSD 3-clause license, as presented in the LICENSE file

Program is Copyright (c) University of Cincinnati


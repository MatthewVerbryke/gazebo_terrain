# Automatic Gazebo Terrain Model Generator

## Summary

This repository contains a simple python-based program that can generate a Gazebo terrain model from a greyscale PNG image input. The program creates the necessary files for the model based on user input, while also resizing and reformating the given heightmap image to ensure compatability with Gazebo. (Based on this [tutorial](https://github.com/AS4SR/general_info/wiki/Creating-Heightmaps-for-Gazebo)).


## Requirements

The program requires the following to function:
* [Gazebo](http://gazebosim.org/)
* [Pillow](https://python-pillow.org/)

This software was developed and tested using
* Ubuntu 18.04 LTS 
* ROS Melodic
* Gazebo 9.0.0
* Python 3.6.9


## Instructions

### Installation

Clone the repository into your catkin workspace `src` directory and then build the workspace using `catkin_make`.

### Heightmap

There are a few requirements for the heightmap image given to the program:

  1. The image must be grayscale with no additional channels (such as an alpha channel) 
  2. The heightmap should be a `.png`
  3. The heightmap image must be square, i.e. The height and width, in number of pixels, must be equal.

### Launching the GUI

In order to start the program through the main GUI, use:

        rosrun gazebo_terrain launch_gui.sh

### Model Creation

To create a new model, click the `Create New Model` button. This will allow you to select a heightmap and fill values into the configuration entries. Once a heightmap image is selected using the file dialog, the GUI will display the Gazebo compatable version of it. At minimum, a model name, rescaled side length, side dimension, and terrain height range are required. Once finished inputing data, press `Generate Model` to create the model, as well as corrosponding Gazebo launch and world files.

**NOTE**: The rescaled side length must be an integer number in the series `l = 2^n+1, n = 1,2,3,...`. Appropriate sizes therefore include 3, 5, 9, 17, and so on.

### Model Deletion

To delete an existing model click the `Delete Existing Model`, which will bring up a popup to enter the name of the model you want to delete. Once selected, the program will list the files to be deleted before prompting the user to confirm or cancel the operation.

### Testing Models 

In order to test a newly generated model use the generated launch file:

        roslaunch gazebo_terrain $YOUR_MODEL_NAME$.launch

The model's world and launch files (in the `world` directory and `launch` directory, respectively) can be called by other programs within the same catkin workspace.


## Notes

* I have managed to get up to 8km x 8km terrains to spawn without issue on my computer
* The image output should be an unsigned 8-bit greyscale image. Conversion from 16-bit to 8-bit images are confirmed to work, but it should work with larger grayscales (this still needs to be tested).
* Based on [issues](http://answers.gazebosim.org/question/17984/heightmap-insertion-unsuccessful-with-gazebo-7/) [others](http://answers.gazebosim.org/question/16319/gazebo-700-crash-on-heightmap-insertion/) have been [having](https://github.com/MatthewVerbryke/gazebo_terrain/issues/1), it appears that you need Gazebo 7.9 or higher for heightmap insertion to work (may work with versions as low as 7.7).


## License

This program is licensed under the BSD 3-clause license, as presented in the LICENSE file

Program is Copyright (c) University of Cincinnati


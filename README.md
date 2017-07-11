# gazebo_terrain

## Summary

This repository contains a simple program that can generate a Gazebo model of terrain based on a greyscale .png image input. The program creates the necessary model files for the model based on user input, and resizes the given heightmap image to ensure compatability with Gazebo. (Based from this [tutorial](https://github.com/AS4SR/general_info/wiki/Creating-Heightmaps-for-Gazebo))

Tested on Ubuntu 16.04 LTS with Gazebo 7

## Requirements

The program requires the following to function:
* [Pillow](http://pillow.readthedocs.io/en/3.0.x/index.html)
* [python-resize-image](https://pypi.python.org/pypi/python-resize-image)

## Instructions

### Installation

Copy the repsitory into your `~/catkin_ws/src/` directory; the program assumes that your catkin workspace and the file are located here. If you located it somewhere else, you will need to edit the path location in the bash script.

### Usage

Place your image into your `Pictures` directory before running the program so that it can be found. This image should be a PNG.

In the gazebo terrain directory, run the program with:

```
./terrain_gen.sh
```

When running the program, it will first ask you for the name of your image; make sure that this is the same as the image in the `Pictures` directory but without the ".png"! You will then be asked to enter various information needed to fill out the configuration files, such as the menu name for the model, size, and others.

Once the program is finished generating the files, open up Gazebo to test out your model. The name that you inputed for the model should appear on the models list for input.

Also included in this repository is `delete_model.sh`, a script that can look into the Gazebo model directory and delete the user selected directory if it exsists. Be careful when using this to not delete default Gazebo models!

Run it with:

```
./delete_models.sh
```

## Notes

* I have managed to get up to 8km x 8km terrains to spawn with no problems on my computer

## License

This program is licensed under the BSD 3-clause license, as presented in the LICENSE file

Program is Copyright (c) University of Cincinnati


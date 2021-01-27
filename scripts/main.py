#!/usr/bin/env python

"""
  GUI related code for gazebo terrain model generator.

  Copyright 2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""

 
import os
from shutil import copyfile
import tkFileDialog
import Tkinter as tk
import traceback

from image_resize import rescale_and_resize_image, check_image_size
from model import create_model, write_config_file, write_sdf_file
from model import ModelInfo


class MainApp:
    """
    Main GUI class
    """
    
    def __init__(self, master):
        
        # Get CWD 
        self.setdir = os.getcwd()
        
        # Create container for all the subframes on the GUI
        self.container = tk.Frame(master)
        self.container.grid(sticky="nsew")
        
        # Create subframes
        self.action_frame = tk.Frame(self.container, highlightthickness=2)
        self.config_frame = tk.Frame(self.container, highlightthickness=2)
        self.model_frame = tk.Frame(self.container, highlightthickness=2)
        self.generation_frame = tk.Frame(self.container, highlightthickness=2)
        self.heightmap_frame = tk.Frame(self.container, highlightthickness=2)
        
        # Declare entry variables
        self.model_name_var = tk.StringVar()
        self.creator_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.full_path_var = tk.StringVar()
        self.size_x_var = tk.StringVar()
        self.size_z_var = tk.StringVar()
        self.pixel_len_var = tk.IntVar()
        
        # Position subframes
        self.action_frame.grid(row=0, sticky="ew")
        self.config_frame.grid(row=1, sticky="nsew")
        self.model_frame.grid(row=2, sticky="nsew")
        self.generation_frame.grid(row=3, sticky="nsew")
        self.heightmap_frame.grid(row=0, column=1, sticky="nsew", rowspan=4)
        
        # Fill all frames:
        # Action Frame
        self.action_frame_title = tk.Label(self.action_frame,
                                           text="What do you want to do?")
        self.action_frame_title.grid(row=0, columnspan=3, sticky="nsew")
        
        self.create_model_button = tk.Button(self.action_frame, width=17,
                                             text="Create New Model",
                                             command=lambda: self.enable_editing())
        self.create_model_button.grid(row=1, column=0, sticky="nsew")
        
        self.edit_model_button = tk.Button(self.action_frame,width=17,
                                           text="Edit Existing Model",
                                           command=lambda: self.edit_model(),
                                           state=tk.DISABLED)
        self.edit_model_button.grid(row=1, column=1, sticky="nsew")
                
        self.delete_model_button = tk.Button(self.action_frame,width=17,
                                             text="Delete Existing Model",
                                             command=lambda: self.delete_model(),
                                             state=tk.DISABLED)
        self.delete_model_button.grid(row=2, column=0, sticky="nsew")
        
        # Config Frame
        self.action_frame_title = tk.Label(self.config_frame, width=40,
                                           text="Model Configuration")
        self.action_frame_title.grid(row=0, columnspan=2, sticky="nsew")
        
        self.model_name_label = tk.Label(self.config_frame,
                                         text="Model Name")
        self.model_name_label.grid(row=1, column=0)
            
        self.model_name_entry = tk.Entry(self.config_frame,
                                         textvariable=self.model_name_var,
                                         state=tk.DISABLED)
        self.model_name_entry.grid(row=1, column=1, sticky="ew")

        self.author_name_label = tk.Label(self.config_frame,
                                          text="Your Name")
        self.author_name_label.grid(row=2, column=0)
        
        self.author_name_entry = tk.Entry(self.config_frame,
                                          textvariable=self.creator_name_var,
                                          state=tk.DISABLED)
        self.author_name_entry.grid(row=2, column=1, sticky="ew")
        
        self.email_label = tk.Label(self.config_frame,
                                    text="Your Email")
        self.email_label.grid(row=3, column=0)
        
        self.email_entry = tk.Entry(self.config_frame, 
                                    textvariable=self.email_var,
                                    state=tk.DISABLED)
        self.email_entry.grid(row=3, column=1, sticky="ew")

        self.description_label = tk.Label(self.config_frame,
                                          text="Add a short model description")
        self.description_label.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        self.description_entry = tk.Entry(self.config_frame,
                                          textvariable=self.description_var,
                                          state=tk.DISABLED)
        self.description_entry.grid(row=5, column=0, columnspan=2, sticky="ew")
        
        # Model Information Frame
        self.model_frame_title = tk.Label(self.model_frame, width=40,
                                          text="Terrain Configuration*")
        self.model_frame_title.grid(row=0, columnspan=3, sticky="nsew")
        
        self.model_select_button = tk.Button(self.model_frame, width=17,
                                             text="Choose Heightmap",
                                             command=lambda: self.load_heightmap(),
                                             state=tk.DISABLED)
        self.model_select_button.grid(row=1, column=0)

        self.model_path_entry = tk.Entry(self.model_frame,
                                         textvariable=self.full_path_var,
                                         state="readonly")
        self.model_path_entry.grid(row=2, column=0, columnspan=3, sticky="ew")
        
        self.model_res_label = tk.Label(self.model_frame,
                                        text="Rescaled Side Length")
        self.model_res_label.grid(row=3, column=0, sticky="ew")
        
        self.model_res_entry = tk.Entry(self.model_frame, width=12,
                                        textvariable=self.pixel_len_var,
                                        state=tk.DISABLED)
        self.model_res_entry.grid(row=3, column=1, sticky="ew")
        
        self.model_res_unit = tk.Label(self.model_frame,
                                       text="pixels")
        self.model_res_unit.grid(row=3, column=2, sticky="ew")
        
        self.side_length_label = tk.Label(self.model_frame,
                                          text="Side Dimension")
        self.side_length_label.grid(row=4, column=0, sticky="ew")
    
        self.side_length_entry = tk.Entry(self.model_frame, width=12,
                                          textvariable=self.size_x_var,
                                          state=tk.DISABLED)
        self.side_length_entry.grid(row=4, column=1, sticky="ew")
    
        self.side_length_unit = tk.Label(self.model_frame, text="meters")
        self.side_length_unit.grid(row=4, column=2, sticky="ew")
    
        self.terrain_height_label = tk.Label(self.model_frame,
                                             text="Highest Elevation")
        self.terrain_height_label.grid(row=5, column=0, sticky="ew")
    
        self.terrain_height_entry = tk.Entry(self.model_frame, width=12, 
                                             textvariable=self.size_z_var,
                                             state=tk.DISABLED)
        self.terrain_height_entry.grid(row=5, column=1, sticky="ew")
    
        self.terrain_height_unit = tk.Label(self.model_frame, text="meters")
        self.terrain_height_unit.grid(row=5, column=2, sticky="ew")
        
        # Generation Frame
        self.generate_model_button = tk.Button(self.generation_frame,
                                               width=17,
                                               text="Generate Model",
                                               command=lambda: self.generate_model(),
                                               state=tk.DISABLED)
        self.generate_model_button.grid(row=0, column=0)
        self.cancel_button = tk.Button(self.generation_frame,
                                       width=17,
                                       text="Cancel",
                                       command=lambda: self.cancel_program(),
                                       state=tk.DISABLED)
        self.cancel_button.grid(row=0, column=1)
        
        # Picture Frame
        self.image_canvas = tk.Canvas(self.heightmap_frame, width=530, height=530)
        self.image_canvas.grid(row=0)
    
    def edit_model(self):
        """
        TODO
        """
        pass
        
    def delete_model(self):
        """
        TODO
        """
        pass
        
    def load_heightmap(self):
        """
        Function to select a heightmap, check that the image meets 
        Gazebo's requirements, and display the image onto the GUI canvas.
        """
        
        # Get the desired heightmap file name and location
        self.heightmap_file = tkFileDialog.askopenfilename()
        self.heightmap_path, self.heightmap_name = os.path.split(self.heightmap_file)
        
        try:
            
            # Go to the selected directory
            os.chdir(self.heightmap_path)

            # Check the desired image for issues
            is_square, is_single_channel = check_image_size(self.heightmap_name, self.heightmap_path)
            if not is_square:
                print("ERROR: The specified image is not square (height=width)")
            if not is_single_channel:
                print("ERROR: There may be another channel in the image. Make sure the image is greyscale with all other channels removed.")
            
            # Display the image in the GUI canvas
            # https://stackoverflow.com/questions/45668895/tkinter-tclerror-image-doesnt-exist
            if is_square and is_single_channel:
                ph = rescale_and_resize_image(self.heightmap_name, 512, False)
                self.image_canvas.create_image(265, 265, image=ph)
                self.image_canvas.image = ph
                
            # Display the heightmap path
            self.full_path_var.set(self.heightmap_path + "/" + self.heightmap_name)
                
        finally: 
            
            # Go back to the main directory
            os.chdir(self.setdir)
        
    def generate_model(self):
        """
        Function to funnel entered values to the model creation functions.
        """
        
        # Store entries from the GUI
        model_info = ModelInfo()
        model_info.name = self.model_name_var.get()
        model_info.author = self.creator_name_var.get()
        model_info.email = self.email_var.get()
        model_info.description = self.description_var.get()
        model_info.heightmap = self.heightmap_name
        model_info.resolution = self.pixel_len_var.get()
        model_info.side = self.size_x_var.get()
        model_info.range = self.size_z_var.get()
        
        # Check the entries for issues
        is_ok = model_info.check_entries()

        # Create model
        if is_ok:
            success = create_model(self.heightmap_path,
                                   self.heightmap_name,
                                   model_info)
            if success:
                print "Terrain model generated."
            else:
                print "Failed to generate terrain model."
                
        else:
            pass #TODO
    
    def cancel_program(self):
        """
        Disable model creation and purge entered information
        
        TODO: finish
        """
        
        # Reset Buttons
        self.disable_editing()
        
        # Delete image and model information
        self.image_canvas.delete('all')
        self.heightmap_path = None
        self.heightmap_name = None
        # self.model_name_var.get()
        # self.creator_name_var.get()
        # self.email_var.get()
        # self.description_var.get()
        # self.heightmap_name
        # self.pixel_len_var.get()
        # self.size_x_var.get()
        # self.size_z_var.get()
        
    def enable_editing(self):
        """
        Set GUI to enable editing
        """
        
        self.model_name_entry.configure(state=tk.NORMAL)
        self.author_name_entry.configure(state=tk.NORMAL)
        self.email_entry.configure(state=tk.NORMAL)
        self.description_entry.configure(state=tk.NORMAL)
        self.model_select_button.configure(state=tk.NORMAL)
        self.model_res_entry.configure(state=tk.NORMAL)
        self.side_length_entry.configure(state=tk.NORMAL)
        self.terrain_height_entry.configure(state=tk.NORMAL)
        self.generate_model_button.configure(state=tk.NORMAL)
        self.cancel_button.configure(state=tk.NORMAL)
        self.create_model_button.configure(state=tk.DISABLED)
        #self.edit_model_button.configure(state=tk.DISABLED)
        #self.delete_model_button.configure(state=tk.DISABLED)
        
    def disable_editing(self):
        """
        Set GUI back to start position
        """
        
        self.model_name_entry.configure(state=tk.DISABLED)
        self.author_name_entry.configure(state=tk.DISABLED)
        self.email_entry.configure(state=tk.DISABLED)
        self.description_entry.configure(state=tk.DISABLED)
        self.model_select_button.configure(state=tk.DISABLED)
        self.model_res_entry.configure(state=tk.DISABLED)
        self.side_length_entry.configure(state=tk.DISABLED)
        self.terrain_height_entry.configure(state=tk.DISABLED)
        self.generate_model_button.configure(state=tk.DISABLED)
        self.cancel_button.configure(state=tk.DISABLED)
        self.create_model_button.configure(state=tk.NORMAL)
        #self.edit_model_button.configure(state=tk.NORMAL)
        #self.delete_model_button.configure(state=tk.NORMAL)
        

if __name__=="__main__":
    
    try:
        root = tk.Tk()
        root.wm_title("Gazebo Terrain Model Generator")
        app = MainApp(root)
        root.mainloop()
    except Exception:
        traceback.print_exc()

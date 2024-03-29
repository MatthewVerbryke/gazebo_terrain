#!/usr/bin/env python

"""
  GUI related code for Gazebo terrain model generator.

  Copyright 2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""

 
import os
from shutil import copyfile
from tkinter import filedialog
import tkinter as tk
import traceback

from delete import DeleteMenuApp
from image_resize import rescale_and_resize_image, check_image_size
from model import create_model
from model import ModelInfo
from world import create_gazebo_files


class MainApp():
    """
    Main GUI class
    """
    
    def __init__(self, master):
        
        # Get relevant directories
        self.home_dir = os.getcwd()
        self.pict_dir = os.path.expanduser("~") + "/Pictures"
        self.pkg_dir = os.path.split(self.home_dir)[0]
        
        # Store master
        self.master = master
        
        # Create container for all the subframes on the GUI
        self.container = tk.Frame(self.master)
        self.container.grid(sticky="nsew")
        
        # Create subframes
        self.action_frame = tk.Frame(self.container)
        self.config_frame = tk.Frame(self.container)
        self.model_frame = tk.Frame(self.container)
        self.generation_frame = tk.Frame(self.container)
        self.heightmap_frame = tk.Frame(self.container)
        
        # Declare entry variables
        self.model_name_var = tk.StringVar()
        self.creator_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.full_path_var = tk.StringVar()
        self.size_x_var = tk.DoubleVar()
        self.size_z_var = tk.DoubleVar()
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
                                             command=lambda: self.delete_model())
        self.delete_model_button.grid(row=2, column=0, sticky="nsew")
        
        # Config Frame
        self.config_frame_title = tk.Label(self.config_frame, width=40,
                                           text="Model Configuration",
                                           fg="gray")
        self.config_frame_title.grid(row=0, columnspan=2, sticky="nsew")
        
        self.model_name_label = tk.Label(self.config_frame,
                                         text="Model Name",
                                         fg="gray")
        self.model_name_label.grid(row=1, column=0)
            
        self.model_name_entry = tk.Entry(self.config_frame,
                                         textvariable=self.model_name_var,
                                         state=tk.DISABLED)
        self.model_name_entry.grid(row=1, column=1, sticky="ew")

        self.author_name_label = tk.Label(self.config_frame,
                                          text="Your Name",
                                          fg="gray")
        self.author_name_label.grid(row=2, column=0)
        
        self.author_name_entry = tk.Entry(self.config_frame,
                                          textvariable=self.creator_name_var,
                                          state=tk.DISABLED)
        self.author_name_entry.grid(row=2, column=1, sticky="ew")
        
        self.email_label = tk.Label(self.config_frame,
                                    text="Your Email",
                                    fg="gray")
        self.email_label.grid(row=3, column=0)
        
        self.email_entry = tk.Entry(self.config_frame, 
                                    textvariable=self.email_var,
                                    state=tk.DISABLED)
        self.email_entry.grid(row=3, column=1, sticky="ew")

        self.description_label = tk.Label(self.config_frame,
                                          text="Add a short model description",
                                          fg="gray")
        self.description_label.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        self.description_entry = tk.Entry(self.config_frame,
                                          textvariable=self.description_var,
                                          state=tk.DISABLED)
        self.description_entry.grid(row=5, column=0, columnspan=2, sticky="ew")
        
        # Model Information Frame
        self.model_frame_title = tk.Label(self.model_frame, width=40,
                                          text="Terrain Configuration",
                                          fg="gray")
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
                                        text="Rescaled Side Length",
                                        fg="gray")
        self.model_res_label.grid(row=3, column=0, sticky="ew")
        
        self.model_res_entry = tk.Entry(self.model_frame, width=12,
                                        textvariable=self.pixel_len_var,
                                        state=tk.DISABLED)
        self.model_res_entry.grid(row=3, column=1, sticky="ew")
        
        self.model_res_unit = tk.Label(self.model_frame,
                                       text="pixels",
                                       fg="gray")
        self.model_res_unit.grid(row=3, column=2, sticky="ew")
        
        self.side_length_label = tk.Label(self.model_frame,
                                          text="Side Dimension",
                                          fg="gray")
        self.side_length_label.grid(row=4, column=0, sticky="ew")
    
        self.side_length_entry = tk.Entry(self.model_frame, width=12,
                                          textvariable=self.size_x_var,
                                          state=tk.DISABLED)
        self.side_length_entry.grid(row=4, column=1, sticky="ew")
    
        self.side_length_unit = tk.Label(self.model_frame, text="meters",
                                         fg="gray")
        self.side_length_unit.grid(row=4, column=2, sticky="ew")
    
        self.terrain_height_label = tk.Label(self.model_frame,
                                             text="Highest Elevation",
                                             fg="gray")
        self.terrain_height_label.grid(row=5, column=0, sticky="ew")
    
        self.terrain_height_entry = tk.Entry(self.model_frame, width=12, 
                                             textvariable=self.size_z_var,
                                             state=tk.DISABLED)
        self.terrain_height_entry.grid(row=5, column=1, sticky="ew")
    
        self.terrain_height_unit = tk.Label(self.model_frame, text="meters",
                                            fg="gray")
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
        
    def load_heightmap(self):
        """
        Function to select a heightmap, check that the image meets 
        Gazebo's requirements, and display the image onto the GUI canvas.
        """
        
        # Get the desired heightmap file name and location
        self.heightmap_file = filedialog.askopenfilename(initialdir=self.pict_dir)
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
            os.chdir(self.home_dir)
        
    def generate_model(self):
        """
        Function to funnel entered values to the model creation functions.
        """
        
        # Make sure a heightmap has been selected
        try: 
            type(self.heightmap_name) == None
        except:
            print("Error: No heightmap file selected")
            return
        
        # Store entries from the GUI
        model_info = ModelInfo()
        model_info.name = str(self.model_name_var.get())
        model_info.author = str(self.creator_name_var.get())
        model_info.email = str(self.email_var.get())
        model_info.description = str(self.description_var.get())
        model_info.heightmap = str(self.heightmap_name)
        model_info.resolution = int(self.pixel_len_var.get())
        model_info.side = float(self.size_x_var.get())
        model_info.range = float(self.size_z_var.get())
        
        # Check the entries for issues
        is_ok, error_msgs = model_info.check_entries()

        # Create model and Gazebo world/launch files
        if is_ok:
            success = create_model(self.heightmap_path,
                                   self.heightmap_name,
                                   self.pkg_dir,
                                   model_info)
            if success:
                print("Terrain model generated.")
            else:
                print("Failed to generate terrain model.")
                
            success2 = create_gazebo_files(self.pkg_dir,
                                           model_info)
            if success2:
                print("Gazebo world and launch files generated.")
            else:
                print("Failed to generate Gazebo world and/or launch files.")
        
        # Print errors to terminal        
        else:
            for msg in error_msgs:
                print("ERROR: " + msg)
            print("")
            
        # Purge entries and return to main buttons
        self.cancel_program()
            
    def edit_model(self):
        """
        TODO
        """
        pass
        
    def delete_model(self):
        """
        Create a model deletion popup
        """
        
        # Launch delete menu popup
        self.new = tk.Toplevel(self.master)
        delete_menu = DeleteMenuApp(self.new, self.pkg_dir)
        self.new.grab_set()           
    
    def cancel_program(self):
        """
        Disable model creation and purge entered information.
        """
        
        # Delete image and entry widgets
        self.image_canvas.delete('all')
        self.heightmap_path = None
        self.heightmap_name = None
        self.full_path_var.set("")
        self.model_name_entry.delete(0, tk.END)
        self.author_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.model_path_entry.delete(0, tk.END)
        self.model_res_entry.delete(0, tk.END)
        self.side_length_entry.delete(0, tk.END)
        self.terrain_height_entry.delete(0, tk.END)
        
        # Reset Labels and Buttons
        self.disable_editing()
        
    def change_label_colors(self, color):
        """
        Change all config and model frame labels to the specified color.
        """
        
        self.config_frame_title.config(fg=color)
        self.model_name_label.config(fg=color)
        self.author_name_label.config(fg=color)
        self.email_label.config(fg=color)
        self.description_label.config(fg=color)
        self.model_frame_title.config(fg=color)
        self.model_res_label.config(fg=color)
        self.model_res_unit.config(fg=color)
        self.side_length_label.config(fg=color)
        self.side_length_unit.config(fg=color)
        self.terrain_height_label.config(fg=color)
        self.terrain_height_unit.config(fg=color)
        
    def enable_editing(self):
        """
        Set GUI to enable editing
        """
        
        # Disable/Enable correct buttons
        self.model_name_entry.config(state=tk.NORMAL)
        self.author_name_entry.config(state=tk.NORMAL)
        self.email_entry.config(state=tk.NORMAL)
        self.description_entry.config(state=tk.NORMAL)
        self.model_select_button.config(state=tk.NORMAL)
        self.model_res_entry.config(state=tk.NORMAL)
        self.side_length_entry.config(state=tk.NORMAL)
        self.terrain_height_entry.config(state=tk.NORMAL)
        self.generate_model_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.NORMAL)
        self.create_model_button.config(state=tk.DISABLED)
        #self.edit_model_button.config(state=tk.DISABLED)
        self.delete_model_button.config(state=tk.DISABLED)
        
        # Change label colors
        self.change_label_colors("black")
        
    def disable_editing(self):
        """
        Set GUI back to start position
        """
        
        # Disable/Enable correct buttons
        self.model_name_entry.config(state=tk.DISABLED)
        self.author_name_entry.config(state=tk.DISABLED)
        self.email_entry.config(state=tk.DISABLED)
        self.description_entry.config(state=tk.DISABLED)
        self.model_select_button.config(state=tk.DISABLED)
        self.model_res_entry.config(state=tk.DISABLED)
        self.side_length_entry.config(state=tk.DISABLED)
        self.terrain_height_entry.config(state=tk.DISABLED)
        self.generate_model_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        self.create_model_button.config(state=tk.NORMAL)
        #self.edit_model_button.config(state=tk.NORMAL)
        self.delete_model_button.config(state=tk.NORMAL)
        
        # Change label colors
        self.change_label_colors("gray")

if __name__=="__main__":
    try:
        root = tk.Tk()
        root.wm_title("Gazebo Terrain Model Generator")
        app = MainApp(root)
        root.mainloop()
    except Exception:
        traceback.print_exc()

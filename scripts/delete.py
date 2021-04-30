#!/usr/bin/env python

"""
  Popup GUI and functions for deleting all files relevant to a specified
  model.

  Copyright 2021 University of Cincinnati
  All rights reserved. See LICENSE file at:
  https://github.com/MatthewVerbryke/gazebo_terrain
  Additional copyright may be held by others, as reflected in the commit
  history.
"""


import glob
import os
import tkinter as tk


class DeleteMenuApp():
    """
    Delete model popup GUI object.
    """
    
    def __init__(self, master, pkg_dir):
        
        # Relevant directories
        self.home_dir = os.getcwd()
        self.pkg_dir = pkg_dir
        self.model_dir = os.path.join(self.pkg_dir, "models")
        self.world_dir = os.path.join(self.pkg_dir, "worlds")
        self.launch_dir = os.path.join(self.pkg_dir, "launch")
        
        # Item list variables
        self.file_list = []
        self.dir_list = []
        
        # Create container for all the subframes on the GUI
        self.container = tk.Frame(master)
        self.container.grid(sticky="nsew")
        
        # Store master in object
        self.master = master
        
        # Declare entry variables
        self.model_name_var = tk.StringVar()
        
        # Create main frame
        self.popup_frame = tk.Frame(self.master)
        self.popup_frame.grid(sticky="nsew")
        
        # Create subframes
        self.model_name_frame = tk.Frame(self.popup_frame,
                                         highlightthickness=2)
        self.action_frame = tk.Frame(self.popup_frame,
                                     highlightthickness=2)
        self.name_frame = tk.Frame(self.popup_frame,
                                   highlightthickness=2)
        self.action2_frame = tk.Frame(self.popup_frame,
                                      highlightthickness=2)
        
        # Position subframes
        self.model_name_frame.grid(row=0, sticky="ew")
        self.action_frame.grid(row=1)
        self.name_frame.grid(row=2)
        self.action2_frame.grid(row=3)
        
        # Populate frames
        self.instruction = tk.Label(self.model_name_frame, width=75,
                                    text="Enter the name of the model to be deleted:")
        self.instruction.grid(row=0, column=0, sticky="nsew")

        self.name_entry = tk.Entry(self.model_name_frame, width=30,
                                   textvariable=self.model_name_var)
        self.name_entry.grid(row=1, column=0)
        
        self.delete_button = tk.Button(self.action_frame, text="Delete", 
                                       width=12,
                                       command=lambda: self.check_model_elements())
        self.delete_button.grid(row=0, column=0, sticky="ew")
        
        self.cancel_button = tk.Button(self.action_frame, text="Cancel",
                                       width=12,
                                       command=lambda: self.master.destroy())
        self.cancel_button.grid(row=0, column=1, sticky="ew")
        
        self.dir_list_label = tk.Label(self.name_frame, width=73, fg="gray",
                                       text="Directories to be deleted:")
        self.dir_list_label.grid(row=0)
        
        self.dirs_msg = tk.Message(self.name_frame, text="", width=1000,
                                   justify="left", bg="white")
        self.dirs_msg.grid(row=1, sticky="ew")
        
        self.file_list_label = tk.Label(self.name_frame, fg="gray",
                                        text="Files to be deleted:")
        self.file_list_label.grid(row=2, sticky="ew")
        
        self.files_msg = tk.Message(self.name_frame, text="", width=1000,
                                    justify="left", bg="white")
        self.files_msg.grid(row=3, sticky="ew")
        
        warning_str = "Are you absolutely sure you want to delete this model?"
        self.warning_label = tk.Label(self.action2_frame, text=warning_str,
                                      fg="gray")
        self.warning_label.grid(row=0, columnspan=2, sticky="ew")
        
        self.delete_final_button = tk.Button(self.action2_frame, text="Yes", 
                                             width=12, state=tk.DISABLED,
                                             command=lambda: self.delete_model_files())
        self.delete_final_button.grid(row=1, column=0, sticky="ew")
        
        self.cancel_final_button = tk.Button(self.action2_frame, text="No",
                                             width=12, state=tk.DISABLED,
                                             command=lambda: self.master.destroy())
        self.cancel_final_button.grid(row=1, column=1, sticky="ew")
        

        
    def check_model_elements(self):
        """
        Check the model provided by the user to ensure it actually exists
        and that it will not present problems during deletion. Also 
        build a list of files and directories that will be deleted.
        """
        
        # Retrieve model name
        name = str(self.model_name_var.get())
        model_full_path = os.path.join(self.model_dir, name)
        
        # Check if a name has actually been put in yet
        if name == "":
            print ("ERROR: No model name input")
            return False
        
        # Check if model directory actually exists
        top_exists = os.path.isdir(model_full_path)
        if not top_exists:
            print ("ERROR: No model named '{}' exists in the model directory".format(name))
            self.master.destroy()
            
        # Retrieve name of all files within the model directory
        self.dir_list = [os.path.join(model_full_path, "materials/textures/"),
                         os.path.join(model_full_path, "materials/"),
                         model_full_path + "/"]
        for i in range(0,3):
            for j in glob.glob(self.dir_list[i] + "*"):
                is_file = os.path.isfile(j)
                is_dir = os.path.isdir(j)
                if is_file:
                    self.file_list.append(j)
                    
                # Check for directories that may complicate deletion
                if is_dir:
                    j_dir = j + "/"
                    if j_dir not in self.dir_list:
                        print ("ERROR: Additional directory found in model structure:")
                        print ("       " + j_dir)
                        self.master.destroy()

        # Check for world and launch files
        world_ext = os.path.join(self.world_dir, name + ".world")
        launch_ext = os.path.join(self.launch_dir, name + ".launch")
        gazebo_list = [world_ext, launch_ext]
        for k in gazebo_list:
            if os.path.isfile(k):
                self.file_list.append(k)
            else:
                print ("WARN: Could not find '{}'".format(k))
        
        # Parse directory names into a string
        dir_str = ""
        for directory in self.dir_list:
            new_line = "- " + directory + "\n"
            dir_str += new_line
        
        # Parse filenames into a string
        file_str = ""
        for file_path in self.file_list:
            new_line = "- " + file_path + "\n"
            file_str += new_line
        
        # Display directories and files to be deleted
        self.dirs_msg.config(text=dir_str)
        self.files_msg.config(text=file_str)
        self.dir_list_label.config(fg="black")
        self.file_list_label.config(fg="black")
        self.warning_label.config(fg="black")
        
        # Enable/Disable buttons
        self.delete_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        self.delete_final_button.config(state=tk.NORMAL)
        self.cancel_final_button.config(state=tk.NORMAL)
        
        return True
        
    def delete_model_files(self):
        """
        Delete all files and directories, then shut down the deletion 
        menu.
        """
        
        # Delete files in file list
        for file_path in self.file_list:
            os.remove(file_path)
            
        # Delete all directories in the directory list
        for dir_path in self.dir_list:
            os.rmdir(dir_path)
        
        # Shutdown popup menu
        print ("All specifed files and directories deleted")
        self.master.destroy()

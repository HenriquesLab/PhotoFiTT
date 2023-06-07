import os
import shutil
import random

def copy_files(root_folder, output_folder):
    # Get all subfolders in the root folder
    subfolders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]

    for subfolder in subfolders:
        frame_folder = os.path.join(root_folder, subfolder, "Frame_1")
        channel_folders = ["Channel_1", "Channel_2", "Channel_3", "Channel_4"]

        # Create target folders for training and quality control
        for i, channel_folder in enumerate(channel_folders, start=1):
            quality_control_folder = os.path.join(output_folder, f"Training_dataset_{i}")
            training_folder = os.path.join(output_folder, f"Quality_control_dataset_{i}")
            os.makedirs(training_folder, exist_ok=True)
            os.makedirs(quality_control_folder, exist_ok=True)

            channel_path = os.path.join(frame_folder, channel_folder)

            # Get all .png files ending in "_Image3" from the channel subfolder. The number at the end of "_Image()" dictates the slice
            files = [f for f in os.listdir(channel_path) if f.endswith("_Image3.png")]
            files.sort()  # Sort the files list

            # Copy files to the training dataset folder
            for file in files:
                src = os.path.join(channel_path, file)
                dst = os.path.join(training_folder, file)
                shutil.copy2(src, dst)
                print(f"Copied file: {src} -> {dst}")

            # Count the number of files in the training folder
            training_files = os.listdir(training_folder)
            num_files = len(training_files)

            # Move 10% of files to the quality control folder
            num_files_to_move = int(num_files * 0.1)  # Calculate 10% of the files
            files_to_move = random.sample(training_files, num_files_to_move)

            for file in files_to_move:
                src = os.path.join(training_folder, file)
                dst = os.path.join(quality_control_folder, file)
                shutil.move(src, dst)
                print(f"Moved file: {src} -> {dst}")


# PATHS
root_folder = "/Users/mrosario/Desktop/20230530_dyes_split-files"
output_folder = "/Users/mrosario/Desktop/Data_pix2pix"
copy_files(root_folder, output_folder)

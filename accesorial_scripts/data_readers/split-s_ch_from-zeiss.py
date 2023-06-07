import os
import glob
import czifile
import numpy as np
import cv2


def separate_frames_channels_from_czi(input_folder, output_folder):
    # Get all .czi files in the input folder
    czi_files = glob.glob(os.path.join(input_folder, "*.czi"))

    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for czi_file in czi_files:
        # Read the .czi file
        czi_data = czifile.imread(czi_file)

        # Create a subfolder in the output folder for each .czi file
        file_name = os.path.splitext(os.path.basename(czi_file))[0]
        file_folder = os.path.join(output_folder, file_name)
        os.makedirs(file_folder, exist_ok=True)

        # Iterate over frames
        for frame_index, frame_data in enumerate(czi_data):
            # Create a folder for each frame
            frame_folder = os.path.join(file_folder, f"Frame_{frame_index + 1}")
            os.makedirs(frame_folder, exist_ok=True)

            # Iterate over channels in each frame
            for channel_index, channel_data in enumerate(frame_data):
                # Create a folder for each channel
                channel_folder = os.path.join(frame_folder, f"Channel_{channel_index + 1}")
                os.makedirs(channel_folder, exist_ok=True)

                # Normalize channel data to 0-255 range
                channel_data = normalize_channel(channel_data)

                # Save each channel as individual .png images
                for image_index, image_data in enumerate(channel_data):
                    image_path = os.path.join(channel_folder, f"{file_name}_Frame{frame_index + 1}_Channel{channel_index + 1}_Image{image_index + 1}.png")
                    cv2.imwrite(image_path, image_data)
                    print(f"Saved: {image_path}")

    print("Frame and channel separation complete.")

# needed to work with non-RGB files
def normalize_channel(channel_data):
    min_val = np.min(channel_data)
    max_val = np.max(channel_data)

    normalized_data = (channel_data - min_val) * (255.0 / (max_val - min_val))
    normalized_data = normalized_data.astype(np.uint8)

    return normalized_data


# Example usage
input_folder = "/Users/mrosario/Desktop/20230530_dyes/individual_3"  # Replace with your input folder path
output_folder = "/Users/mrosario/Desktop/20230530_dyes_split-files"  # Replace with your output folder path

separate_frames_channels_from_czi(input_folder, output_folder)

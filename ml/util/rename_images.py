import os
import argparse

def rename_images(directory, new_suffix):
    # Iterate over each file in the specified directory
    for filename in os.listdir(directory):
        # Check if the file name starts with 'img' followed by a number and contains an underscore
        if filename.startswith("img") and "_" in filename:
            # Split the filename into 'imgX' and the rest, including extension
            prefix, rest = filename.split("_", 1)
            # Extract the file extension
            extension = os.path.splitext(rest)[1]
            # Create the new filename with the specified suffix and original extension
            new_filename = f"{prefix}_{new_suffix}{extension}"
            # Define the full paths for renaming
            original_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(original_path, new_path)
            print(f"Renamed '{filename}' to '{new_filename}'")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Rename images from imgX_FILE_NAME to imgX_Y while keeping file extension")
    parser.add_argument("directory", type=str, help="Directory containing the images")
    parser.add_argument("new_suffix", type=str, help="New suffix to replace FILE_NAME")

    args = parser.parse_args()
    # Call the rename function with provided arguments
    rename_images(args.directory, args.new_suffix)

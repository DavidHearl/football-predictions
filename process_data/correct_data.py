import os
import json
import pandas as pd
import ast
from key_corrections import club_corrections, player_corrections
import shutil
from tqdm import tqdm
from unidecode import unidecode

def copy_data():
    source = 'raw_data'
    destination = 'clean_data'
    json_counter = 0

    print("Copying data...")

    # Delete the 'clean_data' directory if it already exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Copy the entire directory tree
    shutil.copytree(source, destination)

    # Count the number of .json files
    for subdir, dirs, files in os.walk(destination):
        for file in files:
            if file.endswith('.json'):
                json_counter += 1

    print("Data copied successfully!")
    print(f"Number of .json files: {json_counter}")

def correct_data():
    destination = 'clean_data'

    # Get the total number of files for the progress bar
    total_files = sum([len(files) for r, d, files in os.walk(destination)])

    print("Correcting data...")

    # Create a progress bar
    with tqdm(total=total_files, desc="Processing files", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        # Iterate over all files in the new directory
        for subdir, dirs, files in os.walk(destination):
            for file in files:
                # Create the file path
                file_path = os.path.join(subdir, file)

                # Open the file
                with open(file_path, 'r', encoding="utf-8") as f:
                    json_str = f.read()

                # Replace Unicode escape sequences in the JSON string
                json_str = json_str.encode().decode('unicode-escape')

                # Convert non-ASCII characters to their closest ASCII equivalents
                json_str = unidecode(json_str)

                # Write the modified string back to the file
                with open(file_path, 'w', encoding="utf-8") as f:
                    f.write(json_str)

                # Update the progress bar
                pbar.update()
    
    print("Data corrected successfully!")

copy_data()
# correct_data()

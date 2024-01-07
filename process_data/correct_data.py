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

    print("Copying data...")

    # Delete the 'clean_data' directory if it already exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Copy the entire directory tree
    shutil.copytree(source, destination)

    print("Data copied successfully!")

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
correct_data()

# def remove_keys(data, keys_to_remove):
#     cleaned_data = []

#     for entry in data:
#         cleaned_entry = {key: value for key, value in entry.items() if key not in keys_to_remove}
#         cleaned_data.append(cleaned_entry)

#     return cleaned_data

# def correct_data(data):
#     corrected_data = []

#     for entry in data:
#         corrected_entry = {}
#         for key, value in entry.items():
#             corrected_key = corrections.get(key, key)
#             corrected_value = corrections.get(value, value)
#             corrected_entry[corrected_key] = corrected_value
#         corrected_data.append(corrected_entry)

#     return corrected_data

# def correct_and_save(file_path):
#     # Load JSON data from the file
#     with open(file_path, 'r', encoding="utf-8") as file:
#         json_str = file.read()

#     # Search and replace Unicode escape sequences
#     json_str = search_and_replace_unicode(json_str)

#     # Load the modified JSON data
#     json_data = json.loads(json_str)

#     # Remove specified keys
#     keys_to_remove = ['Notes']  # Add more keys as needed
#     cleaned_data = remove_keys(json_data, keys_to_remove)

#     # Apply corrections
#     corrected_data = correct_data(cleaned_data)

#     # Create the output directory if it doesn't exist
#     output_directory = os.path.join("corrected_data", "squad_data")
#     os.makedirs(output_directory, exist_ok=True)

#     # Create a new file name
#     base_name, extension = os.path.splitext(os.path.basename(file_path))
#     new_file_path = os.path.join(output_directory, f"{base_name}{extension}")

#     # Save the corrected data to the new file
#     with open(new_file_path, 'w', encoding="utf-8") as file:
#         json.dump(corrected_data, file, ensure_ascii=False, indent=2)

# def main():
#     # Set directory for squad json files
#     squad_directory = "raw_data/squad_data/"

#     # List all JSON files in the directory
#     squad_tables = [file for file in os.listdir(squad_directory) if file.endswith(".json")]

#     # Create full path by joining directory and squad_table
#     squad_tables = [os.path.join(squad_directory, file) for file in squad_tables]

#     # Iterate through the list of files and apply corrections
#     for file_path in squad_tables:
#         correct_and_save(file_path)


# if __name__ == '__main__':
#     main()

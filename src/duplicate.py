import os
import json


def load_json_files(folder_path):
    combined_data = []

    # Iterate over files in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a JSON file
        if filename.endswith(".json"):
            with open(file_path, "r") as file:
                # Load JSON content from the file
                json_content = json.load(file)

                # Assuming there is a single array in each JSON file
                if isinstance(json_content, list):
                    # Extend the combined_data with the array from the current file
                    print(len(json_content))
                    combined_data.extend(json_content)

    return combined_data


# Specify the folder path containing your JSON files
path = "../results"

# Load and combine JSON data from files
resulting_array = load_json_files(path)

# Now, resulting_array contains the combined data from all JSON files
print(f"Number of all items fetched: {len(resulting_array)}")

# Create a set to track seen elements
seen = set()
# List to store duplicated items
duplicates = []

# Iterate over the combined data to find duplicates
for item in resulting_array:
    if item in seen:
        duplicates.append(item)
    else:
        seen.add(item)

# Print the number of unique items
print(f"Number of uniques: {len(seen)}")

# Print the number of duplicates and the duplicated items
print(f"Number of duplicates: {len(duplicates)}")
print(f"Duplicated items: {duplicates}")
import argparse
import os
import re


def is_valid_project_name(name: str) -> bool:
    # Check that the project name is not empty and does not contain invalid characters
    return bool(re.match(r'^[a-zA-Zа-я0-9_-]+$', name))


def rename_project(directory: str, new_project_name: str):
    # Get the old project name from the directory name
    old_project_name = os.path.basename(directory)

    # Check if the old project name matches the new name
    if old_project_name == new_project_name:
        if old_project_name == new_project_name:
            raise NameError(f"The project name '{new_project_name}' is already the current name.")

    # Step 1: Rename the main directory
    parent_dir = os.path.dirname(directory)
    new_directory = os.path.join(parent_dir, new_project_name)
    os.rename(directory, new_directory)
    # Update the directory path to the new path
    directory = new_directory

    # Step 2: Rename files and subdirectories
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files + dirs:
            if old_project_name in name:
                old_path = os.path.join(root, name)
                # Replace the old project name with the new one in the file or directory name
                new_name = name.replace(old_project_name, new_project_name)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

    # Step 3: Replace the old project name inside files
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Open the file and read its contents
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Replace the old project name with the new one in the file content
                new_content = content.replace(old_project_name, new_project_name)
                # Write the modified content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            except UnicodeDecodeError:
                # Skip files that are not text-based
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renaming the Keil µVision project.')
    parser.add_argument('--directory', type=str, help='Path to the project directory')
    parser.add_argument('--new_project_name', type=str, help='New project name')

    args = parser.parse_args()

    try:
        if args.directory and args.new_project_name:
            directory = args.directory
            new_project_name = args.new_project_name
        else:
            directory = input("Enter the path to the project directory: ")
            new_project_name = input("Enter the new project name: ")
            print()

        # Check if the initial directory exists
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.")
        # Check the validity of the new project name
        elif not is_valid_project_name(new_project_name):
            print(f"Error: Invalid project name '{new_project_name}'. The name should only contain letters, numbers, dashes, and underscores.")
        else:
            rename_project(directory, new_project_name)
            print("Project successfully renamed.")
    except KeyboardInterrupt:
        print("Operation aborted by user.")
    except NameError as e:
        print(f"Error: {e}")

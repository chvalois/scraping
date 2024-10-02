import os
import shutil

from inject_to_postgres import add_scraped_data_to_postgresDB

# This script was used to repopulate database from existing files
# os.walk is a generator and calling next will get the first result in the form of a 3-tuple (dirpath, dirnames, filenames). Thus the [1] index returns only the dirnames from that tuple

def list_directories(base_dir):
    directories = []
    subdirectories = {}

    for root, dirs, files in os.walk(base_dir):
        # Only consider directories that are directly under the base_dir
        if root == base_dir:
            directories.extend(dirs)
        else:
            # Get the parent directory name
            parent_dir = os.path.basename(os.path.dirname(root))
            # Get the current directory name
            current_dir = os.path.basename(root)
            # Add the current directory to the subdirectories of its parent
            if parent_dir not in subdirectories:
                subdirectories[parent_dir] = []
            subdirectories[parent_dir].append(current_dir)

    return directories, subdirectories


# Get dept and dates existing files
base_directory = './files/'
dept, dept_dates = list_directories(base_directory)
del(dept_dates['files'])

for dept in dept_dates.keys():
    for date in dept_dates[dept]:
        add_scraped_data_to_postgresDB(dept, date)
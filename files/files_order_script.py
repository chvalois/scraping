import os
import shutil

# This script was used to clean and order files that were previosuly saved under files directory

files = [f for f in os.listdir() if f.endswith('.csv')]

for f in files:
    date = f[-34:-24]
    dept = f.split("_")[1]
    print(f)

    # Create directories for missing directories
    save_dir = f'{str(dept)}/{date}'
    if not os.path.exists(f'{str(dept)}'):
        os.makedirs(f'{str(dept)}')
            
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    shutil.move(f, f"./{dept}/{date}/{f}")

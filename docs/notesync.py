import os
import shutil
import time

"""Note sync tool to copy mds from
source directory to a destination directory
"""
# Define the source and destination directories
source_dir = "C:\\path\\to\\your\\notes"  # Change this to your actual source directory
destination_dir = "mnt/c/Users/GSACS/Documents/aviate master/GSADS/docs"  # Change this to your actual WSL destination directory

def copy_files():
    # Copy files from source to destination
    if os.path.exists(source_dir):
        for filename in os.listdir(source_dir):
            src_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(destination_dir, filename)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dest_file)
                print(f"Copied {src_file} to {dest_file}")
            else:
                print(f"Skipped {src_file}, not a file")
    else:
        print(f"Source directory {source_dir} does not exist")

def main():
    while True:
        # Perform the copy operation
        copy_files()
        # Wait for 60 seconds
        print("Waiting for next copy operation...")
        time.sleep(60)

if __name__ == "__main__":
    main()
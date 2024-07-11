import zipfile
import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog

def extract_cbz(cbz_path, extract_to):
    with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def create_cbz(folder_path, cbz_path):
    with zipfile.ZipFile(cbz_path, 'w') as zip_ref:
        for root, dirs, files in os.walk(folder_path):
            for file in sorted(files):  # Sorting files to maintain order
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zip_ref.write(file_path, arcname)

def merge_cbz(cbz_paths, output_cbz_path, remove_last_page):
    temp_dirs = []
    merged_dir = "merged_cbz"
    page = 0

    # Create the merged directory
    os.makedirs(merged_dir, exist_ok=True)

    # Extract all CBZ files and optionally remove the last page
    for i, cbz_path in enumerate(cbz_paths):
        temp_dir = f"temp_cbz_{i}"
        os.makedirs(temp_dir, exist_ok=True)
        temp_dirs.append(temp_dir)
        
        extract_cbz(cbz_path, temp_dir)
        
        # remove xml files
        for file in sorted(os.listdir(temp_dir)):
            if file.endswith(".xml"):
                os.remove(os.path.join(temp_dir, file))
     
        if remove_last_page:
            last_page = sorted(os.listdir(temp_dir))[-1]
            os.remove(os.path.join(temp_dir, last_page))
        
        
        # rename files to avoid conficts
        for file in sorted(os.listdir(temp_dir)):
            page += 1
            shutil.move(os.path.join(temp_dir, file), os.path.join(temp_dir, f"page_{page}.jpg"))

        # Copy all files to the merged directory
        for file in sorted(os.listdir(temp_dir)):  # Sorting files to maintain order
            shutil.copy(os.path.join(temp_dir, file), os.path.join(merged_dir, file))

    # Create the merged CBZ
    create_cbz(merged_dir, output_cbz_path)

    # Clean up temporary directories
    for temp_dir in temp_dirs:
        shutil.rmtree(temp_dir)
    shutil.rmtree(merged_dir)

# GUI to select files and options
root = tk.Tk()
root.withdraw()

cbz_paths = filedialog.askopenfilenames(title="Select CBZ files to merge", filetypes=[("CBZ files", "*.cbz")])
if not cbz_paths:
    print("No CBZ files selected. Exiting.")
    exit()

output_cbz_path = filedialog.asksaveasfilename(title="Save merged CBZ as", defaultextension=".cbz", filetypes=[("CBZ files", "*.cbz")])
if not output_cbz_path:
    print("No output CBZ file specified. Exiting.")
    exit()

remove_last_page = simpledialog.askstring("Remove Last Page", "Do you want to remove the last page of each CBZ? (yes/no)").lower() == 'yes'

# Merge CBZ files
merge_cbz(cbz_paths, output_cbz_path, remove_last_page)

print(f"Merged CBZ saved as {output_cbz_path}")

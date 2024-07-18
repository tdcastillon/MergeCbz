import zipfile
import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import tempfile

def extract_cbz(cbz_path, extract_to):
    try:
        with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except PermissionError as e:
        messagebox.showerror("Permission Error", f"Failed to extract {cbz_path}: {str(e)}")

def create_cbz(folder_path, cbz_path):
    try:
        with zipfile.ZipFile(cbz_path, 'w') as zip_ref:
            for root, _, files in os.walk(folder_path):
                for file in sorted(files):  # Sorting files to maintain order
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zip_ref.write(file_path, arcname)
    except PermissionError as e:
        messagebox.showerror("Permission Error", f"Failed to create {cbz_path}: {str(e)}")

def merge_cbz(cbz_paths, output_cbz_path):
    temp_dirs = []
    try:
        merged_dir = tempfile.mkdtemp()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create merged directory: {str(e)}")
        return

    page = 0

    try:
        # Extract all CBZ files and optionally remove the last page
        for i, cbz_path in enumerate(cbz_paths):
            try:
                temp_dir = tempfile.mkdtemp()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create temp directory: {str(e)}")
                continue
            
            temp_dirs.append(temp_dir)
            extract_cbz(cbz_path, temp_dir)
            
            # Remove all non-image files
            for file in os.listdir(temp_dir):
                if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                    try:
                        os.remove(os.path.join(temp_dir, file))
                    except PermissionError as e:
                        pass  # Ignore errors when removing files

            # Rename files to avoid conflicts and move to merged directory
            for file in sorted(os.listdir(temp_dir)):
                page += 1
                try:
                    shutil.move(os.path.join(temp_dir, file), os.path.join(merged_dir, f"{page}.jpg"))
                except PermissionError as e:
                    pass  # Ignore errors when moving files

        # Create the merged CBZ
        create_cbz(merged_dir, output_cbz_path)

        # Cleanup temporary directories
        for temp_dir in temp_dirs:
            try:
                shutil.rmtree(temp_dir)
            except PermissionError as e:
                messagebox.showerror("Permission Error", f"Failed to remove temp directory {temp_dir}: {str(e)}")
        try:
            shutil.rmtree(merged_dir)
        except PermissionError as e:
            pass  # Ignore errors when removing merged directory

        messagebox.showinfo("Success", f"Merged CBZ saved as:\n{output_cbz_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        # Cleanup in case of error
        for temp_dir in temp_dirs:
            shutil.rmtree(temp_dir)
        shutil.rmtree(merged_dir)

def select_cbz_files():
    return filedialog.askopenfilenames(title="Select CBZ files to merge", filetypes=[("CBZ files", "*.cbz")])

def select_output_path():
    return filedialog.asksaveasfilename(title="Save merged CBZ as", defaultextension=".cbz", filetypes=[("CBZ files", "*.cbz")])

def merge_cbz_gui():
    def on_select_cbz_files():
        nonlocal cbz_paths
        cbz_paths = select_cbz_files()
        if cbz_paths:
            cbz_files_label.config(text=f"Selected {len(cbz_paths)} CBZ files.")
        else:
            cbz_files_label.config(text="No CBZ files selected.")

    def on_select_output_path():
        nonlocal output_cbz_path
        output_cbz_path = select_output_path()
        if output_cbz_path:
            output_path_label.config(text=f"Output CBZ: {output_cbz_path}")
        else:
            output_path_label.config(text="No output path selected.")

    def on_merge():
        if not cbz_paths:
            messagebox.showwarning("Warning", "No CBZ files selected.")
            return
        if not output_cbz_path:
            messagebox.showwarning("Warning", "No output CBZ file specified.")
            return
        merge_cbz(cbz_paths, output_cbz_path)

    # Create GUI
    root = tk.Tk()
    root.title("CBZ Merger")

    cbz_paths = []
    output_cbz_path = ""

    # Buttons and labels
    select_cbz_button = tk.Button(root, text="Select CBZ Files", command=on_select_cbz_files)
    select_cbz_button.pack(pady=10)

    cbz_files_label = tk.Label(root, text="No CBZ files selected.")
    cbz_files_label.pack(pady=5)

    select_output_button = tk.Button(root, text="Select Output Path", command=on_select_output_path)
    select_output_button.pack(pady=10)

    output_path_label = tk.Label(root, text="No output path selected.")
    output_path_label.pack(pady=5)

    merge_button = tk.Button(root, text="Merge CBZ Files", command=on_merge)
    merge_button.pack(pady=20)

    root.mainloop()

# Run the GUI
merge_cbz_gui()

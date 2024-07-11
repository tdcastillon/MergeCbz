# CBZ File Merger

This Python script allows you to merge multiple CBZ (Comic Book Zip) files into a single CBZ file. Optionally, you can remove the last page of each CBZ before merging.

## Features

- Merge multiple CBZ files into one.
- Optionally remove the last page of each CBZ before merging.
- User-friendly GUI for file selection and options.

## Requirements

- Python 3.x
- tkinter (usually included in standard Python distributions)
- No additional Python packages are required.

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/mergeCbz.git
   cd mergeCbz
   ```

2. **Run the script:**

   ```bash
   python mergeCbz.py
   ```

3. **Instructions:**

   - A GUI window will open asking you to select multiple CBZ files to merge.
   - After selecting files, a prompt will ask if you want to remove the last page of each CBZ file.
   - Finally, select where to save the merged CBZ file.

4. **Output:**

   - The merged CBZ file will be saved in the location you specified.

## Notes

- Ensure that all CBZ files you select are valid and contain images.
- The script creates temporary directories (`temp_cbz_1`, `temp_cbz_2`, etc.) during the process, which are deleted after merging.

## Example

Here's a simple example of using the script:

1. Select CBZ files `comic1.cbz` and `comic2.cbz`.
2. Choose to remove the last page of each CBZ. (useful when there is the scanlator's note or blank page at the end)
3. Save the merged CBZ file as `merged_comics.cbz`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- [Thibault CASTILLON](@tdcastillon)
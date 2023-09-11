import os
import shutil
from tkinter import filedialog
import tkinter as tk
import exiftool

basedir = os.path.dirname(__file__)
img_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.dng')
video_formats = ('.mp4', '.avi', '.mkv', '.mov')

IMAGE_TYPE = "Images"
VIDEO_TYPE = "Videos"
UNKNOWN = "Unknown"

HORIZONTAL_ORIENTATION = "Horizontal"
VERTICAL_ORIENTATION = "Vertical"
SQUARE_ORIENTATION = "Square"

MSG_TIME = 3000

def write_image_info_to_txt(output_folder, images_info):
    txt_file_path = os.path.join(output_folder, "images_info.txt")
    with open(txt_file_path, 'w') as txt_file:
        for info in images_info:
            txt_file.write(f"== File Name: {info['file_name']}\n")
            txt_file.write(f"\tOrientation: {info['file_orientation']}\n")
            txt_file.write(f"\tSize: {info['file_size']}\n")
            txt_file.write(f"\tGPS Position: {info['file_GPSPosition']}\n")
            txt_file.write("\n")

def get_media_orientation(media_path):
    _, file_ext = os.path.splitext(media_path)
    with exiftool.ExifToolHelper() as et:
        try:
            metadata = et.get_metadata(media_path)[0]
            orientation = metadata['EXIF:Orientation'] if file_ext.lower() in img_formats else metadata['Composite:Rotation']
        
            if orientation == 1 or orientation == 0:
                orientation = HORIZONTAL_ORIENTATION
            elif orientation == 8 or orientation == 270:
                orientation = VERTICAL_ORIENTATION
            else:
                orientation = SQUARE_ORIENTATION
            return (orientation, metadata)
        except:
            return (UNKNOWN, metadata)
        
def get_media_type(media_path):
    _, file_ext = os.path.splitext(media_path)

    if file_ext.lower() in img_formats:
        return IMAGE_TYPE
    elif file_ext.lower() in video_formats:
        return VIDEO_TYPE
    else:
        return UNKNOWN

def sort_by_orientation():
    try:
        show_msg_label("Sorting by orientation...", False, "blue")
        # root.withdraw()  # Hide the main window
        folder_selected = filedialog.askdirectory(title="Select a folder containing media files")

        if not folder_selected:
            show_msg_label("No folder selected.", True, "red")
            return

        # Define output folders
        horizontal_folder = os.path.join(folder_selected, HORIZONTAL_ORIENTATION)
        vertical_folder = os.path.join(folder_selected, VERTICAL_ORIENTATION)
        unknown_folder = os.path.join(folder_selected, UNKNOWN)

        # Create output folders if they don't exist
        os.makedirs(horizontal_folder, exist_ok=True)
        os.makedirs(vertical_folder, exist_ok=True)
        os.makedirs(unknown_folder, exist_ok=True)

        # List all files in the selected folder
        files = os.listdir(folder_selected)
        images_info = []
        for file in files:
            file_path = os.path.join(folder_selected, file)
            if os.path.isfile(file_path):
                orientation, metadata = get_media_orientation(file_path)
                if orientation == HORIZONTAL_ORIENTATION:
                    destination_folder = horizontal_folder
                elif orientation == VERTICAL_ORIENTATION:
                    destination_folder = vertical_folder
                else:
                    destination_folder = unknown_folder

                images_info.append({
                    'file_name': metadata.get('File:FileName', 'none'),
                    'file_orientation': orientation,
                    'file_size': metadata.get('Composite:ImageSize', 'none'),
                    'file_GPSPosition': metadata.get('Composite:GPSPosition', 'none'),
                })

                # Move the file to the appropriate folder
                shutil.move(file_path, os.path.join(destination_folder, file))

        show_msg_label("Media files sorted by orientation.", True, "green")
        write_image_info_to_txt(folder_selected, images_info)
    except Exception as e:
        print(e)
        show_msg_label(f"Error:{e}", False, "red")

def sort_by_type():
    try:
        show_msg_label("Sorting by type...", False, "blue")
        folder_selected = filedialog.askdirectory(title="Select a folder containing media files")
        if not folder_selected:
            show_msg_label("No folder selected.", True, "red")
            return

        # Define output folders
        images_folder = os.path.join(folder_selected, IMAGE_TYPE)
        videos_folder = os.path.join(folder_selected, VIDEO_TYPE)
        unknown_folder = os.path.join(folder_selected, UNKNOWN)

        # Create output folders if they don't exist
        os.makedirs(images_folder, exist_ok=True)
        os.makedirs(videos_folder, exist_ok=True)
        os.makedirs(unknown_folder, exist_ok=True)

        # List all files in the selected folder
        files = os.listdir(folder_selected)
        for file in files:
            file_path = os.path.join(folder_selected, file)
            if os.path.isfile(file_path):
                type = get_media_type(file_path)
                if type == IMAGE_TYPE:
                    destination_folder = images_folder
                elif type == VIDEO_TYPE:
                    destination_folder = videos_folder
                else:
                    destination_folder = unknown_folder

                # Move the file to the appropriate folder
                shutil.move(file_path, os.path.join(destination_folder, file))

        show_msg_label("Media files sorted by type.", True, "green")
    except Exception as e:
        print(e)
        show_msg_label(f"Error:{e}", False, "red")

def show_msg_label(text, timed, color):
    msg_label.config(text = text, foreground=color)
    if timed:
        root.after(MSG_TIME, reset_msg_label)

def reset_msg_label():
    msg_label.config(text="", foreground="black")

# Create a GUI window to select the folder
root = tk.Tk()
root.title('Media Toolkit')
root.geometry("250x150")
root.iconbitmap(os.path.join(basedir, "SortMedia2.ico"))


frame = tk.Frame(root, bg="white")
frame.pack(fill=tk.BOTH, expand=True)

sort_by_orientation_btn = tk.Button(frame, text="Sort by orientation", command=sort_by_orientation, bg="white", relief=tk.GROOVE)
sort_by_type_btn = tk.Button(frame, text="Sort by type", command=sort_by_type, bg="white", relief=tk.GROOVE)

sort_by_orientation_btn.pack(fill=tk.BOTH, expand=True, padx=10, pady=7)
sort_by_type_btn.pack(fill=tk.BOTH, expand=True, padx=10, pady=7)

msg_label = tk.Label(frame, text="")
msg_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=7)

root.mainloop()
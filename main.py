import os
from datetime import datetime
import re
from media_exif_handler import MediaExifHandler

count = 1100
default_output_path = './output'
def get_subfolder_names(directory):
    # Liste aller Unterordner ohne den Root-Pfad
    subfolder_names = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    return subfolder_names


def get_coordinates(files, dir_path):

    pattern = r'^reference\.(png|jpeg|jpg|heic|mp4|mov|txt)$'
    reference = [os.path.join(dir_path, file) for file in files if re.match(pattern, file, re.IGNORECASE)]
    if len(reference) < 1:
        raise ValueError("There is no reference file in the folder.")
    elif len(reference) > 1:
        raise ValueError("There are to many reference files in the folder.")
    if reference[0].lower().endswith('.txt'):
        metadata = []
    else:
        metadata = MediaExifHandler.get_metadata(reference[0])
        print(metadata)

    return metadata["GPSCoordinates"]

def get_date_object(file_metadata):
    return datetime.strptime(file_metadata['CreateDate'], "%Y:%m:%d %H:%M:%S")

def get_new_filename(file):
    global count

    file_metadata = MediaExifHandler.get_metadata(file)
    _, file_extension = os.path.splitext(file)
    date = get_date_object(file_metadata).strftime("%Y_%m_%d")

    if file_metadata['Model']:
        model = (file_metadata['Model']).replace(' ', '-')
    else:
        model = 'No-Device-Info'
    print(date)
    new_filename = date + "_" + model + "_" + str(count).zfill(6) + file_extension

    count += 1

    return new_filename
def get_output_path(file):
    file_metadata = MediaExifHandler.get_metadata(file)
    location = 'Thailand'
    date = get_date_object(file_metadata).strftime("%Y")
    path = os.path.join(default_output_path, location, date)
    path += '/'
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)  # Creates the directory (and parent directories if needed)
        print(f"Created directory: {path}")
    return path


print(get_coordinates(os.listdir('./input/test'), './input/test'))
source_folder = './input'
subfolders = get_subfolder_names(source_folder)

for subfolder in subfolders:
    # Liste aller Dateien im Unterordner
    files = os.listdir(os.path.join(source_folder, subfolder))
    print(files)
    for file in files:
        file = os.path.join(source_folder, subfolder, file)
        if os.path.isfile(file):
            #TODO
            #MediaExifHandler.set_gps_coordinates(file, 10.5, 10, 10)
            get_new_filename(file)
            get_output_path(file)
            os.rename(file, (get_output_path(file) + get_new_filename(file)))







# Beispiel: Ersetze 'x' durch den Pfad deines Ordners

'''print(subfolders_list)
print(os.path.join(source_folder, subfolders_list[0]))
subfolder = os.path.join(source_folder, subfolders_list[0])
files = os.listdir('./input/test')
print(files)
files = [f for f in files if os.path.isfile(os.path.join(subfolder, f))]
print(files)
'''
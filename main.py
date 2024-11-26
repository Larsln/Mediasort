import os
from datetime import datetime
import re
from media_exif_handler import MediaExifHandler
from locator import Locator

count = 11002312
default_input_path = r'D:\Bilder\KohTao_test'
default_output_path = r'D:\Bilder\Test_output'
locator = Locator()


def get_coordinates(files, dir_path):
    pattern = r'^reference\.(png|jpeg|jpg|heic|mp4|mov|txt)$'
    reference = [os.path.join(dir_path, file) for file in files if re.match(pattern, file, re.IGNORECASE)]
    if len(reference) < 1:
        raise ValueError("There is no reference file in the folder.")
    elif len(reference) > 1:
        raise ValueError("There are to many reference files in the folder.")
    if reference[0].lower().endswith('.txt'):
        with open(reference[0], "r") as file:
            line = file.readline().strip()  # Nur die erste Zeile lesen und Leerzeichen entfernen

        values = line.split(", ")
        numbers = [float(value) for value in values]
        if len(numbers) < 2 or len(numbers) > 3:
            raise ValueError("There are no Coordinates found in the .txt file")
        if len(numbers) == 2:
            numbers.append(float(0))

        metadata = tuple(numbers)
    else:
        metadata = MediaExifHandler.get_metadata(reference[0])["GPSCoordinates"]

    return metadata


def get_date_object(file_metadata, format):
    return datetime.strptime(file_metadata['CreateDate'], "%Y:%m:%d %H:%M:%S")


def get_new_filename(file):
    global count

    file_metadata = MediaExifHandler.get_metadata(file)
    _, file_extension = os.path.splitext(file)
    date = file_metadata['CreateDate'].strftime("%Y_%m_%d")

    if file_metadata['Model']:
        model = (file_metadata['Model']).replace(' ', '-')
    else:
        model = 'No-Device-Info'
    new_filename = date + "_" + model + "_" + str(count).zfill(6) + file_extension.lower()

    count += 1

    return new_filename


def get_output_path(file):
    file_metadata = MediaExifHandler.get_metadata(file)
    country = locator.get_country_name((file_metadata['GPSCoordinates'][0], file_metadata['GPSCoordinates'][1]))
    city = locator.get_city_name((file_metadata['GPSCoordinates'][0], file_metadata['GPSCoordinates'][1]))
    date = file_metadata['CreateDate'].strftime("%Y")
    path = os.path.join(default_output_path, country, date, city)
    path = path.replace(" ", "_") + "/"
    if not os.path.exists(path):
        os.makedirs(path)  # Creates the directory (and parent directories if needed)
        print(f"Created directory: {path}")
    return path


def get_subfolder_names(directory):
    try:
        # Gibt eine Liste aller Unterordner im Verzeichnis zurück
        return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    except FileNotFoundError:
        return []  # Rückgabe einer leeren Liste, falls der Ordner nicht existiert


def folder_crawler(source_folder):
    # Verarbeite alle Dateien im aktuellen Ordner (source_folder)

    files = os.listdir(source_folder)
    for file in files:
        file_path = os.path.join(source_folder, file)
        if os.path.isfile(file_path) and file_path.lower().endswith(MediaExifHandler.supported_photo_files +
                                                                    MediaExifHandler.supported_video_files):
            reference = get_coordinates(files, source_folder)
            if MediaExifHandler.check_coordinates(file_path):
                MediaExifHandler.set_gps_coordinates(file_path, reference[0], reference[1], reference[2])

            else:
                MediaExifHandler.set_gps_coordinates(file_path, reference[0], reference[1], reference[2])

            os.rename(file_path, (get_output_path(file_path) + get_new_filename(file_path)))

    # Rekursion: Verarbeite alle Subfolder
    subfolders = get_subfolder_names(source_folder)
    for subfolder in subfolders:
        subfolder_path = os.path.join(source_folder, subfolder)
        print(f"Entering folder: {subfolder_path}")
        folder_crawler(subfolder_path)


folder_crawler(default_input_path)

import os
from datetime import datetime
import re

from media_metadata import MediaMetadata
from media_exif_handler import MediaExifHandler
from locator import Locator
from metadata import Metadata
from static_data_loader import StaticDataLoader


def get_coordinates(reference_object: Metadata):
    files = os.listdir(reference_object.source_folder_path)
    pattern = r'^reference\.(png|jpeg|jpg|heic|mp4|mov|txt)$'
    reference_files = [file for file in files if re.match(pattern, file, re.IGNORECASE)]
    if len(reference_files) < 1:
        return False
        raise ValueError("There is no reference file in the folder.")
    elif len(reference_files) > 1:
        return False
        raise ValueError("There are to many reference files in the folder.")
    reference_object.file_path = reference_files[0]
    if reference_object.file_path.lower().endswith('.txt'):
        with open(reference_object.get_full_file_path(), "r") as file:
            line = file.readline().strip()  # Nur die erste Zeile lesen und Leerzeichen entfernen

        values = line.split(", ")
        numbers = [float(value) for value in values]
        if len(numbers) < 2 or len(numbers) > 3:
            raise ValueError("There are no Coordinates found in the .txt file")
        if len(numbers) == 2:
            numbers.append(float(0))

        reference_object.gps_coordinates = tuple(numbers)
    else:
        reference_object.set_metadata()

    reference_object.check_is_video()


def get_new_filename(media_metadata):
    _, file_extension = os.path.splitext(media_metadata.file_path)
    date = media_metadata.get_create_date("%Y_%m_%d")

    if media_metadata.model:
        model = media_metadata.model.replace(' ', '-')
    else:
        model = 'No-Model'
    new_filename = date + "_" + model + "_" + str(static_data_loader.load_counter()).zfill(8) + file_extension.lower()

    return new_filename


def get_output_path(media_metadata):
    locator = Locator()
    country = locator.get_country_name(
        (media_metadata.get_gps_coordinates()[0], media_metadata.get_gps_coordinates()[1]))
    city = locator.get_city_name((media_metadata.get_gps_coordinates()[0], media_metadata.get_gps_coordinates()[1]))
    date = media_metadata.get_create_date("%Y")
    path = os.path.join(static_data_loader.output_path, country, date, city)
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


def move_file(media_metadata):
    os.rename(media_metadata.get_full_file_path(), (get_output_path(media_metadata) + get_new_filename(media_metadata)))
    static_data_loader.increase_counter()


def sort_files(media_metadata, reference):
    get_coordinates(reference)
    if media_metadata.check_coordinates():
        move_file(media_metadata)
    else:
        if not static_data_loader.only_sort and reference:

            if media_metadata.set_reference(reference):
                MediaExifHandler.set_gps_coordinates(media_metadata)
                move_file(media_metadata)


def check_only_reference_txt(directory):
    files = os.listdir(directory)
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    return len(files) == 1 and files[0].lower() == 'reference.txt'


def folder_crawler(source_folder, function_used):
    files = os.listdir(source_folder)
    reference = Metadata()
    reference.source_folder_path = source_folder
    for file in files:
        media_metadata = MediaMetadata(file, source_folder)

        if os.path.isfile(media_metadata.get_full_file_path()) and media_metadata.file_path.lower().endswith(
                MediaExifHandler.SUPPORTED_PHOTO_FILES +
                MediaExifHandler.SUPPORTED_VIDEO_FILES):
            media_metadata.set_metadata()
            function_used(media_metadata, reference)

    # Rekursion: Verarbeite alle Subfolder
    subfolders = get_subfolder_names(source_folder)
    for subfolder in subfolders:
        subfolder_path = os.path.join(source_folder, subfolder)
        folder_crawler(subfolder_path, function_used)
        try:
            os.rmdir(subfolder_path)
        except OSError:
            if check_only_reference_txt(subfolder_path):
                os.remove(os.path.join(subfolder_path, 'reference.txt'))
                os.rmdir(subfolder_path)


static_data_loader = StaticDataLoader()
folder_crawler(static_data_loader.input_path, sort_files)

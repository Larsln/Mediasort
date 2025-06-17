import os
import re
import shutil

from media_exif_handler import MediaExifHandler
from locator import Locator
from metadata import Metadata
from static_data_loader import StaticDataLoader


class Sorter:

    def __init__(self, static_data_loader):
        self.static_data_loader = StaticDataLoader()

    def sort_files(self, media_metadata, reference):
        self.get_coordinates(reference)
        if media_metadata.check_coordinates():
            self.move_file(media_metadata)
        else:
            if not self.static_data_loader.only_sort and reference:

                if media_metadata.set_reference(reference):
                    MediaExifHandler.set_gps_coordinates(media_metadata)
                    self.move_file(media_metadata)
        if media_metadata.live_photo is None:
            self.static_data_loader.increase_counter()

    def move_file(self, media_metadata):
        shutil.move(media_metadata.get_full_file_path(),
                  (self.get_output_path(media_metadata) + self.get_new_filename(media_metadata)))

    def get_output_path(self, media_metadata):
        locator = Locator()
        country = locator.get_country_name(
            (media_metadata.get_gps_coordinates()[0], media_metadata.get_gps_coordinates()[1]))
        city = locator.get_city_name((media_metadata.get_gps_coordinates()[0], media_metadata.get_gps_coordinates()[1]))
        date = media_metadata.get_create_date("%Y")
        path = os.path.join(self.static_data_loader.output_path, country, date, city)
        path = path.replace(" ", "_") + "/"
        if not os.path.exists(path):
            os.makedirs(path)  # Creates the directory (and parent directories if needed)
            print(f"Created directory: {path}")
        return path

    def get_new_filename(self, media_metadata):
        _, file_extension = os.path.splitext(media_metadata.file_path)
        date = media_metadata.get_create_date("%Y_%m_%d")

        if media_metadata.model:
            model = media_metadata.model.replace(' ', '-')
        else:
            model = 'No-Model'
        new_filename = date + "_" + model + "_" + str(self.static_data_loader.load_counter()).zfill(
            8) + file_extension.lower()

        return new_filename

    @staticmethod
    def get_coordinates(reference_object: Metadata):
        files = os.listdir(reference_object.source_folder_path)
        pattern = r'^reference\.(png|jpeg|jpg|heic|dng|mp4|mov|txt)$'
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

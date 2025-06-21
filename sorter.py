import os
import re
import shutil
from logger_config import logger
from media_exif_handler import MediaExifHandler
from locator import Locator
from metadata import Metadata
from static_data_loader import StaticDataLoader


class Sorter:

    def __init__(self, static_data_loader: StaticDataLoader):
        self.static_data_loader = static_data_loader

    def sort_files(self, media_metadata):
        if media_metadata.check_coordinates():
            self.move_file(media_metadata)
        else:
            if not self.static_data_loader.only_sort and media_metadata.reference:
                    media_metadata.set_embedded_metadata()
                    if media_metadata.check_coordinates():
                        self.move_file(media_metadata)
                    else:
                        raise ValueError(
                            f"File {media_metadata.file_path} has no GPS coordinates and cannot be sorted.")
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
        date = media_metadata.get_create_date('%Y')
        path = os.path.join(self.static_data_loader.output_path, country, date, city)
        path = path.replace(' ', '_') + '/'
        if not os.path.exists(path):
            os.makedirs(path)  # Creates the directory (and parent directories if needed)
            logger.info(f'Created directory: {path}')
            logger.info(f'Moving file to: {path}')
        return path

    def get_new_filename(self, media_metadata):
        _, file_extension = os.path.splitext(media_metadata.file_path)
        date = media_metadata.get_create_date('%Y_%m_%d')

        if media_metadata.model:
            model = media_metadata.model.replace(' ', '-')
        else:
            model = 'No-Model'

        if media_metadata.make:
            make = media_metadata.make.replace(' ', '-')
        else:
            make = 'No-Make'
        live = ''
        if media_metadata.live_photo:
            live = '_Live-Photo'
        new_filename = date + '_' + make + '_' + model + live + '_' + str(self.static_data_loader.load_counter()).zfill(
            8) + file_extension.lower()

        return new_filename





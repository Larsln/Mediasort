from dataclasses import dataclass
from datetime import datetime
from metadata import Metadata
from media_exif_handler import MediaExifHandler
import os
import re

@dataclass
class MediaMetadata(Metadata):
    make: str = None
    model: str = None
    create_date: datetime = None
    reference: Metadata = None

    def __init__(self, file_path, source_folder_path, reference, matching_file=None):
        self.file_path = file_path
        self.source_folder_path = source_folder_path
        self.reference = reference
        if matching_file is not None:
            self.live_photo = matching_file
        self.video = self.check_is_video()

    def __str__(self):
        current_attrs = ", ".join(f"{k}={v}" for k, v in vars(self).items())
        return f"{super().__str__()}, MediaMetadata: {current_attrs}"

    def set_metadata(self):
        data = MediaExifHandler.get_metadata(self)
        self.gps_coordinates = data["GPSCoordinates"]
        self.make = data["Make"]
        self.model = data["Model"]
        self.create_date = data["CreateDate"]

    def set_embedded_metadata(self):
        gps = False
        make = False
        if not self.gps_coordinates and self.reference.gps_coordinates:
            self.gps_coordinates = self.reference.gps_coordinates
            gps = True
        if (self.make == '' or self.make is None) and 'hero' in self.model.lower():
            self.make = 'GoPro'
            make = True
        if make == True or gps == True:
            MediaExifHandler.set_exif_tags(self, gps, make)

    def get_create_date(self, date_format):
        return self.create_date.strftime(date_format)

    def get_coordinates(self):
        files = os.listdir(self.reference.source_folder_path)
        pattern = r'^reference\.(png|jpeg|jpg|heic|dng|mp4|mov|txt)$'
        reference_files = [file for file in files if re.match(pattern, file, re.IGNORECASE)]
        if len(reference_files) < 1:
            return False
            raise ValueError('There is no reference file in the folder.')
        elif len(reference_files) > 1:
            return False
            raise ValueError('There are to many reference files in the folder.')
        self.reference.file_path = reference_files[0]
        if self.reference.file_path.lower().endswith('.txt'):
            with open(self.reference.get_full_file_path(), 'r') as file:
                line = file.readline().strip()  # Nur die erste Zeile lesen und Leerzeichen entfernen

            values = line.split(', ')
            numbers = [float(value) for value in values]
            if len(numbers) < 2 or len(numbers) > 3:
                raise ValueError('There are no Coordinates found in the .txt file')
            if len(numbers) == 2:
                numbers.append(float(0))

            self.reference.gps_coordinates = tuple(numbers)
        else:
            self.reference.set_metadata()
            self.reference.check_is_video()

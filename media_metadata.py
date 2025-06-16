from dataclasses import dataclass
from datetime import datetime
from metadata import Metadata
from media_exif_handler import MediaExifHandler


@dataclass
class MediaMetadata(Metadata):
    make: str = None
    model: str = None
    create_date: datetime = None

    def __init__(self, file_path, source_folder_path):
        self.file_path = file_path
        self.source_folder_path = source_folder_path
        self.is_video = self.check_is_video()

    def __str__(self):
        current_attrs = ", ".join(f"{k}={v}" for k, v in vars(self).items())
        return f"{super().__str__()}, MediaMetadata: {current_attrs}"

    def set_metadata(self):
        print(self)
        data = MediaExifHandler.get_metadata(self)
        self.gps_coordinates = data["GPSCoordinates"]
        self.make = data["Make"]
        self.model = data["Model"]
        self.create_date = data["CreateDate"]

    def get_make(self):
        if self.make:
            return self.make
        else:
            return ""

    def get_model(self):
        if self.model:
            return self.model
        else:
            return ""

    def get_create_date(self, date_format):
        if self.create_date:
            return self.create_date.strftime(date_format)
        else:
            return ""

    def set_reference(self, reference):
        if reference.gps_coordinates:
            self.gps_coordinates = reference.gps_coordinates
            return True
        else:
            return False

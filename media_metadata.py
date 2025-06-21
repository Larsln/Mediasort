from dataclasses import dataclass
from datetime import datetime
from metadata import Metadata
from media_exif_handler import MediaExifHandler


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
        if not self.gps_coordinates and self.reference:
            pass

    def get_create_date(self, date_format):
        return self.create_date.strftime(date_format)

    def set_reference(self, reference):
        if reference.gps_coordinates:
            self.gps_coordinates = reference.gps_coordinates
        else:
            raise TypeError("Reference does not have GPS coordinates.")

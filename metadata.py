import os
from media_exif_handler import MediaExifHandler


class Metadata:
    file_path: str | None = None
    source_folder_path: str | None = None
    gps_coordinates: list | None = None
    live_photo: str | None = None
    video: bool | None = None

    def __str__(self):
        base_attrs = ", ".join(f"{k}={v}" for k, v in vars(self).items())
        return f"Metadata: {base_attrs}"

    def check_is_video(self):
        if self.file_path.lower().endswith(MediaExifHandler.SUPPORTED_VIDEO_FILES):
            return True

        elif self.file_path.lower().endswith(MediaExifHandler.SUPPORTED_PHOTO_FILES):
            return False
        else:
            raise TypeError("The file is not a supported file. [jpg, jpeg, png, heic, mp4, mov]")

    def get_gps_coordinates(self):
        if self.gps_coordinates:
            return self.gps_coordinates
        else:
            return []

    def get_gps_coordinates_as_string(self):
        if self.gps_coordinates:
            return f"{self.gps_coordinates[0]} {self.gps_coordinates[1]} {self.gps_coordinates[2]}"
        else:
            return ""

    def set_metadata(self):
        data = MediaExifHandler.get_metadata(self)
        self.gps_coordinates = data["GPSCoordinates"]

    def check_coordinates(self):
        if len(self.gps_coordinates) < 2:
            return False
        else:
            return True

    def get_full_file_path(self):
        if self.file_path and self.source_folder_path:
            return os.path.join(self.source_folder_path, self.file_path)
        else:
            return False

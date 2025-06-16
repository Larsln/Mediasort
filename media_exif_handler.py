import re
from datetime import datetime

import exiftool

from coordinates_calculation import CoordinatesCalculation


class MediaExifHandler:
    SUPPORTED_PHOTO_FILES = ('.jpg', '.jpeg', '.png', '.heic', '.dng')
    SUPPORTED_VIDEO_FILES = ('.mp4', '.mov')

    @staticmethod
    def __extract_metadata(media_metadata):
        with exiftool.ExifTool(encoding='utf-8') as et:
            metadata = et.execute_json('-ExtractEmbedded', media_metadata.get_full_file_path())
            return metadata[0]

    @staticmethod
    def set_gps_coordinates(media_metadata):

        with exiftool.ExifTool() as et:
            try:

                if media_metadata.video:

                    command = [

                        f'-Keys:GPSCoordinates={media_metadata.get_gps_coordinates()[0]}'
                        f'{media_metadata.get_gps_coordinates()[1]} {media_metadata.get_gps_coordinates()[2]}',
                        '-overwrite_original',
                        media_metadata.get_full_file_path
                    ]
                else:

                    latitude_dd_with_car_dir, latitude_car_dir = CoordinatesCalculation.dd_to_dd_with_car_dir(
                        media_metadata.get_gps_coordinates()[0], ["S", "N"])
                    longitude_dd_with_car_dir, longitude_car_dir = CoordinatesCalculation.dd_to_dd_with_car_dir(
                        media_metadata.get_gps_coordinates()[1], ["W", "E"])
                    altitude_dd_with_car_dir, altitude_car_dir = CoordinatesCalculation.dd_to_dd_with_car_dir(
                        media_metadata.get_gps_coordinates()[2], ["1", "0"])

                    command = [

                        f'-EXIF:GPSLatitude={latitude_dd_with_car_dir}',
                        f'-EXIF:GPSLatitudeRef={latitude_car_dir}',
                        f'-EXIF:GPSLongitude={longitude_dd_with_car_dir}',
                        f'-EXIF:GPSLongitudeRef={longitude_car_dir}',
                        f'-EXIF:GPSAltitude={altitude_dd_with_car_dir}',
                        f'-EXIF:GPSAltitudeRef={altitude_car_dir}',
                        '-overwrite_original',
                        media_metadata.get_full_file_path()
                    ]
                et.execute(*command)

                print("GPS coordinates successfully set!")

            except Exception as e:
                print(f"An error occurred: {e}")


    @staticmethod
    def get_metadata(media_metadata):
        metadata = MediaExifHandler.__extract_metadata(media_metadata)
        data = {"GPSCoordinates": list,
                "Make": str,
                "Model": str,
                "CreateDate": str}
        if media_metadata.video:
            try:
                if "QuickTime:GPSCoordinates" in metadata:
                    data["GPSCoordinates"] = [float(value) for value in metadata["QuickTime:GPSCoordinates"].split()]
                elif "QuickTime:LocationInformation" in metadata:
                    pattern = r"Lat=([-+]?[0-9]*\.?[0-9]+)\s+Lon=([-+]?[0-9]*\.?[0-9]+)\s+Alt=([-+]?[0-9]*\.?[0-9]+)"
                    match = re.search(pattern, metadata["QuickTime:LocationInformation"])
                    data["GPSCoordinates"] = [float(match.group(1)), float(match.group(2)),
                                              float(match.group(3))] if match else []
                else:
                    data["GPSCoordinates"] = []
            except KeyError:
                data["GPSCoordinates"] = []
            data["Make"] = metadata.get("QuickTime:Make", "")
            data["Model"] = metadata.get("QuickTime:Model", "")
            raw_date = metadata.get("QuickTime:CreateDate", "")
            if not raw_date or raw_date == "0000:00:00 00:00:00":
                raw_date = metadata.get("File:FileModifyDate", "")
                data["CreateDate"] = MediaExifHandler.get_date_object(raw_date, "%Y:%m:%d %H:%M:%S%z")
            else:
                data["CreateDate"] = MediaExifHandler.get_date_object(raw_date, "%Y:%m:%d %H:%M:%S")

        else:
            try:
                data["GPSCoordinates"] = [CoordinatesCalculation.dd_with_car_dir_to_dd(metadata["EXIF:GPSLatitude"],
                                                                                       metadata[
                                                                                           "EXIF:GPSLatitudeRef"]),
                                          CoordinatesCalculation.dd_with_car_dir_to_dd(metadata["EXIF:GPSLongitude"],
                                                                                       metadata[
                                                                                           "EXIF:GPSLongitudeRef"])]
                try:
                    data["GPSCoordinates"].append(
                        CoordinatesCalculation.dd_with_car_dir_to_dd(metadata["EXIF:GPSAltitude"],
                                                                     metadata["EXIF:GPSAltitudeRef"]))
                except KeyError:
                    pass
            except KeyError:
                data["GPSCoordinates"] = []
            print(metadata)
            data["Make"] = metadata.get("EXIF:Make", "")
            data["Model"] = metadata.get("EXIF:Model", "")
            if metadata.get("EXIF:DateTimeOriginal", ""):
                raw_date = metadata["EXIF:DateTimeOriginal"]
                data["CreateDate"] = MediaExifHandler.get_date_object(raw_date, "%Y:%m:%d %H:%M:%S")

            elif metadata.get("File:FileModifyDate", ""):
                raw_date = metadata.get("File:FileModifyDate", "")
                data["CreateDate"] = MediaExifHandler.get_date_object(raw_date, "%Y:%m:%d %H:%M:%S%z")
        return data

    @staticmethod
    def get_date_object(raw_date, date_format):
        return datetime.strptime(raw_date, date_format)

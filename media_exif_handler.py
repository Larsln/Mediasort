import re
from datetime import datetime

import exiftool

from coordinates_calculation import CoordinatesCalculation


class MediaExifHandler:
    supported_photo_files = ('.jpg', '.jpeg', '.png', '.heic')
    supported_video_files = ('.mp4', '.mov')

    @staticmethod
    def check_coordinates(file_path):
        metadata = MediaExifHandler.get_metadata(file_path)
        if len(metadata['GPSCoordinates']) < 2:
            return False
        else:
            return True
    @staticmethod
    def get_date_object(raw_date, date_format):
        return datetime.strptime(raw_date, date_format)

    @staticmethod
    def __check_file_type(file_path):
        if file_path.lower().endswith(('.mp4', '.mov')):
            return True

        elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
            return False

        else:
            raise TypeError("The file is not a supported video file. [jpg, jpeg, png, heic, mp4, mov]")

    @staticmethod
    def set_gps_coordinates(file_path, latitude, longitude, altitude):

        with exiftool.ExifTool() as et:
            try:

                if MediaExifHandler.__check_file_type(file_path):

                    command = [

                        f'-Keys:GPSCoordinates={latitude} {longitude} {altitude}',
                        '-overwrite_original',
                        file_path
                    ]
                else:

                    latitude_dd_with_car_dir, latitude_car_dir = CoordinatesCalculation.dd_to_dd_with_car_dir(latitude, ["S", "N"])
                    longitude_dd_with_car_dir, longitude_car_dir = CoordinatesCalculation.dd_to_dd_with_car_dir(longitude, ["W", "E"])
                    altitude_dd_with_car_dir, altitude_car_dir = CoordinatesCalculation.dd_to_dd_with_car_dir(altitude, ["1", "0"])

                    command = [

                        f'-EXIF:GPSLatitude={latitude_dd_with_car_dir}',
                        f'-EXIF:GPSLatitudeRef={latitude_car_dir}',
                        f'-EXIF:GPSLongitude={longitude_dd_with_car_dir}',
                        f'-EXIF:GPSLongitudeRef={longitude_car_dir}',
                        f'-EXIF:GPSAltitude={altitude_dd_with_car_dir}',
                        f'-EXIF:GPSAltitudeRef={altitude_car_dir}',
                        '-overwrite_original',
                        file_path
                    ]
                et.execute(*command)

                print("GPS coordinates successfully set!")

            except Exception as e:
                print(f"An error occurred: {e}")

    @staticmethod
    def __extract_metadata(file_path):
        with exiftool.ExifTool() as et:
            metadata = et.execute_json('-ExtractEmbedded', file_path)
            return metadata[0]

    @staticmethod
    def get_metadata(file_path):
        metadata = MediaExifHandler.__extract_metadata(file_path)
        data = {"GPSCoordinates": list,
                "Make": str,
                "Model": str,
                "CreateDate": str}
        if MediaExifHandler.__check_file_type(file_path):
            try:
                if "QuickTime:GPSCoordinates" in metadata:
                    data["GPSCoordinates"] = [float(value) for value in metadata["QuickTime:GPSCoordinates"].split()]
                elif "QuickTime:LocationInformation" in metadata:
                    pattern = r"Lat=([-+]?[0-9]*\.?[0-9]+)\s+Lon=([-+]?[0-9]*\.?[0-9]+)\s+Alt=([-+]?[0-9]*\.?[0-9]+)"
                    match = re.search(pattern, metadata["QuickTime:LocationInformation"])
                    data["GPSCoordinates"] = [float(match.group(1)), float(match.group(2)), float(match.group(3))] if match else []
                else:
                    data["GPSCoordinates"] = []
            except KeyError:
                data["GPSCoordinates"] = []
            data["Make"] = metadata.get("QuickTime:Make", "")
            data["Model"] = metadata.get("QuickTime:Model", "")
            raw_date = metadata.get("QuickTime:CreateDate", "")
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

            data["Make"] = metadata.get("EXIF:Make", "")
            data["Model"] = metadata.get("EXIF:Model", "")
            raw_date = data["CreateDate"] = metadata.get("File:FileCreateDate", "")
            data["CreateDate"] = MediaExifHandler.get_date_object(raw_date, "%Y:%m:%d %H:%M:%S%z")
        return data

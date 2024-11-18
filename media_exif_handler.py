import exiftool

from coordinates_calculation import CoordinatesCalculation


class MediaExifHandler:

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
                        file_path
                    ]
                else:

                    latitude = CoordinatesCalculation.deg_to_exif_dms(latitude, ["N", "S"])
                    longitude = CoordinatesCalculation.deg_to_exif_dms(longitude, ["E", "W"])
                    altitude = CoordinatesCalculation.deg_to_exif_dms(altitude, ["0", "1"])

                    command = [

                        f'-EXIF:GPSLatitude={latitude[0]}',  # Set EXIF GPS Latitude
                        f'-EXIF:GPSLatitudeRef={latitude[1]}',  # Set EXIF GPS Latitude Reference (N or S)
                        f'-EXIF:GPSLongitude={longitude[0]}',  # Set EXIF GPS Longitude
                        f'-EXIF:GPSLongitudeRef={longitude[1]}',  # Set EXIF GPS Longitude Reference (E or W)
                        f'-EXIF:GPSAltitude={altitude[0]}',  # Set EXIF GPS Altitude
                        f'-EXIF:GPSAltitudeRef={altitude[1]}',  # Set EXIF GPS Altitude Reference (0 or 1)
                        file_path  # Specify the file to modify
                    ]
                # Execute the ExifTool command to modify the file
                et.execute(*command)

                print("GPS coordinates successfully set!")

            except Exception as e:
                print(f"An error occurred: {e}")

    @staticmethod
    def __extract_metadata(file_path):
        with exiftool.ExifTool() as et:
            # Execute ExifTool and get metadata as a dictionary
            metadata = et.execute_json(file_path)
            return metadata[0]

    @staticmethod
    def get_metadata(file_path):
        metadata = MediaExifHandler.__extract_metadata(file_path)
        #print(metadata)
        data = {"GPSCoordinates": list,
                "Make": str,
                "Model": str,
                "CreateDate": str,}
        if MediaExifHandler.__check_file_type(file_path):
            try:
                data["GPSCoordinates"] = [float(value) for value in metadata["Keys:GPSCoordinates"].split()]
            except KeyError:
                data["GPSCoordinates"] = []
            data["Make"] = metadata.get("QuickTime:Make","")
            data["Model"] = metadata.get("QuickTime:Model","")
            data["CreateDate"] = metadata.get("QuickTime:CreateDate","")

        else:
            try:
                data["GPSCoordinates"] = [CoordinatesCalculation.deg_with_car_dir_to_deg(metadata["EXIF:GPSLatitude"],metadata["EXIF:GPSLatitudeRef"]),
                                            CoordinatesCalculation.deg_with_car_dir_to_deg(metadata["EXIF:GPSLongitude"],metadata["EXIF:GPSLongitudeRef"])]
                try:
                    data["GPSCoordinates"].append(
                        CoordinatesCalculation.deg_with_car_dir_to_deg(metadata["EXIF:GPSAltitude"],
                                                                       metadata["EXIF:GPSAltitudeRef"]))
                except KeyError:
                    pass
            except KeyError:
                data["GPSCoordinates"] = []

            data["Make"] = metadata.get("EXIF:Make", "")
            data["Model"] = metadata.get("EXIF:Model","")
            data["CreateDate"] = metadata.get("EXIF:CreateDate","")

        return data

# Example usage
#file_path = "./input/img.jpg"
#latitude = 40.1881
#longitude = 19.5996
#altitude = 909.174
#lon_ref = "W"  # W for West, E for East
#lat_ref = "N"  # N for North, S for South
#print(MediaExifHandler.extract_metadata("input/test/test.mp4"))

#set_gps_coordinates_as_exif(file_path, latitude, longitude, lat_ref, lon_ref, altitude, 0)

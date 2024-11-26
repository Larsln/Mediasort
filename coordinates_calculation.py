from fractions import Fraction


class CoordinatesCalculation:

    @staticmethod
    def __dd_to_dms(decimal_coordinate, cardinal_directions):
        """
        This function converts decimal coordinates into the DMS (degrees, minutes and seconds) format.
        It also determines the cardinal direction of the coordinates.

        :param decimal_coordinate: the decimal coordinates, such as 34.0522
        :param cardinal_directions: the locations of the decimal coordinate, such as ["N", "S"] or ["E", "W"] or ["0", "1"]
        :return: degrees, minutes, seconds and compass_direction
        :rtype: int, int, float, string
        """
        if decimal_coordinate <= 0:
            compass_direction = cardinal_directions[1]
        elif decimal_coordinate > 0:
            compass_direction = cardinal_directions[0]
        else:
            compass_direction = ""
        degrees = int(abs(decimal_coordinate))
        decimal_minutes = (abs(decimal_coordinate) - degrees) * 60
        minutes = int(decimal_minutes)
        seconds = Fraction((decimal_minutes - minutes) * 60).limit_denominator(100)
        return degrees, minutes, seconds, compass_direction

    @staticmethod
    def __dms_to_exif_format(dms_degrees, dms_minutes, dms_seconds):
        """
        This function converts DMS (degrees, minutes and seconds) to values that can
        be used with the EXIF (Exchangeable Image File Format).

        :param dms_degrees: int value for degrees
        :param dms_minutes: int value for minutes
        :param dms_seconds: fractions.Fraction value for seconds
        :return: EXIF values for the provided DMS values
        :rtype: nested tuple
        """
        exif_format = (
            (dms_degrees, 1),
            (dms_minutes, 1),
            (int(dms_seconds.limit_denominator(100).numerator), int(dms_seconds.limit_denominator(100).denominator))
        )
        return exif_format

    @staticmethod
    def deg_to_exif_dms(decimal_coordinate, cardinal_directions):
        """
        This function converts decimal coordinates into the EXIF (Exchangeable Image File Format) DMS (degrees, minutes and seconds) format.
        It also determines the cardinal direction of the coordinates.

        :param decimal_coordinate: the decimal coordinates, such as 34.0522
        :param cardinal_directions: the locations of the decimal coordinate, such as ["N", "S"] or ["E", "W"] or ["0", "1"]
        :return: EXIF values for the provided DMS values
        :rtype: nested tuple
        """
        dms = CoordinatesCalculation.__dd_to_dms(decimal_coordinate, cardinal_directions)
        exif_format = CoordinatesCalculation.__dms_to_exif_format(dms[0], dms[1], dms[2])
        return exif_format, dms[3]

    @staticmethod
    def dms_to_deg(dms_degrees, dms_minutes, dms_seconds, cardinal_direction):
        """
        This function converts DMS (degrees, minutes and seconds) to decimal coordinates.

        :param dms_degrees: int value for degrees
        :param dms_minutes: int value for minutes
        :param dms_seconds: fractions.Fraction value for seconds
        :param cardinal_direction: the locations of the decimal coordinate, such as ["N", "S"] or ["E", "W"] or ["0", "1"]
        :return: decimal coordinates
        :rtype: float
        """
        decimal_coordinate = dms_degrees + dms_minutes / 60 + dms_seconds / 3600
        if cardinal_direction == "S" or cardinal_direction == "W" or cardinal_direction == "1":
            decimal_coordinate = -decimal_coordinate
        return decimal_coordinate

    @staticmethod
    def dd_with_car_dir_to_dd(decimal_coordinate, cardinal_direction):
        """
        This function converts decimal coordinates with cardinal direction into decimal coordinates.

        :param decimal_coordinate: the decimal coordinates, such as 34.0522
        :param cardinal_direction: the locations of the decimal coordinate, such as ["N", "S"] or ["E", "W"] or ["0", "1"]
        :return: decimal coordinates
        :rtype: float
        """
        if cardinal_direction == "S" or cardinal_direction == "W" or cardinal_direction == "1":
            decimal_coordinate = -decimal_coordinate
        return decimal_coordinate

    @staticmethod
    def dd_to_dd_with_car_dir(decimal_coordinate: float, cardinal_directions):

        if decimal_coordinate <= 0:
            direction = cardinal_directions[0]
            decimal_coordinate = abs(decimal_coordinate)

        elif decimal_coordinate > 0:
            direction = cardinal_directions[1]

        else:
            raise ValueError("Coordinate is not in Range")

        return decimal_coordinate, direction

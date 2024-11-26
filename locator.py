import pycountry
import reverse_geocode
import gettext


class Locator:

    def __init__(self):
        german = gettext.translation('iso3166-1', pycountry.LOCALES_DIR, languages=['de'])
        german.install()

    def get_country_name(self, decimal_coordinates):
        location_data = reverse_geocode.get(decimal_coordinates)
        return _(location_data['country'])

    def get_city_name(self, decimal_coordinates):
        location_data = reverse_geocode.get(decimal_coordinates)
        return (location_data['city'])

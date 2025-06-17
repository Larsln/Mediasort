import json
import warnings

from dotenv import load_dotenv
import os


class StaticDataLoader:
    dotenv_path = '.env'
    data_path = './data/data.json'
    only_sort: bool = False
    counter = 0
    input_path = './input'
    output_path = './output'

    def __init__(self):
        load_dotenv(self.dotenv_path)
        if os.getenv('ONLY_SORT').lower() == 'false':
            self.only_sort = False
        else:
            self.only_sort = True

    def load_data(self):
        data = {'counter': self.counter}
        try:
            with open(self.data_path, 'r') as file:
                data = json.load(file)
        except TypeError:
            raise TypeError('No data file found!')
        except FileNotFoundError:
            warnings.warn('No data file found!')
            self.write_data(data)

        return data

    def write_data(self, data):
        with open(self.data_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def load_counter(self):
        self.counter = self.load_data()['counter']
        return self.counter

    def increase_counter(self):
        counter = self.counter + 1
        self.write_data({'counter': counter})
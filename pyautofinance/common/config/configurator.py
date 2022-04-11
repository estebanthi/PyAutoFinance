import os
import yaml


class Configurator:

    def __init__(self, path='.'):
        self.path = path
        if not os.path.isdir(path):
            os.makedirs(path)

    def create_config_file(self):
        if not os.path.isfile(f"{self.path}/config.yml"):
            initial_config_data = {
                'ohlcv_pathname': None,
                'engine_results_pathname': None,
                'live_results_pathname': None,
            }

            with open(f"{self.path}/config.yml", 'w') as file:
                yaml.safe_dump(initial_config_data, file)

    def create_folders(self):
        with open(f'{self.path}/config.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)

            for field, value in config.items():
                if 'pathname' in field:
                    if value is not None:
                        pathname = f'{self.path}/{value}'
                        os.makedirs(pathname) if not os.path.isdir(pathname) else ''

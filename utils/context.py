from os import path

import yaml

from utils import data_classes as dc


class ProjectContext:

    def __init__(self):
        self.project_path = path.dirname(path.realpath(__file__))
        config_path = path.join(self.project_path, 'config.yaml')
        self.chromedriver_path = r'E:\Chromedriver.exe'

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        database = self.config['database']
        self.database_config = dc.DatabaseConfig(**database)

        parser = self.config['parsing']
        self.parsing_config = dc.ParsingConfig(**parser)

        api = self.config['api']
        self.api_config = dc.APIConfig(**api)

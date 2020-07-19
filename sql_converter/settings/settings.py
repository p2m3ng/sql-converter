import os

import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILES_PATH = os.path.join(BASE_DIR, "files")


class Config:
    def __init__(self, file="config.yaml"):
        self.file = file

    @property
    def get(self):
        if "SQL_EXPORT_DB_HOST" in os.environ.keys():
            self.dump_environment_variables()
        try:
            return self.get_file_content()
        except FileNotFoundError:
            raise FileNotFoundError(
                "Configuration file not set: check docs and fill `config.yaml` accordingly."
            )

    def get_file_content(self):
        with open(self.get_file_path()) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def dump_environment_variables(self):
        config = {
            "db": {
                "host": os.environ["SQL_EXPORT_DB_HOST"],
                "port": int(os.environ["SQL_EXPORT_DB_PORT"]),
                "user": os.environ["SQL_EXPORT_DB_USER"],
                "name": os.environ["SQL_EXPORT_DB_NAME"],
                "password": os.environ["SQL_EXPORT_DB_PASSWORD"],
            }
        }
        self.dump_to_config_file(config=config)

    def dump_to_config_file(self, config):
        with open(self.get_file_path(), "w") as file:
            yaml.dump(config, file)

    def get_file_path(self):
        return os.path.join(BASE_DIR, "files", self.file)

    def __repr__(self):
        return f"<Configuration: {self.file}>"


def get_config(file="config.yaml"):
    return Config(file=file)

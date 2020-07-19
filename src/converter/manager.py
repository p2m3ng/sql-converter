from typing import Optional

from src.converter.formatters import (
    CSVFormatter,
    DictFormatter,
    JsonFormatter,
    ConsoleFormatter,
)
from settings.base import get_config

config = get_config()


class File:
    def __init__(self, filename):
        self.filename = filename

    def get_extension(self):
        try:
            return self.filename.split(".")[1]
        except (IndexError, AttributeError):
            return None

    def get_filename(self):
        if self.filename is None:
            return ""
        return self.filename


class OutputManager:
    formats = {"csv": "csv", "json": "json", "console": "console"}

    def __init__(self, data: tuple, headers: list, export_to: Optional[str] = None):
        self._filename = File(filename=export_to)
        self.headers = headers
        self.data = data

    @property
    def filename(self):
        return self._filename.get_filename()

    @property
    def formatter(self):
        extension = self._filename.get_extension()
        return self.formats.get(extension, "console")

    def run(self, pprint: bool = False, json: bool = False):
        if self.formatter == "csv":
            return self.__to_csv(pprint=pprint)
        elif self.formatter == "console" and json or self.formatter == "json":
            return self.__to_json(pprint=pprint, json=json)
        elif self.formatter == "console":
            return self.__to_console(pprint=pprint)

    def __to_console(self, pprint: bool = False):
        if pprint:
            return ConsoleFormatter(
                headers=self.headers, data=self.data, export_to=self.filename
            ).print()
        return DictFormatter(
            headers=self.headers, data=self.data, export_to=self.filename
        ).to_dict()

    def __to_csv(self, pprint: bool = False):
        formatter = CSVFormatter(
            headers=self.headers, data=self.data, export_to=self.filename
        )
        if pprint:
            return formatter.print()
        return formatter.export()

    def __to_json(self, pprint: bool = False, json: bool = False):
        formatter = JsonFormatter(
            headers=self.headers, data=self.data, export_to=self.filename
        )
        if pprint:
            formatter.print()
        if self._filename and not json:
            return formatter.export()
        return formatter.use()

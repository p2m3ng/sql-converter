import csv
import json
from abc import ABC


class BaseFormatter(ABC):
    def __init__(self, headers, data, export_to):
        self.headers = headers
        self.data = data
        self.export_to = export_to

    def export(self):
        """"""

    def print(self):
        """"""


class CSVFormatter(BaseFormatter):
    def export(self):
        with open(f"{self.export_to}", "w") as file:
            writer = csv.writer(file, delimiter="|")
            writer.writerow(self.headers)
            writer.writerows(self.data)
        print(f"{self.export_to} has been created successfully.")
        return ""

    def print(self):
        self.export()
        with open(f"{self.export_to}", "r") as file:
            reader = csv.reader(file, delimiter="|")
            for line in reader:
                print(line)
        return ""


class DictFormatter(BaseFormatter, ABC):
    def to_dict(self):
        result = []
        for data in self.data:
            result.append(dict(zip(self.headers, data)))
        return result


class JsonFormatter(DictFormatter):
    def export(self):
        with open(f"{self.export_to}", "w") as file:
            json.dump(
                self.to_dict(),
                file,
                indent=2,
                ensure_ascii=False,
                sort_keys=False,
                default=str,
            )
        print(f"{self.export_to} has been created successfully.")
        return self.use()

    def use(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)

    def print(self):
        return print(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)
        )


class ConsoleFormatter(DictFormatter):
    def export(self):
        raise ValueError("Unusable method.")

    def print(self):
        for data in self.to_dict():
            print(data)

import csv
import json
import abc


class BaseFormatter(abc.ABC):
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
        headers = self.data[0].keys()
        with open(f"{self.export_to}", "w") as file:
            writer = csv.DictWriter(file, delimiter="|", fieldnames=headers)
            writer.writeheader()
            for data in self.data:
                writer.writerow(data)
        print(f"{self.export_to} has been created successfully.")
        return ""

    def print(self):
        self.export()
        with open(f"{self.export_to}", "r") as file:
            reader = csv.reader(file, delimiter="|")
            for line in reader:
                print(line)
        return ""


class DictFormatter(BaseFormatter, abc.ABC):
    def export(self):
        return self.data


class JsonFormatter(BaseFormatter):
    def export(self):
        with open(f"{self.export_to}", "w") as file:
            json.dump(
                self.data,
                file,
                indent=2,
                ensure_ascii=False,
                sort_keys=False,
                default=str,
            )
        print(f"{self.export_to} has been created successfully.")
        return self.use()

    def use(self):
        return json.dumps(self.data, ensure_ascii=False, default=str)

    def print(self):
        return print(json.dumps(self.data, indent=2, ensure_ascii=False, default=str))


class ConsoleFormatter(BaseFormatter):
    def export(self):
        raise ValueError("Unusable method.")

    def print(self):
        if isinstance(self.data, list):
            for data in self.data:
                print(data)
        elif isinstance(self.data, dict):
            print(self.data)

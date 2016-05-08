import json
import os.path

class Configuration():
    def __init__(self, path):
        with open(path) as f:
            self.data = json.load(f)
        print(self.data)
        self.root = os.path.split(path)[0]
        print(self.root)

    @property
    def db_path(self):
        return os.path.join(self.root, self.data['database'])




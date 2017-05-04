class Command:

    def __init__(self, path, type, data):
        self.path = path
        self.data = data
        self.type = type

    def get_path(self):
        return self.path

    def get_data(self):
        return self.data

    def get_data_type(self):
        return self.type

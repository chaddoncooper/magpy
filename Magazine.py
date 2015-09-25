import ntpath

class Magazine:

    def __init__(self):
        self.filepath = filepath
        self.filename = ntpath.basename(filepath)
        self.name = self.filename('/')[-1].split('.')[0]





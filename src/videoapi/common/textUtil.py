class TextArea(object):
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)

    def flush(self, *args, **kwargs):
        pass
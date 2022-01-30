class Tab:
    def __init__(self, width:int, height:int):
        self.list = []
        self.width = width
        self.height = height

class Options:
    def __init__(self, lines:int, columns:int, box_size:int):
        self.lines = lines
        self.columns = columns
        self.box_size = box_size

        self.height = lines*box_size
        self.width = columns*box_size

        self.auto_generation = False
        self.auto_generation_delay = 1000
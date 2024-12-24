class Room:
    pass

class World:
    
    def __init__(self):
        self.interactables: set = set()
        self.rooms = []

    def update(self):
        pass
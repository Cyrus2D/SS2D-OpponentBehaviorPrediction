class PlayerType:
    def __init__(self):
        self.kickAble_area = 0
        self.id = -1
    def display(self):
        disp = ""
        disp += "{id: " + str(self.id) + "\n kickAble_area: " + self.kickAble_area + "}"
        return disp
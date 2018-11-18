import object
import pos

class Ball(object.Object):
    def __init__(self):
        self.pos = pos.Pos(-1000,-1000)
        self.vel = pos.Pos(-1000,-1000)
    def set_data(self,string):
        dt = string.split(" ")
        self.pos.x = float(dt[0])
        self.pos.y = float(dt[1])
        self.vel.x = float(dt[2])
        self.vel.y = float(dt[3])
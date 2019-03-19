from makeLog import pos, object

class Ball(object.Object):
    def __init__(self):
        self.pos = pos.Pos(-1000, -1000)
        self.vel = pos.Pos(-1000, -1000)
        self.vel_p = pos.Polar(-100, 10)
    def set_data(self,string):
        dt = string.split(" ")
        self.pos.x = float(dt[0])
        self.pos.y = float(dt[1])
        self.vel.x = float(dt[2])
        self.vel.y = float(dt[3])
        teta_vb = self.vel.teta(pos.Pos(0, 0))
        r_vb = self.vel.r()
        self.vel_p = pos.Polar(r_vb, teta_vb)
    def pos_p(self, o):
        teta_b = self.pos.teta(o)
        r_b = self.pos.dist(o)
        return pos.Polar(r_b, teta_b)

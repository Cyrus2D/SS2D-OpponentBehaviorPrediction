import math
class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def dist(self, other_pos):
        return ((self.x - other_pos.x)**2 + (self.y - other_pos.y)**2)**0.5
    def r(self):
        return self.dist(Pos(0,0))
    def display(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    def set(self,x,y):
        self.x = x
        self.y = y
    def teta(self,p):
        dy = p.y - self.y
        dx = p.x - self.x
        if dx == 0:
            dx = 0.00000001
        alpha = math.atan(dy / dx)
        if dx < 0:
            alpha += math.pi
        if alpha < 0:
            alpha = math.pi*2 + alpha
        return alpha
class Polar:
    def __init__(self,r,teta):
        self.r = r
        self.teta = teta
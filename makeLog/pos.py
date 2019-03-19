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
    def teta(self,p = None):
        if p == None:
            p = Pos(0,0)
        dy = self.y - p.y
        dx = self.x - p.x
        # if dx == 0:
        #     dx = 0.00000001
        # alpha = math.atan(dy / dx)
        # if dx < 0:
        #     alpha += math.pi
        # if alpha < 0:
        #     alpha = math.pi*2 + alpha
        alpha = 0
        if dx == 0 and dy == 0:
            alpha = 0
        else:
            alpha = math.atan2(dy, dx)
        return alpha

class Polar:
    def __init__(self,r,teta):
        self.r = r
        self.teta = teta

def plus(p1: Pos, p2: Pos):
    p = Pos(p1.x + p2.x,p1.y + p2.y)
    return p

def vector(start, end):
    return Pos(end.x - start.x, end.y - start.y)

def make_polar(p: Pos):
    teta = p.teta(Pos(0,0))
    r = p.dist(Pos(0,0))
    return Polar(r, teta)
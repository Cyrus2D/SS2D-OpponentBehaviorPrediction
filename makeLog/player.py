from makeLog import pos, playerType, object


class Player(object.Object):
    def __init__(self):
        self.side = "l" #l or r
        self.unum = -1
        self.playerType = playerType.PlayerType()
        self.pos = pos.Pos(-1000, -1000)
        self.features = Feature()
        self.vel = pos.Pos(-1000, -1000)
        self.body = 361
        self.head = 361
        self.stamina_l = -10
        self.stamina_s = -2
    def is_kickAble(self, ballpos):
        distToball = self.pos.dist(ballpos)
        if(distToball > self.playerType.kickAble_area):
            return False
        return True
    def set(self,lst,player_types):
        self.side = lst[0][0]
        self.unum = int(lst[0][1])
        self.playerType = player_types[int(lst[0][2])]
        self.pos.set(float(lst[0][4]), float(lst[0][5]))
        self.vel.set(float(lst[0][6]), float(lst[0][7]))
        self.body = float(lst[0][8])
        self.head = float(lst[0][9])
        self.stamina_s = float(lst[2][1])
        self.stamina_l = float(lst[2][4])
    def set_data(self, string, pt):
        dt = string.split(" ")
        self.side = dt[0]
        self.unum = int(dt[1])
        self.playerType = pt[int(dt[2])]
        self.pos.x = float(dt[3])
        self.pos.y = float(dt[4])
        self.vel.x = float(dt[5])
        self.vel.y = float(dt[6])
        self.body = float(dt[7])
        self.head = float(dt[8])
class Feature:
    def __init__(self):
        self.polar = pos.Polar(-100, 10)
        self.open_angle = 0
        self.goal_vector = pos.Polar(-100, 10)
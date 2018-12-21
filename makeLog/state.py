from makeLog import ball, pos, player

class State:
    def __init__(self, line, pt):
        self.cycle = 0
        self.players = []
        self.ball = ball.Ball()
        self.kicker = player.Player()
        self.side_playing = "n"
        self.make(line, pt)
    def make(self, line, pt):
        details = line.split("|")
        # Cycle and Ball
        self.cycle = int(details[1])
        self.ball.set_data(details[2])

        # make Players
        for ply_str in details:
            if ply_str == '':
                continue
            if ply_str[0] != "r" and ply_str[0] != "l":
                continue
            playerobj = player.Player()
            playerobj.set_data(ply_str, pt)
            self.players.append(playerobj)

        self.set_side()
        self.set_kicker()

        # make Polars pos for players
        for i in range(len(self.players)):
            self.players[i].features.polar = pos.make_polar(pos.vector(self.players[i].pos, self.kicker.pos))

        # find open tm angle for pass FFFFFFFFFFFFFFFFFFFFFFFFFFFFFUCCCCCKKKKKKKKKKKKKKKKKKKkk
        opp_angles = [p.features.polar for p in self.players if p.side == "r"]
        for p in self.players:
            if p.side == "r": continue
            less = []
            for angle in opp_angles:
                if angle.r > p.features.polar.r: continue
                if angle.teta <= p.features.polar.teta:
                    less.append(angle.teta)
            more = []
            for angle in opp_angles:
                if angle.r > p.features.polar.r: continue
                if angle.teta > p.features.polar.teta:
                    more.append(angle.teta)

        # for i in range(len(players)): #tm
        #     left_ang = 10
        #     right_ang = -10
        #     if players[i].side != kicker.side: continue
        #
        #     for j in range(len(players)): #opp
        #         if j == i: continue
        #         if j == n: continue
        #         if players[j].side == players[i].side: continue
        #         if players[i].pos.dist(kicker.pos) + 2 < players[j].pos.dist(kicker.pos): continue
        #         if left_ang >   players[j].features.polar.teta and players[j].features.polar.teta > players[i].features.polar.teta:
        #             left_ang =  players[j].features.polar.teta
        #         if right_ang <  players[j].features.polar.teta and players[j].features.polar.teta < players[i].features.polar.teta:
        #             right_ang = players[j].features.polar.teta
        #     open_ang = (left_ang - right_ang)
        #     players[i].features.open_angle = open_ang

        # make vector to goals
        for i in range(len(self.players)):
            playerToGoal = pos.vector(self.players[i].pos, pos.Pos(52.5, 0))
            self.players[i].features.goal_vector = pos.make_polar(playerToGoal)

    def set_side(self):
        for p in self.players:
            if p.is_kickAble(self.ball.pos):
                self.side_playing = p.side
                return
        self.side_playing = "n"

    def set_kicker(self):
        for p in self.players:
            if p.is_kickAble(self.ball.pos):
                self.kicker = p
                return

    def make_line(self, next_state, next_cycle):
        new_line = ""
        # XXXXXXXXXXXXXXXXXXXXXX
        new_line += "R|" + str(self.cycle) + "|"
        new_line += str(self.ball.pos.x) + " " + str(self.ball.pos.y) + " " + str(self.ball.pos_p(self.kicker.pos).r) + " " + str(self.ball.pos_p(self.kicker.pos).teta) + " " + str(self.ball.vel_p.r) + " " + str(self.ball.vel_p.teta) + "|"
        for p in self.players:
            if p.unum == self.kicker.unum and p.side == self.kicker.side:
                new_line += str(p.pos.x) + " " + str(p.pos.y) + " "
            else:
                new_line += str(p.features.polar.r) + " " + str(p.features.polar.teta) + " "
            # new_line += str(p.features.open_angle) + " "
            new_line += str(p.features.goal_vector.r) + " " + str((p.features.goal_vector.teta))
            new_line += "|"
        # YYYYYYYYYYYYYYYYYYYYYYYYYYYY
        new_line += str(self.kicker.unum) + " " + str(next_state.kicker.unum) + "|" #+ str(next_cycle.ball.vel.x) + " " + str(next_cycle.ball.vel.y) + "|"
        # new_line += str(next_cycle.ball.vel_p.r) + " " + str(next_cycle.ball.vel_p.teta) + "|"
        return new_line

def next_kick_tm(now: State, lines, line_num, pt):
    for l_n, line in enumerate(lines):
        if l_n <= line_num: continue
        if line == "*": break
        next = State(line,pt)
        if next.side_playing == now.side_playing:
            return next
    return None

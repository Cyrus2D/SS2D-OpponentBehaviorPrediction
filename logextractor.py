#For Sample Extract

import player
import playerType
import ball
import pos
import os

def counter():
    if 'cnt' not in counter.__dict__:
        counter.cnt = 0
    counter.cnt += 1
    return counter.cnt

def logExtractor(log):
    # Find Player Types
    player_types = []
    lines = log.split("\n")
    for line in lines:
        if(line.find("player_type") == -1 or line.find("player_param") != -1):
            continue
        player_types.append(find_playerTypes(line))

    players = []
    #Run Cycles
    run_log(log, player_types)

def run_log(log, player_types):
    os.chdir("../samples")
    new_log = open(str(counter()) + ".rca", "w")
    play_on = False
    # write types in file
    for pt in player_types:
        new_log.write("pt " + str(pt.id) + " " + str(pt.kickAble_area) + "\n")
    for line in log.split("\n"):
        if line.find("playmode") != -1:
            if line.find("play_on") != -1:
                play_on = True
                new_log.write("*\n")
            else:
                play_on = False
        if not play_on:
            continue
        if line.find("show") == -1:
            continue
        #Seprate
        show_str = line[:line.find("(b)") - 2].strip("()")
        line = line[line.find("(b)")-1:]
        ball_str = line[:line.find("(l ") - 2].strip("()")
        line = line[line.find("(l ")-0:].strip("()")
        players_str = line.split(")) ((")

        #Cycle
        cycle = int(show_str.split(" ")[1].strip(")("))

        #Ball
        ball_str = ball_str.split(" ")
        ballobj = ball.Ball()
        ballobj.pos.set(ball_str[1],ball_str[2])
        ballobj.vel.set(ball_str[3],ball_str[4])

        #setPlayers
        players = []
        for player_str in players_str:
            player_str = player_str.split(" (")
            player_details = []
            for player_d in player_str:
                x = player_d.split(" ")
                xx = []
                for i in range(len(x)):
                    x[i] = x[i].strip(")(")
                    if(x[i][0] != 'f'):
                        xx.append(x[i])
                player_details.append(xx)
            plyr = player.Player()
            plyr.set(player_details,player_types)
            players.append(plyr)

        # Write in file
        new_line = "R|"
        new_line += str(cycle) + "|"
        new_line += str(ballobj.pos.x) + " " + str(ballobj.pos.y) + " " + str(ballobj.vel.x) + " " + str(ballobj.vel.y) + "|"
        for plyr in players:
            new_line += plyr.side + " " + str(plyr.unum) + " " + str(plyr.playerType.id) + " "
            new_line += str(plyr.pos.x) + " " + str(plyr.pos.y) + " " + str(plyr.vel.x) + " " + str(plyr.vel.y) + " "
            new_line += str(plyr.body) + " " + str(plyr.head) + "|"
        new_log.write(new_line + "\n")
        print("samples:",cycle)
    os.chdir("../orginalLogs")



def find_playerTypes(line):
    types = make_dictionery(line)
    player_type = playerType.PlayerType()
    player_type.id = types["(id"]
    player_type.kickAble_area = float(types["kickable_margin"])
    return player_type

def make_dictionery(line):
    types_lst = []
    for x in line.split(")("):
        x_strip = x.strip(")(")
        types_lst.append(x_strip.split(" "))
    types_lst[0].pop(0)
    types_dic = {}
    for type in types_lst:
        types_dic[type[0]] = type[1]
    return types_dic

# Featurs
def makeFeaturs(log):
    lines = log.split("\n")
    player_types = []
    for line in lines:
        if(line.find("pt") == -1):
            continue
        pt_str = line.split(" ")
        pt = playerType.PlayerType()
        pt.id = float(pt_str[1])
        pt.kickAble_area = float(pt_str[2])
        player_types.append(pt)
    extractFeatur(log, player_types)

def extractFeatur(log, player_types):
    os.chdir("../features")
    new_log = open(str(counter()) + ".rcb", "w")
    # write types in file
    for pt in player_types:
        new_log.write("pt " + str(pt.id) + " " + str(pt.kickAble_area) + "\n")
    lines = log.split("\n")

    last_kickAble_cycle = -10
    last_kickAble_unum = -1
    for line in lines:
        #Reading a cycle data
        if line.find("*") != -1:
            last_kickAble_unum = -1
            last_kickAble_cycle = -10
        if(line.find("R") == -1):
            continue
        details = line.split("|")
        cycle = int(details[1])
        ballobj = ball.Ball()
        ballobj.set_data(details[2])

        players = []
        for ply_str in details:
            if ply_str == '':
                continue
            if ply_str[0] != "r" and ply_str[0] != "l":
                continue
            playerobj = player.Player()
            playerobj.set_data(ply_str, player_types)
            players.append(playerobj)

        if not side(players, ballobj, "l"):
            if side(players, ballobj, "r"):
                last_kickAble_unum = -1
                last_kickAble_cycle = -10
            continue

        n = 0
        for i in range(len(players)):
            if players[i].is_kickAble(ballobj.pos) and players[i].side == "l":
                n = i
                break
        polars = []
        kicker = players[n]
        for plyr in players:
            teta = plyr.pos.teta(kicker.pos)
            r = plyr.pos.dist(kicker.pos)
            polar = pos.Polar(r,teta)
            polars.append(polar)
        new_line = ""
        new_line += "R|" + str(cycle) + "|"
        #find polar pos and vel of ball
        teta_b = ballobj.pos.teta(kicker.pos)
        r_b = ballobj.pos.dist(kicker.pos)
        polar_b = pos.Polar(r_b, teta_b)
        next_ballpos = pos.Pos(ballobj.pos.x + ballobj.vel.x, ballobj.pos.y + ballobj.vel.y)
        teta_vb = next_ballpos.teta(ballobj.pos)
        r_vb = ballobj.vel.r()
        polar_vb = pos.Polar(r_vb, teta_vb)
        new_line += str(polar_b.r) + " " + str(polar_b.teta) + " " + str(polar_vb.r) + " " + str(polar_vb.teta) + "|"
        for polar in polars:
            new_line += str(polar.r) + " " + str(polar.teta) + "|"
        new_line += str(polars[last_kickAble_unum].r) + " " + str(polars[last_kickAble_unum].teta) + "|"
        if last_kickAble_unum != -1:
            new_log.write(new_line + "\n")
        last_kickAble_unum = kicker.unum
        print("feature:",cycle)
    os.chdir("../samples")

def side(players, ballobj, team_side):
    for plyr in players:
        if plyr.is_kickAble(ballobj.pos) and plyr.side == team_side:
            return True
    return False
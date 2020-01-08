class Player:
    def __init__(self, name, pos, salary, team, avg):
        self.name = name
        self.pos = pos
        self.salary = salary
        self.team = team
        self.avg = avg
        self.PPD = None
        self.flag = False   #Set to true if currently on a lineup, False if available to be
    
    def setPPD(self,PPD):
        self.PPD = PPD
    
    def setType(self, playerType):
        self.playerType = playerType

    def __repr__(self):
        return self.name + "(" + self.pos + "," + self.team + ") Salary:" + self.salary + "\tPPD: " + str(self.PPD)
    
    def __str__(self):
        return self.name + "(" + self.pos + "," + self.team + ") Salary:" + self.salary + "\tPPD: " + str(self.PPD)

class Team:
    def __init__(self, location, pitcher):
        #True == Home. False == Away
        self.homeGame = location
        self.pitcher = pitcher

class Game:
    def __init__(self, Home, Away):
        self.Home = Home
        self.Away = Away
        self.hPitcher = None
        self.aPitcher = None

    def __str__(self):
        return str(self.Away) + "@" + str(self.Home) + "\nAP: " + str(self.aPitcher) + "\nHP: " + str(self.hPitcher) + "\n"

class GameBook:
    def __init__(self):
        self.Games = []

    def addGame(self, Home, Away):
        for g in self.Games:
            if g.Home == Home:
                return
        self.Games.append(Game(Home,Away))

    def addPitcher(self, Pitcher):
        for g in self.Games:
            if g.Home == Pitcher.team:
                g.hPitcher = Pitcher
            elif g.Away == Pitcher.team:
                g.aPitcher = Pitcher
    
    def __repr__(self):
        temp = ""
        for g in self.Games:
            temp += str(g) + " "

        return temp

    def setPitchers(self, Pitchers):
        #Put starting Pitchers in each game
        return "Done"

class ClassicLineup:
    def __init__(self, total):
        self.P = ["EMPTY", "EMPTY"]
        self.C = "EMPTY"
        self.fB = "EMPTY"
        self.sB = "EMPTY"
        self.tB = "EMPTY"
        self.SS = "EMPTY"
        self.OF = ["EMPTY","EMPTY","EMPTY"]
        self.total = total
        self.PPD = 0

    def reset(self):
        self.P = ["EMPTY", "EMPTY"]
        self.C = "EMPTY"
        self.fB = "EMPTY"
        self.sB = "EMPTY"
        self.tB = "EMPTY"
        self.SS = "EMPTY"
        self.OF = ["EMPTY","EMPTY","EMPTY"]
        self.total = 0
        self.PPD = 0
    
    def copy(self, Lineup):
        self.P = Lineup.P
        self.C = Lineup.C
        self.fB = Lineup.fB
        self.sB = Lineup.sB
        self.tB = Lineup.tB
        self.SS = Lineup.SS
        self.OF = Lineup.OF
        self.total = Lineup.total
        self.PPD = Lineup.PPD

    def getTotalPPD(self):
        return self.PPD


    def __repr__(self):
        return "Optimized Lineup:\nP: " + str(self.P[0]) + "\nP: " + str(self.P[1]) + "\nC: " + str(self.C) + "\n1B: " + str(self.fB) + "\
            \n2B: " + str(self.sB) + "\n3B: " + str(self.tB) + "\nSS: " + str(self.SS) + "\
            \nOF: " + str(self.OF[0]) + "\nOF: " + str(self.OF[1]) + "\nOF: " + str(self.OF[2]) + "\
            \nTotal Salary: " + str(self.total) + "\nTotal PPD: " + str(self.getTotalPPD())

class ShowdownLineup:
    def __init__(self, total):
        self.Capt = "EMPTY"
        self.Util = ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"]
        self.total = total
        self.PPD = 0

    def reset(self):
        self.Capt = "EMPTY"
        self.Util = ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"]
        self.total = 0
        self.PPD = 0
    
    def copy(self, Lineup):
        self.Capt = Lineup.Capt
        self.Util = Lineup.Util
        self.total = Lineup.total
        self.PPD = Lineup.PPD

    def getTotalPPD(self):
        return self.PPD


    def __repr__(self):
        return "Optimized Lineup:\nCaptain: " + str(self.Capt) + "\nUTIL: " + str(self.Util[0]) + "\nUTIL: " + str(self.Util[1]) + "\nUTIL: " + str(self.Util[2]) + "\
            \nUTIL: " + str(self.Util[3]) + "\nUTIL: " + str(self.Util[4]) + "\
            \nTotal Salary: " + str(self.total) + "\nTotal PPD: " + str(self.getTotalPPD())

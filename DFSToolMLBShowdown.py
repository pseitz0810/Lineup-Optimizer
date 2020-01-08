from HTMLRetrieve import simple_get
from bs4 import BeautifulSoup
from MLBClasses import Player, ClassicLineup, ShowdownLineup
#from functools import lru_cache
import csv
import re
import copy

#PPD = Points per $1,000
def getPPD(player):
    PPD = float(player.avg)/(float(player.salary)/1000)
    player.setPPD(PPD)
    return PPD

def returnPPD(player):
    return player.PPD

def LineupOptimizer(playerList, MyLineup, size=10):
    currSize = 0
    while currSize < size:
        playerAdded = False
        for player in playerList:
            if (MyLineup.total + float(player.salary)) <= 50000:
                if player.pos == "P":
                    if MyLineup.P[0] == "EMPTY":
                        MyLineup.P[0] = player
                        playerAdded = True
                    elif MyLineup.P[1] == "EMPTY":
                        MyLineup.P[1] = player
                        playerAdded = True
                elif player.pos == "C" and MyLineup.C == "EMPTY":
                    MyLineup.C = player
                    playerAdded = True
                elif player.pos == "1B" and MyLineup.fB == "EMPTY":
                    MyLineup.fB = player
                    playerAdded = True
                elif player.pos == "2B" and MyLineup.sB == "EMPTY":
                    MyLineup.sB = player
                    playerAdded = True
                elif player.pos == "3B" and MyLineup.tB == "EMPTY":
                    MyLineup.tB = player
                    playerAdded = True
                elif player.pos == "SS" and MyLineup.SS == "EMPTY":
                    MyLineup.SS = player
                    playerAdded = True
                elif player.pos == "OF":
                    if MyLineup.OF[0] == "EMPTY":
                        MyLineup.OF[0] = player
                        playerAdded = True
                    elif MyLineup.OF[1] == "EMPTY":
                        MyLineup.OF[1] = player
                        playerAdded = True
                    elif MyLineup.OF[2] == "EMPTY":
                        MyLineup.OF[2] = player
                        playerAdded = True
            if playerAdded:
                MyLineup.total += float(player.salary)
                currSize+=1
                playerList = [p for p in playerList if not p.name == player.name]
                print("Player Added")
                break
        if playerAdded == False:
            print("No Lineup")
            break


#@lru_cache(maxsize=None)
def LineupOptimizerRecurse(playerList, CurrLineup, BestLineup, currSize, size=6):
        playerAdded = False
        if currSize == size:
            #print("Curr: " + str(CurrLineup.getTotalPPD()))
            #print("Best: " + str(BestLineup.getTotalPPD()))
            if float(CurrLineup.getTotalPPD()) > float(BestLineup.getTotalPPD()):
                BestLineup = copy.deepcopy(CurrLineup)
                print("New Best")
                print(BestLineup)
            #print("Finished Lineup")
            #print(BestLineup)
            return BestLineup  
        else:
            if currSize == (size-1) and (BestLineup.getTotalPPD()-7) > CurrLineup.getTotalPPD():
                return BestLineup

            for player in playerList:
                if (CurrLineup.total + float(player.salary)) <= 50000 and not player.flag:
                    if currSize == 0:
                        print("New Player: " + player.name)
                    if CurrLineup.Capt == "EMPTY":
                        CurrLineup.Capt = player
                        CurrLineup.total += float(player.salary) * 1.5
                        CurrLineup.PPD += float(player.PPD) * 1.5
                        player.flag = True
                        print(CurrLineup)
                        BestLineup = LineupOptimizerRecurse(playerList, CurrLineup, BestLineup, currSize+1, size)
                        CurrLineup.Capt = "EMPTY"
                        CurrLineup.total = float(CurrLineup.total) - (float(player.salary) * 1.5)
                        CurrLineup.PPD = float(CurrLineup.PPD) - (float(player.PPD) * 1.5)
                        player.flag = False
                    elif CurrLineup.Util[0] == "EMPTY":
                        CurrLineup.Util[0] = player
                        CurrLineup.total += float(player.salary)
                        CurrLineup.PPD += float(player.PPD)
                        player.flag = True
                        BestLineup = LineupOptimizerRecurse(playerList, CurrLineup, BestLineup, currSize+1, size)
                        CurrLineup.Util[0] = "EMPTY"
                        CurrLineup.total = float(CurrLineup.total) - float(player.salary)
                        CurrLineup.PPD = float(CurrLineup.PPD) - float(player.PPD)
                        player.flag = False
                    elif CurrLineup.Util[1] == "EMPTY":
                        CurrLineup.Util[1] = player
                        CurrLineup.total += float(player.salary)
                        CurrLineup.PPD += float(player.PPD)
                        player.flag = True
                        BestLineup = LineupOptimizerRecurse(playerList, CurrLineup, BestLineup, currSize+1, size)
                        CurrLineup.Util[1] = "EMPTY"
                        CurrLineup.total = float(CurrLineup.total) - float(player.salary)
                        CurrLineup.PPD = float(CurrLineup.PPD) - float(player.PPD)
                        player.flag = False
                    elif CurrLineup.Util[2] == "EMPTY":
                        CurrLineup.Util[2] = player
                        CurrLineup.total += float(player.salary)
                        CurrLineup.PPD += float(player.PPD)
                        player.flag = True
                        BestLineup = LineupOptimizerRecurse(playerList, CurrLineup, BestLineup, currSize+1, size)
                        CurrLineup.Util[2] = "EMPTY"
                        CurrLineup.total = float(CurrLineup.total) - float(player.salary)
                        CurrLineup.PPD = float(CurrLineup.PPD) - float(player.PPD)
                        player.flag = False
                    elif CurrLineup.Util[3] == "EMPTY":
                        CurrLineup.Util[3] = player
                        CurrLineup.total += float(player.salary)
                        CurrLineup.PPD += float(player.PPD)
                        player.flag = True
                        BestLineup = LineupOptimizerRecurse(playerList, CurrLineup, BestLineup, currSize+1, size)
                        CurrLineup.Util[3] = "EMPTY"
                        CurrLineup.total = float(CurrLineup.total) - float(player.salary)
                        CurrLineup.PPD = float(CurrLineup.PPD) - float(player.PPD)
                        player.flag = False
                    elif CurrLineup.Util[4] == "EMPTY":
                        CurrLineup.Util[4] = player
                        CurrLineup.total += float(player.salary)
                        CurrLineup.PPD += float(player.PPD)
                        player.flag = True
                        BestLineup = LineupOptimizerRecurse(playerList, CurrLineup, BestLineup, currSize+1, size)
                        CurrLineup.Util[4] = "EMPTY"
                        CurrLineup.total = float(CurrLineup.total) - float(player.salary)
                        CurrLineup.PPD = float(CurrLineup.PPD) - float(player.PPD)
                        player.flag = False
            return BestLineup

if __name__ == '__main__':
    playerList = []
    Pitchers = []
    Hitters = []

    #Finds the statring pitchers for the day so only takes pitchers who are starting that day
    raw_starting_pitchers = simple_get('https://www.mlb.com/probable-pitchers')
    starting_pitchers = BeautifulSoup(raw_starting_pitchers, 'html.parser')
    starting_pitchers = starting_pitchers.find_all('a',{'class': 'probable-pitchers__pitcher-name-link'})
    starting_pitchers = [p.string for p in starting_pitchers]

    with open('DKSalaries.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                #row[2]=name, row[0]=position row[5]=salary row[8]=avg points per game
                temp = Player(row[2],row[0][:2],row[5],row[8])
                if row[0] == "SP" and row[4] == "UTIL":
                    temp.setType("P")
                    Pitchers.append(temp)
                    playerList.append(temp)
                elif row[0] != "SP" and row[0] != "RP" and row[4] == "UTIL":
                    temp.setType("H")
                    Hitters.append(temp)
                    playerList.append(temp)

            line_count+=1

    playerList.sort(key=getPPD, reverse=True)
    #[print(n) for n in playerList if not n.PPD == 0]

    MyLineup = ShowdownLineup(0)
    CurrLineup = ShowdownLineup(0)

    #oRAR affects PPD value - Need updated csv table from Baseball-Reference. Player Value table
    #BA last 5 days affects PPD value - Need updated csv from Baseball-Reference. Hitters last 5 days
    for p in Hitters:
        #print("New")
        #print(p.name)
        with open('Batting_Stats.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                #print(row[0] + re.findall(r"[a-zA-Z\s]*",row[1])[0] + row[20])
                if p.name == (re.findall(r"[a-zA-Z\s]*",row[1])[0]):
                    p.PPD = p.PPD + (float(row[20])/10)
        
        with open('5DayBatting.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                #print(row[0] + re.findall(r"[a-zA-Z\s]*",row[1])[0] + row[25])
                if p.name == (re.findall(r"[a-zA-Z\s]*",row[1])[0]) and int(row[9]) >= 3:
                    p.PPD = p.PPD + (float(row[25].strip())/.1) - 2.99

    for p in Pitchers:
        with open('14DayPitching.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if p.name == (re.findall(r"[a-zA-Z\s]*",row[1])[0]) and float(row[12]) >= 1.1:
                    #print("Change")
                    p.PPD = p.PPD - (float(row[20].strip()) - 3) 


    playerList.sort(key=returnPPD, reverse=True)
    print(len(playerList))
                    

    choose = input("First Lineup(1) or Best Lineup(2)")

    if choose == "1":
        LineupOptimizer(playerList, MyLineup)
        cont = True
        while cont:
            print(MyLineup)
            data = input("Remove a player and retry?")
            if data == "done":
                cont = False
            else:
                for i in playerList:
                    if i.name == data:
                        playerList.remove(i)
                        print(data + " was removed. Re-Optimizing")
                        break
                MyLineup.reset()
                LineupOptimizer(playerList, MyLineup)
    if choose == "2":
        MyLineup = LineupOptimizerRecurse(playerList, CurrLineup, MyLineup, 0)
        print(MyLineup)


    """print("Hitters:")
    print(Hitters)
    print("Pitchers:")
    print(Pitchers)"""
            

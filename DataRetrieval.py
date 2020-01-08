from HTMLRetrieve import simple_get
from bs4 import BeautifulSoup
from MLBClasses import Player, ClassicLineup, Game, GameBook
from DFSToolMLB1 import LineupOptimizer, LineupOptimizerRecurse
import csv
import re

#find_all('td')[1]=name, find_all('td')[19]=wOBA, find_all('td')[7]=AVG, find_all('td')[13]=BABIP
def adjustPPD(player):
    #return None
    print(p.find_all('td')[1].text + " " + p.find_all('td')[7].text + " " + p.find_all('td')[13].text + " " + p.find_all('td')[19].text)

def returnPPD(player):
    return player.PPD

if __name__ == '__main__':
    playerList = []
    Pitchers = []
    Hitters = []
    Games = GameBook()

    #Finds the statring pitchers for the day so only takes pitchers who are starting that day
    raw_starting_pitchers = simple_get('https://www.mlb.com/probable-pitchers')
    starting_pitchers = BeautifulSoup(raw_starting_pitchers, 'html.parser')
    starting_pitchers = starting_pitchers.find_all('a',{'class': 'probable-pitchers__pitcher-name-link'})
    starting_pitchers = [p.string for p in starting_pitchers]

    #imports list of available players on DK
    with open('DKSalaries.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                #row[2]=name, row[4]=position row[5]=salary row[6]=game teams row[7]=player team row[8]=avg points per game
                temp = Player(row[2],row[4][:2],row[5],row[7],row[8])
                temp.PPD = float(row[8])/(float(row[5])/1000)
                if row[4] == "P" and float(temp.avg) != 0.0 and row[2] in starting_pitchers:
                    temp.setType("P")
                    Pitchers.append(temp)
                    playerList.append(temp)
                elif row[4] != "P" and float(temp.avg) != 0.0:
                    temp.setType("H")
                    Hitters.append(temp)
                    playerList.append(temp)

                teams = re.findall(r"[A-Z]{2,3}",row[6])
                Games.addGame(teams[1],teams[0])
                    
            line_count+=1
    
    #Adding pitchers to each game
    for p in Pitchers:
        Games.addPitcher(p)

    MyLineup = ClassicLineup(0)
    CurrLineup = ClassicLineup(0)

    #list of batters from fangraph
    batters = []
    #makes list of batters with AVG, BABIP, and wOBA as attributes
    for i in range(1,13):
        raw_batters = simple_get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=1&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31&sort=19,d&page=' + str(i) + '_50')
        batters_temp = BeautifulSoup(raw_batters, 'html.parser')
        #print(batters_temp.find_all('tr',{'class': ['rgRow','rgAltRow']}))
        batters_temp = batters_temp.find_all('tr',{'class': ['rgRow','rgAltRow']})
        for p in batters_temp:
            #adjustPPD(p)
            batters.append({'name':p.find_all('td')[1].text, 'avg':p.find_all('td')[7].text, 'babip':p.find_all('td')[13].text, 'woba':p.find_all('td')[19].text})
        #[batters.append(p) for p in batters_temp]

    #list of batters from fangraph
    throwers = []
    #makes list of batters with AVG, BABIP, and wOBA as attributes
    for i in range(1,5):
        raw_throwers = simple_get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=40&type=8&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31&page=' + str(i) + '_50')
        throwers_temp = BeautifulSoup(raw_throwers, 'html.parser')
        #print(batters_temp.find_all('tr',{'class': ['rgRow','rgAltRow']}))
        throwers_temp = throwers_temp.find_all('tr',{'class': ['rgRow','rgAltRow']})
        for t in throwers_temp:
            #adjustPPD(p)
            throwers.append({'name':t.find_all('td')[1].text, 'k/9':t.find_all('td')[9].text, 'bb/9':t.find_all('td')[10].text, 'babip':t.find_all('td')[12].text, 'era':t.find_all('td')[16].text})

    print(throwers[0])
    i=0
    for h in Hitters:
        for b in batters:
            if h.name == b['name']:
                h.PPD = h.PPD + float(b['woba'])*5 #+ (float(b['avg']) - float(b['babip'])) * 10
                i+=1

    """for p in Pitchers:
            with open('14DayPitching.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if p.name == (re.findall(r"[a-zA-Z\s]*",row[1])[0]) and float(row[12]) >= 1.1:
                        #print("Change")
                        p.PPD = p.PPD - (float(row[20].strip()) - 3)""" 

    for p in Pitchers:
        for t in throwers:
            if p.name == t['name']:
                p.PPD = p.PPD + float(t['k/9'])/2 - float(t['bb/9']) + (float(t['babip']) * 20 - float(t['era']))

    playerList.sort(key=returnPPD, reverse=True)
    [print(p.PPD) for p in playerList]
    print(Games)

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
    
    """
    print(i)
    #Returns wOBA of player
    batters_temp = batters_temp[0].find_all('td')[19]
    print('Fangraph: ' + str(len(batters)))
    print('DK: ' + str(len(Hitters)))
    print(batters[0]['name'])
    #[print(p.td) for p in batters]
    """
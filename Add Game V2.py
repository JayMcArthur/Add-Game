import random
import math
import os
clear = lambda: os.system('cls')

class Player:

    def __init__(self, name=None):
        self.add     = 1
        self.points  = 1
        self.upgrade = 1
        self.name = "None"
        self.moves = ["Start"]
        self.name = name

    def addPoints(self):
        self.points += self.add
        self.moves += ["Add"]

    def upgradeAdd(self):
        self.add += math.floor(self.points/self.upgrade)
        self.points = 0
        self.upgrade += 1
        self.moves += ["Upgrade"]

    def movesToStr(self):
        moveInt = 0
        output = ""
        for i in (self.moves):
            if i == "Add":
                moveInt += 1
            elif i == "Upgrade":
                output += str(moveInt) + "-"
                moveInt = 0
        output += str(moveInt)
        return output



class Game:

    def __init__(self):
        self.goal  = 1
        self.round = 1
        self.player1 = Player("1")
        self.player2 = Player("2")
        self.theAI = Player("AI")
        self.gameMode = 0
        self.bestPath = ["Start"]
        self.Yes = 0
        self.No = 0

    def checkWin(self):
        if self.player1.points >= max(self.goal, self.player2.points, self.theAI.points) :
            return 1
        elif self.player2.points >= self.goal:
            return 2
        elif self.theAI.points >= self.goal:
            return 3
        else:
            return 0

    def playerTurn(self, player):
        print("\n" + "Player: " + player.name)
        print("Round: " + str(self.round))
        print("Points: " + str(player.points))
        print("Add: +" + str(player.add) + " Points")
        print("Upgrade: +" +  str(math.floor(player.points/player.upgrade)) + "/turn")
        print("[a]dd or [u]pgrade?")
        while True:
            try:
                pick = input("Pick: ")
                if pick == "a" or pick == "u":
                    break
            except:
                pass
        if pick == "a":
            player.addPoints()
            
        elif pick == "u":
            player.upgradeAdd()

    def maxTurn(self):
        i = 1
        last = self.goal+1
        while True:
            hold = math.ceil(self.goal ** (1. / i)) * sum(range(1,i+1))
            if hold < last:
                last = hold
            else:
                return last
            i += 1

    def reasonable(self, a1, a2):
        '''
        a1Tp = a1[4] + (a1[1] * (a1[2] - 1)) # TODO Adjust for fairness
        a2Tp = a2[4] + (a2[1] * (a2[2] - 1))
        if a1Tp >= a2Tp or a1Tp + a1[1] >= a1Tp:
            self.Yes += 1
            return True
        self.No += 1
        return False
        '''
        return True
        

    def findSolution(self):
        #           Points, Add, Upgrade,           Turn, Total Pt, Path
        cStack = [ [     1,   1,       1,              1,        1,  ["Start"] ] ]
        nStack = []
        cBest = [        1,   1,       1,              1,         1, ["Start"] ]
        oBest = [self.goal - 1,   1,       1, self.maxTurn(), self.goal, ["Start"] ]
        
        while (len(cStack) + len(nStack) > 0):
            if len(cStack) > 0:
                cur = len(cStack) - 1
                pts = cStack[cur][0]
                add = cStack[cur][1]
                upd = cStack[cur][2]
                turn = cStack[cur][3]
                toPt = cStack[cur][4]
                stk = cStack[cur][5]

                # Haven't won, Under best turns, and its around realtive points
                if (pts < self.goal) and (turn < oBest[3]) and self.reasonable(cStack[cur], cBest):
                    # Upgrade if it is faster then adding and is past some threshold
                    if  (game.goal-pts)/add > game.goal/(add + math.floor(pts/upd)) and math.floor(pts/upd) >= math.ceil(0.5*add): #math.floor(math.sqrt(pts)) + 2:
                        nStack.append([0, add + math.floor(pts/upd), upd + 1, turn + 1, toPt, stk + ["Upgrade"]])
                    nStack.append([pts + add, add, upd, turn + 1, toPt + add, stk + ["Add"]])
                elif (pts >= self.goal) and (turn < oBest[3] or (turn == oBest[3] and pts > oBest[0]) ):
                    oBest[0] = pts
                    oBest[1] = add
                    oBest[2] = upd
                    oBest[3] = turn
                    oBest[4] = toPt
                    oBest[5] = stk
                cStack.remove(cStack[cur])
            else:
                for i in nStack:
                    if i[4] > cBest[4]:
                        cBest = i
                    cStack.append(i)
                del(nStack)
                nStack = []
        return oBest[5]

    def AI_Turn(self, AI):
        if self.gameMode == 1: #Easy AI
            lenA = (game.goal - AI.points) / AI.add # Add Length
            lenU = game.goal / (AI.add + math.floor(AI.points / AI.upgrade)) # Upgrade Length
            if lenU < lenA:
                choice = random.randint(0,5)
            else:
                choice = 0
            
            if choice != 3 and choice != 4:
                AI.addPoints()
            else:
                AI.upgradeAdd()

        elif self.gameMode == 2: #Hard AI
            if self.bestPath[self.round] == "Add":
                AI.addPoints()
            elif self.bestPath[self.round] == "Upgrade":
                AI.upgradeAdd()

    def playGame(self):
        clear()
        print("--Add--")
        print("v2.00" + "\n")
        print("Game Goal:")
        while True:
            try:
                self.goal = int(input("Points: "))
                break
            except ValueError:
                pass
        clear()
        print("Pick opponent:")
        print("0: Player 2")
        print("1: Easy AI")
        print("2: Hard AI")
        while True:
            try:
                self.gameMode = int(input("Mode: "))
                if -1 < self.gameMode < 3:
                    break
            except ValueError:
                pass
        if self.gameMode == 2:
            self.bestPath = self.findSolution()
        clear()
        if self.gameMode == 0:
            while True:
                self.playerTurn(self.player1)
                clear()
                input("Player 2")
                clear()
                self.playerTurn(self.player2)
                clear()
                if self.checkWin() != 0:
                    print("Game Over")
                    print("Round " + str(self.round))
                    input("")
                    print("Player " + str(self.checkWin()) + " Won!")
                    print("Goal: " + str(self.goal) + " Points" + "\n")
                    print("PLayer 1 Points: " + str(self.player1.points))
                    print("PLayer 2 Points: " + str(self.player2.points) + "\n")
                    print("Player 1 Moves: " + self.player1.movesToStr())
                    print("Player 2 Moves: " + self.player2.movesToStr())
                    break
                self.round += 1
                input("Player 1")
                clear()
        else:
            while True:
                self.playerTurn(self.player1)
                clear()
                self.AI_Turn(self.theAI)
                if self.checkWin() != 0:
                    print("Game Over")
                    print("Round " + str(self.round))
                    input("")
                    if self.checkWin() != 3:
                        print("You Won!")
                    else:
                        print("The AI Won")
                    print("Goal: " + str(self.goal) + " Points" + "\n")
                    print("Your Points: " + str(self.player1.points))
                    print("AI Points: " + str(self.theAI.points) + "\n")
                    print("Your Moves: " + self.player1.movesToStr())
                    print("AI Moves: " + self.theAI.movesToStr()) 
                    break
                self.round += 1
        print(str(self.No) + " + " + str(self.Yes+self.No))

game = Game()
game.playGame()

'''
game.gameMode = 2
game.goal = 300
while True:
    game.bestPath = game.findSolution()
    for i in range(len(game.bestPath)-1):
        game.AI_Turn(game.theAI)
        game.round += 1
    print("Goal: " + str(game.goal) + " > " + str(game.theAI.points) + " > " + game.theAI.movesToStr())
    input()
    game.goal = game.theAI.points+1
    del(game.player1)
    game.player1 = Player("1")
    del(game.theAI)
    game.theAI = Player("AI")
    game.round = 1
'''

        
        
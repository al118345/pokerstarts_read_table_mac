import tools
import models
import os
import cv2
import threading
from poker.hand import Combo, Range
import poker_prob.holdem_calc


# Function to convert
def listToString2(s):
    # initialize an empty string
    str1 = []

    # traverse in the string
    for ele in s:
        if '?' not in str(ele) and 'X' not in str(ele):
            str1.append(str(ele))
        # return string
    return str1



def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        if '?' not in  str(ele) and 'X' not in str(ele):
            str1 += str(ele)
        # return string
    return str1


class PokerBot:
    gameState = ""
    playerCards = []
    tableCards = []
    # tableName = ""

    def checkGameState(self) -> str:
        if not len(self.tableCards):
            return "Prefloop"
        elif len(self.tableCards) == 4:
            return "Turn"
        elif len(self.tableCards) == 5:
            return "River"
        else:
            return "Floop"

    def readData(self, screenshot):
        self.tableCards = tools.readTableCards(screenshot.filename)
        self.playerCards = tools.readPlayerCards(screenshot.filename)
        self.number_player = tools.number_player(screenshot.filename)
        self.gameState = self.checkGameState()
        

class ChangesHandler:
    tableName = ""
    def __init__(self, bot: PokerBot, tableName: str):
        self.gameState = bot.gameState
        self.playerCards = bot.playerCards
        self.tableCards = bot.tableCards
        self.tableName = tableName
        self.number_player = 5


    def check(self, bot: PokerBot):
        if self.gameState != bot.gameState or self.playerCards != bot.playerCards or self.tableCards != bot.tableCards:
            self.gameState = bot.gameState
            self.playerCards = bot.playerCards
            self.tableCards = bot.tableCards
            self.number_player =  bot.number_player
            self.printData()

        
    def printData(self):





        print (f'Player cards: {self.playerCards} and {self.number_player}')
        print (f'Cards on table: {self.tableCards}')
        print (f'Game state: {self.gameState}')
        print (f'Table: {self.tableName}')
        print ("########################")
        try:
            villan_hand = None
            exact_calculation = False
            verbose = True
            num_sims = 1
            read_from_file = None
            hero_hand = Combo(listToString(self.playerCards))
            try:
                board =  listToString2(self.tableCards)
            except:
                print("vacio")
                board = []
            odds = poker_prob.holdem_calc.calculate_odds_villan(board,
                                                                exact_calculation,
                                                                num_sims,
                                                                read_from_file,
                                                                hero_hand,
                                                                villan_hand,
                                                                verbose,
                                                                num_player=self.number_player,
                                                                print_elapsed_time=True)
            print(f'Resultado: {odds}')
        except Exception as e:
            pass


class MultiBot:
    bot_dict = {}
    def __init__(self):
        #self.gameWindows = tools.moveAndResizeWindows()
        screenshots = tools.grabScreen()

        for img in screenshots:
            bot = PokerBot()
            img.tableName

            changesHandler = ChangesHandler(bot, img.tableName)
            self.bot_dict[img.tableName] = [bot, changesHandler]
    
    def run(self):
        while 1:
            screenshots = tools.grabScreen()
            for img in screenshots:
                bot, changesHandler = self.bot_dict[img.tableName]
                bot.readData(img)
                changesHandler.check(bot)
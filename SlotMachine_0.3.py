# Source File Name: SlotMachine.py
# Author's Name: Michael Burnie
# Last Modified By: Michael Burnie
# Date Last Modified: June 3, 2013
""" 
  Program Description:  This program simulates a Casino-Style Slot Machine. It provides an GUI
                        for the user that is an image of a slot machine with Label and Button objects
                        created through the pygame module. The player can specify a bet of 10, 100 or 1000.
                        The player can then spin the reels or reset the game to defaults.

  Version: 0.3      - Added new buttons & functionality for:
                        - Bet 10, 100, 1000
                        - Reset
                    - Added GUI text elements for:
                        - Credits
                        - Bet
                        - Jackpot
                    - Background updated to hold new GUI elements
                    - New reel images
                        - including source image
                    - Changed Banana to Watermelon
                    - Updated Description
                    - Changed caption
                    - Changed some local variables to Global Constants, as they never change
                    - Changed some variable names
                        - eg. 'playerMoney' to 'credits'
                    - Minor revisions to impoted file: Buttons.py
"""

#I - Import and initialize
import pygame, random, Buttons

#set global constants. These values do not change
FONT = pygame.font.SysFont("arial",30, 1)
SCREEN = pygame.display.set_mode((640, 480))

WHITE = (255,255,255)
BLACK = (  0,  0,  0)

def main():
    
    pygame.init()
    
    #D - Display configuration
    
    pygame.display.set_caption("Slot Machine!")
    
    #E - Entities (just background for now)
    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()
    background = pygame.image.load("background.png")
    
    #A - Action (broken into ALTER steps)
    
        #A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    
    SCREEN.blit(background, (0, 0))
       
    reel = [pygame.Surface((0, 0)), pygame.Surface((0, 0)), pygame.Surface((0, 0))]
    
    credits, jackpot, turn, bet, prevBet, winNumber, lossNumber = newGame(SCREEN, background, reel)
     
        #L - Set up main loop
    while keepGoing:
        
        clock.tick(30)

        #Declare buttons, using the Buttons.py import
        spinButton = Buttons.Button()
        resetButton = Buttons.Button()
        bet10Button = Buttons.Button()
        bet100Button = Buttons.Button()
        bet1000Button = Buttons.Button()
        #Parameters:                surface,   color,     x,   y,   length, height, width,  text,      text_color
        spinButton.create_button(   SCREEN, (107,142, 35), 475, 390, 75,    65,    0,        "Spin!", WHITE)
        resetButton.create_button(  SCREEN, (255, 50, 50),  75, 390, 75,    65,    0,        "Reset", WHITE)
        bet10Button.create_button(  SCREEN, (150,150,255), 175, 390, 75,    65,    0,        "Bet 10", WHITE)
        bet100Button.create_button( SCREEN, (125,125,255), 275, 390, 75,    65,    0,        "Bet 100", WHITE)
        bet1000Button.create_button(SCREEN, (100,100,255), 375, 390, 75,    65,    0,        "Bet 1000", WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if spinButton.pressed(pygame.mouse.get_pos()):
                    if bet > credits:
                        print("Sorry, you only have $" + str(credits) + " \n")
    
                    elif bet <= credits:
                        turn +=1
                        prevBet = bet
                        credits, jackpot, win, fruitReel = pullthehandle(bet, credits, jackpot)

                        showReels(reel, fruitReel)
                        
                        showSection(credits, 107, 287, "blank_credits.png")
                        showSection(jackpot, 393, 288, "blank_jackpot.png")
                        
                elif resetButton.pressed(pygame.mouse.get_pos()):
                    credits, jackpot, turn, bet, prevBet, winNumber, lossNumber = newGame(SCREEN, background, reel)
                elif bet10Button.pressed(pygame.mouse.get_pos()):
                    bet = 10
                    showSection(bet, 298, 288, "blank_bet.png")
                elif bet100Button.pressed(pygame.mouse.get_pos()):
                    bet = 100
                    showSection(bet, 298, 288, "blank_bet.png")
                elif bet1000Button.pressed(pygame.mouse.get_pos()):
                    bet = 1000
                    showSection(bet, 298, 288, "blank_bet.png")

        pygame.display.flip()  
        
def newGame(SCREEN, background, reel):

    
    # Initial Values
    credits =      1000
    jackpot =      500
    turn =         1
    bet =          100
    prevBet =      0
    winNumber =    0
    lossNumber =   0    
    
    for spin in range(3):
        reel[spin] = pygame.Surface((0, 0))
        reel[spin] = background.convert()
        reel[spin] = pygame.image.load("Spin.png")
        SCREEN.blit(reel[spin], (135 + spin * 135, 175))
    
    showSection(credits, 107, 287, "blank_credits.png")
    showSection(bet, 298, 288, "blank_bet.png")
    showSection(jackpot, 393, 288, "blank_jackpot.png")
    
    return credits, jackpot, turn, bet, prevBet, winNumber, lossNumber

def showReels(reel, fruitReel):
    for spin in range(3):
        if fruitReel[spin] == 'Blank':
            reel[spin] = pygame.image.load("Blank.png")
        if fruitReel[spin] == 'Grapes':
            reel[spin] = pygame.image.load("Grapes.png")
        if fruitReel[spin] == 'Watermelon':
            reel[spin] = pygame.image.load("Watermelon.png")
        if fruitReel[spin] == 'Orange':
            reel[spin] = pygame.image.load("Orange.png")
        if fruitReel[spin] == 'Cherry':
            reel[spin] = pygame.image.load("Cherry.png")
        if fruitReel[spin] == 'Bar':
            reel[spin] = pygame.image.load("Bar.png")
        if fruitReel[spin] == 'Bell':
            reel[spin] = pygame.image.load("Bell.png")
        if fruitReel[spin] == 'Seven':
            reel[spin] = pygame.image.load("Seven.png")
        
        SCREEN.blit(reel[spin], (135 + spin * 135, 175))                       

def showSection(value, x, y, blankImage):
    section = pygame.image.load(blankImage)
    SCREEN.blit(section,(x, y))

    section = FONT.render(str(value), True, BLACK)
    SCREEN.blit(section,(x, y))
       
#          User Input
#         Prompt = raw_input(" Place Your Bet ! \n Jackpot $ " + str(jackpot) + "\n Money $ " + str(Player_Money) + "\n Q = quit \n")
#         if Prompt  == "q" or Prompt  == "Q":
#             KeepGoing = False
#             break
#  
#                 if Prompt == "" and Turn >1:
#             Bet = Prev_Bet
#             print("Using Previous Bet")
#             if Bet > Player_Money:
#                 print("Sorry, you only have $" + str(Player_Money) + " \n")
#             elif Bet <= Player_Money:
#                 Turn +=1
#                 Prev_Bet = Bet
#                 credits, jackpot, win = pullthehandle(bet, credits, jackpot)
#         
#         elif is_number(Prompt ):
#             Bet = int(Prompt )
#             # not enough money
#             if Bet > Player_Money:
#                 print("Sorry, you only have $" + str(Player_Money) + " \n")
#                 
#             # Let's Play
#             elif Bet <= Player_Money:
#                 Turn +=1
#                 Prev_Bet = Bet
#                 credits, jackpot, win = pullthehandle(bet, credits, jackpot)
    
#def spin(reel):        
    
    
        
#     if win:
#         winNumber += 1
#         winRatio = "{:.2%}".format(winNumber / turn)
#     
#     else:
#         loss_number += 1
#         win_ratio = "{:.2%}".format(winNumber / turn)
#     print("Wins: " + str(winNumber) + "\nLosses: " + str(lossNumber) + "\nWin Ratio: " + winRatio + "\n") 
#     win = 0      

        
def Reels():
    """ When this function is called it determines the Bet_Line results.
        e.g. Bar - Orange - Watermelon """
        
    # [0]Fruit, [1]Fruit, [2]Fruit
    betLine = [" "," "," "]
    outcome = [0,0,0]
    
    # Spin those reels
    for spin in range(3):
        outcome[spin] = random.randrange(1,65,1)
        # Spin those Reels!
        if outcome[spin] >= 1 and outcome[spin] <=26:   # 40.10% Chance
            betLine[spin] = "Blank"
        if outcome[spin] >= 27 and outcome[spin] <=36:  # 16.15% Chance
            betLine[spin] = "Grapes"
        if outcome[spin] >= 37 and outcome[spin] <=45:  # 13.54% Chance
            betLine[spin] = "Watermelon"
        if outcome[spin] >= 46 and outcome[spin] <=53:  # 11.98% Chance
            betLine[spin] = "Orange"
        if outcome[spin] >= 54 and outcome[spin] <=58:  # 7.29%  Chance
            betLine[spin] = "Cherry"
        if outcome[spin] >= 59 and outcome[spin] <=61:  # 5.73%  Chance
            betLine[spin] = "Bar"
        if outcome[spin] >= 62 and outcome[spin] <=63:  # 3.65%  Chance
            betLine[spin] = "Bell"  
        if outcome[spin] == 64:                         # 1.56%  Chance
            betLine[spin] = "Seven"    

    
    return betLine

def pullthehandle(bet, credits, jackpot):
    """ This function takes the Player's Bet, Player's Money and Current JackPot as inputs.
        It then calls the Reels function which generates the random Bet Line results.
        It calculates if the player wins or loses the spin.
        It returns the Player's Money and the Current Jackpot to the main function """
    credits -= bet
    jackpot += (int(bet*.15)) # 15% of the player's bet goes to the jackpot
    win = False
    fruitReel = Reels()
    fruits = fruitReel[0] + " - " + fruitReel[1] + " - " + fruitReel[2]
    
    # Match 3
    if fruitReel.count("Grapes") == 3:
        winnings,win = bet*20,True
    elif fruitReel.count("Watermelon") == 3:
        winnings,win = bet*30,True
    elif fruitReel.count("Orange") == 3:
        winnings,win = bet*40,True
    elif fruitReel.count("Cherry") == 3:
        winnings,win = bet*100,True
    elif fruitReel.count("Bar") == 3:
        winnings,win = bet*200,True
    elif fruitReel.count("Bell") == 3:
        winnings,win = bet*300,True
    elif fruitReel.count("Seven") == 3:
        print("Lucky Seven!!!")
        winnings,win = bet*1000,True
    # Match 2
    elif fruitReel.count("Blank") == 0:
        if fruitReel.count("Grapes") == 2:
            winnings,win = bet*2,True
        if fruitReel.count("Watermelon") == 2:
            winnings,win = bet*2,True
        elif fruitReel.count("Orange") == 2:
            winnings,win = bet*3,True
        elif fruitReel.count("Cherry") == 2:
            winnings,win = bet*4,True
        elif fruitReel.count("Bar") == 2:
            winnings,win = bet*5,True
        elif fruitReel.count("Bell") == 2:
            winnings,win = bet*10,True
        elif fruitReel.count("Seven") == 2:
            winnings,win = bet*20,True
    
        # Match Lucky Seven
        elif fruitReel.count("Seven") == 1:
            winnings, win = bet*10,True
            
        else:
            winnings, win = bet*2,True
    if win:    
        credits += int(winnings)
    
        # Jackpot 1 in 450 chance of winning
        jackpotTry = random.randrange(1,51,1)
        jackpotWin = random.randrange(1,51,1)
        if  jackpotTry  == jackpotWin:
            jackpot = 500
    # No win
    else:
        print("PLACEHOLDER")
    
    return credits, jackpot, win, fruitReel

if __name__ == "__main__": main()
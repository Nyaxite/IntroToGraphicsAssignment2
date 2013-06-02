# Source File Name: SlotMachine.py
# Author's Name: Michael Burnie
# Last Modified By: Michael Burnie
# Date Last Modified: June 2, 2013
""" 
  Program Description:  This program simulates a Casino-Style Slot Machine. It provides an GUI
                        for the user that is an image of a slot machine with Label and Button objects
                        created through the tkinter module

  Version: 0.2      - Uses slotmachine_0_1.py base code
                    - Added GUI model with slot machine background
                    - Added button for spin
                    - Numbers appear in each slot representing the 8 different individual reel outcomes
                    - Many features still missing from base code
                    
"""

#I - Import and initialize
import pygame, random, Buttons

def main():
    
    pygame.init()
    
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)
    
    # Initial Values
    playerMoney =  1000
    jackpot =      500
    turn =         1
    bet =          0
    prevBet =      0
    winNumber =    0
    lossNumber =   0
    
    #D - Display configuration
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Hello, world!")
    
    #E - Entities (just background for now)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background = pygame.image.load("background_test.png")
    
    #A - Action (broken into ALTER steps)
    
        #A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    
    screen.blit(background, (0, 0))
    reel = [pygame.Surface((0, 0)), pygame.Surface((0, 0)), pygame.Surface((0, 0))]
    for spin in range(3):
        reel[spin] = pygame.Surface((0, 0))
        reel[spin] = background.convert()
        reel[spin] = pygame.image.load("Blank.png")
            
          
        #L - Set up main loop
    while keepGoing:
        
        clock.tick(30)
        
        reel = [pygame.Surface((0, 0)), pygame.Surface((0, 0)), pygame.Surface((0, 0))]
        for spin in range(3):
            reel[spin] = pygame.Surface((0, 0))
            reel[spin] = background.convert()
            reel[spin] = pygame.image.load("Blank.png")
            
        
        spinButton = Buttons.Button()
        #Parameters:             surface,    color,     x,   y,   length, height, width,    text,      text_color
        spinButton.create_button(screen, (107,142,35), 225, 400, 200,    100,    0,        "Spin!", (255,255,255))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if spinButton.pressed(pygame.mouse.get_pos()):
                    bet = 100
                    if bet > playerMoney:
                        print("Sorry, you only have $" + str(playerMoney) + " \n")
    
                    elif bet <= playerMoney:
                        turn +=1
                        prevBet = bet
                        playerMoney, jackpot, win, fruitReel = pullthehandle(bet, playerMoney, jackpot)
                                
                        for spin in range(3):
                            reel[spin] = pygame.Surface((0, 0))
                            reel[spin] = background.convert()
                            if fruitReel[spin] == 'Blank':
                                reel[spin] = pygame.image.load("Blank.png")
                            if fruitReel[spin] == 'Grapes':
                                reel[spin] = pygame.image.load("Grapes.png")
                            if fruitReel[spin] == 'Banana':
                                reel[spin] = pygame.image.load("Banana.png")
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
                            
                            x = 150
                            for spin in range(3):
                                screen.blit(reel[spin], (x*(spin + 1) - 50, 150))
        
       

        pygame.display.flip()  
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
#                 playerMoney, jackpot, win = pullthehandle(bet, playerMoney, jackpot)
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
#                 playerMoney, jackpot, win = pullthehandle(bet, playerMoney, jackpot)
    
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
    
    
    
    # Give the player some money if he goes broke
    if playerMoney <1:
        playerMoney = 500        

        
def Reels():
    """ When this function is called it determines the Bet_Line results.
        e.g. Bar - Orange - Banana """
        
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
            betLine[spin] = "Banana"
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

def is_number(bet):
    """ This function Checks if the Bet entered by the user is a valid number """
    try:
        int(bet)
        return True
    except ValueError:
        print("Please enter a valid number or Q to quit")
        return False

def pullthehandle(bet, playerMoney, jackpot):
    """ This function takes the Player's Bet, Player's Money and Current JackPot as inputs.
        It then calls the Reels function which generates the random Bet Line results.
        It calculates if the player wins or loses the spin.
        It returns the Player's Money and the Current Jackpot to the main function """
    playerMoney -= bet
    jackpot += (int(bet*.15)) # 15% of the player's bet goes to the jackpot
    win = False
    fruitReel = Reels()
    fruits = fruitReel[0] + " - " + fruitReel[1] + " - " + fruitReel[2]
    
    # Match 3
    if fruitReel.count("Grapes") == 3:
        winnings,win = bet*20,True
    elif fruitReel.count("Banana") == 3:
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
        if fruitReel.count("Banana") == 2:
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
        print(fruits + "\n" + "You Won $ " + str(int(winnings)) + " !!! \n")
        playerMoney += int(winnings)
    
        # Jackpot 1 in 450 chance of winning
        jackpotTry = random.randrange(1,51,1)
        jackpotWin = random.randrange(1,51,1)
        if  jackpotTry  == jackpotWin:
            print ("You Won The Jackpot !!!\nHere is your $ " + str(jackpot) + "prize! \n")
            jackpot = 500
        elif jackpotTry != jackpotWin:
            print ("You did not win the Jackpot this time. \nPlease try again ! \n")
    # No win
    else:
        print(fruits + "\nPlease try again. \n")
    
    return playerMoney, jackpot, win, fruitReel

if __name__ == "__main__": main()
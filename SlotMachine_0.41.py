# Source File Name: SlotMachine.py
# Author's Name: Michael Burnie
# Last Modified By: Michael Burnie
# Date Last Modified: June 6, 2013
""" 
  Program Description:  This program simulates a Casino-Style Slot Machine. It provides an GUI
                        for the user that is an image of a slot machine with Label and Button objects
                        created through the pygame module. The player can specify a bet of 10, 100 or 1000.
                        The player can then spin the reels or reset the game to defaults. Uses Simon Larson's Buttons.py.

  Version: 0.41       - Added comments
                      - Fixed spin image
                      - Changed winning jackpot background slightly
                      - Added external documentation
  
"""

#I - Import and initialize
import pygame, random, time, Buttons

#set global constants. These values do not change
FONT = pygame.font.SysFont("arial",30, 1)
SCREEN = pygame.display.set_mode((640, 480))
#color constants
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
#Coordinates for the location of the top-left corner of the: credit, bet, and jackpot text sections.
CREDITS_X = 114
CREDITS_Y = 280
BET_X = 305
BET_Y = 281
JACKPOT_X = 398
JACKPOT_Y = 281

'''
The main method deals with the mouse events required for the buttons, as well as instantiating main variables.
Many of the other methods are called from here.
'''
def main():
    #initialize pygame
    pygame.init()
    
    pygame.display.set_caption("Slot Machine!")
    
    #create the background and load the background image
    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()

    #initialize the clock variable, used for FPS and internal game timing
    clock = pygame.time.Clock()
    keepGoing = True #sentinel variable for game loop
    
    #declare reel
    reel = [pygame.Surface((0, 0)), pygame.Surface((0, 0)), pygame.Surface((0, 0))]
    
    # Initial Values
    credits =      1000
    jackpot =      500
    turn =         1
    bet =          100
    prevBet =      0 
    
    #setup the game's music
    volume = 0.2
    pygame.mixer.music.load('ttd00.mp3')
    pygame.mixer.music.play(-1, 0.0)#repeat
    pygame.mixer.music.set_volume(volume)
    
    #initialize each of the sounds by pulling the .ogg file
    playSpinSound = pygame.mixer.Sound("spin.ogg")
    playWinSound = pygame.mixer.Sound("win.ogg")
    playBetSound = pygame.mixer.Sound("bet.ogg")
    playResetSound = pygame.mixer.Sound("reset.ogg")
    playInvalidSpinSound = pygame.mixer.Sound("invalid_spin.ogg")
    playNoCreditsSound = pygame.mixer.Sound("no_credits.ogg")
    playJackpotSound = pygame.mixer.Sound("jackpot.ogg")
    
    #initialize each button in the GUI
    spinButton = Buttons.Button()
    resetButton = Buttons.Button()
    quitButton = Buttons.Button()
    bet10Button = Buttons.Button()
    bet100Button = Buttons.Button()
    bet1000Button = Buttons.Button()
    invalidSpinButton = Buttons.Button()  
        
    #set up a new game
    refreshGame(SCREEN, background, reel, credits, jackpot, turn, bet, prevBet)
    showButtons(spinButton, resetButton, quitButton, bet10Button, bet100Button, bet1000Button, invalidSpinButton)
 
    #The main loop for the game. The game continues to run while keepGoing = true
    while keepGoing:
        
        #set the game's FPS to 30
        clock.tick(30)

        #Listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False #end the game if the user closes the program. Necessary for IDLE as well.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if spinButton.pressed(pygame.mouse.get_pos()) and bet > credits:
                    #play the invalidSpinButton sound if the user tries clicking on the spin button with a bet > credits
                    playInvalidSpinSound.play() 
                elif spinButton.pressed(pygame.mouse.get_pos()) and bet <= credits:
                    #spin the reels...
                    
                    #play the spin sound
                    playSpinSound.play()

                    prevBet = bet#hold the value of bet in the previous bet variable
                    
                    #call the pullthehandle method, and get the required values
                    credits, jackpot, win, fruitReel, wonJackpot = pullthehandle(bet, credits, jackpot)
                   
                   #call the showReels method
                    showReels(reel, fruitReel, True)
                    
                    #if the player wins...
                    if win:
                        #if they also win the jackpot (very rare)
                        if wonJackpot:
                            
                            playJackpotSound.play()#play the jackpot sound
                            
                            #for the next section, the background will flip between 2 images,
                            #so the canvas must be rebuilt each time
                            oddFlip = True
                            for iterate in range(6): #flip the background 6 times...
                                
                                #instantiate the background, ready for the new background to be sent
                                background = pygame.Surface(SCREEN.get_size())
                                background = background.convert()
                                if(oddFlip):
                                    background = pygame.image.load("background jackpot 1-2.png")#set the background to the odd flip
                                    oddFlip = False
                                else:
                                    background = pygame.image.load("background jackpot 2-2.png")#set the background to the even flip
                                    oddFlip = True
                                SCREEN.blit(background, (0, 0))#blit the background
                                
                                showReels(reel, fruitReel, False)#call the showReels function to rebuild the reel images
                                
                                #show the credit, bet and jackpot values on the GUI again
                                showSection(credits, CREDITS_X, CREDITS_Y, "blank_credits.png")
                                showSection(bet, BET_X, BET_Y, "blank_bet.png")
                                showSection(jackpot, JACKPOT_X, JACKPOT_Y, "blank_jackpot.png")
                                pygame.display.flip()#flip the background
                                time.sleep(0.5)#0.5 second delay between flashes
                                
                            #refresh the game, sending in the new values as arguments and showing the buttons again
                            refreshGame(SCREEN, background, reel, credits, jackpot, turn, bet, prevBet)
                            showButtons(spinButton, resetButton, quitButton, bet10Button, bet100Button, bet1000Button, invalidSpinButton)                        
                        else:
                            playWinSound.play()#just play the win sound if the user did not win the jackpot, but won the round
   
                    else:#if the user lost...
                        if bet > credits:
                            #overwrite the spinButton with the invalidSpinButton as the player's current bet is greater than credits
                            invalidSpinButton.create_button(   SCREEN, (255,  0,  0), 475, 390, 75,    65,    0,        "Invalid Bet!", WHITE)
                            if credits == 0:#if the user run out of credits, play the out of credits sound. Basically game over
                                playNoCreditsSound.play()
                        
                    #refresh the credits and jackpot text sections on the GUI
                    showSection(credits, CREDITS_X, CREDITS_Y, "blank_credits.png")
                    showSection(jackpot, JACKPOT_X, JACKPOT_Y, "blank_jackpot.png")
                    
                elif resetButton.pressed(pygame.mouse.get_pos()): #if the reset button was clicked...
                    playResetSound.play()#play the reset sound
                    
                    #reset the variables
                    credits =      1000
                    jackpot =      500
                    turn =         1
                    bet =          100
                    prevBet =      0 
                    
                    #refresh the game, sending in the new values as arguments and showing the buttons again
                    refreshGame(SCREEN, background, reel, credits, jackpot, turn, bet, prevBet)
                    showButtons(spinButton, resetButton, quitButton, bet10Button, bet100Button, bet1000Button, invalidSpinButton)                        
                        
                elif quitButton.pressed(pygame.mouse.get_pos()):
                    keepGoing = False #quit the game loop, ending the game
                elif bet10Button.pressed(pygame.mouse.get_pos()): #bet 10 button was pressed...
                    bet = 10#set the bet to 10
                    clickBetButton(bet, credits, spinButton, invalidSpinButton, playBetSound)#play the bet sound
                elif bet100Button.pressed(pygame.mouse.get_pos()):
                    bet = 100#set the bet to 100
                    clickBetButton(bet, credits, spinButton, invalidSpinButton, playBetSound)
                elif bet1000Button.pressed(pygame.mouse.get_pos()):
                    bet = 1000#set the bet to 1000
                    clickBetButton(bet, credits, spinButton, invalidSpinButton, playBetSound)
        pygame.display.flip() #flip the display

'''
refreshGame accepts the primary values required to play the game to rebuild the GUI.
This method is called when the game starts, is restarted, or when a jackpot is won.

'''
def refreshGame(SCREEN, background, reel, credits, jackpot, turn, bet, prevBet): 
    
    background = pygame.image.load("background 2.png")#set the background image to the default image
    SCREEN.blit(background, (0, 0))#blit the background
    
    for spin in range(3):#set the reels to the default image (spin) and set the locatioon of each reel
        reel[spin] = pygame.Surface((0, 0))
        reel[spin] = background.convert()
        reel[spin] = pygame.image.load("Spin.png")
        SCREEN.blit(reel[spin], (135 * (spin + 1), 175))#coordinates
    
    #refresh the value sections of the GUI by calling the showSection() method
    showSection(credits, CREDITS_X, CREDITS_Y, "blank_credits.png")
    showSection(bet, BET_X, BET_Y, "blank_bet.png")
    showSection(jackpot, JACKPOT_X, JACKPOT_Y, "blank_jackpot.png")
    
    pygame.display.flip()#flip the display
    
'''
showButtons creates the buttons, calling the Buttons class from Buttons.py, created by Simon Larson.
Buttons are declared and sent in from main()
'''
def showButtons(spinButton, resetButton, quitButton, bet10Button, bet100Button, bet1000Button, invalidSpinButton):
    
    #Parameters:                surface,   color,     x,   y,   length, height, width,  text,      text_color
    spinButton.create_button(   SCREEN, (107,142, 35), 475, 390, 75,    65,    0,        "Spin!", WHITE)
    resetButton.create_button(  SCREEN, (150, 50, 50),  75, 390, 75,    65,    0,        "Reset", WHITE)
    quitButton.create_button(   SCREEN, (255,  0,  0), 600,   0, 40,    40,    0,        "Quit", WHITE)
    bet10Button.create_button(  SCREEN, (150,150,255), 175, 390, 75,    65,    0,        "Bet 10", WHITE)
    bet100Button.create_button( SCREEN, (125,125,255), 275, 390, 75,    65,    0,        "Bet 100", WHITE)
    bet1000Button.create_button(SCREEN, (100,100,255), 375, 390, 75,    65,    0,        "Bet 1000", WHITE)
    
    pygame.display.flip()#flip the display to show the buttons

'''
showReels places the reels in the GUI. It takes in the current bet line. It also takes in a boolean: showSpinAnimation,
which determines whether or not there should be a delay when this method is called and show the "spinning" image
during the delay.
'''
def showReels(reel, fruitReel, showSpinAnimation):
    
    if showSpinAnimation:#show the spin animation
        
        for spin in range(3):
            reel[spin] = pygame.image.load("Spinning.png")#change the image of the reels to the spinning picture
            SCREEN.blit(reel[spin], (135 * (spin + 1), 175))#blit the reels to show the spinning image
        
        pygame.display.flip()#flip the display
        time.sleep(1)#set a delay of 1 second during spin
    
    #show the different images on the screen depending on the bet line given (after showing the spinning if applicable)
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
        
        SCREEN.blit(reel[spin], (135 * (spin + 1), 175)) #blit the reel images                      

'''
clickBetButton is called if a bet button is clicked (10, 100, 1000). This function accepts the bet, the player's
current credits, and the two buttons it will change depending if the bet is a valid one.
'''
def clickBetButton(bet, credits, spinButton, invalidSpinButton, playBetSound):
    showSection(bet, BET_X, BET_Y, "blank_bet.png")#refresh the bet section of the GUI by calling the showSection() function
    playBetSound.play()#play the bet sound
    
    #determine if the player has enough credits for each click of the bet button
    #if they do not have enough credits, change the spin button to the invalid spin button by recreating the button each time
    if bet <= credits:
        spinButton.create_button(   SCREEN, (107,142, 35), 475, 390, 75,    65,    0,        "Spin!", WHITE)
    else:
        invalidSpinButton.create_button(   SCREEN, (255,  0,  0), 475, 390, 75,    65,    0,        "Invalid Bet!", WHITE)

'''
showSection is a crucial function used to refresh the text sections of the GUI. This refreshes the credits, bet, and 
jackpot text areas currently. It accepts the value it puts to the screen, the x and y coordinates for the section,
and the blankImage file to clear the current values first. Each section has a different-sized blank area.
'''
def showSection(value, x, y, blankImage):
    section = pygame.image.load(blankImage)#reset the current values on the GUI by placing a blank space over it
    SCREEN.blit(section,(x, y))#show this blank space by blit

    section = FONT.render(str(value), True, BLACK)#set the new text value by using the value sent in, and write on the blank space
    SCREEN.blit(section,(x, y))#blit this text

'''
Reels simply determines the outcome of the given reel/slot for a win/loss. It uses an array to generate 3 random values.
These reels determine the image file shown and the amount of credits the player wins if they win.
'''   
def Reels():
        
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
    """ This function takes the Player's Bet, Player's Money and Current JackPot as inputs.
        It then calls the Reels function which generates the random Bet Line results.
        It calculates if the player wins or loses the spin.
        It returns the Player's Money and the Current Jackpot to the main function """
def pullthehandle(bet, credits, jackpot):
   
    credits -= bet
    jackpot += (int(bet*.15)) # 15% of the player's bet goes to the jackpot
    win = False
    wonJackpot = False
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
            credits = jackpot + credits #add the jackpot credits to player
            jackpot = 500 #reset jackpot to 500
            wonJackpot = True
    
    return credits, jackpot, win, fruitReel, wonJackpot

if __name__ == "__main__": main() #call main
'''
Created on 2013-05-23

@author: Michael
'''
import random
def main():
    keepPlaying = 'y'
    while keepPlaying != 'q':
        randomNum = random.randrange(1, 7, 1)
        if randomNum == 1:
            print("=========") 
            print("|       |")
            print("|   0   |")
            print("|       |")
            print("=========") 
        elif randomNum == 2:
            print("=========") 
            print("| 0     |")
            print("|       |")
            print("|     0 |")
            print("=========") 
        elif randomNum == 3:
            print("=========") 
            print("| 0     |")
            print("|   0   |")
            print("|     0 |")
            print("=========") 
        elif randomNum == 4:
            print("=========") 
            print("| 0   0 |")
            print("|       |")
            print("| 0   0 |")
            print("=========") 
        elif randomNum == 5:
            print("=========") 
            print("| 0   0 |")
            print("|   0   |")
            print("| 0   0 |")
            print("=========") 
        elif randomNum == 6:
            print("=========") 
            print("| 0   0 |")
            print("| 0   0 |")
            print("| 0   0 |")
            print("=========")
        print "Keep playing? Press q to quit."
        keepPlaying = raw_input() 
    print("Thanks for playing!")
if __name__ == '__main__': main()
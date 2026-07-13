#Score Reset Program
import os, pickle, time
highScore=input("Do you want to reset your high score to the default?")
if highScore in ["Yes" , "Y" , "yes" , "yes" , "YES", "y"]:
    highScore = 0
    with open('highScore.pkl', 'wb') as f:
        pickle.dump(highScore, f)
        print("High score reset sucessfully")
        time.sleep(1)
        exit()
else:
    print("Ok - high score unchanged")
    time.sleep(1)
    exit()

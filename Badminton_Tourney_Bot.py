import math, time
from cmu_112_graphics import *
from Badminton_Tourney import *


def bot(app):

    #gets the landing x location of the shuttle right when its hit
    if app.newUserShot == True:
        app.returnToCenter = False
        app.nextShotX = getShuttleLandingX(app)
        app.botSwung = False
    
    #when there is no new shot, bot goes to the x landing of the current shot
    if app.nextShotX != None:
        if app.difficulty != 2:
            if ((app.newUserShot == False and app.botSwung == False) 
                or app.newUserShot == True):
                #move into position
                if app.player2.x < app.nextShotX + 5:
                    if app.difficulty == 0:
                        app.player2.moveX(0.25)
                    elif app.difficulty == 1:
                        app.player2.moveX(0.5)

                elif abs(app.player2.x - (app.nextShotX + 5)) < 1:
                    #when in position, call swing function
                    #which swings when the shuttle is near
                    botSwing(app)
                else:
                    if app.difficulty == 0:
                        app.player2.moveX(-0.25)
                    elif app.difficulty == 1:
                        app.player2.moveX(-0.5)
        
        #different for hard mode, as there is overhand but same concept
        else:
            
            if ((app.newUserShot == False and app.botSwung == False) 
                or app.newUserShot == True): 

                if app.willOverhand == False:
                    atPosition = True
                    if app.player2.overhand == True:
                        app.player2.changePosition()



                    if app.player2.y < 64.5:
                        app.player2.moveY(1)
                        atPosition = False
                    elif app.player2.y > 65.5:
                        app.player2.moveY(-1)
                        atPosition = False

                    if app.player2.x < app.nextShotX + 4.5:         
                        app.player2.moveX(1)
                        atPosition = False

                    elif app.player2.x > app.nextShotX + 5.5:
                        app.player2.moveX(-1)
                        atPosition = False
                        
                    if atPosition == True:
                        botSwing(app)

                else:
                    
                    atPosition = True
                    if app.player2.overhand == False:
                        app.player2.changePosition()

                    if app.player2.x < app.botOverhandX + 3.5:         
                        app.player2.moveX(1)
                        atPosition = False
                    elif app.player2.x > app.botOverhandX + 4.5:
                        app.player2.moveX(-1)
                        atPosition = False

                    if app.player2.y < app.botOverhandY + 5:
                        app.player2.moveY(2)
                        atPosition = False
                    elif app.player2.y > app.botOverhandY + 8:

                        app.player2.moveY(-2)
                        atPosition = False

                    if atPosition == True:
                        botSwing(app)


def returnToCenter(app):
    #only for hard mode
    atCenter = True

    if app.player2.x < 59:
        app.player2.moveX(1)
        atCenter = False
    
    elif app.player2.x > 61:
        app.player2.moveX(-1)
        atCenter = False

    if app.player2.y < 49:
        app.player2.moveY(1)

    elif app.player2.y > 51:
        app.player2.moveY(-1)

    if atCenter == True:
        app.returnToCenter = False

def botServe(app):

    app.timeSwing2 = time.time()
    app.player2.swing = True

def doSwing(app):
    if app.botSwingTimeSet == False:
        app.timeSwing2 = time.time()
        app.botSwingTimeSet = True
    app.player2.swing = True

def botSwing(app):
    #called when the bot is in position - only swings when shuttle is near
    if app.botSwung == False:

        if app.difficulty == 0:
            swingEasy(app)
        elif app.difficulty == 1:
            swingMedium(app)
        else:
            swingHard(app)

        

def swingEasy(app):

    if app.shuttle.y > 60 and app.shuttle.x > 51:
        doSwing(app)

def swingMedium(app):

    if app.player1.positionLastShot == 1: #underhand

        if 51 < app.shuttle.x < 62:

            if app.shuttle.y > 52.5:
                doSwing(app)
            
        elif 62 < app.shuttle.x < 73:

            if app.shuttle.y > 57.5:
                doSwing(app)

        elif 73 < app.shuttle.x < 84:

            if app.shuttle.y > 60:
                doSwing(app)

        elif 84 < app.shuttle.x < 95:

            if app.shuttle.y > 62.5:
                doSwing(app)
    else: #overhand
        if 51 < app.shuttle.x < 62:

            if app.shuttle.y > 55:
                doSwing(app)
            
        elif 62 < app.shuttle.x < 73:

            if app.shuttle.y > 63.5:
                doSwing(app)

        elif 73 < app.shuttle.x < 84:

            if app.shuttle.y > 65:
                doSwing(app)

        elif 84 < app.shuttle.x < 95:

            if app.shuttle.y > 67:
                doSwing(app) 
 
def swingHard(app):

    if app.willOverhand == False:
        swingMedium(app)

    else:

        if (app.player2.y - app.shuttle.y > 1
            and app.shuttle.x > 51 and app.player2.x > app.shuttle.x):
            doSwing(app)

               
    
def getShuttleLandingX(app):
    
    gravity = app.shuttle.gravity
    #loop to simulate the trajectory of the shuttle 
    #to get the x landing location
    while not (app.initialY > 65 and app.initialX > 51):

        #Checks if shuttle will hit into the net
        if ((49 < app.initialX < 53 and app.initialY > 56)
           or (app.initialX > 95.5 and app.initialY < 65)
           or (app.initialX < 49 and app.initialY > 81)):
            return None

        app.initialX += math.cos(app.shuttle.angle) * app.initialVelocity
        app.initialY -= math.sin(app.shuttle.angle) * app.initialVelocity
        app.initialY += gravity*app.height/815
        gravity += app.shuttle.gravityAcceleration*app.height/815
        if app.initialVelocity > 0:
            app.initialVelocity += app.shuttle.acceleration
        else:
            app.initialVelocity = 0

        if (app.initialY < 35 and abs(app.initialX - 55) < 1
            and app.initialVelocity < 1.4):
            app.willOverhand = True
            app.botOverhandX = app.initialX
            app.botOverhandY = app.initialY

    
    return app.initialX
    





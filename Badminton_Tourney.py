#Forest Ma
#CMU 15-112 Fall 2022 Term Project - Badminton Tourney

import math, time
from cmu_112_graphics import *
from Badminton_Tourney_Bot import *


##############################################
# helper functions for angles
##############################################

def radiansToDegrees(radians):
    return radians/(2*math.pi)*360

def simplifiedRadians(radians):
    if radians >= 0:
        return radians%(2*math.pi)
    else:
        return 2*math.pi - ((-radians)%(2*math.pi))

##############################################
# App Started - initialize all objects or variables
##############################################

def appStarted(app):

    initializeImages(app)

    #initialize players
    app.player1 = Player(True, 30, 65)
    app.player2 = Player(False, 70, 65)
    app.score = [0,0]

    #initialize shuttle
    app.shuttle = Shuttle(35, 67.5, app)

    #booleans for different pages
    app.timerDelay = 10
    app.startPage = True
    app.gamePage = False
    app.helpPage = False
    app.multiplayer = False
    app.singleplayerSelection = False

    #booleans for continuing the game after a point, starting game, etc.
    app.inPlay = False
    app.shot = False
    app.pointInterval = False
    app.gameStarted = False
    app.canSwing = True
    app.pointAwarded = False
    app.serve = True
    app.winner = None
    app.pointWinner = app.player1

    #initializations for the bot
    app.difficulty = None #0 is easy, 1 is medium, 2 is hard
    app.botNames = ['EASY BOT','MEDIUM BOT','HARD BOT']
    app.botStart = False
    app.newUserShot = False
    app.botSwingTimeSet = False
    app.botSwung = False
    app.player2Swung = False
    app.botOverhandY = None
    app.botOverhandX = None
    app.willOverhand = False
    app.returnToCenter = False

    app.gameOver = False

##############################################
# Creating a Player class which does all the main functions of the player
##############################################

class Player():
    def __init__(self, leftCourt, x, y):


        self.leftCourt = leftCourt

        #x and y out of 100
        self.x = x
        self.y = y

        #initialize starting angle of player/racket, 
        #in terms of top part of racket from angle 0
        if self.leftCourt == True:
            self.angle = 4*math.pi/3
        else:
            self.angle = 5*math.pi/3

        self.overhand = False
        self.positionLastShot = None #0 overhand, 1 underhand
        self.swing = False

    def __str__(self):
        if self.leftCourt == True:
            return 'Player 1'
        else:
            return 'Player 2'
    def changePosition(self):
        
        self.overhand = not self.overhand
        if self.leftCourt == True:
            
            if self.overhand == True:
                self.angle = 2*math.pi/3
            else:
                self.angle = 4*math.pi/3
        
        else:
            if self.overhand == True:
                self.angle = math.pi/3
            else:
                self.angle = 5*math.pi/3

    def moveX(self, n):
        self.x += n
    def moveY(self, n):
        self.y += n

    def drawPlayer(self, app, canvas):

        xunit = app.width/100
        yunit = app.height/100

        if self.leftCourt:

            canvas.create_image(self.x*xunit,self.y*yunit,
                image=ImageTk.PhotoImage(app.racketSprite.rotate(
                                        radiansToDegrees(self.angle))))


        else:
            canvas.create_image(self.x*xunit,self.y*yunit,
                image=ImageTk.PhotoImage(app.racketSprite.rotate(
                                        radiansToDegrees(self.angle))))

#Since both players can swing at the same time, we create two swing fuctions
#outside of the class
def swing1(app, player):


    if player.overhand == True:
        swingTime = time.time()
        if swingTime - app.timeSwing1 <= 0.3:
            player.angle = (2*math.pi/3 - 
                2*math.pi/3*(swingTime - app.timeSwing1)/0.3)


        elif 0.6 > swingTime - app.timeSwing1 > 0.3:
            player.angle = 2*math.pi/3*(((swingTime - app.timeSwing1)-0.3)/0.3)

        
        else:
            player.angle = 2*math.pi/3
            player.swing = False



    else:
        swingTime = time.time()
        if swingTime - app.timeSwing1 <= 0.3:
            player.angle = (4*math.pi/3 + 
                2*math.pi/3*(swingTime - app.timeSwing1)/0.3)


        elif 0.6 > swingTime - app.timeSwing1 > 0.3:
            player.angle = -2*math.pi/3*((swingTime - app.timeSwing1)-0.3)/0.3
        
        else:
            player.angle = 4*math.pi/3
            player.swing = False



def swing2(app, player):

    if player.overhand == True:
        swingTime = time.time()
        if swingTime - app.timeSwing2 <= 0.3:
            player.angle = (math.pi/3 + 
                2*math.pi/3*(swingTime - app.timeSwing2)/0.3)

        elif 0.6 > swingTime - app.timeSwing2 > 0.3:
            player.angle = (math.pi - 
                2*math.pi/3*(((swingTime - app.timeSwing2)-0.3)/0.3))
        
        else:
            player.angle = math.pi/3
            player.swing = False

            if app.multiplayer == False:
                app.botSwingTimeSet = False
                app.botSwung = True
                app.willOverhand = False
                app.returnToCenter = True

            
    else:
        swingTime = time.time()
        if swingTime - app.timeSwing2 <= 0.3:
            player.angle = (-math.pi/3 - 
                2*math.pi/3*(swingTime - app.timeSwing2)/0.3)


        elif 0.6 > swingTime - app.timeSwing2 > 0.3:
            player.angle = (math.pi + 
                2*math.pi/3*((swingTime - app.timeSwing2)-0.3)/0.3)
        
        else:
            
            player.angle = -math.pi/3
            player.swing = False
            if app.multiplayer == False:
                app.botSwingTimeSet = False
                app.botSwung = True
                app.returnToCenter = True

##############################################
# Creating a Shuttle class which does all the main functions of the shuttle
##############################################

class Shuttle():
    def __init__(self, x, y, app):

        self.x = x
        self.y = y
        self.velocity = 0 #pixels per second
        self.acceleration = 0 #change in velocity per frame
        self.gravity = 0
        self.gravityAcceleration = 0.015
        self.angle = 3*math.pi/2
        self.theta = 3*math.pi/2

    def rotateAngle(self, app):
        
        y = self.gravity-((math.sin(self.angle)) * self.velocity)
        x = math.cos(self.angle) * self.velocity
        if x != 0:
            self.angle = math.atan(y/x)

        
    def drawShuttle(self, app, canvas):

        xunit = app.width/100
        yunit = app.height/100
        canvas.create_image(self.x*xunit,self.y*yunit,
                            image=ImageTk.PhotoImage(app.shuttleSprite))

    def hitShuttle(self, app):
        #returns the player of which the shuttle was hit by, None if not hit
        #destructively modifies the angle of the shuttle

        xunit = app.width/100
        yunit = app.height/100

        #player 1
        
        racketHeadLength = math.sqrt((4.167*xunit)**2 + (12.396*yunit)**2)

        #distance from the bottom of racket head to the head of shuttle
        distance = math.sqrt(abs((app.player1.x-self.x)*xunit)**2 + 
                    abs((app.player1.y-self.y)*yunit)**2)


        #for the racket to hit, the shuttle must be inside the distance
        #of the top part of the racket to the bottom
        if distance <= racketHeadLength:
            
            if (self.x*xunit-app.player1.x*xunit) != 0:
                shuttleAngleToRacket = math.atan2((app.player1.y*yunit-
                    self.y*yunit),(self.x*xunit-app.player1.x*xunit)) 
                
                if abs(simplifiedRadians(shuttleAngleToRacket) - 
                            simplifiedRadians(app.player1.angle)) < math.pi/8:

                    if app.player1.overhand == True:
                        self.angle = app.player1.angle - math.pi/2
                        self.theta = self.angle
                    else:

                        self.angle = app.player1.angle + math.pi/2
                        self.theta = self.angle
    
                    return app.player1
            
        #player 2
        distance = math.sqrt(((app.player2.x-self.x)*xunit)**2 + 
                                    ((app.player2.y-self.y)*yunit)**2)
        if distance <= racketHeadLength + 5:
            if (self.x*xunit-app.player2.x*xunit) != 0:

                shuttleAngleToRacket = math.atan2((app.player2.y*yunit-
                            self.y*yunit),(self.x*xunit-app.player2.x*xunit))

                if abs(simplifiedRadians(shuttleAngleToRacket) - 
                    simplifiedRadians(app.player2.angle)) < math.pi/8:
             
                    if app.player2.overhand == True:
                        self.angle = app.player2.angle + math.pi/2
                        self.theta = self.angle
                    else:

                        self.angle = app.player2.angle - math.pi/2
                        self.theta = self.angle

                    return app.player2
                
    def moveShuttle(self, app):

        #move the shuttle object with self.theta
        self.x += (math.cos(self.theta)) * self.velocity
        self.y -= (math.sin(self.theta)) * self.velocity
        if app.shuttle.velocity > 0:
            app.shuttle.velocity += app.shuttle.acceleration
        if app.shuttle.velocity < 0:
            app.shuttle.velocity = 0
        

        #rotate the shuttle sprite with self.angle
        if (math.cos(self.theta)) * self.velocity != 0 :
            self.angle = math.atan2((math.sin(self.theta)-self.gravity/
                self.velocity),((math.cos(self.theta))))
        else:
            self.angle = 3*math.pi/2

    def doGravity(self, app):

        self.y += self.gravity*app.height/815
        self.gravity += self.gravityAcceleration*app.height/815
    
    def intoNet(self, app):
        
        #points the shuttle downwards at the net where it will eventually
        #hit the ground which we check for via the next method
        if 49 < self.x < 53 and self.y > 55:
            self.angle = 3*math.pi/2
            x = self.angle
            self.theta = x

    def intoGround(self):

        if self.y > 80:
            return True
        return False

    def awardPoint(self, app):

        if app.pointAwarded == False and app.serve == False:
            if (self.x < 5 or
            (self.x > 51 and self.x < 95)):
                app.score[0] += 1
                app.pointWinner = app.player1

            elif (self.x > 95 or
                self.x < 51 and self.x > 5):
                app.score[1] += 1
                app.pointWinner = app.player2
            app.pointAwarded = True
        
    def reposition(self, app):
        #repositions the shuttle based on the who the winner of the point was
        if app.pointWinner == app.player1:
            app.shuttle = Shuttle(35, 67.5, app)
            
            app.shuttle.angle = 3*math.pi/2
            app.shuttle.theta = 3*math.pi/2

        elif app.pointWinner == app.player2:
            app.shuttle = Shuttle(65, 67.5, app)
            app.shuttle.angle = 3*math.pi/2
            app.shuttle.theta = 3*math.pi/2
            
##############################################
# Timer fired does all the physics work, and is called every 10 ms
##############################################

def timerFired(app):

    app.racketSprite = app.scaleImage(app.racketSpriteOriginal, 
        1/7*app.width/1440)
    app.shuttleSprite = app.scaleImage(app.shuttleSpriteOriginal,
        1/6*app.width/1440)
    #rotate the shuttle to its angle every time
    app.shuttleSprite = app.shuttleSprite.rotate(
                                        radiansToDegrees(app.shuttle.angle))

    if app.gamePage == True and app.gameOver == False:

        if app.player1.swing == True:

            swing1(app, app.player1)
            if app.serve == False or (app.serve == True and app.shuttle.x < 50):
                app.inPlay = True
                app.serve = False
                app.pointInterval = False
                app.gameStarted = True

        if app.player2.swing == True:

            swing2(app, app.player2)
            if app.serve == False or (app.serve == True and app.shuttle.x > 50):
                app.inPlay = True
                app.serve = False
                app.pointInterval = False
                app.gameStarted = True
                app.player2Swung = True

        if app.inPlay == True:

            #only check for a shot if a swing is detected
            if (app.shot==False and 
            ((app.player1.swing==True and time.time()-app.timeSwing1<= .3)
            or (app.player2.swing==True and time.time()-app.timeSwing2<=0.3))):

           
            #returns None if there's no contact of shuttle (including in flight)
                hitShuttle = app.shuttle.hitShuttle(app)
                if hitShuttle != None:

                    app.shuttle.velocity = 2
                    app.shuttle.gravity = 0
                    app.shot = True
                    if hitShuttle.overhand == True:
                        
                        #makes the decelerate faster when the hit is overhand
                        app.shuttle.acceleration = -0.04
                        hitShuttle.positionLastShot = 0
                    else:
                        app.shuttle.acceleration = -0.025
                        hitShuttle.positionLastShot = 1

                    #for AI calculations:
                    
                    if app.multiplayer == False and hitShuttle == app.player1:
                        #if the user hits the shot
                        #store all variables of the shot for the bot
                        #to calculate location
                        
                        app.newUserShot = True
                        app.botStart = True
                        app.initialX = app.shuttle.x
                        app.initialY = app.shuttle.y
                        app.initialAngle = app.shuttle.angle
                        app.initialVelocity = app.shuttle.velocity
                                      
            if 49 < app.shuttle.x < 51:
                app.shot = False

            if app.shuttle.intoGround() == False:
                

                app.shuttle.intoNet(app)
                app.shuttle.moveShuttle(app)
                app.shuttle.doGravity(app)
            else:

                app.inPlay = False

        if app.inPlay == False and app.gameStarted == True:
            
            app.shuttle.awardPoint(app)
            nextPoint(app)

        if (app.multiplayer == False and app.botStart == True and 
            app.canSwing == True and app.inPlay):
            
            bot(app)
            if (app.difficulty == 2 and app.returnToCenter == True):

                returnToCenter(app)
            app.newUserShot = False
        if (app.multiplayer == False and app.serve == True and 
                    str(app.pointWinner) == 'Player 2'):
            botServe(app)
        

        gameOver(app)


def gameOver(app):

    #checks for game over with deuce at 11
    if app.score[0] >= 11 and app.score[0] > app.score[1] + 1:
        app.winner = app.player1
        app.gameOver = True
    
    if app.score[1] >= 11 and app.score[1] > app.score[0] + 1: 
        app.winner = app.player2
        app.gameOver = True

def nextPoint(app):

    #makes for a two second interval between points and resets everything
    if app.pointInterval == False:
        app.timeOfPointEnd = time.time()

        app.pointInterval = True
    
    else:

        if abs(time.time() - app.timeOfPointEnd) > 2 and app.serve == False:
            app.shuttle.reposition(app)
            app.player1 = Player(True, 30, 65)
            app.player2 = Player(False, 70, 65)
            app.serve = True
            app.inPlay = False
            app.shot = False
            app.canSwing = True
            app.pointAwarded = False
            app.nextShotX = None


            
            
        elif abs(time.time() - app.timeOfPointEnd) < 2:
            app.canSwing = False

##############################################
# User controls in keyPressed
##############################################

def keyPressed(app, event):

    if app.gameOver == False and app.canSwing == True and app.gamePage == True:
        if event.key == 'a':
            app.player1.moveX(-2)
        if event.key == 'd' and app.player1.x < 46:
            app.player1.moveX(2)
        if event.key == 'w':
            app.player1.moveY(-2)
            if app.player1.overhand == False and app.player1.swing == False:
                app.player1.changePosition()
        if event.key == 's':
            app.player1.moveY(2)
            if app.player1.overhand == True and app.player1.swing == False:
                app.player1.changePosition()
        if event.key == 'x':
            if app.player1.swing == False:
                app.timeSwing1 = time.time()            
                app.player1.swing = True

        #player 2
        if app.multiplayer == True:
            if event.key == 'j' and app.player2.x > 54:
                app.player2.moveX(-2)
            if event.key == 'l':
                app.player2.moveX(2)
            if event.key == 'i':
                app.player2.moveY(-2)
                if app.player2.overhand == False and app.player2.swing == False:
                    app.player2.changePosition()
            if event.key == 'k':
                app.player2.moveY(2)
                if app.player2.overhand == True and app.player2.swing == False:
                    app.player2.changePosition()
            if event.key == 'm':
                if app.player2.swing == False:
                    app.timeSwing2 = time.time()
                    app.player2.swing = True

##############################################
# mousePressed used for selection of game mode
##############################################
        
def mousePressed(app, event):

    xunit = app.width/100
    yunit = app.height/100

    if app.startPage == True:
        if (event.x > xunit*20 and event.x < xunit*40
           and event.y > yunit*50 and event.y < yunit*60):
            app.singleplayerSelection = True
            app.startPage = False
            event.x, event.y = 0,0

        elif (event.x > xunit*60 and event.x < xunit*80
            and event.y > yunit*50 and event.y < yunit*60):
            app.gamePage = True
            app.multiplayer = True
            app.startPage = False

        elif (event.x > xunit*2 and event.x < xunit*4
            and event.y > yunit*4 and event.y < yunit*6):

            app.helpPage = True
            app.startPage = False

    if app.startPage == False:
        
        #if home button clicked, reset everything
        if (event.x > xunit*95.3 and event.x < xunit*98.6
           and event.y > yunit*2.45 and event.y < yunit*7.36):
            appStarted(app)
    
        if app.gameOver == True:
            if (xunit*40 < event.x < xunit*60 and
                yunit*75 < event.y < yunit*85):
                appStarted(app)

    if app.singleplayerSelection == True:
        if (event.x > xunit*20 and event.x < xunit*40
            and event.y > yunit*50 and event.y < yunit*60):
            app.gamePage = True
            app.singleplayerSelection = False
            app.difficulty = 0 #easy
            app.multiplayer = False
        elif (event.x > xunit*60 and event.x < xunit*80
            and event.y > yunit*50 and event.y < yunit*60):
            app.gamePage = True
            app.singleplayerSelection = False
            app.difficulty = 1
            app.multiplayer = False

        elif (event.x > xunit*40 and event.x < xunit*60
            and event.y > yunit*70 and event.y < yunit*80):
            app.gamePage = True
            app.singleplayerSelection = False
            app.difficulty = 2
            app.multiplayer = False

##############################################
# draws everything
##############################################

def redrawAll(app, canvas):
    xunit = app.width/100
    yunit = app.height/100

    if app.startPage == True:

        drawStartPage(app, canvas)
    elif app.singleplayerSelection == True:
        
        drawSingleplayerSelection(app, canvas)
    elif app.gamePage == True:


        drawGameBackground(app, canvas)
        app.player1.drawPlayer(app, canvas)
        app.player2.drawPlayer(app, canvas)
        app.shuttle.drawShuttle(app, canvas)
        drawTop(app, canvas)
        drawScores(app, canvas)
        if app.winner != None:
            drawGameOver(app, canvas)
    elif app.helpPage == True:

        drawHelpPage(app, canvas)

    if app.startPage == False:
    #home button
        canvas.create_image(xunit*97, yunit*5, 
                        image=ImageTk.PhotoImage(app.homeButton))
                 
def drawTop(app, canvas):

    xunit = app.width/100
    yunit = app.height/100

    canvas.create_rectangle(3,3,99.7*xunit,12*yunit,fill='green',
                                                    outline='red',width=3)



    canvas.create_text(25*xunit,6*yunit,text='PLAYER 1',font='Helvetica 40',
                            fill='black')
    if app.multiplayer == False:
        canvas.create_text(75*xunit,6*yunit,
            text=f'{app.botNames[app.difficulty]}',font='Helvetica 40',
                            fill='black')
    else:
        canvas.create_text(75*xunit,6*yunit,text='PLAYER 2',font='Helvetica 40',
                            fill='black')
def drawScores(app, canvas):    
    xunit = app.width/100
    yunit = app.height/100
    canvas.create_text(25*xunit,25*yunit,text=f'{app.score[0]}',
        font='Helvetica 100')
    canvas.create_text(75*xunit,25*yunit,text=f'{app.score[1]}',
        font='Helvetica 100')

def drawHelpPage(app, canvas):

    xunit = app.width/100
    yunit = app.height/100

    canvas.create_image(50*xunit,50*yunit,
        image=ImageTk.PhotoImage(app.startBackground))
    canvas.create_text(xunit*25,yunit*30,text='Player 1:',
                                    font=f'Futura {int(app.width/30)}')
    canvas.create_text(xunit*25,yunit*40,text='WASD to move', 
                                    font=f'Futura {int(app.width/30)}')
    canvas.create_text(xunit*25,yunit*50,text='X to swing', 
                                    font=f'Futura {int(app.width/30)}')                                   
    canvas.create_text(xunit*75,yunit*30,text='Player 2:',
                                    font=f'Futura {int(app.width/30)}')
    canvas.create_text(xunit*75,yunit*40,text='IJKL to move',
                                    font=f'Futura {int(app.width/30)}')
    canvas.create_text(xunit*75,yunit*50,text='M to swing',
                                    font=f'Futura {int(app.width/30)}')
    canvas.create_text(xunit*50,yunit*70,
        text='Move down for underhand, move up for overhand',
            font=f'Futura {int(app.width/40)}')
def drawSingleplayerSelection(app, canvas):
    
    xunit = app.width/100
    yunit = app.height/100
    canvas.create_image(50*xunit,50*yunit,
        image=ImageTk.PhotoImage(app.startBackground))
    canvas.create_text(app.width/2,app.height/6,fill='black',
                    text='Singleplayer',font=f'Futura {int(app.width/25)}')
    canvas.create_rectangle(xunit*20,yunit*50,xunit*40,yunit*60,fill='yellow')


    canvas.create_rectangle(xunit*60,yunit*50,xunit*80,yunit*60,fill='yellow')

    canvas.create_rectangle(xunit*40,yunit*70,xunit*60,yunit*80,fill='yellow')

    canvas.create_text(xunit*30,yunit*55,text='EASY',
                                fill='red',font=f'Futura {int(app.width/40)}')
    canvas.create_text(xunit*70,yunit*55,text='MEDIUM',
                                fill='red',font=f'Futura {int(app.width/40)}')
    canvas.create_text(xunit*50,yunit*75,text='HARD',
                                fill='red',font=f'Futura {int(app.width/40)}')
def drawGameOver(app, canvas):
    xunit = app.width/100
    yunit = app.height/100
    if (app.multiplayer == True or 
        (app.multiplayer == False and app.winner == app.player1)):
        canvas.create_text(50*xunit,50*yunit,text=f'{str(app.winner)} wins!',
                        font=f'Helvetica {int(app.width/10)}',fill='Green')
    else:

        canvas.create_text(50*xunit,50*yunit,
            text=f'{app.botNames[app.difficulty]} wins!',
                        font=f'Helvetica {int(app.width/10)}',fill='Green')     
    canvas.create_rectangle(xunit*40,yunit*75,xunit*60,yunit*85,fill='yellow')
    canvas.create_text(xunit*50,yunit*80,text='HOME',fill='red',
                                        font=f'Futura {int(app.width/40)}')

    



def drawStartPage(app, canvas):
    xunit = app.width/100
    yunit = app.height/100
    canvas.create_rectangle(0,0,app.width,app.height,fill='green')
    canvas.create_image(50*xunit,50*yunit,
        image=ImageTk.PhotoImage(app.startBackground))
    canvas.create_text(app.width/2,app.height/6,fill='black',
                    text='Badminton Tourney',font=f'Futura {int(app.width/25)}')
    canvas.create_rectangle(xunit*20,yunit*50,xunit*40,yunit*60,fill='yellow')

    #singleplayer button
    canvas.create_rectangle(xunit*60,yunit*50,xunit*80,yunit*60,fill='yellow')
    #multiplayer button

    canvas.create_text(xunit*30,yunit*55,text='SINGLEPLAYER',
                                fill='red',font=f'Futura {int(app.width/40)}')
    canvas.create_text(xunit*70,yunit*55,text='MULTIPLAYER',
                                fill='red',font=f'Futura {int(app.width/40)}')


    canvas.create_image(xunit*3, yunit*5,
            image=ImageTk.PhotoImage(app.helpButton))


    


def drawGameBackground(app, canvas):
    xunit = app.width/100
    yunit = app.height/100
 
    canvas.create_rectangle(0,0,app.width,app.height,fill='light green')

    #court lines
    canvas.create_line(xunit*15,yunit*50,xunit*85,yunit*50,
                                                fill='black',width=5)
    canvas.create_line(xunit*5,yunit*80,xunit*95,yunit*80,
                                                fill='black',width=5)
    canvas.create_line(xunit*5,yunit*80.2,xunit*15,yunit*49.8,
                                                fill='black',width=5) 
    canvas.create_line(xunit*95,yunit*80.2,xunit*85,yunit*49.8,
                                                fill='black',width=5)
    canvas.create_line(xunit*40,yunit*50,xunit*41,yunit*80,
                                                fill='black',width=5)
    canvas.create_line(xunit*57,yunit*50,xunit*61,yunit*80,
                                                fill='black',width=5)
    
    
    #net pole, far side
    canvas.create_line(xunit*48,yunit*50,xunit*48,yunit*40,
                                                fill='blue',width=10)


    #net
    canvas.create_line(xunit*48,yunit*40,xunit*51,yunit*65,
                                                fill='white',width=2)
    canvas.create_line(xunit*48,yunit*42,xunit*51,yunit*67,
                                                fill='white',width=2)
    canvas.create_line(xunit*48,yunit*44,xunit*51,yunit*69,
                                                fill='white',width=2)         
    canvas.create_line(xunit*48,yunit*46,xunit*51,yunit*71,
                                                fill='white',width=2)
    
    #net pole, near side
    canvas.create_line(xunit*51,yunit*80,xunit*51,yunit*65,
                                                fill='blue',width=10)
                                            
def initializeImages(app):

    #https://www.shutterstock.com/image-vector/green-spotlight-abstract-background-eps10-vector-1535069894
    app.startBackground = app.loadImage('background.v1.jpg')


    #https://www.clipartmax.com/middle/m2H7d3K9i8G6K9Z5_home-button-image-black-home-icon-png/
    app.homeButton = app.loadImage('homeButton.png')
    app.homeButton = app.scaleImage(app.homeButton, 1/10)

    #https://www.nicepng.com/ourpic/u2e6a9a9y3i1e6i1_badminton-shuttlecock-png-background-image-badminton/
    app.shuttleSpriteOriginal = app.loadImage('shuttle.png')

    #drew myself
    app.racketSpriteOriginal = app.loadImage('racket.png')


    #https://thenounproject.com/icon/help-568541/
    app.helpButton = app.loadImage('help.png')
    app.helpButton = app.scaleImage(app.helpButton, 1/4)   
def playBadmintonTourney():
    runApp(width=1440,height=815)


def main():

    playBadmintonTourney()

if __name__ == '__main__':
    main()


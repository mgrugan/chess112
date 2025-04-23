from cmu_graphics import *
import subprocess

def onAppStart(app):
    app.logo = "/Users/mariogrugan/Documents/15-112/CHESS-112.png" #created this on canva.com with free canva graphics
    app.letters = '/Users/mariogrugan/Documents/15-112/letters.png'#created this on canva.com 
    app.background1 = '/Users/mariogrugan/Documents/15-112/background1.png' #created this gradient on canva.com with graphic
    

    app.buttonWidth = 300
    app.buttonHeight = 100

    app.pvpLeft = 920
    app.pvpTop = 548

    app.cvpLeft = 220
    app.cvpTop = 548

    app.dashesOnPvp = False
    app.dashesOnCvp = False
    
def redrawAll(app):                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    drawBackground(app)
    drawLetters(app)
    drawLogo(app)
    drawPVPButton(app)
    drawCVPButton(app)

def drawLetters(app):
    imageWidth, imageHeight = getImageSize(app.letters)

    coordX = ((app.width - imageWidth)//2)
    coordY = ((app.height - imageHeight)//2) - 250

    drawImage(app.letters, coordX, coordY)
def drawBackground(app):
    imageWidth, imageHeight = getImageSize(app.logo)
    newWidth = imageWidth//1.3
    newHeight = imageHeight//1.3
    
    drawImage(app.background1, 0, 0, width = newWidth, height= newHeight)
    # drawRect(0, 0, app.width, app.height, fill = rgb(97, 38, 163))



def drawLogo(app):
    imageWidth, imageHeight = getImageSize(app.logo)
    newWidth = imageWidth//3
    newHeight = imageHeight//3
    coordX = ((app.width - newWidth)//2)
    coordY = ((app.height - newHeight)//2) 

    drawImage(app.logo, coordX, coordY,width = newWidth, height= newHeight)

def drawPVPButton(app):
    drawRect(app.pvpLeft, app.pvpTop, app.buttonWidth, app.buttonHeight, 
            fill = 'purple', border = "white", dashes = app.dashesOnPvp)
    drawLabel("Player Vs. Player", app.pvpLeft + app.buttonWidth//2, 
              app.pvpTop  + app.buttonHeight//2, size = 35, fill = "white")


def drawCVPButton(app):

    drawRect(app.cvpLeft, app.cvpTop, app.buttonWidth, app.buttonHeight, 
             fill = 'purple',border = "white", dashes = app.dashesOnCvp)
    drawLabel("Computer Vs. Player", app.cvpLeft + app.buttonWidth//2,  
              app.cvpTop + app.buttonHeight//2, size = 31, fill = "white")
def onMouseMove(app, mouseX, mouseY):
    pvpRight = app.pvpLeft + app.buttonWidth
    pvpBottom = app.pvpTop + app.buttonHeight
    if (app.pvpLeft <= mouseX <= pvpRight) and (app.pvpTop <= mouseY <= pvpBottom):
        app.dashesOnPvp = True
    else:
        app.dashesOnPvp = False

    cvpRight = app.cvpLeft + app.buttonWidth
    cvpBottom = app.cvpTop + app.buttonHeight
    if (app.cvpLeft <= mouseX <= cvpRight) and (app.cvpTop <= mouseY <= cvpBottom):
        app.dashesOnCvp = True
    else:
        app.dashesOnCvp = False

def onMousePress(app, mouseX, mouseY):
    pvpRight = app.pvpLeft + app.buttonWidth
    pvpBottom = app.pvpTop + app.buttonHeight
    if (app.pvpLeft <= mouseX <= pvpRight) and (app.pvpTop <= mouseY <= pvpBottom):
        subprocess.Popen(['python3', '/Users/mariogrugan/Documents/15-112/pvpChess.py'], start_new_session=True) #https://www.youtube.com/watch?v=LTcmdZhrc00 learned about subprocess and for specific argument I found https://www.datacamp.com/tutorial/python-subprocess here
        exit()
    cvpRight = app.cvpLeft + app.buttonWidth
    cvpBottom = app.cvpTop + app.buttonHeight
    if (app.cvpLeft <= mouseX <= cvpRight) and (app.cvpTop <= mouseY <= cvpBottom):
        subprocess.Popen(['python3', '/Users/mariogrugan/Documents/15-112/cvpChess.py'], start_new_session=True) #https://www.youtube.com/watch?v=LTcmdZhrc00 learned about subprocess and for specific argument I found https://www.datacamp.com/tutorial/python-subprocess here
        exit()

def main():
    runApp(width=1500, height = 800)
main()
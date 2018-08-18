#coding: latin1

'''
@author: Lars Heppert
'''
import pygame, sys, math, datetime

windowMargin            = 30
windowWidth             = 600
windowHeight            = 600 #windowHeight
windowCenter            = windowWidth/2, windowHeight/2
clockMarginWidth        = 20
secondColor             = (255, 0, 0)
minuteColor             = (100, 200, 0)
hourColor               = (100, 200, 0)
clockMarginColor        = (130, 130, 0)
clockBackgroundColor    = (20, 40, 30)
backgroundColor         = (255, 255, 255)
hourCursorLength        = windowWidth/2.0-windowMargin-140
minuteCursorLength      = windowWidth/2.0-windowMargin-40
secondCursorLength      = windowWidth/2.0-windowMargin-10

virtualSpeed    = 100
useVirtualTimer = True

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            terminate()
            
def getCirclePoint(position, scale, cursorLength):
    degrees = getCursorPositionDegrees(position, scale)
    bogenmass = gradToBogenmass(degrees)
    xPos = round(math.cos(bogenmass)*cursorLength+windowCenter[0])
    yPos = round(math.sin(bogenmass)*cursorLength+windowCenter[1])
    return (xPos, yPos)

def gradToBogenmass(degrees):
    # python bietet auch die Funktion math.radians(degrees),
    # welche die Umrechnung genauso ausfuehrt, aber so wird 
    # der Sachverhalt deutlicher
    return degrees/180.0*math.pi

def getCursorPositionDegrees(position, scale):
    cursorOffset = -90 # 12 o'Clock is -90 degrees
    degrees = 360 / scale * position + cursorOffset
    return degrees

def drawCursor(color, width, length, position, scale):
    end = getCirclePoint(position, scale, length);
    pygame.draw.line(screen, color, windowCenter, end, width)
    
def drawBackground():
    screen.fill(backgroundColor)
    pygame.draw.ellipse(screen, clockMarginColor, (windowMargin, windowMargin, windowWidth-2*windowMargin, windowWidth-2*windowMargin))
    pygame.draw.ellipse(screen, clockBackgroundColor, (windowMargin+clockMarginWidth/2, windowMargin+clockMarginWidth/2, windowWidth-(windowMargin+clockMarginWidth/2)*2, windowWidth-(windowMargin+clockMarginWidth/2)*2))
    
def drawForeground():
    pygame.draw.ellipse(screen, clockMarginColor, (windowWidth/2.0-9, windowHeight/2.0-9, 18, 18))    

hour    = 8
minute  = 30
second  = 40
micro   = 0

# how to get the clock running counter-clockwise:
# instead of checking if the value is >60 check to see if it is <0.
# If that's the case, then instead of adding 1 to second, minutes etc., subtract
# 1 to give it a lesser value, thereby moving the clock backwards. 
def timeGoesOn():
    global hour, minute, second, micro
    micro += virtualSpeed
    if micro >= 2: # half seconds - not micro seconds
        second -= 1
        micro %= 2
    if second < 0:
        minute -= 1
        second %= 60
    if minute < 0:
        hour -= 1
        minute %= 60
    if hour > 12:
        hour %= 12

def drawCurrentTime():
    if useVirtualTimer:
        global hour, minute, second, micro
        timeGoesOn()
    else:
        now     = datetime.datetime.now()
        micro   = now.microsecond
        hour    = now.hour
        minute  = now.minute
        second  = now.second
        
    drawCursor(  hourColor, 15, hourCursorLength,   hour+minute/60.0, 12)
    drawCursor(minuteColor,  8, minuteCursorLength, minute+second/60.0, 60)
    drawCursor(secondColor,  3, secondCursorLength, second+micro/1000000.0, 60)

def terminate():
    pygame.quit()
    sys.exit(0)


def main():
    # Initialise screen
    global screen
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE | pygame.DOUBLEBUF);
    pygame.display.set_caption('Analog Clock');

    # Event loop
    while True:
        handleEvents()
        drawBackground()
        drawCurrentTime() 
        drawForeground()
        pygame.display.flip()
        pygame.time.delay(10)

if __name__ == '__main__':
    main()

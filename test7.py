from graphics import *
from random import *    

def matrise(img):

    bildematrise = []
    bredde = img.getWidth()
    høyde = img.getHeight()

    for i in range(høyde):
        bildematrise.append([])
        for j in range(bredde):
            bildematrise[i].append(img.getPixel(j,i))
        # End for.
    # End for.

    return bildematrise
    
def kopi(bildematrise):

    x = 0
    y = 90
    for  rad in range(10):
        for pixel in rad:
            bildematrise[rad][y + 10 + pixel] = bildematrise[rad][y + pixel]
    return bildematrise
            


def tegnkopi(img, bildematrise):
    x = 50
    y = 100
    for i in range(300):
        for j in range(300):
            minimatrise = bildematrise[x+j][y+i]
            img.setPixel(x+j+10,y+i,color_rgb(*minimatrise))
    
def hexcode(r,g,b):
    return "#%02x%02x%02x" % (r, g, b)      

def update(image, bildematrise):
    matrise = []
    for rad in bildematrise:
        radmatrise = []
        for pixel in rad:
            radmatrise.append(hexcode(*pixel))
        matrise.append("{ " + " ".join(radmatrise) + " }")
    image.img.put(" ".join(matrise))

def only_red(bildematrise):
    for x,row in enumerate(bildematrise):       
        for y,pixel in enumerate(row):
            r,_,_ = pixel
            bildematrise[x][y] = [r,0,0]           
    return bildematrise

def make_grey(bildematrise):
    for y,row in enumerate(bildematrise):
        for x,pixel in enumerate(row):
              _,g,_= pixel
              bildematrise[y][x] = [g,g,g]
    return bildematrise
              

def main():
    img = Image(Point(0, 0), 'bilde.gif')
    bredde = img.getWidth()
    høyde = img.getHeight()
    img.anchor = Point(bredde/2, høyde/2)
    win = GraphWin('Bilde', bredde, høyde)
    img.draw(win)

    bildematrise = matrise(img)
    #bildematrise = only_red(bildematrise)
    bildematrise = make_grey(bildematrise)
    update(img, bildematrise)
    win.update
    print('Kanskje')
#main()

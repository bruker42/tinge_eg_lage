"""Oblig 7
"""

from graphics import *
import time
class Filter:
    """
    Skal utføre operasjoner på bildet
    """
    def __init__(self, bilde, bildematrise, bredde, høyde, vindu):
        self.bilde = bilde
        self.bildematrise = bildematrise
        self.bredde = bredde
        self.høyde = høyde
        self.vindu = vindu
        self.historie = []
        self.save_state()

    def tidtaking(self, funksjon):
        """
        starttid = time.now()
        Å kjøre funksjon som funksjon,
        deltatid = time.now() - starttid
        save_state
        """
        None

    def save_state(self):
        self.historie.append(list(self.bildematrise))

    def load_state(self, i=0):
        self.bildematrise = self.historie[i]

    def save_file(self):
        None

    def increase_brigthness(self):
        None

    def decrease_brightness(self):
        None

    def flip(self):
        self.bildematrise=reversed(self.bildematrise)
        

    def mirror(self):
        None

    def blur(self):
        None

    def distort_colour(self):
        None

    def add_frame(self):
        None

    def keep_colour(self, colour='r'):
        for y,rad in enumerate(self.bildematrise):
            for x,pixel in enumerate(rad):
                 r,g,b = pixel
                 if colour == 'r':
                     g, b = 0, 0
                 elif colour == 'g':
                    r, b = 0, 0
                 else:
                     r, g = 0, 0
                 self.bildematrise[y][x] = [r,g,b]
                


    def increase_contrast(self):
        None

    def decrease_contrast(self):
        None

    def grayscale(self):
        None

    def pixelate(self):
        None

    def pop_art(self):
        None

    def complete_undo(self):
        None

    def sepia(self):
        None

    def timing(self):
        None

    def update(self):
        matrise = []
        for rad in self.bildematrise:
            radmatrise = []
            for pixel in rad:
               radmatrise.append(self.hexcode(*pixel))
            matrise.append("{ " + " ".join(radmatrise) + " }")
        self.bilde.img.put(" ".join(matrise))
        self.vindu.update

    def hexcode(self,r,g,b):
        return "#%02x%02x%02x" % (r, g, b)

class Kontroll:
    """
    Skal fordele funksjone til knapper i kontrollpanelet
    """
    def __init__(self):
        None
class Knapp:
    """
    Skal lager knapper
    """
    def __init__(self):
        None

def main(bildevalg='bilde.gif'):
    img = Image(Point(0, 0), bildevalg) 
    bredde = img.getWidth()
    høyde = img.getHeight()
    img.anchor = Point(bredde/2, høyde/2)
    vindu = GraphWin('Bilde', bredde, høyde)
    img.draw(vindu)
    
    bildematrise = []
    for y in range(høyde):
            bildematrise.append([])
            for x in range(bredde):
                bildematrise[y].append(img.getPixel(x, y))
    
    test = Filter(img, bildematrise, bredde, høyde, vindu)

    test.flip()
    test.update()
    test.load_state()
    test.update()

main()

    
    

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
        self.bilde.save('bilde.bmp')

    def undo(self):
        if len(self.historie) > 1:
            self.historie.pop()
            self.bildematrise = self.historie[-1]
            
    def fix_pixels(self):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                pixels = list(pixel)
                for i,val in enumerate(pixels):
                    if val > 255:
                        pixels[i] = 255
                    elif val < 0:
                        pixels[i] = 0
                self.bildematrise[y][x] = pixels[0], pixels[1], pixels[2]
        
    def increase_brigthness(self):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                r, g, b = pixel
                r += 10
                g += 10
                b += 10
                self.bildematrise[y][x] = r, g, b

    def decrease_brightness(self):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                r, g, b = pixel
                r -= 10
                g -= 10
                b -= 10
                self.bildematrise[y][x] = r, g, b
    
    def flip(self):
        self.bildematrise=reversed(self.bildematrise)

        
    def mirror(self):
        for y, rad in enumerate(self.bildematrise):
            self.bildematrise[y] = reversed(rad)

    def blur(self):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                teller, avg_r, avg_g, avg_b = 0, 0, 0, 0             
                for i in range(3):
                    for j in range(3):
                        if (y-i<0 or x-j<0) or (y-i>self.høyde or x-j>self.bredde):
                            teller += 1
                            avg_r += pixel[0]
                            avg_g += pixel[1]
                            avg_b += pixel[2]
                        #end if
                    #end for
                #end for
                avg_r, avg_g, avg_b = avg_r/teller, avg_g/teller, avg_b/teller
                self.bildematrise[y][x] = avg_r, avg_g, avg_b
                        

    def distort_colour(self):
        None

    def add_frame(self):
        None

    def keep_colour(self, colour='r'):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
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

    def update(self):
        self.fix_pixels()
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
        
def bilde_til_rgb_matrise(img):
    bredde = img.getWidth()
    høyde = img.getHeight()
    bildematrise = []
    for y in range(høyde):
            bildematrise.append([])
            for x in range(bredde):
                bildematrise[y].append(img.getPixel(x, y))
    return bildematrise
    
def main(bildevalg='bilde.gif'):
    img = Image(Point(0, 0), bildevalg) 
    bredde = img.getWidth()
    høyde = img.getHeight()
    img.anchor = Point(bredde/2, høyde/2)
    vindu = GraphWin('Bilde', bredde, høyde)
    img.draw(vindu)
    
    bildematrise = bilde_til_rgb_matrise(img)
    
    test = Filter(img, bildematrise, bredde, høyde, vindu)

    test.mirror()
    test.update()

#main()

    
    

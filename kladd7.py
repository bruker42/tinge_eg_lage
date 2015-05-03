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

    def tidtakning(self, funksjon, *args):
        start = time.time()
        funksjon(*args)
        self.save_state()
        self.update()
        deltatid = time.time() - start
        print(deltatid)

    def save_state(self):
        temp = []
        for rad in self.bildematrise:
            temp.append(list(rad))
        self.historie.append(list(temp))

    def load_state(self, i=0):
        temp = self.historie[i]
        self.bildematrise = []
        for rad in temp:
            self.bildematrise.append(list(rad))

    def save_file(self):
        self.bilde.save('nytt_bilde.gif')

    def undo(self):
        print(len(self.historie))
        if len(self.historie) > 1:
            self.historie.pop()
            self.load_state(-1)
            self.update()

    def fix_pixels(self):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                pixels = list(pixel)
                for i, valg in enumerate(pixels):
                    if valg > 255:
                        pixels[i] = 255
                    elif valg < 0:
                        pixels[i] = 0
                self.bildematrise[y][x] = pixels[0], pixels[1], pixels[2]

    def increase_brightness(self):
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
        self.bildematrise = list(reversed(self.bildematrise))

    def mirror(self):
        for y, rad in enumerate(self.bildematrise):
            self.bildematrise[y] = list(reversed(rad))

    def blur(self):
        for _ in range(2):
            for y, rad in enumerate(self.bildematrise):
                for x, pixel in enumerate(rad):
                    teller, avg_r, avg_g, avg_b = 0, 0, 0, 0            
                    for i in range(3):
                        for j in range(3):
                            if (y-1+i > 0 and x-1+j > 0) and (y-1+i < self.høyde and x-1+j < self.bredde):
                                teller += 1
                                hold_pixel = self.bildematrise[y-1+i][x-1+j]
                                avg_r += hold_pixel[0]
                                avg_g += hold_pixel[1]
                                avg_b += hold_pixel[2]
                            #end if
                        #end for
                    #end for                 
                    self.bildematrise[y][x] = avg_r/teller, avg_g/teller, avg_b/teller

    def distort_colour(self, skift=0.5):
        if skift > 1.0:
            raise Exception('Skiftverdi for høy')
        restdel = (1.0 - skift)/2
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                hold_r, hold_g, hold_b = pixel
                r = (hold_r * skift) + (hold_g * restdel) + (hold_b * restdel)
                g = (hold_r * restdel) + (hold_g * skift) + (hold_b * restdel)
                b = (hold_r * restdel) + (hold_g * restdel) + (hold_b * skift)
                self.bildematrise[y][x] = r, g, b

    def keep_colour(self, colour='r', y_start=None, x_start=None, høyde=1, bredde=1):
        if y_start == None and x_start == None:           
            for y, rad in enumerate(self.bildematrise):
                for x, pixel in enumerate(rad):
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    if colour == 'r':
                        g, b = 0, 0
                    elif colour == 'g':
                        r, b = 0, 0
                    else:
                        r, g = 0, 0
                    self.bildematrise[y][x] = r, g, b
        else:
            for y in range(høyde):
                for x in range(bredde):
                    r, g, b = self.bildematrise[y_start + y][x_start + x]
                    if colour == 'r':
                        g, b = 0, 0
                    elif colour == 'g':
                        r, b = 0, 0
                    else:
                        r, g = 0, 0
                    self.bildematrise[y_start + y][x_start + x] = r, g, b

    def change_contrast(self, faktor=1.6):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                r, g, b = pixel
                self.bildematrise[y][x] = r * faktor, g * faktor, b * faktor

    def grayscale(self):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                r, g, b = pixel
                luminanse = (r * 0.3) + (g * 0.59) + (b * 0.11)
                self.bildematrise[y][x] = luminanse, luminanse, luminanse

    def pixelate(self, radius=1):
        radius += 1
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                ##velger senter
                if (y % (1+radius) == 0) and (x % (1+radius) == 0):
                    for i in range(3+(2*(radius-1))):
                        for j in range(3+(2*(radius-1))):
                            ##Sjekker om pixel er gyldig
                            if (y - radius + i > 0 and x - radius + j > 0) and (y - radius + i < self.høyde and x - radius + j < self.bredde):
                                self.bildematrise[y-radius+i][x-radius+j] = self.bildematrise[y][x]
                  
    def pop_art(self):
        mini_matrise = self._del_matrise()
        mini_høyde = len(mini_matrise)
        mini_bredde = len(mini_matrise[0])
        for y, rad in enumerate(self.bildematrise):
            for x, _ in enumerate(rad):
                self.bildematrise[y][x] = mini_matrise[y%mini_høyde][x%mini_bredde]
        self.keep_colour('r', 0, mini_bredde, mini_høyde, mini_bredde)
        self.keep_colour('g', mini_høyde, 0, mini_høyde, mini_bredde)
        self.keep_colour('b', mini_høyde, mini_bredde, mini_høyde, mini_bredde)
     
    def _del_matrise(self):
        mini_matrise = []
        y_teller = 0
        for y, rad in enumerate(self.bildematrise):
            if y % 2 == 0:
                mini_matrise.append([])
            for x, pixel in enumerate(rad):
                if (y % 2 == 0) and (x % 2 == 0):
                    mini_matrise[y_teller].append(pixel)
            if y % 2 == 0:
                y_teller += 1
        return mini_matrise

    def complete_undo(self):
        self.bildematrise = self.historie[0]
        while len(self.historie) > 1:
            self.historie.remove(self.historie[1])

    def sepia(self, sepia=20):
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                r, g, b = pixel
                luminanse = (r * 0.3) + (g * 0.59) + (b * 0.11)
                self.bildematrise[y][x] = luminanse + sepia * 2, luminanse, luminanse - sepia

    def enkod(self, beskjed):
        tekst = Stenografi.enkod(beskjed)
        lengde = len(tekst)
        y = 0
        x = 0
        for c in tekst:
            r, g, b = self.bildematrise[y][x]
            if c == '0' and b % 2 == 1:
                if b == 255:
                    b -= 1
                else:
                    b += 1
            elif c == '1' and b % 2 == 0:
                b += 1
            self.bildematrise[y][x] = r, g, b
            x += 1
            if x >= self.bredde:
                y += 1
                x = 0

    def dekod(self):
        beskjed = ''
        for y, rad in enumerate(self.bildematrise):
            for x, pixel in enumerate(rad):
                r, g, b = pixel
                if b % 2 == 0:
                    beskjed += '0'
                elif b % 2 == 1:
                    beskjed += '1'
        dekodet = Stenografi.dekod(beskjed)
        print(dekodet)

    def update(self):
        self.fix_pixels()
        matrise = []
        for rad in self.bildematrise:
            radmatrise = []
            for pixel in rad:
                radmatrise.append(self.hexcode(*pixel))
            matrise.append("{ " + " ".join(radmatrise) + " }")
        self.bilde.img.put(" ".join(matrise))

    def hexcode(self, r, g, b):
        return "#%02x%02x%02x" % (r, g, b)


class Stenografi:

    @staticmethod
    def enkod(tekst):
        binær = ''
        for i in tekst:
             hold = bin(ord(i))[2:]
             binær += '0'*(8-len(hold))+hold
        lengde = len(binær)
        hold = bin(lengde)[2:]
        lengdestreng = '0'*(16-len(hold))+ hold
        return lengdestreng + binær

    @staticmethod
    def dekod(tekst):
        hode = tekst[:16]
        lengde = int(hode, 2)
        dekodet = ''
        for i in range(16, lengde + 16, 8):
            bit = chr(int(tekst[i:i+8], 2))
            dekodet += bit      
        return dekodet


class Kontroll:
    """
    Skal fordele funksjone til knapper i kontrollpanelet
    """
    def __init__(self, vindu):
        self.vindu = vindu
        self.knapper = [] 
        self.vindu.setCoords(0, 0, 100, 300)
        self.vindu.setMouseHandler(self.påklikk)
        self.y = 5
        self.x = 5

    def tegn(self):
        for knapp in self.knapper:
            knapp.tegn(self.vindu)

    def lag_knapp(self, tekst, funksjon,*args):
        self.knapper.append(Knapp(self.x , self.y, 40, 20, tekst, funksjon, *args))
        self.x += 50
        if self.x > 100:
            self.x = 5
            self.y += 25

    def lag_entry(self, x, y):
        self.knapper[-1].entry = Entry(Point(x, y), 40) 



    def påklikk(self, punkt):
        punkt = self.vindu.trans.world(punkt.getX(), punkt.getY())
        for i in self.knapper:
            i.påklikk(punkt[0], punkt[1], self.vindu)


class Knapp:
    """
    Skal lager knapper
    """
    def __init__(self, x, y, bredde, høyde, tekst, klikk, *args):
        self.x = x
        self.y = y
        self.bredde = bredde
        self.høyde = høyde
        self.tekst = tekst 
        self._klikk = klikk 
        self.args = args
        self.entry = None

    def tegn(self, vindu):
        self.boks = Rectangle(Point(self.x,self.y),Point(self.x+self.bredde,self.y+self.høyde))
        self.boks.setFill('White')
        knappetekst = Text(self.boks.getCenter(),self.tekst)
        self.boks.draw(vindu)
        knappetekst.draw(vindu)
        if self.entry != None:
            self.entry.draw(vindu)

    def påklikk(self, x, y, vindu):
        if (self.x< x < (self.x+self.bredde)) and (self.y < y < (self.y + self.høyde)):
            if self.entry != None:
                temp = self.args + (self.entry.getText(),)
                self._klikk(*temp)
            else:
                self._klikk(*self.args)



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
     
    kontrollpanel = GraphWin('Kontrollpanel', 400, 400)
    kontroller = Kontroll(kontrollpanel)
    kontroller.lag_knapp('Avslutt', exit)
    kontroller.lag_knapp('Start om', test.tidtakning, test.complete_undo)
    kontroller.lag_knapp('Flip', test.tidtakning, test.flip)
    kontroller.lag_knapp('Speil', test.tidtakning, test.mirror)
    kontroller.lag_knapp('Blur', test.tidtakning, test.blur)
    kontroller.lag_knapp('Vreng farger', test.tidtakning, test.distort_colour)
    kontroller.lag_knapp('Øk lysstyrke', test.tidtakning, test.increase_brightness)
    kontroller.lag_knapp('Mink lysstyrke', test.tidtakning, test.decrease_brightness)
    kontroller.lag_knapp('Gjør grå', test.tidtakning, test.grayscale)
    kontroller.lag_knapp('Sepia', test.tidtakning, test.sepia)
    kontroller.lag_knapp('Endre kontrast', test.tidtakning, test.change_contrast)
    kontroller.lag_knapp('Pixeler', test.tidtakning, test.pixelate)
    kontroller.lag_knapp('Pop art', test.tidtakning, test.pop_art)
    kontroller.lag_knapp('Kun rød', test.tidtakning, test.keep_colour)
    kontroller.lag_knapp('Lagre', test.tidtakning, test.save_file)
    kontroller.lag_knapp('Angre', test.undo)
    kontroller.lag_knapp('Dekod', test.tidtakning, test.dekod)
    kontroller.lag_knapp('Enkod', test.tidtakning, test.enkod)
    kontroller.lag_entry(50, 270)
    kontroller.tegn()

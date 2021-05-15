####################################################################
##### 	  CHUTE DE FLOCON DE NEIGE AVEC VITESSE DIFFERENTES	   #####
#####	  AVEC OSCILLATIONS ET ACCUMULATION DES FLOCONS 	   #####
#####     INTERFACE GRAPHIQUE : PYGAME                         #####
####################################################################

import random
import sys
import pygame
import pygame.gfxdraw
from pygame.locals import *


class FloconNeige:
    def __init__(self, largeur, hauteur, couleur):

        self.largeur = largeur
        self.hauteur = hauteur
        self.rayon = 2
        self.couleur = couleur
        self.gravite = random.uniform(9,15)
        self.position = [random.randint(0, self.largeur-200), 20]
        self.enabled = True
        self.vent = 0

    def update(self, temps, flocon_limite):
        if self.enabled:
            speed = (self.gravite * temps)/100
            if not self.collision(flocon_limite):
                self.position[1] += speed

            else:
                self.position[1] += 0.0004
                self.vent = 0
            if self.position[0] >= 700:
                self.position[0] = 1
            elif self.position[0] <= 0:
                self.position[0] = 698
            self.position[0] += self.vent

    def collision(self, flocon_limite):
        #Verification des collisions
        x = int(self.position[0])
        y = self.position[1]
        r = self.rayon
        points = flocon_limite[x-r:x+r]
        for p in points:
            if y + r >= p:
                for i in range(x-r, x+r):
                    if i >= 0 and i < self.largeur:
                        flocon_limite[i] = y
                return True

        #Verifier si le flocon arrive en bas
        if self.position[1] >= self.hauteur:
            return True
        else:
            return False

    def creation(self, surface):
        pygame.gfxdraw.filled_circle(surface, int(self.position[0]), int(self.position[1]), self.rayon, self.couleur)

    def creationNuages(largeur, surface):
        couleur = (245, 245, 245)
        r = 40
        r2 = 48
        x = r
        x2 = 0
        y = int(-r/1.8) + 5
        y2 = int(-r2/1.7)
        p = int(largeur/(2*r))
        compteur = 0
        while compteur <= p :
            pygame.gfxdraw.filled_circle(surface, x , y, r, couleur)
            pygame.gfxdraw.filled_circle(surface, x2 , y2, r2, couleur)
            x += 2*r
            x2 += 2*r + 1
            compteur += 1


class PyGame:
    force_vent = 0
    def __init__(self, largeur, hauteur, titre=""):
        # plethora of fields
        self.largeur = largeur
        self.hauteur = hauteur
        self.titre = titre
        self.IPS = 65
        self.couleur_flocon = (255, 255, 255)
        self.couleur_fond = (0, 0, 0)
        self.listeFlocon = []
        self.compteur_flocon = 0
        self.vit_apparition = 40
        self.hauteur = hauteur
        self.largeur = largeur
        self.flocon_limite = [self.hauteur] * self.largeur #Pour dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tecter la collision
        self.force_vent = 0
        self.text_onoff = True
        self.initialisation()
        self.loop()

    def initialisation(self): #Initialisation de PyGame
        pygame.init()
        pygame.display.set_caption(self.titre)
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.font = pygame.font.Font("police.ttf", 20) #Police d'affichage du compteur de flocons

    def loop(self):
        self.clock = pygame.time.Clock()
        while 1:
            temps = self.clock.get_time()
            self.update(temps)
            self.render(temps)
            self.clock.tick(self.IPS)

    def update(self, temps):
        if self.compteur_flocon > self.vit_apparition:
            self.compteur_flocon = 0
            flocondeneige = FloconNeige(self.largeur, self.hauteur, self.couleur_flocon)
            self.listeFlocon.append(flocondeneige)
        else:
            self.compteur_flocon += 1

        for flocondeneige in self.listeFlocon:
            if flocondeneige.enabled:
                flocondeneige.vent = self.force_vent
            flocondeneige.update(temps, self.flocon_limite)

        #Afficher le compteur de flocons avec saisi clavier
        if self.text_onoff:
            self.afficher_nb = self.font.render("FLocons : %d" % len(self.listeFlocon), 1, (9,27,157))
        self.saisi_clavier(pygame.event.get())


    def render(self, temps):
        surface = pygame.Surface(self.fenetre.get_size())
        surface.convert()
        surface.fill(self.couleur_fond)
        FloconNeige.creationNuages(700,surface)
        widgetBoutons = pygame.image.load("fond boutons.png").convert()
        surface.blit(widgetBoutons, (700,0))
        for flocondeneige in self.listeFlocon:
            flocondeneige.creation(surface)

        if self.text_onoff:
            surface.blit(self.afficher_nb, (8, 0))
        self.fenetre.blit(surface, (0, 0))
        pygame.display.flip()

    def saisi_clavier(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.text_onoff = False if self.text_onoff else True
                if event.key == pygame.K_z:
                    pygame.time.wait(5000)

            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1 and event.pos[0] > 730 and event.pos[0] < 770 and event.pos[1] > 70 and event.pos[1] < 110:
                    if self.vit_apparition > 10 :
                        self.vit_apparition-=5
                    else :
                        self.vit_apparition-=1
                if event.button == 1 and event.pos[0] > 830 and event.pos[0] < 870 and event.pos[1] > 70 and event.pos[1] < 110:
                    if self.vit_apparition > 10 :
                        self.vit_apparition+=5
                    else :
                        self.vit_apparition+=1
                if event.button == 1 and event.pos[0] > 730 and event.pos[0] < 770 and event.pos[1] > 180 and event.pos[1] < 230:
                    self.force_vent -= 0.2
                if event.button == 1 and event.pos[0] > 830 and event.pos[0] < 870 and event.pos[1] > 180 and event.pos[1] < 230:
                    self.force_vent += 0.2
                if event.button == 1 and event.pos[0] > 770 and event.pos[0] < 830 and event.pos[1] > 180 and event.pos[1] < 230:
                    self.force_vent = 0
                if event.button == 1 and event.pos[0] > 725 and event.pos[0] < 790 and event.pos[1] > 320 and event.pos[1] < 380:
                    self.vit_apparition = 0
                if event.button == 1 and event.pos[0] > 815 and event.pos[0] < 870 and event.pos[1] > 320 and event.pos[1] < 380:
                    self.vit_apparition += 10000000
                if event.button == 1 and event.pos[0] > 770 and event.pos[0]< 840 and event.pos[1] > 430 and event.pos[1] < 480 :
                    self.listeFlocon = []
                    self.flocon_limite = [self.hauteur] * self.largeur


if __name__ == "__main__":
    game = PyGame(900, 500, "Flocons de neige")


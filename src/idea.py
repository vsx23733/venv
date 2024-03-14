import pygame

def draw_bars(self, win):
    # Dessiner la barre de mesure 1 en rouge
    pygame.draw.rect(win, (255, 0, 0), (10, 10, 100, 10))
    # Dessiner la partie remplie de la barre de mesure 1 en vert
    pygame.draw.rect(win, (0, 255, 0), (10, 10, self.mesure1, 10))
    # Dessiner un cadre blanc autour de la barre de mesure 1
    pygame.draw.rect(win, (255, 255, 255), (10, 10, 100, 10), 1)
    # Dessiner la barre de mesure 2 en bleu
    pygame.draw.rect(win, (0, 0, 255), (10, 30, 100, 10))
    # Dessiner la partie remplie de la barre de mesure 2 en jaune
    pygame.draw.rect(win, (255, 255, 0), (10, 30, self.mesure2, 10))
    # Dessiner un cadre blanc autour de la barre de mesure 2
    pygame.draw.rect(win, (255, 255, 255), (10, 30, 100, 10), 1)



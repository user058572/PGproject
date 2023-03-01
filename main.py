import pygame

from platformerhabrahabr import Game
pygame.init()
g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
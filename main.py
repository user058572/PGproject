import pygame #файл для запуска

from Game import Game
pygame.init()
g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
#p.s тимур не трогай!!!!
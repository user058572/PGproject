#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from blocks import *
from monsters import *
from menu import *
import time

#Объявляем переменные
WIN_WIDTH = 850 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"
minim = 10000
FILE_DIR = os.path.dirname(__file__)

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel(a, b):

    global playerX, playerY
    levelFile1 = open(a)
    line = " "
    global minim
    while line[0] != "e":
        line = levelFile1.readline()
        level.append(line[0:len(line) - 1])
        if len(line) != 1:
            minim = min(len(line), minim)
    levelFile2 = open(b)
    line = " "
    while line[0] != "e":
        line = levelFile2.readline()
        chars = line.split()
        if chars[0] == 'player':
            playerX, playerY = int(chars[1]), int(chars[2])
        elif line[0] != "e":
            x, y, speedu, speedd, maxl, maxu = map(int, [chars[1], chars[2], chars[3],chars[4], chars[5], chars[6]])
            mn = Monster(x, y, speedu, speedd, maxl, maxu)

            entities.add(mn)
            platforms.append(mn)
            monsters.add(mn)

class Game():
    def __init__(self):
        size = (WIN_WIDTH, WIN_HEIGHT)
        self.level = 1
        self.screen = pygame.display.set_mode(size)
        self.display = Surface(size)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = WIN_WIDTH, WIN_HEIGHT

        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.main_menu = MainMenu(self)
        self.levelmenu = LevelsMenu(self)
        self.curr_menu = self.main_menu
        self.main_menu.display_menu()





    def game_loop(self):
        global level

        while self.playing:

            self.check_events()
            level = []

            flag = 1
            platforms = []
            size = (WIN_WIDTH, WIN_HEIGHT)
            entities = pygame.sprite.Group()
            animatedEntities = pygame.sprite.Group()
            monsters = pygame.sprite.Group()
            if self.level:
                loadLevel('first.txt', 'characters.txt')
            else:
                print("Добавьте уровень")
                self.playing = 0
                break
            pygame.init()

            pygame.display.set_caption("The BEST game in the world")
            monsters.update(platforms)

            def load_image(name, colorkey=None):
                fullname = name
                return pygame.image.load(fullname).convert()
            image = load_image("fon.jpg")
            self.display.blit(image, [0, -100])
            left = right = False
            up = False
            hero = Player(playerX, playerY, self)
            entities.add(hero)

            timer = pygame.time.Clock()
            x = y = 0
            for i in range(len(level) - 1):  # заполнение спрайт групп, забей
                for j in range(len(level[i]) - 1):
                    abo = level[i][j]
                    if abo != " ":
                        if abo == '-':
                            cy = Platform(x, y)
                        if abo == "*":
                            cy = BlockDie(x, y)
                        if abo == "P":
                            print(1)
                            cy = Princess(x, y)
                        entities.add(cy)
                        platforms.append(cy)
                    x += PLATFORM_WIDTH
                y += PLATFORM_HEIGHT
                x = 0

            level_width = minim * PLATFORM_WIDTH - 1
            level_height = len(level) * PLATFORM_HEIGHT

            camera = Camera(camera_configure, level_width, level_height)
            monsters.update(platforms)
            flag = 1
            while not hero.winner and flag:
                timer.tick(60)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                        pygame.quit()
                    elif event.type == KEYDOWN and event.key == K_0:
                        self.START_KEY = 1
                        flag = 0
                        break

                    elif event.type == KEYDOWN:
                        if event.key == K_LEFT:
                            left = 1
                        elif event.key == K_RIGHT:
                            right = 1
                        elif event.key == K_UP:
                            up = 1
                    elif event.type == KEYUP:
                        if event.key == K_LEFT:
                            left = 0
                        elif event.key == K_RIGHT:
                            right = 0
                        elif event.key == K_UP:
                            up = 0
                self.screen.blit(self.display, (0, 0))
                animatedEntities.update()
                monsters.update(platforms)
                camera.update(hero)
                hero.update(left, right, up, platforms)
                for e in entities:
                    self.screen.blit(e.image, camera.apply(e))
                pygame.display.update()


            self.playing = False
            self.display.fill(self.BLACK)

            if hero.winner:
                self.draw_text('You win', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()
            else:
                self.draw_text('Thanks for Playing', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()

            timing = time.time()
            while True:
                if time.time() - timing > 1.0:
                    break

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)


level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться


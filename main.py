import pygame
from pygame.locals import *
import dataLoad
import map
import gameStatus
import mine
import enemy
import gun
import battleField
import scorecount
import sys

SCR_RECT = Rect(0, 0, 1440, 810)
TITLE, PLAY, GAMEOVER = 0, 1, 2
SAVEFILE = "Data/save"

class Main:
    count = 0
    highscore = 0
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("GAME")

        self.init_mixer()
        self.init_game()
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update(screen)
            self.infoUpdate()
            self.key_handler()
            pygame.display.update()
            
    def init_game(self):
        '''ゲームの初期化'''
        self.count = 0
        self.game_state = TITLE
        self.all = pygame.sprite.RenderUpdates()
        self.mineCollige = pygame.sprite.Group()
        self.enemyCollige = pygame.sprite.Group()
        self.mineBulletsCollige = pygame.sprite.Group()
        self.enemyBulletsCollige = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.loadSaveData()

        mine.Mine.containers = self.all, self.mineCollige
        map.Block.containers = self.all, self.blocks
        enemy.Enemy.containers = self.all, self.enemyCollige
        gun.Bullet1.containers = self.all, self.enemyBulletsCollige
        gun.MyBullet.containers = self.all, self.mineBulletsCollige

        self.map = map.Map("Data/MAP.map", self.all, SCR_RECT, GS=32)
        self.mine = mine.Mine((200, 600), self.blocks, "Data/YELLOW.bmp")
        self.scorecount = scorecount.ScoreCount()
        self.cursor = 520

    def update(self, screen):
        if self.game_state == TITLE:
            gameStatus.gametitle_draw(screen, self.cursor, self.highscore)

        elif self.game_state == PLAY:
            battleField.generation()
            self.collideBullets()
            self.map.update(screen, self.mine)
            self.map.draw()
            self.scorecount.draw(screen)
            time05 = pygame.time.get_ticks() % 30
            if pygame.time.get_ticks() % 60 == 0:
            #if  (time05 >= 27 and time05 <= 30) or (time05 >= 0 and time05 <= 3):
                self.scorecount.addScore(1)

        elif self.game_state == GAMEOVER:
            gameStatus.gameover_draw(screen, self.scorecount.getScore())
        
    def key_handler(self):
        '''キー入力受付'''
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit()
            if self.game_state == TITLE:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if self.cursor == 520:
                            self.init_game()
                            self.game_state = PLAY
                        elif self.cursor == 610:
                            self.quit()
                    if event.key == K_UP and self.cursor != 520:
                        self.cursor -= 90
                    if event.key == K_DOWN and self.cursor != 610:
                        self.cursor += 90
            if self.game_state == GAMEOVER:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if self.highscore < self.scorecount.getScore():
                            self.highscore = self.scorecount.getScore()
                        self.init_game()
                        self.game_state = TITLE

    def infoUpdate(self):
        '''条件を満たしていれば、ゲーム状態を変更する'''
        if self.liveOrDie():
            self.game_state = GAMEOVER
        if self.shootDown():
            self.scorecount.addScore(50)

    def shootDown(self):
        collide = pygame.sprite.groupcollide(self.mineBulletsCollige, self.enemyCollige, True, True)
        for enemy in collide.keys():
            return 1
        return 0

    def liveOrDie(self):
        collide = pygame.sprite.groupcollide(self.mineCollige, self.enemyBulletsCollige, False, False)
        for enemy in collide.keys():
            return 1
        collide = pygame.sprite.groupcollide(self.mineCollige, self.enemyCollige, False, False)
        for enemy in collide.keys():
            return 1
        if self.mine.rect.y > 1000:
            return 1
        return 0

    def collideBullets(self):
        collide = pygame.sprite.groupcollide(self.blocks, self.enemyBulletsCollige, False, True)
        for enemy in collide.keys():
            pass

    def init_mixer(self):
        pygame.mixer.quit()
        pygame.mixer.init(buffer=1024)

    def loadSaveData(self):
        with open(SAVEFILE, mode='r') as file:
            f = file.readline()
            if self.highscore < int(f):
                self.highscore = int(f)

    def quit(self):
        with open(SAVEFILE, mode='w') as file:
            f = file.write(str(self.highscore))
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main()
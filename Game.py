import pygame
import time
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_e,
    K_i,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("2DGameRpg/sprites/Player.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.inventory = []

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    # def openInventory(self):
    #     global invcheck
    #     if invcheck == False:
    #         invcheck = True
    #         all_sprites.add(inv)
    #         x = inv.rect.x + 30
    #         y = inv.rect.y + 30
    #         for item in self.inventory:
    #             if x > inv.rect.x + 480:
    #                 x = inv.rect.x + 30
    #                 y += 60







class Item(pygame.sprite.Sprite):
    def __init__(self):
        super(Item, self).__init__()
    def Update(self):
        
        collisionCheck(player, sword)

class Sword(Item):
    def __init__(self):
        super(Sword, self).__init__()
        self.surf = pygame.image.load("2DGameRpg new/sprites/Sword.png")
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(center = (200,200))
        self.type = "Sword"

class InventoryBack(pygame.sprite.Sprite):
    def __init__(self):
        super(InventoryBack, self).__init__()
        self.surf = pygame.Surface((500, 500))
        self.surf.fill((92, 92, 87))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

def collisionCheck(obj1, obj2):
    if (obj1.rect.x + obj1.surf.get_width()) > obj2.rect.x and obj1.rect.x < (obj2.rect.x + obj2.surf.get_width()) and (obj1.rect.y + obj1.surf.get_height()) > obj2.rect.y and obj1.rect.y < (obj2.rect.y + obj2.surf.get_width()):
        return True

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
sword = Sword()
inv = InventoryBack()

running = True

invcheck = False

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(sword)

while running:
    
    for event in pygame.event.get():
       
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
        
    screen.fill((135, 206, 250))

    pressed_keys = pygame.key.get_pressed()

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    player.update(pressed_keys)

    sword.Update()

    pygame.display.flip()

    clock.tick(30)
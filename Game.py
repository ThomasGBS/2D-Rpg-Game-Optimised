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
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Player.png").convert()
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
        

    def openInventory(self):
        global invcheck
        if not invcheck:
            invcheck = True
            all_sprites.add(inv)
            x = inv.rect.x + 30
            y = inv.rect.y + 30
            for item in self.inventory:
                if x > inv.rect.x + 480:
                    x = inv.rect.x + 30
                    y += 60
                item.rect = newitem.surf.get_rect(center = (x, y))
                item.surf = pygame.transform.scale(newitem.surf, (50,50)).convert()
                all_sprites.add(item)
                all_items.add(item)
                x += 60
        elif invcheck:
            all_sprites.remove(inv)

            for item in player.inventory:
                item.kill()
            
            invcheck = False



class Item(pygame.sprite.Sprite):
    def __init__(self):
        super(Item, self).__init__()
    def Update(self, pressedKeys):
        if collisionCheck(player, self) and not invcheck and not self.inv:
            all_text.add(self.pickup)
            if pressedKeys[K_e] and len(player.inventory) < 64:
                all_text.remove(self.pickup)
                player.inventory.append(self)
                self.index = len(player.inventory) - 1
                self.inv = True
                self.kill()
        elif not collisionCheck(player, self) and not invcheck:
            all_text.remove(self.pickup)
        
        if hoverCheck(self) and invcheck and self.inv:
            if not self.hover:
                self.surf.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD) 
                self.hover = True
        
        #if hoverCheck(self) and pygame.mouse.get_pressed([0]) and invcheck and self.inv

        elif not hoverCheck(self):
            self.hover = False


class Sword(Item):
    def __init__(self):
        super(Sword, self).__init__()
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Sword.png")
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
        self.type = "Sword"
        self.pickup = Text("E", 25, (254,254,254), (self.rect.centerx + 10, self.rect.centery - 30), self)
        self.inv = False
        self.hover = False
    def Update(self, pressedKeys):

        super(Sword, self).Update(pressedKeys)


class InventoryBack(pygame.sprite.Sprite):
    def __init__(self):
        super(InventoryBack, self).__init__()
        self.surf = pygame.Surface((500, 500))
        self.surf.fill((92, 92, 87))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

class Text(pygame.sprite.Sprite):
    def __init__(self, txt, size, color, position, parent = 0):
        super(Text, self).__init__()
        self.font = pygame.font.Font("2D-Rpg-Game-Optimised/CenturyGothic.ttf", size)
        self.text = self.font.render(txt, True, color, (254,254,254))
        self.text.set_colorkey((255,255,255))
        self.rect = (position)
        self.parent = parent


def collisionCheck(obj1, obj2):
    if (obj1.rect.x + obj1.surf.get_width()) > obj2.rect.x and obj1.rect.x < (obj2.rect.x + obj2.surf.get_width()) and (obj1.rect.y + obj1.surf.get_height()) > obj2.rect.y and obj1.rect.y < (obj2.rect.y + obj2.surf.get_width()):
        return True
    else:
        return False
def hoverCheck(obj):
    x, y = pygame.mouse.get_pos()
    if (obj.rect.x + obj.surf.get_width()) > x and obj.rect.x < x and (obj.rect.y + obj.surf.get_height()) > y and obj.rect.y < y:
        return True
    else:
        return False


clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
inv = InventoryBack()

ADDITEM = pygame.USEREVENT + 1
pygame.time.set_timer(ADDITEM, 1000)

running = True

invcheck = False

all_text = pygame.sprite.Group()
all_items = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)

while running:
    
    for event in pygame.event.get():
       
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_i:
                player.openInventory()

        elif event.type == QUIT:
            running = False
        
        elif event.type == ADDITEM and not invcheck:
            if len(all_items) < 5:
                newitem = Sword()
                all_items.add(newitem)
                all_sprites.add(newitem)
        
    screen.fill((135, 206, 250))

    pressed_keys = pygame.key.get_pressed()

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)
    for text in all_text:
        screen.blit(text.text, text.rect)

    player.update(pressed_keys)

    for item in all_items:
        item.Update(pressed_keys)

    pygame.display.flip()

    clock.tick(30)
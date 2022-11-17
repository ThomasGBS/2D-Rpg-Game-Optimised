import pygame
import time
import random
import math

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

playerx, playery = -20, 0

tiles = ['GrassBig', 'CobbelBig', 'CobbelBigBorder']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1,],
    [1, 0, 0, 0, 1, 0, 0, 1,],
    [1, 0, 0, 0, 1, 1, 0, 1,],
    [1, 1, 1, 0, 0, 0, 0, 1,],
    [1, 1, 1, 0, 1, 0, 0, 1,],
    [1, 1, 1, 0, 1, 0, 0, 1,],
    [1, 0, 0, 0, 0, 0, 0, 1,],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

TILE_SIZE = 128
SCREEN_WIDTH = TILE_SIZE * 4 + 100
SCREEN_HEIGHT = TILE_SIZE * 4 + 50

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Player.png").convert()
        self.surf = pygame.transform.scale(self.surf, (70, 100))
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.inventory = []
        self.hand = None
        self.attacking = False
        self.dir = "down"


    def update(self, pressed_keys):
        global wait

        if self.hand != None:
            if self.dir == "down":
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx + 45, player.rect.centery + 45))
            if self.dir == "up":
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx + 45, player.rect.centery + 45))
            if self.dir == "left":
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx - 15, player.rect.centery + 45))
            if self.dir == "right":
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx + 45, player.rect.centery + 45))

            if not self.hand in all_sprites:
                all_sprites.add(self.hand)
            if pygame.mouse.get_pressed()[0] and not invcheck and self.hand.rotation == 0 and time.time() > wait + 0.5:
                wait = time.time()
                self.hand.rotation -= 40
                self.hand.surf = pygame.transform.rotate(player.hand.surf, self.hand.rotation)
                self.attacking = True
            elif time.time() > wait + 0.3:
                self.hand.surf = pygame.image.load(f"2D-Rpg-Game-Optimised/sprites/{self.hand.type}.png").convert()
                self.hand.surf.set_colorkey((255,255,255))
                self.hand.rotation = 0
                self.attacking = False
                self.hand.slash = None
            if self.attacking and not invcheck:
                self.hand.slash = Empty(self.hand.rect.x + 65,self.hand.rect.y + 30,"2D-Rpg-Game-Optimised/sprites/Slash.png")
                self.hand.slash.surf.set_colorkey((0,0,0))
                screen.blit(pygame.transform.flip(self.hand.slash.surf, True, False), self.hand.slash.rect)
                
        if not invcheck:
            if pressed_keys[K_UP]:
                self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/PlayerUp.png").convert()
                self.surf = pygame.transform.scale(self.surf, (70, 100))
                self.surf.set_colorkey((255,255,255), RLEACCEL)
                move(0,-5)
                self.dir = "up"

            if pressed_keys[K_DOWN]:
                self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Player.png").convert()
                self.surf = pygame.transform.scale(self.surf, (70, 100))
                self.surf.set_colorkey((255,255,255), RLEACCEL)
                move(0,5)
                self.dir = "down"

            if pressed_keys[K_LEFT]:
                self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/PlayerLeft.png").convert()
                self.surf = pygame.transform.scale(self.surf, (70, 100))
                self.surf.set_colorkey((255,255,255), RLEACCEL)
                move(-5,0)
                self.dir = "left"

            if pressed_keys[K_RIGHT]:
                self.surf = pygame.transform.flip(pygame.image.load("2D-Rpg-Game-Optimised/sprites/PlayerLeft.png"), True, False).convert()
                self.surf = pygame.transform.scale(self.surf, (70, 100))
                self.surf.set_colorkey((255,255,255), RLEACCEL)
                move(5,0)
                self.dir = "right"

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
            for text in all_text:
                text.kill()

            invcheck = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Slime.png")
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH + 200, 200))

    def Update(self):
        x, y = self.rect.x, self.rect.y
        pX = player.rect.centerx
        pY = player.rect.centery

        dist = math.hypot(pX-x, pY-y)

        if dist < 200: 
            busy = False
            for row in range(len(maze)):
                for column in range(len(maze[row])):
                    tilex = column * TILE_SIZE + playerx
                    tiley = row * TILE_SIZE + playery
                    tile = tiles[maze[row][column]]
                    if tile == "CobbelBig":
                        if self.rect.x + self.surf.get_width() - (x-pX) / 30 > tilex and self.rect.x < tilex - (x-pX) / 30 + TILE_SIZE and self.rect.y + self.surf.get_height() - (y-pY) / 30 > tiley and self.rect.y - (y-pY) / 30  < tiley + TILE_SIZE:
                            busy = True
            if not busy:
                self.rect.x -= (x-pX) / 50
                self.rect.y -= (y-pY) / 50 


        # angle = math.atan2(targetX, targetY)
        # dx = math.cos(angle) * 3
        # dy = math.sin(angle) * 3
        # self.rect.x += dx
        # self.rect.y +=  dy

        # disX = (x-pX)
        # disY = (y-pY)
        # difx = disX / disY
        # dify = disY / disX
        # self.rect.x -= 1 / difx
        # self.rect.y -= 1 / dify
        

        if player.hand != None and not invcheck and player.hand.slash != None:
            if collisionCheck(player.hand.slash, self):
                self.kill()

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super(Item, self).__init__()
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Sword.png")
        self.surf.set_colorkey((255,255,255))
        self.die = False

        ranx = random.randint(0, SCREEN_WIDTH)
        rany = random.randint(0, SCREEN_HEIGHT)

        clones = 0

        for row in range(len(maze)):
            for column in range(len(maze[row])):
                x = column * TILE_SIZE + playerx
                y = row * TILE_SIZE + playery
                tile = tiles[maze[row][column]]
                if tile == "CobbelBig":
                    if ranx + self.surf.get_width() > x and ranx < x + TILE_SIZE and rany + self.surf.get_height() > y and rany < y + TILE_SIZE:
                        if clones == 0:
                            newitem = Sword()
                            self.die = True
                            clones += 1
                            break
                        
        self.rect = self.surf.get_rect(center = (ranx, rany))
        self.pickup = Text("E", 25, (0,0,0), (self.rect.centerx + 10, self.rect.centery - 30), self)
        self.inv = False
        self.hover = False
        self.clicked = False
        if not self.die:
            all_items.add(self)
            all_sprites.add(self)

    def Update(self, pressedKeys):
        if self.die:
            self.kill()
            return
        global wait
        if collisionCheck(player, self) and not invcheck and not self.inv:
            all_text.remove(self.pickup)
            self.pickup = Text("E", 25, (0,0,0), (self.rect.centerx + 10, self.rect.centery - 30), self)
            all_text.add(self.pickup)
            if pressedKeys[K_e] and len(player.inventory) < 64:
                all_text.remove(self.pickup)
                player.inventory.append(self)
                self.index = len(player.inventory) - 1
                self.inv = True
                self.kill()
        elif not collisionCheck(player, self) and not self.inv or invcheck and not self.inv:
            all_text.remove(self.pickup)
        
        if hoverCheck(self) and invcheck and self.inv:
            if not self.hover:
                self.surf.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD) 
                self.hover = True
        
        if pygame.mouse.get_pressed()[0] and hoverCheck(self) and invcheck and self.inv and time.time() > wait + 0.2 and not textHover(self.pickup):
            if self.clicked == True:
                self.clicked = False
                all_text.remove(self.pickup)
            else:
                self.pickup = Text("Drop", 25, (254,254,254), (self.rect.centerx + 10, self.rect.centery - 30), self)
                all_text.add(self.pickup)
                self.clicked = True

            wait = time.time()

        elif not hoverCheck(self) and invcheck and self.inv and not textHover(self.pickup):
            self.hover = False
            self.surf = pygame.image.load(f"2D-Rpg-Game-Optimised/sprites/{self.type}.png").convert()
            self.surf.set_colorkey((255,255,255))
        
        if textHover(self.pickup) and pygame.mouse.get_pressed()[0] and invcheck and time.time() > wait + 0.2 and self.pickup in all_text:
            wait = time.time()

            self.surf = pygame.image.load(f"2D-Rpg-Game-Optimised/sprites/{self.type}.png").convert()
            self.surf.set_colorkey((255,255,255))
            self.rect = player.surf.get_rect(center = (player.rect.centerx, player.rect.centery))
            self.pickup = Text("E", 25, (0,0,0), (self.rect.centerx, self.rect.centery - 70), self)
            self.inv = False

            all_items.add(self)

            player.inventory.pop(self.index)
            self.pickup.kill()
            
            for item in player.inventory:
                if item.index > self.index:
                    item.index -= 1
            
            player.openInventory()
            player.openInventory()
            

class Sword(Item):
    def __init__(self):
        super(Sword, self).__init__()
        self.type = "Sword"
        self.pickup2 = Text("Equip", 25, (255,255,255), (self.rect.centerx + 10, self.rect.centery - 10), self)
        self.slash = None

    def Update(self, pressedKeys):
        global wait
        if pygame.mouse.get_pressed()[0] and hoverCheck(self) and invcheck and self.inv and time.time() > wait + 0.2 and not textHover(self.pickup) and self in all_sprites:
            if self.clicked:
                all_text.remove(self.pickup2)
            elif not self.clicked:
                self.pickup2 = Text("Equip", 25, (255,255,255), (self.rect.centerx + 10, self.rect.centery - 10), self)
                all_text.add(self.pickup2)
        if textHover(self.pickup) and pygame.mouse.get_pressed()[0] and invcheck and time.time() > wait + 0.2:
            self.pickup2.kill() 
        if textHover(self.pickup2) and pygame.mouse.get_pressed()[0] and invcheck and time.time() > wait + 0.2 and self in all_sprites and self.clicked:
            if player.hand == None:
                wait = time.time()

                self.surf = pygame.image.load(f"2D-Rpg-Game-Optimised/sprites/{self.type}.png").convert()
                self.surf.set_colorkey((255,255,255))
                
                player.hand = self
                self.rotation = 0

                player.inventory.pop(self.index)
                self.kill()
                self.pickup.kill()
                self.pickup2.kill()

                for item in player.inventory:
                    if item.index > self.index:
                        item.index -= 1
                
                player.openInventory()
                player.openInventory()
            else:
                print("cant equip")

        super(Sword, self).Update(pressedKeys)

class InventoryBack(pygame.sprite.Sprite):
    def __init__(self):
        super(InventoryBack, self).__init__()
        self.surf = pygame.Surface((400, 400))
        self.surf.fill((92, 92, 87))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

class Text(pygame.sprite.Sprite):
    def __init__(self, txt, size, color, position, parent = 0):
        super(Text, self).__init__()
        self.font = pygame.font.Font("2D-Rpg-Game-Optimised/CenturyGothic.ttf", size)
        self.text = self.font.render(txt, True, color, (255,255,255))
        self.text.set_colorkey((255,255,255))
        self.rect = (position)
        self.parent = parent

class Empty(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.surf = pygame.image.load(img).convert()
        self.rect = self.surf.get_rect(center = (x,y))

def move(nr1,nr2):
    global playerx
    global playery
    busy = False
    # for tile in all_cobbel:
    #     if player.rect.x + player.surf.get_width() + nr1 > tile.x and player.rect.x + nr1 < tile.x + TILE_SIZE and player.rect.y + player.surf.get_height() + nr2 > tile.y and player.rect.y + nr2 < tile.y + TILE_SIZE:#x + TILE_SIZE > player.rect.x and x < player.rect.x + player.surf.get_width() and y + TILE_SIZE + 5 > player.rect.y and y + 5 < player.rect.y + player.surf.get_height():
    #         busy = True
    #         print("ow")
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE + playerx
            y = row * TILE_SIZE + playery
            tile = tiles[maze[row][column]]
            if tile == "CobbelBig":
                if player.rect.x + player.surf.get_width() + nr1 > x and player.rect.x + nr1 < x + TILE_SIZE and player.rect.y + player.surf.get_height() + nr2 > y and player.rect.y + nr2 < y + TILE_SIZE:#x + TILE_SIZE > player.rect.x and x < player.rect.x + player.surf.get_width() and y + TILE_SIZE + 5 > player.rect.y and y + 5 < player.rect.y + player.surf.get_height():
                    busy = True
    if not busy:
        playerx -= nr1
        playery -= nr2
        for entity in all_sprites:
            if entity != player and entity != player.hand:    
                entity.rect.x -= nr1
                entity.rect.y -= nr2


def draw():
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE + playerx
            y = row * TILE_SIZE + playery
            tile = tiles[maze[row][column]]
            # tile = pygame.sprite.Sprite()
            # tile.tiles = tiles[maze[row][column]]
            # tile.num = ((row + 1) * 8) - (8-(column + 1))
            # tile.x = x
            # tile.y = y
            # if tile.tiles == "GrassBig":
            #     check = 0
            #     for block in all_grass:
            #         if tile.num == block.num:
            #             check += 1
            #             block = tile
            #     if check == 0:
            #         all_grass.append(tile)

            # if tile.tiles == "CobbelBig":
            #     check = 0
            #     for block in all_cobbel:
            #         if tile.num == block.num:
            #             block = tile
            #             check += 1
            #     if check == 0:
            #         all_grass.append(tile)
            
            screen.blit(pygame.image.load(f"2D-Rpg-Game-Optimised/sprites/{tile}.png"), (x, y))

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
def textHover(obj):
    x, y = pygame.mouse.get_pos()
    xpos, ypos = obj.rect
    width, height = obj.font.size("Drop")
    if xpos + width > x and xpos < x and ypos + height > y and ypos < y:
        return True
    else:
        return False


clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
inv = InventoryBack()
enemy = Enemy()

ADDITEM = pygame.USEREVENT + 1
pygame.time.set_timer(ADDITEM, 1000)

running = True

invcheck = False

all_text = pygame.sprite.Group()
all_items = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_grass = []
all_cobbel = []

all_sprites.add(player)
all_sprites.add(enemy)

wait = time.time()

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
                # all_items.add(newitem)
                # all_sprites.add(newitem)
        
    screen.fill((0, 0, 0))

    draw()

    pressed_keys = pygame.key.get_pressed()

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)
    for text in all_text:
        screen.blit(text.text, text.rect)

    player.update(pressed_keys)
    enemy.Update()


    for item in all_items:
        item.Update(pressed_keys)

    pygame.display.flip()

    clock.tick(30)
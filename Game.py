import pygame
import time
import random
import math
import socket
import mysql.connector

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
#pygame.init() er for åstarte pygame sånn at du kan begynne å kjøre pygame koden
pygame.init()

#her kobler jeg til my sql databasen min
PlayerData = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="2d rpg game db"
)
#her lager jeg cursor som kan redigere og hante ding fra databasen
dbCursor = PlayerData.cursor()

#dette er alle tilsene i levlene
tiles = ['GrassBig', 'CobbelBig', 'CobbelBigBorder']

#her lager jeg alle levlene med array
tutoriallvl = [
    [1, 1, 1, 1, 1, 1, 1, 1,],
    [1, 0, 0, 0, 1, 0, 0, 1,],
    [1, 0, 0, 0, 1, 1, 0, 1,],
    [1, 1, 1, 0, 0, 0, 0, 1,],
    [1, 1, 1, 0, 1, 0, 0, 1,],
    [1, 1, 1, 0, 1, 0, 0, 1,],
    [1, 0, 0, 0, 0, 0, 0, 1,],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
level1 = [
    [1, 1, 1, 1, 1, 1, 1, 1,],
    [1, 0, 1, 0, 0, 0, 0, 1,],
    [1, 0, 1, 0, 0, 0, 0, 1,],
    [1, 0, 1, 0, 0, 0, 0, 1,],
    [1, 0, 1, 0, 1, 0, 0, 1,],
    [1, 0, 1, 1, 1, 0, 0, 1,],
    [1, 0, 0, 0, 0, 0, 0, 1,],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
level2 = [
    [1, 1, 1, 1, 1, 1, 1, 1,],
    [1, 0, 0, 1, 1, 0, 0, 1,],
    [1, 0, 0, 1, 1, 0, 0, 1,],
    [1, 0, 0, 0, 0, 0, 0, 1,],
    [1, 0, 0, 0, 0, 0, 0, 1,],
    [1, 0, 0, 1, 1, 0, 0, 1,],
    [1, 0, 0, 1, 1, 0, 0, 1,],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

TILE_SIZE = 128
SCREEN_WIDTH = TILE_SIZE * 4 + 100
SCREEN_HEIGHT = TILE_SIZE * 4 + 50

#dette er player classen. player classen inheriter fra pygame.sprite.Sprite() classen
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
        self.health = 100

    #dette er update funksjonen til player klassen som blir callet hver frame af spiller.
    def update(self, pressed_keys):
        global wait
        global running
        if self.health <= 0:
            print("died")
            self.kill()
            time.sleep(1)
            running = False
        sworddir = ""
        #her håndterer jeg hviken rettning spilleren ser
        if self.hand != None:
            if self.dir == "down" and not self.attacking:
                sworddir = "self.hand.surf = pygame.transform.flip(pygame.image.load('2D-Rpg-Game-Optimised/sprites/Sword.png'), True, True).convert()"
                exec(sworddir)
                self.hand.surf.set_colorkey((255,255,255))
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx, player.rect.centery + 55))
            if self.dir == "up" and not self.attacking:
                sworddir = "self.hand.surf = pygame.image.load('2D-Rpg-Game-Optimised/sprites/Sword.png').convert()"
                exec(sworddir)
                self.hand.surf.set_colorkey((255,255,255))
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx + 35, player.rect.centery + 10))
            if self.dir == "left" and not self.attacking:
                sworddir = "self.hand.surf = pygame.transform.flip(pygame.image.load('2D-Rpg-Game-Optimised/sprites/Sword.png'), True, False).convert()"
                exec(sworddir)
                self.hand.surf.set_colorkey((255,255,255))                
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx, player.rect.centery + 30))
            if self.dir == "right" and not self.attacking:
                sworddir = "self.hand.surf = pygame.image.load('2D-Rpg-Game-Optimised/sprites/Sword.png').convert()"
                exec(sworddir)
                self.hand.surf.set_colorkey((255,255,255))                
                self.hand.rect = self.surf.get_rect(center = (player.rect.centerx + 45, player.rect.centery + 30))
                
            if not self.hand in all_sprites:
                all_sprites.add(self.hand)
            
            #dette er hvor jeg håndterer spiller attacks
            if pygame.mouse.get_pressed()[0] and not invcheck and self.hand.rotation == 0 and time.time() > wait + 0.5:
                wait = time.time()
                if self.dir == "right" or self.dir == "up":
                    self.hand.rotation -= 40
                elif self.dir == "left" or self.dir == "down":
                    self.hand.rotation += 40
                self.hand.surf = pygame.transform.rotate(player.hand.surf, self.hand.rotation).convert()
                self.hand.surf.set_colorkey((255,255,255))
                self.attacking = True
            elif time.time() > wait + 0.3:
                exec(sworddir)
                self.hand.surf.set_colorkey((255,255,255))
                self.hand.rotation = 0
                self.attacking = False
                self.hand.slash = None
            if self.attacking and not invcheck:
                if self.dir == "right":
                    self.hand.slash = Empty(self.hand.rect.x + 50,self.hand.rect.y + 25,"self.surf = pygame.image.load('2D-Rpg-Game-Optimised/sprites/Slash.png').convert()")
                if self.dir == "left":
                    self.hand.slash = Empty(self.hand.rect.x - 10,self.hand.rect.y + 25,"self.surf = pygame.transform.flip(pygame.image.load('2D-Rpg-Game-Optimised/sprites/Slash.png'), True, False).convert()")
                if self.dir == "up":
                    self.hand.slash = Empty(self.hand.rect.x + 10,self.hand.rect.y - 30,"self.surf = pygame.transform.rotate(pygame.image.load('2D-Rpg-Game-Optimised/sprites/Slash.png'), -90).convert()")
                if self.dir == "down":
                    self.hand.slash = Empty(self.hand.rect.x + 40,self.hand.rect.y + 60,"self.surf = pygame.transform.flip(pygame.transform.rotate(pygame.image.load('2D-Rpg-Game-Optimised/sprites/Slash.png'), 90), True, False).convert()")
                
                self.hand.slash.surf.set_colorkey((0,0,0))
                screen.blit(pygame.transform.flip(self.hand.slash.surf, True, False), self.hand.slash.rect)
        
        #her håndterer jeg spiller input
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

    #dette er funksjonen får å åpne inventoryen til spilleren.
    def openInventory(self):
        global invcheck
        if not invcheck:
            invcheck = True
            all_sprites.add(inv)
            x = inv.rect.x + 25
            y = inv.rect.y + 25
            for item in self.inventory:
                if x > inv.rect.x + 400:
                    x = inv.rect.x + 25
                    y += 58
                item.rect = newitem.surf.get_rect(center = (x, y))
                item.surf = pygame.transform.scale(newitem.surf, (50,50)).convert()
                all_sprites.add(item)
                all_items.add(item)
                x += 59
        elif invcheck:
            all_sprites.remove(inv)

            for item in player.inventory:
                item.kill()
            for text in all_text:
                text.kill()

            invcheck = False

#dette er enemy classen
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Slime.png")
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH + 200 + playerx, 200 + playery))
        self.isAlive = True

    #dette er update funksjonen til enemy classen som calles hver frame av spillet
    def Update(self):
        global enemywait
        global immunity
        global currentLvl
        #her regner jeg ut avstanden fra spilleren og fienden.
        x, y = self.rect.x, self.rect.y
        pX = player.rect.centerx - 20
        pY = player.rect.centery-20

        dist = math.hypot(pX-x, pY-y)

        if dist < 200 and self.isAlive: 
            busy = False
            for row in range(len(currentLvl)):
                for column in range(len(currentLvl[row])):
                    tilex = column * TILE_SIZE + playerx
                    tiley = row * TILE_SIZE + playery
                    tile = tiles[currentLvl[row][column]]
                    if tile == "CobbelBig":
                        if self.rect.x + self.surf.get_width() - (x-pX) / 30 > tilex and self.rect.x < tilex - (x-pX) / 30 + TILE_SIZE and self.rect.y + self.surf.get_height() - (y-pY) / 30 > tiley and self.rect.y - (y-pY) / 30  < tiley + TILE_SIZE:
                            busy = True
            if not busy and dist < 100 and time.time() > enemywait + 0.7:
                self.rect.x -= (x-pX) / 4
                self.rect.y -= (y-pY) / 4 
                if dist < 40:
                    enemywait = time.time()
            elif not busy and time.time() > enemywait + 0.9:
                self.rect.x -= (x-pX) / 50
                self.rect.y -= (y-pY) / 50 


        if player.hand != None and not invcheck and player.hand.slash != None:
            if collisionCheck(player.hand.slash, self):
                self.kill()
                self.isAlive = False
        if not invcheck and time.time() > immunity + 1 and self.isAlive:
            if collisionCheck(player, self):
                player.health -= 20
                immunity = time.time()

#dette er item classen som alle items for eksempel apple kommer til å inherite funksjoner fra.
class Item(pygame.sprite.Sprite):
    def __init__(self, inv = False, pos = None):
        global currentLvl
        super(Item, self).__init__()
        self.die = False

        ranx = random.randint(0, SCREEN_WIDTH)
        rany = random.randint(0, SCREEN_HEIGHT)

        clones = 0

        myclass = f"{self.type}()"

        #her legger jeg objekte på et tilfeldig sted på levelet sånn at den ikke kolliderer med vegger
        if pos == None:
            if not inv:
                for row in range(len(currentLvl)):
                    for column in range(len(currentLvl[row])):
                        x = column * TILE_SIZE + playerx
                        y = row * TILE_SIZE + playery
                        tile = tiles[currentLvl[row][column]]
                        if tile == "CobbelBig":
                            if ranx + self.surf.get_width() > x and ranx < x + TILE_SIZE and rany + self.surf.get_height() > y and rany < y + TILE_SIZE:
                                if clones == 0:
                                    newitem = exec(myclass)
                                    self.die = True
                                    clones += 1
                                    break
                            
            self.rect = self.surf.get_rect(center = (ranx, rany))
        else:
            self.rect = self.surf.get_rect(center = (pos))

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
            if pressedKeys[K_e] and len(player.inventory) < 49:
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
    def __init__(self, inv = False, pos = None):
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Sword.png")
        self.surf.set_colorkey((255,255,255))
        self.type = "Sword"
        super(Sword, self).__init__(inv,pos)
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

class Apple(Item):
    def __init__(self,inv = False, pos = None):
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Apple.png")
        self.surf.set_colorkey((255,255,255))
        self.type = "Apple"
        super(Apple, self).__init__(inv,pos)
        self.pickup2 = Text("Eat", 25, (255,255,255), (self.rect.centerx + 10, self.rect.centery - 10), self)
        
    
    def Update(self, pressedKeys):
        global wait
        if pygame.mouse.get_pressed()[0] and hoverCheck(self) and invcheck and self.inv and time.time() > wait + 0.2 and not textHover(self.pickup) and self in all_sprites:
            if self.clicked:
                all_text.remove(self.pickup2)
            elif not self.clicked:
                self.pickup2 = Text("Eat", 25, (255,255,255), (self.rect.centerx + 10, self.rect.centery - 10), self)
                all_text.add(self.pickup2)
        if textHover(self.pickup) and pygame.mouse.get_pressed()[0] and invcheck and time.time() > wait + 0.2:
            self.pickup2.kill() 
        if textHover(self.pickup2) and pygame.mouse.get_pressed()[0] and invcheck and time.time() > wait + 0.2 and self in all_sprites and self.clicked:
            if player.health >= 80:
                player.health = 100
            elif player.health < 80:
                player.health += 20
            
            player.inventory.pop(self.index)
            self.kill()
            self.pickup.kill()
            self.pickup2.kill()

            for item in player.inventory:
                if item.index > self.index:
                    item.index -= 1
        super(Apple, self).Update(pressedKeys)

greenapple = pygame.sprite.Sprite()
greenapple.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Apple-1.png.png")
greenapple.rect = greenapple.surf.get_rect(center=(300,300))


class Goal(pygame.sprite.Sprite):
    def __init__(self,inv = False, pos = None):
        super(Goal, self).__init__()
        self.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Goal.png")
        self.surf.set_colorkey((255,255,255))
        self.type = "Goal"
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH + 100 + playerx, 200 + playery))
        self.pickup = Text("E", 25, (0,0,0), (self.rect.centerx + 10, self.rect.centery - 30), self)
    def Update(self, pressedKeys):
        global currentLvl
        global wait
        global playerx
        global playery
        if collisionCheck(player, self) and not invcheck:
            all_text.remove(self.pickup)
            self.pickup = Text("E", 25, (0,0,0), (self.rect.centerx + 10, self.rect.centery - 30), self)
            all_text.add(self.pickup)
            if pressedKeys[K_e] and time.time() > wait + 0.2:
                wait = time.time()
                all_text.remove(self.pickup)
                if currentLvl == tutoriallvl:
                    currentLvl = level1
                    for item in all_items:
                        item.kill()
                    try:
                        tutorialSign.kill()
                    except NameError:
                        print("ops")
                    goal.rect.x, goal.rect.y = 500,600
                    playerx, playery = 90, 50
                elif currentLvl == level1:
                    currentLvl = level2
        else:
            all_text.remove(self.pickup)

        

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
        exec(img)
        self.rect = self.surf.get_rect(center = (x,y))

def move(nr1,nr2):
    global playerx
    global playery
    global currentLvl
    busy = False
    for row in range(len(currentLvl)):
        for column in range(len(currentLvl[row])):
            x = column * TILE_SIZE + playerx
            y = row * TILE_SIZE + playery
            tile = tiles[currentLvl[row][column]]
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


def draw(level):
    for row in range(len(level)):
        for column in range(len(level[row])):
            x = column * TILE_SIZE + playerx
            y = row * TILE_SIZE + playery
            tile = tiles[level[row][column]]
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

ADDITEM = pygame.USEREVENT + 1
pygame.time.set_timer(ADDITEM, 1000)

running = True

invcheck = False

all_text = pygame.sprite.Group()
all_items = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
menu_buttons = pygame.sprite.Group()
Levels = pygame.sprite.Group()

all_sprites.add(player)
all_sprites.add(greenapple)

wait = time.time()
enemywait = time.time() 
immunity = time.time()

dbCursor.execute("SELECT Ip from playerdata")
adresser = dbCursor.fetchall()
nyadresser = []
for el in adresser:
    el = str(el).replace('(', '').replace(')', '').replace("'", "").replace(',', '')
    nyadresser.append(el)

hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)

if len(nyadresser) != 0 and IPAddr in nyadresser:
    dbCursor.execute(f"SELECT Ip, Health, X, Y, Inventory FROM playerdata WHERE Ip = '{IPAddr}'")
    oldplayerdata = dbCursor.fetchall()
    playerx = oldplayerdata[0][2]
    playery = oldplayerdata[0][3]
    
    player.health = oldplayerdata[0][1]
    oldinv = list(oldplayerdata[0][4].replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").split(","))
    if oldinv != ['']:
        for item in oldinv:
            exec(f"newitem = {item}(True)")
            newitem.kill()
            player.inventory.append(newitem)
            newitem.index = len(player.inventory) - 1
            newitem.inv = True
        
else:   
    playerx, playery = -20, 0

menucheck = True
lvlclicked = False

if len(nyadresser) != 0 and IPAddr in nyadresser:
    dbCursor.execute(f"SELECT `currentlvl` FROM playerdata WHERE Ip = '{IPAddr}'")
    currentLvl = dbCursor.fetchall()
    currentLvl = str(currentLvl).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    if currentLvl == "tutoriallvl":
        currentLvl = tutoriallvl

    elif currentLvl == "level1":
        currentLvl = level1

    elif currentLvl == "level2":
        currentLvl = level2
else:
    currentLvl = tutoriallvl
    print("tutorial")

start = Text("Start", 100, (0,0,0), (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 90))
lvlbtn = Text("Level", 100, (0,0,0), (SCREEN_WIDTH/2 - 115, SCREEN_HEIGHT/2))

tutorial = Text("Tutorial", 40, (0,0,0), (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 120))
lvl1 = Text("Level 1", 40, (0,0,0), (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 70))
lvl2 = Text("Level 2", 40, (0,0,0), (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 20))
back = Text("Back", 40, (0,0,0), (80, 60))

Levels.add(tutorial)
Levels.add(lvl1)
Levels.add(lvl2)
Levels.add(back)

menu_buttons.add(start)
menu_buttons.add(lvlbtn)

while running:
    if menucheck == True:

        for event in pygame.event.get():
        
            if event.type == KEYDOWN:
                
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:                    
                running = False

        screen.fill((40, 40, 240))

        if not lvlclicked:
            for text in menu_buttons:
                screen.blit(text.text, text.rect)
        else:
            for text in Levels:
                screen.blit(text.text, text.rect)

        if textHover(start) and pygame.mouse.get_pressed()[0] and lvlclicked == False:
            menucheck = False
            enemy = Enemy()
            if currentLvl == tutoriallvl:
                tutorialSign = pygame.sprite.Sprite()
                tutorialSign.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Tutorial.png")
                tutorialSign.surf.set_colorkey((255,255,255))
                tutorialSign.rect = tutorialSign.surf.get_rect(center = (SCREEN_WIDTH - 225, 250))
                tutorialSign.rect.x += playerx
                tutorialSign.rect.y += playery
                all_sprites.add(tutorialSign)
                goal = Goal((-750 - playerx, -200 - playery))
                
            elif currentLvl == level1:
                goal = Goal((500, 600))
            elif currentLvl == level2:
                goal = Goal((500, 600))
            else:
                print(currentLvl)
            all_sprites.add(enemy)
            all_sprites.add(goal)
            all_sprites.add(player)

        if textHover(lvlbtn) and pygame.mouse.get_pressed()[0] and lvlclicked == False:
            lvlclicked = True
        if textHover(back) and pygame.mouse.get_pressed()[0]  and lvlclicked == True:
            lvlclicked = False
        if textHover(tutorial) and pygame.mouse.get_pressed()[0]  and lvlclicked == True:
            playerx, playery = 100, 0
            player.health = 100
            enemy = Enemy()
            goal = Goal((-750 - playerx, -200 - playery))
            tutorialSign = pygame.sprite.Sprite()
            tutorialSign.surf = pygame.image.load("2D-Rpg-Game-Optimised/sprites/Tutorial.png")
            tutorialSign.surf.set_colorkey((255,255,255))
            tutorialSign.rect = tutorialSign.surf.get_rect(center = (SCREEN_WIDTH - 110, 250))
            all_sprites.add(enemy)
            all_sprites.add(goal)
            all_sprites.add(tutorialSign)
            all_sprites.add(player)

            menucheck = False
            currentLvl = tutoriallvl
        if textHover(lvl1) and pygame.mouse.get_pressed()[0]  and lvlclicked == True:
            playerx, playery = 90, 50
            player.health = 100
            enemy = Enemy()
            goal = Goal((0,0))
            all_sprites.add(enemy)
            all_sprites.add(goal)
            all_sprites.add(player)

            menucheck = False
            currentLvl = level1

        if textHover(lvl2) and pygame.mouse.get_pressed()[0]  and lvlclicked == True:
            playerx, playery = -500, -500
            player.health = 100
            enemy = Enemy()
            goal = Goal((0,0))
            all_sprites.add(enemy)
            all_sprites.add(goal)
            all_sprites.add(player)

            menucheck = False
            currentLvl = level2

        pygame.display.flip()

        clock.tick(30)
    elif menucheck == False:
    
        for event in pygame.event.get():
        
            if event.type == KEYDOWN:
                
                if event.key == K_ESCAPE:
                    newinv = []
                    for item in player.inventory:
                        newinv.append(item.type)
                    if currentLvl == tutoriallvl:
                        savedlvl = "tutoriallvl"
                    elif currentLvl == level1:
                        savedlvl = "level1"
                    elif currentLvl == level2:
                        savedlvl = "level2"
                    if len(nyadresser) != 0 and IPAddr in nyadresser:
                    
                        dbCursor.execute(f'UPDATE `playerdata` SET `Health`="{player.health}",`X`="{playerx}",`Y`="{playery}",`Inventory`="{newinv}",`currentlvl`="{savedlvl}" WHERE `Ip` = "{IPAddr}"')
                    else:
                        dbCursor.execute(f'INSERT INTO playerdata(Ip,Health,X,Y,Inventory,currentlvl) VALUES("{IPAddr}", {player.health},{playerx},{playery},"{newinv}","{savedlvl}")')
                    PlayerData.commit()
                    menucheck = True 
                    for sprite in all_sprites:
                        sprite.kill()
                elif event.key == K_i:
                    player.openInventory()

            elif event.type == QUIT:
                newinv = []
                for item in player.inventory:
                    newinv.append(item.type)
                if currentLvl == tutoriallvl:
                    savedlvl = "tutoriallvl"
                elif currentLvl == level1:
                    savedlvl = "level1"
                elif currentLvl == level2:
                    savedlvl = "level2"
                if len(nyadresser) != 0 and IPAddr in nyadresser:
                    
                    dbCursor.execute(f'UPDATE `playerdata` SET `Health`="{player.health}",`X`="{playerx}",`Y`="{playery}",`Inventory`="{newinv}",`currentlvl`="{savedlvl}" WHERE `Ip` = "{IPAddr}"')
                else:
                    dbCursor.execute(f'INSERT INTO playerdata(Ip,Health,X,Y,Inventory,currentlvl) VALUES("{IPAddr}", {player.health},{playerx},{playery},"{newinv}","{savedlvl}")')
                PlayerData.commit()
                running = False
            
            elif event.type == ADDITEM and not invcheck:
                if len(all_items) < 5:
                    ran = random.randint(1,10)
                    if ran > 6:
                        newitem = Sword()
                    else:
                        newitem = Apple()

            
        screen.fill((0, 0, 0))

        draw(currentLvl)

        pressed_keys = pygame.key.get_pressed()

        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)
        for text in all_text:
            screen.blit(text.text, text.rect)

        player.update(pressed_keys)
        enemy.Update()
        goal.Update(pressed_keys)


        for item in all_items:
            item.Update(pressed_keys)

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH/ 2 - 110, SCREEN_HEIGHT - 75, 220, 50))
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(SCREEN_WIDTH/ 2 - 100, SCREEN_HEIGHT - 65, player.health * 2, 30))

        pygame.display.flip()

        clock.tick(30)
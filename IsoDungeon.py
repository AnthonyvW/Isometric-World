import pygame
import random
import os
from opensimplex import OpenSimplex


from SpriteSheet import SpriteSheet, scale_image

# game window
SCREEN_WIDTH = 1924
SCREEN_HEIGHT = 1000
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1920,32)

pygame.init()

# Font
gameFont = pygame.font.Font('DungeonFont.ttf', 30)
# Draws Text on screen at x, y
def draw_text(text, _x, _y, color=(255, 255, 255), font=gameFont):
    img = font.render(text, True, color)
    screen.blit(img, (_x, _y))

Scale = 1
OriginalBlockSize = 32
BlockSize = OriginalBlockSize * Scale
BlockZOffset = BlockSize / 2
BlockYOffset = BlockSize / 4
BlockXWidthOffset = BlockSize
BlockXOffset = BlockSize / 2

def ReplaceImg(Source, Dest):
    for x in range(Dest.get_width()):
        for y in range(Dest.get_height()):
            if(Dest.get_at((x,y)) == (255,255,255)): # Border
                Dest.set_at((x,y), Source.get_at((x, y)))
            elif(Dest.get_at((x,y)) == (128,238,191)): # Top
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize, y)))
            elif(Dest.get_at((x,y)) == (64, 174,228)): # Top Left
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*2, y)))
            elif(Dest.get_at((x,y)) == (128,192,191)): # Top Forward
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*3, y)))
            elif(Dest.get_at((x,y)) == (191,174,228)): # Top Right
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*4, y)))
            elif(Dest.get_at((x,y)) == (37,82,206)): # Left
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*5, y)))
            elif(Dest.get_at((x,y)) == (128,128,255)): # Forward
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*6, y)))
            elif(Dest.get_at((x,y)) == (218,82,206)): # Right
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*7, y)))
            elif(Dest.get_at((x,y)) == (64,18,138)): # Bottom Left
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*8, y)))
            elif(Dest.get_at((x,y)) == (128,12,181)): # Bottom Forward
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*9, y)))
            elif(Dest.get_at((x,y)) == (191,18,138)): # Bottom Right
                Dest.set_at((x,y), Source.get_at((x + OriginalBlockSize*10, y)))


# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
# Title
pygame.display.set_caption('Isometric Dungeon')


TileSheet = SpriteSheet("Template.png")
Block = TileSheet.get_image(0, 96,32,32).convert_alpha()
Selector = TileSheet.get_image(0, 128,32,32).convert_alpha()
RedSelector = TileSheet.get_image(0, 160,32,32).convert_alpha()

colorPal = TileSheet.get_image(0,32, 352, 32).convert_alpha()
ReplaceImg(colorPal, Block)

Block = scale_image(Scale, Block)
Selector = scale_image(Scale, Selector)
RedSelector = scale_image(Scale, RedSelector)

pygame.display.set_icon(Block)

SimplexNoise = OpenSimplex(0)
Chunk = []
ChunkXSize = 64
ChunkYSize = 64
ChunkZSize = 64
for x in range(ChunkXSize):
    Chunk.append([])
    xCoord = x / 32
    for y in range(ChunkYSize):
        Chunk[x].append([])
        yCoord = y / 32

        for z in range(ChunkZSize):
            noise = SimplexNoise.noise3d(xCoord, yCoord, z / 32)

            if(noise > 0.3):
                Chunk[x][y].append(1)
            else:
                Chunk[x][y].append(0)



def draw(xSelect, ySelect, zSelect, xOffset, yOffset):
    global BlockZOffset,BlockYOffset,BlockXWidthOffset,BlockXOffset
    for y in range(ChunkYSize):
        for x in range(ChunkXSize - 1, -1, -1):
            for z in range(ChunkZSize):
                if(Chunk[x][y][z] == 1):
                    if(xSelect == x and ySelect == y):
                        screen.blit(Selector, (x * BlockXOffset + y * BlockXOffset + xOffset, y * BlockYOffset - x * BlockYOffset + yOffset - z*BlockZOffset))
                    else:
                        screen.blit(Block, (x * BlockXOffset + y * BlockXOffset + xOffset, y * BlockYOffset - x * BlockYOffset + yOffset - z*BlockZOffset))


def isLeft(aX, aY, bX, bY, cX, cY):
    return ((cX - aX) * (bY - aY) - (cY - aY) * (bX - aX)) < 0


run = True
clock = pygame.time.Clock()
while run:
    # Clock Speed
    clock.tick()
    #print(clock.get_fps())

    XScreenOffset = 0
    YScreenOffset = ChunkXSize * BlockYOffset - BlockYOffset + ChunkYSize * BlockZOffset / 2

    # Mouse Position
    pos = pygame.mouse.get_pos()

    mousePosX1 = (pos[0] - XScreenOffset) / BlockXOffset
    mousePosY1 = (pos[1] - YScreenOffset) / BlockYOffset

    selectedX = (mousePosX1 - mousePosY1) / 2 + 0.5
    selectedY = (mousePosX1 + mousePosY1) / 2 - 0.5
    selectedZ = ChunkZSize - 1

    # Keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Background
    screen.fill((0, 0, 0))
    # Draw Tiles
    draw(int(selectedX), int(selectedY), int(selectedZ), XScreenOffset, YScreenOffset)
    # Puts everything on the display
    pygame.display.update()

pygame.quit()

import pygame
import math
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
drawChunk = []
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

for x in range(ChunkXSize):
    drawChunk.append([])
    for y in range(ChunkYSize):
        drawChunk[x].append([])
        for z in range(ChunkZSize):
            isExposed = False
            # X Axis Check
            if (x > 0 and x + 1 < ChunkXSize):
                isExposed = Chunk[x - 1][y][z] == 0 or Chunk[x + 1][y][z] == 0
            elif (x > 0):
                isExposed = Chunk[x - 1][y][z] == 0
            else:
                isExposed = True

            if(isExposed):
                drawChunk[x][y].append(Chunk[x][y][z])
                continue

            # Y Axis Check
            if (y > 0 and y + 1 < ChunkYSize):
                isExposed = Chunk[x][y - 1][z] == 0 or Chunk[x][y + 1][z] == 0
            elif (y > 0):
                isExposed = True
            else:
                isExposed = Chunk[x][y + 1][z] == 0

            if (isExposed):
                drawChunk[x][y].append(Chunk[x][y][z])
                continue

            # Z Axis Check
            if (z > 0 and z + 1 < ChunkZSize):
                isExposed = Chunk[x][y][z - 1] == 0 or Chunk[x][y][z + 1] == 0
            elif (z > 0):
                isExposed = True
            else:
                isExposed = Chunk[x][y][z + 1] == 0

            if (isExposed):
                drawChunk[x][y].append(Chunk[x][y][z])
                continue
            else:
                drawChunk[x][y].append(0)


def draw(xSelect, ySelect, zSelect, xOffset, yOffset):
    global BlockZOffset,BlockYOffset,BlockXWidthOffset,BlockXOffset

    for y in range(ChunkYSize):
        yLoopOffset = y * BlockYOffset + yOffset
        yXLoopCalc =  y * BlockXOffset + xOffset
        for x in range(ChunkXSize - 1, -1, -1):
            xLoopOffset = x * BlockXOffset + yXLoopCalc
            yMxOffset = yLoopOffset - x * BlockYOffset
            if(xLoopOffset < -BlockXWidthOffset or xLoopOffset > SCREEN_WIDTH or yMxOffset < 0 or yMxOffset - (ChunkZSize - 1) * BlockZOffset > SCREEN_HEIGHT):
                continue
            for z in range(ChunkZSize):
                if(drawChunk[x][y][z] == 1 and yMxOffset - z * BlockZOffset < SCREEN_HEIGHT):
                    screen.blit(Block, (xLoopOffset, yMxOffset - z * BlockZOffset))
                    if (xSelect == x and ySelect == y and zSelect == z):
                        screen.blit(Selector, (xLoopOffset, yMxOffset - z * BlockZOffset))

'''def draw(xSelect, ySelect, zSelect, xOffset, yOffset):
    global BlockZOffset,BlockYOffset,BlockXWidthOffset,BlockXOffset

    for y in range(ChunkYSize):
        for x in range(ChunkXSize - 1, -1, -1):
            for z in range(ChunkZSize):
                if(Chunk[x][y][z] == 1):
                    if(y * BlockYOffset - x * BlockYOffset + yOffset - z * BlockZOffset + BlockSize > 0):
                        screen.blit(Block, (x * BlockXOffset + y * BlockXOffset + xOffset, y * BlockYOffset - x * BlockYOffset + yOffset - z*BlockZOffset))
                        if (xSelect == x and ySelect == y and zSelect == z):
                            screen.blit(Selector, (x * BlockXOffset + y * BlockXOffset + xOffset,y * BlockYOffset - x * BlockYOffset + yOffset - z * BlockZOffset))
                    else:
                        break'''


def isLeft(aX, aY, bX, bY, cX, cY):
    return ((cX - aX) * (bY - aY) - (cY - aY) * (bX - aX)) < 0

def blockExists(x, y, z):
    return x < ChunkXSize and x >= 0 and y < ChunkYSize and y >= 0 and z < ChunkZSize and z >= 0 and Chunk[x][y][z] != 0

def blockTrace(x, y):
    z = ChunkZSize - 1
    curx = math.floor(x)
    cury = math.floor(y)
    found = False
    while not found:
        if z < 0:
            found = True
        elif blockExists(curx, cury, z):
            return (curx, cury, z)
        elif(math.fabs(x % 1) + math.fabs( y % 1) > 1):
            if blockExists(curx + 1, cury, z):
                return (curx + 1, cury, z)
            elif blockExists(curx + 1, cury - 1, z):
                return (curx + 1, cury - 1, z)
            else:
                z -= 1
                curx += 1
                cury -= 1
        else:
            if blockExists(curx, cury - 1, z):
                return (curx, cury - 1, z)
            elif blockExists(curx + 1, cury - 1, z):
                return (curx + 1, cury - 1, z)
            else:
                z -= 1
                curx += 1
                cury -= 1
    return (x, y, z)




run = True
clock = pygame.time.Clock()
XScreenOffset = -0
YScreenOffset = ChunkXSize * BlockYOffset - BlockYOffset + ChunkYSize * BlockZOffset / 2

def ScreenToBlock(x, y):
    global XScreenOffset, YScreenOffset
    selectedX = (x - XScreenOffset) / BlockXOffset
    selectedY = (y - YScreenOffset) / BlockYOffset

    blockX = (selectedX - selectedY) / 2 - (ChunkZSize - 1) + 0.5
    blockY = (selectedX + selectedY) / 2 + (ChunkZSize - 1) - 0.5
    return blockX, blockY

# Keyboard
movingLeft = False
movingRight = False
movingUp = False
movingDown = False

while run:
    # Clock Speed
    clock.tick(60)
    print(clock.get_fps())

    # Mouse Position
    pos = pygame.mouse.get_pos()

    #mousePosX1 = (pos[0] - XScreenOffset) / BlockXOffset
    #mousePosY1 = (pos[1] - YScreenOffset) / BlockYOffset

    selectedX, selectedY = ScreenToBlock(pos[0], pos[1])#(mousePosX1 - mousePosY1) / 2 - (ChunkZSize - 1) + 0.5
    #selectedY = (mousePosX1 + mousePosY1) / 2 + (ChunkZSize - 1) - 0.5
    selectedX, selectedY, selectedZ = blockTrace(selectedX, selectedY)

    # Keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                movingRight = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                movingLeft = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                movingUp = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                movingDown = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                movingRight = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                movingLeft = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                movingUp = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                movingDown = False

    if(movingLeft):
        XScreenOffset += 15
    if(movingRight):
        XScreenOffset -= 15
    if(movingUp):
        YScreenOffset += 15
    if(movingDown):
        YScreenOffset -= 15

    # Background
    screen.fill((0, 0, 0))



    # Draw Tiles
    draw(math.floor(selectedX), math.floor(selectedY), math.floor(selectedZ), XScreenOffset, YScreenOffset)
    # Puts everything on the display
    pygame.display.update()

pygame.quit()

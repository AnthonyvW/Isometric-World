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

Scale = 2
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
ChunkYSize = 156
ChunkZSize = 1
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
        for x in range(ChunkXSize):
            for z in range(ChunkZSize):
                if(Chunk[x][y][z] == 1):
                    if(x == xSelect and y == ySelect and z == zSelect):
                        if (y % 2 == 0):
                            screen.blit(Selector, (x * BlockXWidthOffset + xOffset, y * BlockYOffset - z * BlockZOffset + yOffset))
                        else:
                            screen.blit(Selector, (BlockXOffset + x * BlockXWidthOffset + xOffset,y * BlockYOffset - z * BlockZOffset + yOffset))
                    elif(y % 2 == 0):
                        screen.blit(Block, (x * BlockXWidthOffset + xOffset, y * BlockYOffset - z * BlockZOffset + yOffset))
                    else:
                        screen.blit(Block, (BlockXOffset + x * BlockXWidthOffset + xOffset, y * BlockYOffset - z * BlockZOffset + yOffset))
                    #screen.blit(Block, (x * 16 + y * 16 + xOffset, y * 8 - x * 8 + yOffset - z*16))

def isLeft(aX, aY, bX, bY, cX, cY):
    return ((cX - aX) * (bY - aY) - (cY - aY) * (bX - aX)) < 0


run = True
clock = pygame.time.Clock()
while run:
    # Clock Speed
    clock.tick()
    #print(clock.get_fps())

    XScreenOffset = -BlockXOffset  # -ChunkXSize * 32 / 2 + SCREEN_WIDTH/2
    YScreenOffset = ChunkZSize * BlockZOffset  # ChunkYSize * 32 / 2

    # Mouse Position
    pos = pygame.mouse.get_pos()
    x = (pos[0] - XScreenOffset) / BlockXOffset
    y = (pos[1] - YScreenOffset) / BlockYOffset
    z = ChunkZSize - 1

    if(int(y) % 2 == 1):
        x -= 1

    # Keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Background
    screen.fill((0, 0, 0))

    if(int(y) % 2 == 1):
        if(int(x + 1) % 2 == 0):
            if not isLeft(
                    int(x + 1) * BlockXOffset, int(y)     * BlockYOffset,
                    int(x + 2) * BlockXOffset, int(y + 1) * BlockYOffset,
                    pos[0] - XScreenOffset, pos[1] - YScreenOffset
                ):
                x += 1
                y -= 1
        else:
            if not isLeft(
                    int(x + 1) * BlockXOffset, int(y + 1) * BlockYOffset,
                    int(x + 2) * BlockXOffset, int(y)     * BlockYOffset,
                    pos[0] - XScreenOffset, pos[1] - YScreenOffset
                ):
                x += 1
                y -= 1
    else:
        if (int(x + 1) % 2 == 0):
            if not isLeft(
                    int(x)     * BlockXOffset, int(y)     * BlockYOffset,
                    int(x + 1) * BlockXOffset, int(y + 1) * BlockYOffset,
                    pos[0] - XScreenOffset, pos[1] - YScreenOffset
                ):
                y -= 1

        else:
            if not isLeft(
                    int(x)     * BlockXOffset, int(y + 1) * BlockYOffset,
                    int(x + 1) * BlockXOffset, int(y)     * BlockYOffset,
                    pos[0] - XScreenOffset, pos[1] - YScreenOffset
                ):
                x -= 1
                y -= 1

    # Bottom Top
    pygame.draw.line(screen, (255,0,0),
                     (XScreenOffset, YScreenOffset),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset, YScreenOffset))
    # Bottom Left
    pygame.draw.line(screen, (255,0,0),
                     (XScreenOffset, YScreenOffset),
                     (XScreenOffset, YScreenOffset + ChunkYSize * BlockYOffset + BlockSize))
    # Bottom Right
    pygame.draw.line(screen, (255,0,0),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset, YScreenOffset),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset, YScreenOffset + ChunkYSize * BlockYOffset + BlockSize))
    # Bottom Bottom
    pygame.draw.line(screen, (255,0,0),
                     (XScreenOffset, YScreenOffset + ChunkYSize * BlockYOffset + BlockSize),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset, YScreenOffset + ChunkYSize * BlockYOffset + BlockSize))

    draw(int(x / 2), int(y), z, XScreenOffset, YScreenOffset)

    # Top Top
    pygame.draw.line(screen, (255, 0, 0),
                     (XScreenOffset,YScreenOffset - ChunkZSize * BlockZOffset),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset,YScreenOffset - ChunkZSize * BlockZOffset))
    # Top Left
    pygame.draw.line(screen, (255, 0, 0),
                     (XScreenOffset,YScreenOffset - ChunkZSize * BlockZOffset),
                     (XScreenOffset,YScreenOffset + ChunkYSize * BlockYOffset - ChunkZSize * BlockZOffset + BlockSize))
    # Top Right
    pygame.draw.line(screen, (255, 0, 0),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset,YScreenOffset - ChunkZSize * BlockZOffset),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset,YScreenOffset + ChunkYSize * BlockYOffset - ChunkZSize * BlockZOffset + BlockSize))
    # Top Bottom
    pygame.draw.line(screen, (255, 0, 0),
                     (XScreenOffset,YScreenOffset + ChunkYSize * BlockYOffset - ChunkZSize * BlockZOffset + BlockSize),
                     (XScreenOffset + ChunkXSize * BlockXWidthOffset + BlockXOffset,YScreenOffset + ChunkYSize * BlockYOffset - ChunkZSize * BlockZOffset + BlockSize))

    # Puts everything on the display
    pygame.display.update()

pygame.quit()

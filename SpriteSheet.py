"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.file_name = file_name
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()


    def get_image(self, x, y, width, height):

        sprite = pygame.Surface((width, height))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0), (x,y,width,height))

        return sprite

    def get_image_scale(self, x, y, width, height, scale):
            img = SpriteSheet.get_image(self,x+width,y,width,height)

            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
            return img

    def get_frames(self, x, y, width, height, frames, scale):

        frame_list = []

        for i in range(frames):
            img = SpriteSheet.get_image(self,x+width*i,y,width,height)

            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))

            frame_list.append(img)

        return frame_list



    # flip image
    def flip_img(img, xflip=False, yflip=False):
        return pygame.transform.flip(img, xflip, yflip)

# gets the scaled image
def scale_image(scale, img):
        img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
        return img
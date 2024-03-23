import pygame 
from support import import_folder

# to represent kind of blocks that we can place on the screen
class Tile(pygame.sprite.Sprite):        #inherit from pygame.sprite.Sprite
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size)) #rectangle
		self.rect = self.image.get_rect(topleft = (x,y))
    
	# to scroll through our level
	def update(self,shift):
		self.rect.x += shift

class StaticTile(Tile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface 

class Crate(StaticTile):  
	def __init__(self,size,x,y):
		super().__init__(size,x,y,pygame.image.load('./graphics/terrain/crate.png').convert_alpha()) # because we have one image
		offset_y = y + size # crate is less than other tiles in size => it will appear on topleft (float) of the size occupied
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTile(Tile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,shift):
		self.animate()
		self.rect.x += shift

class Coin(AnimatedTile):
	def __init__(self,size,x,y,path,value):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = value

class Palm(AnimatedTile):
	def __init__(self,size,x,y,path,offset): # offset as arg because we have small palm and large palm
		super().__init__(size,x,y,path)
		offset_y = y - offset
		self.rect.topleft = (x,offset_y)
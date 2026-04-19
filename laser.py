import pygame
class Laser(pygame.sprite.Sprite):
	def __init__(self, player):
		super().__init__(self, self.containers)
		self.location = [(player.x + 10), player.y, (player.x + 10), (player.y - 800)]
		self.laser = True
	def draw(self, screen):
		if self.laser == True:
			pygame.draw.polygon(screen, "blue", self.location)
import pygame as pg
import numpy as np
import random
from math import atan, pi

WIDTH = 800
HEIGHT = 600
MAX_SPEED = 8
SWARM_SIZE = 100
FPS = 30
PERSONAL_SPACE = 30
psize = [0,0]
BOID_IMAGE = 'flappyBird.png'
# BOID_IMAGE = 'arrow.png'
SHARK_IMAGE = 'fixedPeng.png'

class Penguin(pg.sprite.Sprite):
	baseImage = pg.image.load(BOID_IMAGE)
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.vel = [random.randrange(6), random.randrange(6)]
		self.image = pg.image.load(BOID_IMAGE)
		self.image.set_alpha(None)
		edgeColor = self.image.get_at((0,0))
		self.image.set_colorkey(edgeColor)
		w, h = self.image.get_size()
		self.rect = self.image.get_rect(topleft = (random.randrange(WIDTH-w),random.randrange(HEIGHT-h)))
		self.lastAngle = 0


	def rule_get_close(self, neighbours):
		if not neighbours: return
		p = [0,0]
		for n in neighbours:
			p[0] += n.rect.x
			p[1] += n.rect.y
		middle = [m/len(neighbours) for m in p]
		self.vel[0] += (middle[0] - self.rect.x)*0.005 
		self.vel[1] += (middle[1] - self.rect.y)*0.005 

	def rule_stay_on_screen(self):
		if self.rect[0] < 0:
			self.vel[0] = -self.vel[0]
			self.rect[0] = 0

		if self.rect[0]+psize[0] > WIDTH:
			self.vel[0] = -self.vel[0]
			self.rect[0] = WIDTH - psize[0]

		if self.rect[1] < 0:
			self.vel[1] = -self.vel[1]
			self.rect[1] = 0

		if self.rect[1]+psize[1] > HEIGHT:
			self.vel[1] = -self.vel[1]
			self.rect[1] = HEIGHT-psize[1]

	def rule_dont_overcrowd(self, neighbours):
		if not neighbours: return
		c = [0,0]
		for n in neighbours:
			dist = abs(self.rect.x - n.rect.x) + abs(self.rect.y - n.rect.y)
			if dist < PERSONAL_SPACE:
				c[0] += self.rect.x - n.rect.x
				c[1] += self.rect.y - n.rect.y
		self.vel[0] += c[0] * 0.01
		self.vel[1] += c[1] * 0.01

	def rule_match_velocity(self, neighbours):
		if not neighbours: return
		v = [0,0]
		for n in neighbours:
			v[0] += n.vel[0]
			v[1] += n.vel[1]
		v[0] /= len(neighbours)
		v[1] /= len(neighbours)
		self.vel[0] += v[0]*0.01
		self.vel[1] += v[1]*0.01

	def rule_speed_limit(self):
		speed = sum(map(abs, self.vel))
		if speed > MAX_SPEED:
			slowdown = (MAX_SPEED/speed)
			self.vel[0] *= slowdown
			self.vel[1] *= slowdown

	def rotate(self, angle):
		oldCenter = self.rect.center
		im = self.baseImage.copy()
		newImage = pg.transform.rotate(im, angle)
		newImageRect = newImage.get_rect()
		newImageRect.center = oldCenter
		newImage.set_alpha(None)
		edgeColor = self.image.get_at((0,0))
		newImage.set_colorkey(edgeColor)
		return newImage, newImageRect

	def orientatate(self):
		angle = 90
		if self.vel[0] == 0:
			if self.vel[0] <= 0: angle = 270
			else: angle = 90
		else:
			if self.vel[1] > 0:
				angle += 180
			angle += 180 * atan(self.vel[1]/self.vel[0]) / pi
		
		TURN_RATE = 0.1

		angleDelta = (angle - self.lastAngle) * TURN_RATE
		self.image, self.rect = self.rotate(self.lastAngle + angleDelta)
		self.lastAngle = self.lastAngle + angleDelta
		# print(angle)



	def update(self, neighbours):
		self.rule_get_close(neighbours)
		self.rule_stay_on_screen()
		self.rule_dont_overcrowd(neighbours)
		self.rule_match_velocity(neighbours)
		self.rect.x += self.vel[0]
		self.rect.y += self.vel[1]
		self.orientatate()
		self.rule_speed_limit()


class Shark(pg.sprite.Sprite):
	def __init(self):
		pg.sprite.Sprite.__init__(self)
		self.vel = [random.randrange(6), random.randrange(6)]
		self.image = pg.image.load(SHARK_IMAGE)
		self.image.set_alpha(None)
		edgeColor = self.image.get_at((0,0))
		self.image.set_colorkey(edgeColor)
		w, h = self.image.get_size()
		self.rect = self.image.get_rect(topleft = (random.randrange(WIDTH-w),random.randrange(HEIGHT-h)))
		# self.lastAngle = 0
	
	def rule_stay_on_screen(self):
		if self.rect[0] < 0:
			self.vel[0] = -self.vel[0]
			self.rect[0] = 0

		if self.rect[0]+psize[0] > WIDTH:
			self.vel[0] = -self.vel[0]
			self.rect[0] = WIDTH - psize[0]

		if self.rect[1] < 0:
			self.vel[1] = -self.vel[1]
			self.rect[1] = 0

		if self.rect[1]+psize[1] > HEIGHT:
			self.vel[1] = -self.vel[1]
			self.rect[1] = HEIGHT-psize[1]

	def rule_speed_limit(self):
		speed = sum(map(abs, self.vel))
		if speed > MAX_SPEED:
			slowdown = (MAX_SPEED*1.5/speed)
			self.vel[0] *= slowdown
			self.vel[1] *= slowdown

	def chase(victim):
		self.vel[0] += (victim.rect.x - self.rect.x) * 0.01
		self.vel[1] += (victim.rect.y - self.rect.y) * 0.01


	def update(self, neighbours):
		victim = random.randrange(len(neighbours))
		for i, n in enumertate(neighbours):
			if i == victim:
				self.chase(n)
				self.rule_stay_on_screen()
				self.rule_speed_limit()





def main():
	pg.init()
	# logo = pygame.image.load("logo32x32.png")
 #    pygame.display.set_icon(logo)
	pg.display.set_caption("Swarm")

	screen = pg.display.set_mode((WIDTH, HEIGHT))
	im = pg.image.load("fixedPeng.png")
	global psize
	psize = im.get_size()
	pg.display.flip()

	swarm = pg.sprite.Group()
	sharks = pg.sprite.Group()
	# a clock for controlling the fps later
	clock = pg.time.Clock()

	for i in range(SWARM_SIZE):
		penguin = Penguin()
		swarm.add(penguin)

	# sharks.add(Shark())
	# for x in sharks:
	# 	print('HERRE')
	# 	print(x.rect)

	running = True
	count = 0
	while running:
		count += 1
		if count % 50 == 0:
			count = count%50
			print(clock.get_fps())
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
		screen.fill((255,255,255))
		# screen.blit(penguin.im, (penguin.rect[0], penguin.rect[1]))
		# update(swarm, sharks)
		update(swarm)
		swarm.draw(screen)
		pg.display.flip()

		clock.tick(FPS)

def update(swarm):
	dist = psize[0]*3
	for boid in swarm:
		neighbours = [b for b in swarm if b != boid and abs((b.rect[0]+b.rect[1])-(boid.rect[0]+boid.rect[1])) < dist]
		boid.update(neighbours)

	# for shark in sharks:
	# 	victims = [b for b in swarm if abs((b.rect[0]+b.rect[1])-(shark.rect[0]+shark.rect[1])) < dist*2]
	# 	shark.update(victims)




if __name__ == "__main__":
	main()

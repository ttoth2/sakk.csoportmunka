import pygame

from tábla import Tábla

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

T = Tábla(WINDOW_SIZE[0], WINDOW_SIZE[1])

def draw(display):
	display.fill('white')
	T.r(display)
	pygame.display.update()


if __name__ == '__main__':
	running = True
	while running:
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					T.egér(mx, my)
		if T.matt('black'):
			print('fehér nyer!')
			running = False
		elif T.matt('white'):
			print('fekete nyer!')
			running = False

		draw(screen)
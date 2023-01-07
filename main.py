import pygame,sys,random
from pygame.math import Vector2

class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(1,0)
		self.new_block = False		

	def Draw_Snake(self):
		for block in self.body:
			x_pos = int(block.x * Cell_Size)
			y_pos = int(block.y * Cell_Size)
			block_rect = pygame.Rect(x_pos,y_pos,Cell_Size,Cell_Size)
			pygame.draw.rect(screen,(183,191,122),block_rect)

	def Snake_Move(self):
		if self.new_block == True:		
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
	
	def add_block(self):
		self.new_block = True

class APPLE:
	def __init__(self):
		self.randomize()

	def Draw_Apple(self):
		Fruit_Rect = pygame.Rect(int(self.pos.x * Cell_Size),int(self.pos.y * Cell_Size),Cell_Size,Cell_Size)
		pygame.draw.rect(screen,(126,166,114),Fruit_Rect)

	def randomize(self):
		self.x = random.randint(0,Cell_Number - 1)
		self.y = random.randint(0,Cell_Number - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = APPLE()
	
	def update(self):
		self.snake.Snake_Move()
		self.check_collision()
		self.check_fail()
  
	def draw_elements(self):
		self.fruit.Draw_Apple()
		self.snake.Draw_Snake()
		self.draw_score()

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()	
		
		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()
	
	def check_fail(self):
		if not (0 <= self.snake.body[0].x and self.snake.body[0].x < Cell_Number) or not (0 <= self.snake.body[0].y and self.snake.body[0].y < Cell_Number):
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()

	def game_over(self):
		pygame.quit()
		sys.exit()
	
	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text,True,(56,74,12))
		score_x = int(Cell_Size * Cell_Number - 60)	
		score_y = int(Cell_Size * Cell_Number - 40)	
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		screen.blit(score_surface,score_rect)

pygame.init()
Cell_Size = 40
Cell_Number = 20
screen = pygame.display.set_mode((Cell_Number * Cell_Size,Cell_Number * Cell_Size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 25)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0,-1)
			elif event.key == pygame.K_s:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0,1)
			elif event.key == pygame.K_d:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1,0)
			elif event.key == pygame.K_a:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1,0)
	screen.fill((175,215,70))
	main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)
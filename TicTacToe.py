import pygame
from pygame.locals import *

pygame.init()
DISPLAYSURFACE = pygame.display.set_mode((380,380))
BASICFONT = pygame.font.Font(None ,120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


## board functions ##
board = [[0,0,0],[0,0,0],[0,0,0]]

def new_board():
	global board
	board = [[0,0,0],[0,0,0],[0,0,0]]

def get_winner():
	# check rows
	for i in range(3):
		if abs(sum(board[i])) == 3:
			return int(sum(board[i])/3)

	# check cols
	for j in range(3):
		count = 0
		for i in range(3):
			count+=board[i][j]
		if abs(count) == 3:
			return int(count/3)

	# check diagonals
	count = 0
	for i in range(3):
		count+=board[i][i]
	if abs(count) == 3:
		return int(count/3)

	count = 0
	for i in range(3):
		count+=board[i][2-i]
	if abs(count) == 3:
		return int(count/3)

	# no winner
	return 0

def is_draw():
	count = 0
	for i in range(3):
		for j in range(3):
			if board[i][j] == 0:
				count+=1

	if count == 0:
		return True
	return False

def is_valid_move(x, y):
	return board[x][y] == 0

def render_board():
	DISPLAYSURFACE.fill(BLACK)
	x_offset = 20
	y_offset = 20
	for i in range(3):
		for j in range(3):
			pygame.draw.rect(DISPLAYSURFACE, WHITE, (120*j + 20 ,120*i + 20, 100, 100), 0)

	pygame.display.flip()

def update_board( x, y, playerID):
	global board
	col = x//120
	row = y//120
	if is_valid_move(row, col):
		board[row][col] = playerID
		textSurf = BASICFONT.render("X" if playerID == 1 else "O", True, BLACK)
		textRect = textSurf.get_rect()
		textRect.center = pygame.Rect(120*col+20 ,120*row+20 , 100, 100).center
		DISPLAYSURFACE.blit(textSurf, textRect)
		pygame.display.update(textRect)
		return True
	return False

def display_result():
	if is_draw():
		result = "DRAW!"
	else:
		result = "PLAYER " + ("1 " if get_winner() == 1 else "2 ") + "WINS!"

	RESULTFONT = pygame.font.Font(None ,40)
	textSurf = RESULTFONT.render(result, True, WHITE)
	textRect = textSurf.get_rect()
	textRect.center = DISPLAYSURFACE.get_rect().center
	pygame.draw.rect(DISPLAYSURFACE, BLACK, textRect, 0)
	DISPLAYSURFACE.blit(textSurf, textRect)
	pygame.display.update(textRect)

def new_game_requested():
	DIALOGFONT = pygame.font.Font(None ,20)
	textSurf = DIALOGFONT.render("press any key for new game", True, WHITE)
	textRect = textSurf.get_rect()
	textRect.bottom = DISPLAYSURFACE.get_rect().bottom
	pygame.draw.rect(DISPLAYSURFACE, BLACK, textRect, 0)
	DISPLAYSURFACE.blit(textSurf, textRect)
	pygame.display.update(textRect)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				return False
			elif event.type == KEYDOWN:
				return True


def main():
	done = False
	new_board()
	FPSCLOCK = pygame.time.Clock()
	player = 1
	render_board()
	while not done and not is_draw() and get_winner() == 0:
		for event in pygame.event.get():
			if event.type == QUIT:
				done = True
			elif event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if update_board(x, y, player):
					player*=-1

		FPSCLOCK.tick(30)

	display_result()
	if new_game_requested():
		main()


if __name__ == '__main__':
	main()
	pygame.quit()
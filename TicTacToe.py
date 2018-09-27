import pygame, random
from pygame.locals import *

pygame.init()
DISPLAYSURFACE = pygame.display.set_mode((380,380))
BASICFONT = pygame.font.Font(None ,120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

## board functions ##
board = [[0,0,0],[0,0,0],[0,0,0]]

def new_board():
	global board
	board = [[0,0,0],[0,0,0],[0,0,0]]

def get_winner():
	# check rows
	for i in range(3):
		if abs(sum(board[i])) == 3:
			return int(sum(board[i])/3), 'r', i

	# check cols
	for j in range(3):
		count = 0
		for i in range(3):
			count+=board[i][j]
		if abs(count) == 3:
			return int(count/3), 'c', j

	# check diagonals
	count = 0
	for i in range(3):
		count+=board[i][i]
	if abs(count) == 3:
		return int(count/3), 'd', 0

	count = 0
	for i in range(3):
		count+=board[i][2-i]
	if abs(count) == 3:
		return int(count/3), 'd', 1

	# no winner
	return [0]

def is_draw():
	count = 0
	for i in range(3):
		for j in range(3):
			if board[i][j] == 0:
				count+=1

	if count == 0 and get_winner()[0] == 0:
		return True
	return False

def is_valid_move(x, y, board):
	return x>=0 and x<3 and y>=0 and y<3 and (board[x][y] == 0)

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
	if is_valid_move(x, y, board):
		board[x][y] = playerID
		textSurf = BASICFONT.render("X" if playerID == 1 else "O", True, BLACK)
		textRect = textSurf.get_rect()
		textRect.center = pygame.Rect(120*y+20 ,120*x+20 , 100, 100).center
		DISPLAYSURFACE.blit(textSurf, textRect)
		pygame.display.update(textRect)
		return True
	return False

def display_result():
	if is_draw():
		result = "DRAW!"
	else:
		winner, collection_type, collection_index = get_winner()
		result = "PLAYER " + ("1 " if winner == 1 else "2 ") + "WINS!"
		if collection_type == 'r':
			pygame.draw.line(DISPLAYSURFACE, RED, (20,20*(1+collection_index) + 50*(1+2*collection_index)), (360,20*(1+collection_index) + 50*(1+2*collection_index)), 25)
		elif collection_type == 'c':
			pygame.draw.line(DISPLAYSURFACE, RED, (20*(1+collection_index) + 50*(1+2*collection_index),20), (20*(1+collection_index) + 50*(1+2*collection_index),360), 25)
		# diagonal case
		elif collection_index == 0:
			pygame.draw.line(DISPLAYSURFACE, RED, (20,20), (360,360), 25)
		else:
			pygame.draw.line(DISPLAYSURFACE, RED, (360,20), (20,360), 25)

	RESULTFONT = pygame.font.Font(None ,40)
	textSurf = RESULTFONT.render(result, True, WHITE)
	textRect = textSurf.get_rect()
	textRect.center = DISPLAYSURFACE.get_rect().center
	pygame.draw.rect(DISPLAYSURFACE, BLACK, textRect, 0)
	DISPLAYSURFACE.blit(textSurf, textRect)
	pygame.display.flip()

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

## AI ##
def random_ai(board, player):
	x = random.choice([0,1,2])
	y = random.choice([0,1,2])
	if is_valid_move(x, y, board):
		return [x, y]
	else:
		return random_ai(board, player)

def find_winning_moves_ai(board, player):

	# check rows
	for i in range(3):
		count = 0
		has_chance = True
		for j in range(3):
			if board[i][j] == -1*player:
				has_chance = False
				break
			if board[i][j] == player:
				count+=1
			else:
				blank = j
		if count == 2 and has_chance:
			return [i, blank]

	# check cols
	for j in range(3):
		count = 0
		has_chance = True
		for i in range(3):
			if board[i][j] == -1*player:
				has_chance = False
				break
			if board[i][j] == player:
				count+=1
			else:
				blank = i
		if count == 2 and has_chance:
			return [blank, j]

	# check diagonals
	count = 0
	has_chance = True
	for i in range(3):
		if board[i][i] == -1*player:
			has_chance = False
			break
		elif board[i][i] == player:
			count+=1
		else:
			blank = i
	if count == 2 and has_chance:
		return [blank, blank]

	count = 0
	has_chance = True
	for i in range(3):
		if board[i][2-i] == -1*player:
			has_chance = False
			break
		elif board[i][2-i] == player:
			count+=1
		else:
			blank = i
	if count == 2 and has_chance:
		return [blank, 2-blank]

	return random_ai(board, player)

def finds_winning_and_losing_moves_ai(board, player):

	losing_x = -1
	losing_y = -1

	# check rows
	for i in range(3):
		count = 0
		loss_chance_count = 0
		has_blank_spot = False
		has_chance = True
		for j in range(3):
			if board[i][j] == -1*player:
				has_chance = False
				loss_chance_count+=1
			elif board[i][j] == player:
				count+=1
			else:
				has_blank_spot = True
				blank = j
		if count == 2 and has_chance:
			return [i, blank]
		elif loss_chance_count == 2 and has_blank_spot:
			losing_x = i
			losing_y = blank

	# check cols
	for j in range(3):
		count = 0
		loss_chance_count = 0
		has_blank_spot = False
		has_chance = True
		for i in range(3):
			if board[i][j] == -1*player:
				has_chance = False
				loss_chance_count+=1
			elif board[i][j] == player:
				count+=1
			else:
				has_blank_spot = True
				blank = i
		if count == 2 and has_chance:
			return [blank, j]
		elif loss_chance_count == 2 and has_blank_spot:
			losing_x = blank
			losing_y = j


	# check diagonals
	count = 0
	loss_chance_count = 0
	has_blank_spot = False
	has_chance = True
	for i in range(3):
		if board[i][i] == -1*player:
			has_chance = False
			loss_chance_count+=1
		elif board[i][i] == player:
			count+=1
		else:
			has_blank_spot = True
			blank = i
	if count == 2 and has_chance:
		return [blank, blank]
	elif loss_chance_count == 2 and has_blank_spot:
		losing_x = blank
		losing_y = blank


	count = 0
	loss_chance_count = 0
	has_blank_spot = False
	has_chance = True
	for i in range(3):
		if board[i][2-i] == -1*player:
			has_chance = False
			loss_chance_count+=1
		elif board[i][2-i] == player:
			count+=1
		else:
			has_blank_spot = True
			blank = i
	if count == 2 and has_chance:
		return [blank, 2-blank]
	elif loss_chance_count == 2 and has_blank_spot:
		losing_x = blank
		losing_y = 2-blank

	if losing_x != -1:
		return [losing_x, losing_y] #BLOCK

	return random_ai(board, player)


def main():
	new_board()
	FPSCLOCK = pygame.time.Clock()
	player = 1
	render_board()
	while not is_draw() and get_winner()[0] == 0:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			# elif event.type == MOUSEBUTTONDOWN:
			# 	x, y = event.pos
			# 	if update_board(x, y, player):
			# 		player*=-1

		x, y = finds_winning_and_losing_moves_ai(board, player) if player == 1 else find_winning_moves_ai(board, player)
		if update_board(x, y, player):
			player*=-1

		FPSCLOCK.tick(30)

	display_result()
	if new_game_requested():
		main()


if __name__ == '__main__':
	main()
	pygame.quit()

## board functions ##
board = [[0,0,0],[0,0,0],[0,0,0]]

def new_board():
	global board
	board = [[0,0,0],[0,0,0],[0,0,0]]

def update_board( x, y, playerID):
	global board
	board[x][y] = playerID

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

## user interface ##

def get_valid_move():
	print("player"+str(1 if player>0 else 2)+" enter the move x y: ",end="")
	move = input()
	move = move.strip()
	while board[int(move[0])][int(move[2])] != 0:
		print("\nERROR enter a valid move x y: ",end="")
		move = input()
		move = move.strip()
	return move

def render_board():
	for i in range(3):
		for j in range(3):
			if board[i][j] == 1:
				print("X|",end="")
			elif board[i][j] == -1:
				print("O|",end="")
			else:
				print(" |",end="")
		print("\n_______")

## game loop ##

player = 1
render_board()
while not is_draw() and get_winner() == 0:
	move = get_valid_move()
	update_board(int(move[0]), int(move[2]), player)
	render_board()
	player*=-1

# end message #
if is_draw():
	print("DRAW!")
elif get_winner() == 1:
	print("Player 1 Wins!")
else:
	print("Player 2 Wins!")
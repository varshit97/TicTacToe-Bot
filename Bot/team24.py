import sys
import random
import signal

class Player24:

	def __init__(self):
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		new_flag=flag
		new_board = temp_board[:]
		new_block = temp_block[:]
		blocks_allowed = determine_blocks_allowed(old_move,new_block)
		cells = get_empty_out_of(new_board, blocks_allowed,new_block)
		ls=pruning(0,old_move,new_board,new_block,flag,-100000,1000000,new_flag)
		print ls[1]
		return ls[0]

def utility_calculation(new_board,new_block,new_flag):
	calc = []
	final_utility = 0.0000
	r=0
	for k in range(9):
		utility = 0
		starting_row = (k/3)*3
		starting_coloumn = (k%3)*3
	#rows
		for i in range(starting_row,starting_row+3):
			favour=0
			for j in range(starting_coloumn,starting_coloumn+3):
				if new_board[i][j] == new_flag:
					favour += 9
				elif new_board[i][j] == '-':
					favour += 4
				else:
					favour += 1
			if favour == 27:
				utility += 100
			elif favour == 22:
				utility += 10
			elif favour == 17:
				utility += 1
			elif favour == 3:
				utility -= 100
			elif favour == 6:
				utility -= 10
			elif favour == 9:
				utility -= 1
			else:
				utility = utility
	#coloumns
		for i in range(starting_coloumn,starting_coloumn+3):
			favour=0
			for j in range(starting_row,starting_row+3):
				if new_board[j][i] == new_flag:
					favour += 9
				elif new_board[j][i] == '-':
					favour += 4
				else:
					favour += 1
			if favour == 27:
				utility += 100
			elif favour == 22:
				utility += 10
			elif favour == 17:
				utility += 1
			elif favour == 3:
				utility -= 100
			elif favour == 6:
				utility -= 10
			elif favour == 9:
				utility -= 1
			else:
				utility = utility
	#diagonals
		favour = 0
		for i in range(3):
			if new_board[starting_row+i][starting_coloumn+i] == new_flag:
				favour += 9
			elif new_board[starting_row+i][starting_coloumn+i] == '-':
				favour += 4
			else:
				favour += 1
		if favour == 27:
			utility += 100
		elif favour == 22:
			utility += 10
		elif favour == 17:
			utility += 1
		elif favour == 3:
			utility -= 100
		elif favour == 6:
			utility -= 10
		elif favour == 9:
			utility -= 1
		else:
			utility = utility

		favour = 0
		for i in range(3):
			if new_board[starting_row+2-i][starting_coloumn+i] == new_flag:
				favour += 9
			elif new_board[starting_row+2-i][starting_coloumn+i] == '-':
				favour += 4
			else:
				favour += 1
		if favour == 27:
			utility += 100
		elif favour == 22:
			utility += 10
		elif favour == 17:
			utility += 1
		elif favour == 3:
			utility -= 100
		elif favour == 6:
			utility -= 10
		elif favour == 9:
			utility -= 1
		else:
			utility = utility

		calc.append(utility)
	# print calc
#	block heuristic calculation
	for i in range(3):
		favour = 0
		utility = 0
		for j in range(i*3,i*3+3):
			if new_block[j] == new_flag:
				favour += 9
			elif new_block[j] == 'o':
				favour += 1
			else:
				favour += 4
		if favour == 27:
			utility += 1000
		elif favour == 22:
			utility += 100
		elif favour == 17:
			utility += 10
		elif favour == 3:
			utility -= 1000
		elif favour == 6:
			utility -= 100
		elif favour == 9:
			utility -= 10
		else:
			utility = utility
		final_utility += utility
		l = 0
		for j in range(i*3,i*3+3):
			l += calc[j]
		l = l/100.0
		
		if (l>=1 and l<2):
			r=1+(l-1)*9
		elif (l>=2 and l<3):
			r=10+(l-2)*90
		elif (l>=3):
			r=100+(l-3)*900
		elif (l<=-1 and l>-2):
			r=-(1-(l+1)*9)
		elif (l<=-2 and l>-3):
			r=-(10-(l+2)*90)
		elif (l<=-3):
			r=-(100-(l+3)*900)
		else:
			r=l
		final_utility += r
		# print 'afterrows'
		# print final_utility
#   coloumns
	for i in range(3):
		favour = 0
		utility = 0
		for j in range(3):
			if new_block[i+j*3] == new_flag:
				favour += 9
			elif new_block[j*3+i] == 'o':
				favour += 1
			else:
				favour += 4
		if favour == 27:
			utility += 1000
		elif favour == 22:
			utility += 100
		elif favour == 17:
			utility += 10
		elif favour == 3:
			utility -= 1000
		elif favour == 6:
			utility -= 100
		elif favour == 9:
			utility -= 10
		else:
			utility = utility
		final_utility += utility
		l = 0
		for j in range(3):
			l += calc[j*3+i]
		l = l/100.0

		if (l>=1 and l<2):
			r=1+(l-1)*9
		elif (l>=2 and l<3):
			r=10+(l-2)*90
		elif (l>=3):
			r=100+(l-3)*900
		elif (l<=-1 and l>-2):
			r=-(1-(l+1)*9)
		elif (l<=-2 and l>-3):
			r=-(10-(l+2)*90)
		elif (l<=-3):
			r=-(100-(l+3)*900)
		else:
			r=l
		final_utility += r
#   diagonals
	favour = 0
	utility = 0
	for i in range(3):
		if new_block[i*4] == new_flag:
			favour += 9
		elif new_block[i*4] == 'o':
			favour += 1
		else:
			favour += 4
	if favour == 27:
		utility += 1000
	elif favour == 22:
		utility += 100
	elif favour == 17:
		utility += 10
	elif favour == 3:
		utility -= 1000
	elif favour == 6:
		utility -= 100
	elif favour == 9:
		utility -= 10
	else:
		utility = utility
	final_utility += utility
	l = 0
	for j in range(3):
		l += calc[j*4]
	l = l/100.0

	if (l>=1 and l<2):
		r=1+(l-1)*9
	elif (l>=2 and l<3):
		r=10+(l-2)*90
	elif (l>=3):
		r=100+(l-3)*900
	elif (l<=-1 and l>-2):
		r=-(1-(l+1)*9)
	elif (l<=-2 and l>-3):
		r=-(10-(l+2)*90)
	elif (l<=-3):
		r=-(100-(l+3)*900)
	else:
			r=l
	final_utility += r
	

	favour = 0
	utility = 0
	for i in range(1,4):
		if new_block[i*2] == new_flag:
			favour += 9
		elif new_block[i*2] == 'o':
			favour += 1
		else:
			favour += 4
	if favour == 27:
		utility += 1000
	elif favour == 22:
		utility += 100
	elif favour == 17:
		utility += 10
	elif favour == 3:
		utility -= 1000
	elif favour == 6:
		utility -= 100
	elif favour == 9:
		utility -= 10
	else:
		utility = utility
	final_utility += utility
	l = 0
	for j in range(3):
		l += calc[j*2+2]
	l = l/100.0

	if (l>=1 and l<2):
		r=1+(l-1)*9
	elif (l>=2 and l<3):
		r=10+(l-2)*90
	elif (l>=3):
		r=100+(l-3)*900
	elif (l<=-1 and l>-2):
		r=-(1-(l+1)*9)
	elif (l<=-2 and l>-3):
		r=-(10-(l+2)*90)
	elif (l<=-3):
		r=-(100-(l+3)*900)
	else:
			r=l
	final_utility += r
	#print final_utility
	return final_utility


def determine_blocks_allowed(old_move, block_stat):
	blocks_allowed = []
	if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
		blocks_allowed = [1,3]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
		blocks_allowed = [1,5]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
		blocks_allowed = [3,7]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
		blocks_allowed = [5,7]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
		blocks_allowed = [0,2]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
		blocks_allowed = [0,6]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
		blocks_allowed = [6,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
		blocks_allowed = [2,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
		blocks_allowed = [4]
	else:
		blocks_allowed = []
	final_blocks_allowed = []
	for i in blocks_allowed:
		if block_stat[i] == '-':
			final_blocks_allowed.append(i)
	return final_blocks_allowed


def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		new_blal = []
		all_blal = [0,1,2,3,4,5,6,7,8]
		for i in all_blal:
			if block_stat[i]=='-':
				new_blal.append(i)

		for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))
	#print cells
	return cells



def update_lists(local_board, local_block, move_ret, fl):
	local_board[move_ret[0]][move_ret[1]] = fl
	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0

	flag = 0
	for i in range(id1*3,id1*3+3):
		for j in range(id2*3,id2*3+3):
			if local_board[i][j] == '-':
				flag = 1


	if local_block[block_no] == '-':
		if local_board[id1*3][id2*3] == local_board[id1*3+1][id2*3+1] and local_board[id1*3+1][id2*3+1] == local_board[id1*3+2][id2*3+2] and local_board[id1*3+1][id2*3+1] != '-' and local_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if local_board[id1*3+2][id2*3] == local_board[id1*3+1][id2*3+1] and local_board[id1*3+1][id2*3+1] == local_board[id1*3][id2*3 + 2] and local_board[id1*3+1][id2*3+1] != '-' and local_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if local_board[id1*3][i]==local_board[id1*3+1][i] and local_board[id1*3+1][i] == local_board[id1*3+2][i] and local_board[id1*3][i] != '-' and local_board[id1*3][i] != 'D':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if local_board[i][id2*3]==local_board[i][id2*3+1] and local_board[i][id2*3+1] == local_board[i][id2*3+2] and local_board[i][id2*3] != '-' and local_board[i][id2*3] != 'D':
                                mflg = 1
                                break
	if flag == 0:
		local_block[block_no] = 'D'
	if mflg == 1:
		local_block[block_no] = fl
	return local_board


def pruning(step_no,old_move,new_board,new_block,flag,alpha,beta,new_flag):
	ls=[]
	ls.append(old_move)
	block_no = (old_move[0]/3)*3 + old_move[1]/3
	if step_no%2 == 1:
		ls.append(100000)
	else:
		ls.append(-100000)
	if step_no == 4	 :
		ls[1] = utility_calculation(new_board,new_block,new_flag)
		# for p in new_board:
			# print p
		return ls

	blocks_allowed = determine_blocks_allowed(old_move,new_block)
	valid_cells = get_empty_out_of(new_board, blocks_allowed,new_block)
	if len(valid_cells) == 0 :
		ls[1] = utility_calculation(new_board,new_block,new_flag)
		# for i in new_board:
			# print p
		return ls

	#print valid_cells
	if step_no%2==0:
		#print step_no
		for entry in valid_cells:
			local_board=[['-'for i in range(9)] for j in range(9)]
			local_block=['-' for i in range(9)]
			for i in range(9):
				for j in range(9):
					local_board[i][j]=new_board[i][j]
			for i in range(9):
				local_block[i]=new_block[i]
			# print 'newboard'
			# for i in new_board:
			# 	print i
			local_board= update_lists(local_board,local_block,entry,flag)
			# print 'updatednew'
			# for i in new_board:
			# 	print i
			x=pruning(step_no+1,entry,local_board,local_block,'o' if flag == 'x' else 'x',alpha,beta,new_flag)

			if (x[1]>alpha):
				alpha=x[1]
				final=entry
				ls=[]
				ls.append(final)
				ls.append(alpha)
			if (alpha>=beta):
				break;
		return ls
	else:
		#print step_no
		for entry in valid_cells:
			local_board=[['-'for i in range(9)] for j in range(9)]
			local_block=['-' for i in range(9)]
			for i in range(9):	
				for j in range(9):
					local_board[i][j]=new_board[i][j]
			for i in range(9):
				local_block[i]=new_block[i]
			# print 'newboard'
			# for i in new_board:
			# 	print i
			local_board=update_lists(local_board,local_block,entry,flag)
			x=pruning(step_no+1,entry,local_board,local_block,'o' if flag == 'x' else 'x',alpha,beta,new_flag)
			# print 'updatednew'
			# for i in new_board:
			# 	print i
			if (x[1]<beta):
				beta=x[1]
				final=entry
				ls=[]
				ls.append(final)
				ls.append(beta)
			if (alpha>=beta):
				break;
		return ls		

import curses
import random
import re
from curses import textpad
from threading import Timer
import operator

def introduction():
	print('\n')
	space = ' '*40
	game_name = '|Incredible Snake|'
	print(space + '-'*len(game_name))
	print(space + game_name)
	print(space + '-'*len(game_name))
	rule = '|Game introduction|'
	print('-'*len(rule))
	print(rule)
	print('-'*len(rule))
	print('Note: Incredible Snake is different from conventional snake game.')
	print('Some special items is added inside the game:')
	print("1.Cutter (denoted by 'C')")
	print("2.Thunder (denoted by 'X')")
	print("3.Dollar (denoted by '$')")
	print('\n')
	print('>Cutter will shorten the snake by one unit, but without incrementing the score.\n')
	print('>Hit by thunder will kill the snake.\n')
	print('>Dollar will enable the special game mode. Try to eat dollars as much as possible within the special game mode period. Dollar will counted towards the final score.\n')

def create_accout():
	user_list = []
	username = input('please enter your name\n>')
	pw = input('please enter the password\n>')
	# open the account_file to check whether the username already exists
	try:
		with open('account.txt','rt') as account_file:
			for line in account_file:
				if('username:' in line):
					name_with_title = line.rstrip('\n')
					name = name_with_title.replace('username:','')
					user_list.append(name)
	except IOError:
		account_file = open('account.txt','w+')
		
	# if username is already exists
	if(username in user_list):
		print('username already exists, please try others.\n')
		return False
	else:
		if(re.match(r'[A-Za-z0-9@#$%^&*]{8,}',pw) == None):
			print("password pattern is incorrect, password must be 8 characters long, and can mix with characters(upper case/lower case) or digits or special characters in '@#$%^&*' \n")
			return False
		else:
			account_info = 'username:' + username + '\npassword:' + pw + '\n---------------------\n'
			with open('account.txt','a+') as account_file:
				account_file.write(account_info)
			print('Create account successful, please log in.\n')
			return True

def beat_percentage():
	# store all players record into the dict
	player_dict = {}
	num_player = 0
	try:
		with open('game_record.txt','rt') as record_file:
			for line in record_file:
				num_player += 1
				(player,score) = line.rstrip('\n').split(':')
				player_dict[player] = score
		sorted_list = sorted(player_dict, key = lambda k: player_dict[k],reverse = True)
		current_index = sorted_list.index(start_player) + 1
		current_player_max_score = player_dict[start_player]
		num_player_beat = num_player - current_index
		if(num_player == 1):
			beat_percentage = 100
		else:
			beat_percentage = (num_player_beat/num_player)*100
		return (current_player_max_score,beat_percentage)
	except IOError:
		print('game record file has been deleted.')
	

def log_in():
	found_user = False
	username = input('username:\n>')
	pw = input('password:\n>')
	linenum = 0
	try:
		with open('account.txt','rt') as account_file:
			for line in account_file:
				linenum += 1
				if(username in line and 'username:' in line):
					target_line = linenum + 1
					found_user = True
				# if username is found, retrieve the password
				if(found_user == True):
					if(linenum == target_line):
						try:
							pw_line = line.rstrip('\n')
							password = pw_line.replace('password:','')
						except AttributeError:
							password = line
	except IOError:
		account_file = open('account.txt','w+')
	if(found_user == True and pw == password):
		return username
	else:
		print(found_user)
		print(pw)
		print('username not exists or incorrect password.\n')
		return False

def start_game():
	introduction()
	# print the game title
	try:
		choice = int(input('Let\'s start! \n1.Sign up\n2.Log in\n>'))
	except ValueError:
		print('Invalid input, please enter digit 1 or 2.\n')
		return False
	create_ok = False
	login_player = False
	# here handle the ValueError, if user enter non-integer value
	if(choice == 1):
		create_ok = create_accout()
	elif(choice == 2):
		login_player = log_in()
	else:
		print('Please enter only 1 or 2.\n')
		return False
	if(login_player != False):
		return login_player
	else:
		return False


def print_max_score(stdscr):
	record_dict = {}
	try:
		with open('game_record.txt','rt') as game_record:
			for line in game_record:
				(player,score) = line.rstrip('\n').split(':')
				record_dict[player] = score
		result = max(zip(record_dict.values(), record_dict.keys()))
		max_score = str(result[0])
		player = result[1]
		highest_score_output = '| ' + 'Highest record: ' + player + '[' + max_score + ']' + ' |'
	except:
		# if game_record.txt file not exists, just display empty max score
		highest_score_output = '| ' + 'Highest record: ' + ' |'
		
	decor = len(highest_score_output)*'-'
	stdscr.addstr(0,0,decor)
	stdscr.addstr(1,0,highest_score_output)
	stdscr.addstr(2,0,decor)
	stdscr.refresh()
	
	

# log the game record everytime when game over(only update the highest score)
def log_game_record(max_score):
	previous_record = False
	# create a file record file
	search_user_str = start_player + ':'
	try:
		old_file = open('game_record.txt','rt')
		old_record = old_file.read()
		old_file.close()
		with open('game_record.txt','rt') as record_file:
			for line in record_file:
				if(line.startswith(search_user_str)):
					highest_score_line = line.rstrip('\n')
					previous_record = True
		# if this player already has record
		if(previous_record == True):
			highest_score_line_split = highest_score_line.split(':')
			player_name = highest_score_line_split[0]
			highest_score = int(highest_score_line_split[1])
			
			if(max_score > highest_score):
				new_highest_score_line = player_name + ':' + str(max_score)
				new_record = old_record.replace(highest_score_line,new_highest_score_line)
				write_new_record = open('game_record.txt','wt')
				write_new_record.write(new_record)
				write_new_record.close()
		else:
			print('writing new record')
			# just store the record
			record_file = open('game_record.txt','a+')
			write_in_newfile = search_user_str + str(max_score) + '\n'
			record_file.write(write_in_newfile)
			record_file.close()
	except IOError:
		record_file = open('game_record.txt','w+')
		write_in_newfile = search_user_str + str(max_score) + '\n'
		record_file.write(write_in_newfile)
		record_file.close()

def create_dollar(snake,box,food,cutter,thunder_list):
	dollar = None
	while dollar is None:
		dollar =[random.randint(box[0][0]+2,box[1][0]-2),
		random.randint(box[0][1]+2,box[1][1]-2)]
		if dollar == food:
			dollar = None
		elif dollar in snake:
			dollar = None
		elif dollar == cutter:
			dollar = None
		elif dollar in thunder_list:
			dollar == None
	return dollar
	
# -------------------------------------------------
# if snake eat the $ sign, recreate the dollar list
# -------------------------------------------------
def dollar_mode_function(snake,box,food,cutter,thunder_list,stdscr):
	dollar_list = []
	k = 40
	# print $ sign on the screen
	while(k > 0):
		dollar = create_dollar(snake,box,food,cutter,thunder_list)
		dollar_list.append(dollar)
		k -= 1
	for dollar in dollar_list:
		stdscr.addstr(dollar[0],dollar[1],'$')
	return dollar_list	
	
# thunder will hit the snake and snake die
def create_thunder(snake,box,food,cutter):
	thunder = None
	while thunder is None:
		thunder =[random.randint(box[0][0]+1,box[1][0]-1),
		random.randint(box[0][1]+1,box[1][1]-1)]
		if thunder == food:
			thunder = None
		elif thunder in snake:
			thunder = None
		elif thunder == cutter:
			thunderr = None
	return thunder
	
# item 'cutter', after eat the length of the snake will cut half
def create_cutter(snake,box,food):
	cutter = None
	while cutter is None:
		cutter =[random.randint(box[0][0]+1,box[1][0]-1),
		random.randint(box[0][1]+1,box[1][1]-1)]
		# cutter cannot be overlap with food or snake body
		if cutter == food:
			cutter = None
		elif cutter in snake:
			cutter = None
	return cutter

def update_cutter(snake,box,food,cutter,stdscr):
	# current cutter disappear
	stdscr.addstr(cutter[0],cutter[1],' ')
	# create a new cutter
	cutter = create_cutter(snake,box,food)
	return cutter

def update_dollar(snake,box,food,cutter,thunder_list,dollar_list,stdscr):
	# create a new dollar
	dollar = create_dollar(snake,box,food,cutter,thunder_list)
	dollar_list.append(dollar)
	return dollar_list

def update_thunder(snake,box,food,cutter,k,thunder_list,stdscr):
	# create a new thunder_list
	while(k > 0):
		thunder = create_thunder(snake,box,food,cutter)
		thunder_list.append(thunder)
		k -= 1
	return thunder_list

# why do we need to take in snake and box?
# because the food cannot create on snake body or out of border
def create_food(snake,box):
	food = None
	while food is None:
		food = [random.randint(box[0][0]+4,box[1][0]-4),
		random.randint(box[0][1]+4,box[1][1]-4)]
		# food cannot be overlap with snake body
		if food in snake:
			food = None
	return food

def print_score(stdscr,score):
	# create score
	sh, sw = stdscr.getmaxyx()
	score_text = '| SCORE: {} |'.format(score)
	decor = '-'*len(score_text)
	stdscr.addstr(0,sw//2-len(score_text)//2,decor)
	stdscr.addstr(1,sw//2-len(score_text)//2,score_text)
	stdscr.addstr(2,sw//2-len(score_text)//2,decor)
	stdscr.refresh()
	
def main(stdscr):
	curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
	# cancel the cursor blinking
	player_score = {}
	curses.curs_set(0)
	# non blocking
	# intro to nodelay() function:
	# window.nodelay(yes)
	# if yes is 1, getch() will be non-blocking
	stdscr.nodelay(1)
	# how much time i wait for user to input
	# intro to timeout() function:
	# window.timeout(delay)
	# if delay is negative, blocking read is used(which will wait for input),if delay is 0, then non-blocking read is used, and -1 will be returned by getch() if no input is waiting. If delay is positive, then getch() will block for delay milliseconds and return -1 if there is still no input at the end of that time
	stdscr.timeout(time_out)
	# in curses, the coordinates is represented in the order (y,x)
	sh, sw = stdscr.getmaxyx()
	box = [[3,3],[sh-3,sw-3]]
	textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
	
	# ### this represent the snake body at the center of the rectangle
	# initializes the snake body
	# we can see the initialized snake body as a list of coordinates
	snake = [[sh//2,sw//2+1],[sh//2,sw//2],[sh//2,sw//2-1]]
	# snake[0] snake[1] snake[2]
	# snake[0][0] means the y coordinate of the snake body[0]
	# initialize the starting direction
	direction = curses.KEY_RIGHT
	
	# print the snake body
	# print text to screen:
	# you can specify the coordinates that you wish to print the string or
	# you can just print the string at the current position:
	# print at the current position:
	# addstr(str or ch)
	# print at the specify position:
	# addstr(y,x,str or ch)
	# Move to position y,x within the window, and display str or ch
	for y,x in snake:
		stdscr.addstr(y,x,'#') # print a # at the position (y,x)
	
	# create food
	food = create_food(snake,box)
	stdscr.addstr(food[0],food[1],'*',curses.color_pair(1))
	
	cutter = create_cutter(snake,box,food)
	stdscr.addstr(cutter[0],cutter[1],'C',curses.color_pair(2))
	
	max_score = 0
	# print the score
	score = 0

	print_score(stdscr,score)
	print_max_score(stdscr)
	
	move  = 0
	move1 = 0
	move2 = 0
	move3 = 0
	thunder_list = []
	dollar_list = []
	already_eaten_dollar_list = []
	dollar = False
	num_thunder = 4
	dollar_mode = False

	while 1:
		key = stdscr.getch()
		# if the user press any of the direction key, that means they want to change the direction of the snake
		if key in [curses.KEY_RIGHT,curses.KEY_LEFT,curses.KEY_UP,curses.KEY_DOWN]:
			direction = key
		
		# what if the key pressed is not direction key?
		# the direction will remain and do the update for the snake movement
		
		# the initialized head of the snake is snake[0]
		head = snake[0] # [sh//2,sw//2-1] coordinate
		
		# create new head based on different moving direction
		if direction == curses.KEY_RIGHT:
			# the new head y coordinate still the same, the x coordinate add one 
			# head[0] is the y coordinate, head[1] is the x coordinate
			new_head = [head[0],head[1]+1]
			move += 1
			move1 += 1
			move2 += 1
			move3 += 1
		elif direction == curses.KEY_LEFT:
			new_head = [head[0],head[1]-1]
			move += 1
			move1 += 1
			move2 += 1
			move3 += 1
		elif direction == curses.KEY_UP:
			new_head = [head[0]-1,head[1]]
			move += 1
			move1 += 1
			move2 += 1
			move3 += 1
		elif direction == curses.KEY_DOWN:
			new_head = [head[0]+1,head[1]]
			move += 1
			move1 += 1
			move2 += 1
			move3 += 1
		# insert the new head into snake body list
		# insert(0,x) is insert x at the front of the list
		snake.insert(0,new_head)
		# print the new head in front
		stdscr.addstr(new_head[0],new_head[1],'#')
# current snake pattern:
#    ###
#    ####
		
		# if move greater than 20, start to put thunder
		# use thunder list for multiple thunder
		# if enter special mode, stop generate thunder
		if(move == 20 and dollar_mode == False):
			t = num_thunder
			while(t>0):
				thunder = create_thunder(snake,box,food,cutter)
				thunder_list.append(thunder)
				t -= 1
			for thunder in thunder_list:
				stdscr.addstr(thunder[0],thunder[1],'X',curses.color_pair(3))	
		
		# reach 40 moves start to create dollar
		# inside the special mode, new dollar will stop generating also
		if(move == 40 and dollar_mode == False):
			dollar = create_dollar(snake,box,food,cutter,thunder_list)
			dollar_list.append(dollar)
			stdscr.addstr(dollar[0],dollar[1],'$',curses.color_pair(4))
		
		# add number of thunder with increasing of scores
		if(move3 != 0 and move3 % 300 == 0):
			num_thunder += 1
		
		# every 40 moves update the dollar
		# stop update when enter special mode
		if(move2 >= 40 and dollar_mode == False):
			k = num_thunder
			for thunder in thunder_list:
				stdscr.addstr(thunder[0],thunder[1],' ')
			thunder_list[:] = []
			thunder_list = update_thunder(snake,box,food,cutter,k,thunder_list,stdscr)
			for thunder in thunder_list:
				stdscr.addstr(thunder[0],thunder[1],'X',curses.color_pair(3))
			move2 = 0
		
		# update the cutter every 50 moves
		if(move1 > 50 and dollar_mode == False):
			# current cutter disappear
			stdscr.addstr(cutter[0],cutter[1],' ')
			# create a new cutter
			cutter = update_cutter(snake,box,food,cutter,stdscr)
			stdscr.addstr(cutter[0],cutter[1],'C',curses.color_pair(2))
			move1 = 0
			
		# update the dollar every 50 moves
		if(move > 50 and move%20 == 0 and dollar_mode == False):
			# current dollar disappear
			for dollar in dollar_list:
				stdscr.addstr(dollar[0],dollar[1],' ')
			dollar_list[:] = []
			# create a new dollar
			dollar_list = update_dollar(snake,box,food,cutter,thunder_list,dollar_list,stdscr)
			for dollar in dollar_list:
				stdscr.addstr(dollar[0],dollar[1],'$',curses.color_pair(4))
		
		# ---------------------
		# check what snake eat:
		# ---------------------
		if snake[0] == food:
			# update score
			score += 1
			print_score(stdscr,score)
			# create a new food
			food = create_food(snake,box)
			stdscr.addstr(food[0],food[1],'*',curses.color_pair(1))
		elif snake[0] == cutter:
			# remove the added part
			stdscr.addstr(snake[-1][0],snake[-1][1],' ')
			snake.pop()
			# remove one more part
			stdscr.addstr(snake[-1][0],snake[-1][1],' ')
			snake.pop()
			cutter = create_cutter(snake,box,food)
			stdscr.addstr(cutter[0],cutter[1],'C',curses.color_pair(2))
		
		# eat the dollar in normal mode and enter the special mode
		# clear all the items on the screen
		# and print 40 dollars in the special mode
		elif snake[0] in dollar_list:
			if(dollar_mode == False):
				if(snake[0] not in already_eaten_dollar_list):
					score += 1
				already_eaten_dollar_list.append(snake[0])
				print_score(stdscr,score)
				# set the mode to True, enter the special mode
				dollar_mode = True
				# reset the move
				# store all the items first
				cutter_store = cutter
				food_store = food
				thunder_store = thunder_list
				stdscr.addstr(cutter[0],cutter[1],' ')
				cutter = False
				stdscr.addstr(food[0],food[1],' ')
				food = False
				for thunder in thunder_list:
					stdscr.addstr(thunder[0],thunder[1],' ')
				thunder_list[:] = []
				move = 0
				# first clear the dollar sign in the screen also
				for dollar in dollar_list:
					stdscr.addstr(dollar[0],dollar[1],' ')
				dollar_list[:] = []
				# re-create the whole dollar list
				dollar_list = dollar_mode_function(snake,box,food,cutter,thunder_list,stdscr)

			
			# eat dollar inside the special mode
			# eat dollar in special mode will not increase the length
			elif(dollar_mode == True):
				# if the dollar has already been eaten, don't add score again
				if(snake[0] not in already_eaten_dollar_list):
					score += 1
				already_eaten_dollar_list.append(snake[0])
				print_score(stdscr,score)
				# if move reach 100, special mode end and reset the move to start normal mode again
				if(move > 100):
					move = 0
					dollar_mode = False
					# clear all the remaining $
					for dollar in dollar_list:
						stdscr.addstr(dollar[0],dollar[1],' ')
					dollar_list[:] = []
					# write back all the items
					cutter = cutter_store
					food = food_store
					thunder_list = thunder_store
					stdscr.addstr(food[0],food[1],'*',curses.color_pair(1))
					stdscr.addstr(cutter[0],cutter[1],'C',curses.color_pair(2))
					for thunder in thunder_list:
						stdscr.addstr(thunder[0],thunder[1],'X',curses.color_pair(3))
				
		else:
			# first print empty in the tail postion	
			stdscr.addstr(snake[-1][0],snake[-1][1],' ')
			# then pop the tail part 
			snake.pop()
			# complete the movement
		

		
		# when the game will end
		# when snake y position reach box left upper or right lower corner
		# or snake x position
		try:
			# # place a False value for thunder
			# thunder = False
			if (snake[0][0] in [box[0][0], box[1][0]] or
				snake[0][1] in [box[0][1], box[1][1]] or
				snake[0] in snake[1:] or 
				snake[0] in thunder_list):
				already_eaten_dollar_list = []
				record_dict = {}
				with open('game_record.txt','rt') as game_record:
					for line in game_record:
						(player,old_score) = line.rstrip('\n').split(':')
						record_dict[player] = old_score
				if(start_player in record_dict):
					max_score = int(record_dict[start_player])
					print('max score is: ', max_score)
					print('current score is: ',score)
					if(score>max_score):
						print('new record')
						max_score = score
						log_game_record(max_score)
				else:
					log_game_record(score)
				
				percentage_score = beat_percentage()
				current_score = str(percentage_score[0])
				percentage = str(percentage_score[1])
				if(snake[0] in thunder_list):
					msg1 = 'The thunder hit you! Game Over!'
				elif(snake[0] in snake[1:]):
					msg1 = 'You hit snake body! Game Over!'
				else:
					msg1 = 'You hit the border! Game Over!'
				msg2 = 'You highest score is ' + current_score
				msg3 = 'You have beat ' + percentage + '% of players.'
				msg4 = 'Press any key to exit the game.'
				stdscr.addstr(sh//2,sw//2-len(msg1)//2,msg1)
				stdscr.addstr(sh//2+1,sw//2-len(msg2)//2,msg2)
				stdscr.addstr(sh//2+2,sw//2-len(msg3)//2,msg3)
				stdscr.addstr(sh//2+3,sw//2-len(msg4)//2,msg4)
				# set after delay 8000, automatically exit the game,
				# or user enter anything to exit the 
				stdscr.timeout(8000)
				stdscr.getch()
				# break out of the game
				break
		except IndexError:
			already_eaten_dollar_list = []
			# if player manage to decrease the length to zero
			msg1 = 'OMG! The snake length is zero!'
			stdscr.addstr(sh//2,sw//2-len(msg1)//2,msg1)
			msg2 = 'You have unlocked a new ending! Amazing!'
			stdscr.addstr(sh//2+1,sw//2-len(msg2)//2,msg2)
			stdscr.timeout(8000)
			stdscr.getch()
			break
		except IOError:
			log_game_record(score)
		
		# refresh the screen to display the update
		stdscr.refresh()
	
# can just try to do create account function before use wrapper function
start_player = False
while(start_player == False):
	# only if login successful will the start_game return username
	start_player = start_game()
# speed to refresh the screen
time_out = 125
# start_color()
# wrapper(func,...)
# Wrapper function that initializes curses and calls another function, func
curses.wrapper(main)

	
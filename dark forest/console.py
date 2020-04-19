# dark room

# how to design the whole game:
# 1. dinasour 2. food 3. key 4. lotus 5. tree

# Note that there are 3 kinds of trees (climb tree will cost 1 energy)
# 1. with fruit (recover 5 energy)
# 2. able to oversee one side
# 3. you will fall down (HP - )


# the game has 4 levels, player start from first level to final level

import time
import random
import sys

level_complete = False
current_level = 1


first_time_to_level_1 = True
first_time_to_level_2 = True
first_time_to_level_3 = True

def slow_print(s):
	for c in s + '\n':
		sys.stdout.write(c)
		sys.stdout.flush() # defeat buffering
		time.sleep(random.random() * 0.08)

energy = 10
HP = 5

player_pos = [1,1]
# been_before is a list of all cords that visited before
been_before = []

item = {'boat':0}
already_meet_river_god = False

# background
intro_file = open('intro.txt','r')
intro_text = intro_file.read()
intro_file.close()
print(intro_text)



# 手动创建地图
# 4x4 6x6 8x8 10x10

upper_bound_lv1 =  ['#','#','#','#','#','#']
first_line_lv1 = ['#','Y',' ',' ',' ','#']
second_line_lv1 = ['#',' ',' ',' ',' ','#']
third_line_lv1 = ['#',' ',' ',' ',' ','#']
forth_line_lv1 = ['#',' ',' ',' ',' ','#']
lower_bound_lv1 = ['#','#','#','#','#','#']

# level 2 [6x6]
upper_bound_lv2 =  ['#','#','#','#','#','#','#','#']
first_line_lv2 = ['#','Y',' ',' ',' ',' ',' ','#']
second_line_lv2 = ['#',' ',' ',' ',' ',' ',' ','#']
third_line_lv2 = ['#',' ',' ',' ',' ',' ',' ','#']
forth_line_lv2 = ['#',' ',' ',' ',' ',' ',' ','#']
fifth_line_lv2 = ['#',' ',' ',' ',' ',' ',' ','#']
sixth_line_lv2 = ['#',' ',' ',' ',' ',' ',' ','#']
lower_bound_lv2 = ['#','#','#','#','#','#','#','#']

# level 3 [8x8]
upper_bound_lv3 =  ['#','#','#','#','#','#','#','#','#','#']
first_line_lv3 = ['#','Y',' ',' ',' ',' ',' ',' ',' ','#']
second_line_lv3 = ['#',' ',' ',' ',' ',' ',' ',' ',' ','#']
third_line_lv3 = ['#',' ',' ',' ',' ',' ','~','~','~','#']
forth_line_lv3 = ['#',' ',' ',' ','~','~','~',' ',' ','#']
fifth_line_lv3 = ['#',' ',' ',' ','~','~',' ',' ',' ','#']
sixth_line_lv3 = ['#',' ',' ',' ','~',' ',' ',' ',' ','#']
seventh_line_lv3 = ['#','~','~','~',' ',' ',' ',' ',' ','#']
eight_line_lv3 = ['#',' ',' ',' ',' ',' ',' ',' ',' ','#']
lower_bound_lv3 = ['#','#','#','#','#','#','#','#','#','#']


def meet_fall_tree():
	global HP
	global energy
	global broken_tree_pos
	
	try:
		broken_tree_pos.remove(player_pos)
	except ValueError:
		print('current tree already been removed.')
	
	print('There is a huge tree in front of you, you want to:')
	choice = input('1. climb tree\n2. walk away (climb tree will cost one energy)\n>')
	
	if(choice == '1'):
		print('\nThe tree is broken and you fall down! HP-1')
		HP -= 1
		energy -= 1
	elif(choice == '2'):
		print('\nYou walk away...')
	else:
		print('\nInvalid choice, please enter again.')
		meet_fall_tree()

def meet_fruit_tree():
	global energy
	global fruit_tree_pos
	
	try:
		fruit_tree_pos.remove(player_pos)
	except ValueError:
		print('current tree already been removed.')
	
	print('There is a huge tree in front of you, you want to:')
	choice = input('1. climb tree\n2. walk away (climb tree will cost one energy, please enter the number of action.)\n>')
	
	if(choice == '1'):
		print('\nYou found a fruit on the tree! energy + 5')
		energy += 4
	elif(choice == '2'):
		print('\nYou walk away...')
	else:
		print('\nInvalid choice, please enter again.')
		meet_fruit_tree()



def meet_overwatch_tree():
	global energy
	global overwatch_tree_pos

	print('There is a huge tree in front of you, you want to:')
	choice = input('1. climb tree\n2. walk away (climb tree will cost one energy)\n>')
	# use a dict to store all things in that direction
	view = {'tree':0,'dinasour':0,'lotus':0,'key':0}
	
	try:
		overwatch_tree_pos.remove(player_pos)
	except ValueError:
		print('current tree already been removed.')

	if(choice == '1'):
		energy -= 1
		print('\nYou are standing on the top of the tree, you are able to view one direction of dark forest, which direction you would like to view?')
		direction_view = input('up\ndown\nleft\nright\n>')
		
		if(direction_view == 'left'):
			for overwatch_tree in overwatch_tree_pos:
				if(overwatch_tree[0] == player_pos[0] and overwatch_tree[1] < player_pos[1]):
					view['tree'] += 1
			for fruit_tree in fruit_tree_pos:
				if(fruit_tree[0] == player_pos[0] and fruit_tree[1] < player_pos[1]):
					view['tree'] += 1
			for broken_tree in broken_tree_pos:
				if(broken_tree[0] == player_pos[0] and broken_tree[1] < player_pos[1]):
					view['tree'] += 1
			if(type(dinasour_pos[0]) == list):
				for dinasour in dinasour_pos:
					if(dinasour[0] == player_pos[0] and dinasour[1] < player_pos[1]):
						view['dinasour'] += 1
			else:
				if(dinasour[0] == player_pos[0] and dinasour[1] < player_pos[1]):
					view['dinasour'] += 1
			if(key_pos[0] == player_pos[0] and key_pos[1] < player_pos[1]):
				view['key'] += 1
			if(type(lotus_pos[0]) == list):
				for lotus in lotus_pos:
					if(lotus[0] == player_pos[0] and lotus[1] < player_pos[1]):
						view['lotus'] += 1
			else:
				if(lotus_pos[0] == player_pos[0] and lotus_pos[1] < player_pos[1]):
					view['lotus'] += 1
				
		elif(direction_view == 'right'):
			for overwatch_tree in overwatch_tree_pos:
				if(overwatch_tree[0] == player_pos[0] and overwatch_tree[1] > player_pos[1]):
					view['tree'] += 1
			for fruit_tree in fruit_tree_pos:
				if(fruit_tree[0] == player_pos[0] and fruit_tree[1] > player_pos[1]):
					view['tree'] += 1
			for broken_tree in broken_tree_pos:
				if(broken_tree[0] == player_pos[0] and broken_tree[1] > player_pos[1]):
					view['tree'] += 1
			if(type(dinasour_pos[0]) == list):
				for dinasour in dinasour_pos:
					if(dinasour[0] == player_pos[0] and dinasour[1] > player_pos[1]):
						view['dinasour'] += 1
			else:
				if(dinasour_pos[0] == player_pos[0] and dinasour_pos[1] > player_pos[1]):
					view['dinasour'] += 1
			if(key_pos[0] == player_pos[0] and key_pos[1] > player_pos[1]):
				view['key'] += 1
			if(type(lotus_pos[0]) == list):
				for lotus in lotus_pos:
					if(lotus[0] == player_pos[0] and lotus[1] > player_pos[1]):
						view['lotus'] += 1
			else:
				if(lotus_pos[0] == player_pos[0] and lotus_pos[1] > player_pos[1]):
					view['lotus'] += 1
				
		elif(direction_view == 'down'):
			for overwatch_tree in overwatch_tree_pos:
				if(overwatch_tree[1] == player_pos[1] and overwatch_tree[0] > player_pos[0]):
					view['tree'] += 1
			for fruit_tree in fruit_tree_pos:
				if(fruit_tree[1] == player_pos[1] and fruit_tree[0] > player_pos[0]):
					view['tree'] += 1
			for broken_tree in broken_tree_pos:
				if(broken_tree[1] == player_pos[1] and broken_tree[0] > player_pos[0]):
					view['tree'] += 1
			if(type(dinasour_pos[0]) == list):
				for dinasour in dinasour_pos:
					if(dinasour[1] == player_pos[1] and dinasour[0] > player_pos[0]):
						view['dinasour'] += 1
			else:
				if(dinasour_pos[1] == player_pos[1] and dinasour_pos[0] > player_pos[0]):
					view['dinasour'] += 1
			if(key_pos[1] == player_pos[1] and key_pos[0] > player_pos[0]):
				view['key'] += 1
			if(type(lotus_pos[0]) == list):
				for lotus in lotus_pos:
					if(lotus[1] == player_pos[1] and lotus[0] > player_pos[0]):
						view['lotus'] += 1
			else:
				if(lotus_pos[1] == player_pos[1] and lotus_pos[0] > player_pos[0]):
					view['lotus'] += 1
				
		elif(direction_view == 'up'):
			for overwatch_tree in overwatch_tree_pos:
				if(overwatch_tree[1] == player_pos[1] and overwatch_tree[0] < player_pos[0]):
					view['tree'] += 1
			for fruit_tree in fruit_tree_pos:
				if(fruit_tree[1] == player_pos[1] and fruit_tree[0] < player_pos[0]):
					view['tree'] += 1
			for broken_tree in broken_tree_pos:
				if(broken_tree[1] == player_pos[1] and broken_tree[0] < player_pos[0]):
					view['tree'] += 1
			if(type(dinasour_pos[0]) == list):
				for dinasour in dinasour_pos:
					if(dinasour[1] == player_pos[1] and dinasour[0] < player_pos[0]):
						view['dinasour'] += 1
			else:
				if(dinasour_pos[1] == player_pos[1] and dinasour_pos[0] < player_pos[0]):
					view['dinasour'] += 1
			if(key_pos[1] == player_pos[1] and key_pos[0] < player_pos[0]):
				view['key'] += 1
			if(type(lotus_pos[0]) == list):
				for lotus in lotus_pos:
					if(lotus[1] == player_pos[1] and lotus[0] < player_pos[0]):
						view['lotus'] += 1
			else:
				if(lotus_pos[1] == player_pos[1] and lotus_pos[0] < player_pos[0]):
					view['lotus'] += 1
		print('View result:')
		print(view)
		
	elif(choice == '2'):
		print('\nYou walk away...')
	else:
		print('\nInvalid choice, please enter again.')
		meet_overwatch_tree()

def meet_lotus():
	global lotus_pos
	global HP
	# delete the lotus from the map
	
	if(current_level == 3):
		if(len(lotus_pos) == 2):
			lotus_pos.remove(player_pos)
		else:
			lotus_pos = [0,0]
	else:
		lotus_pos = [0,0]
	print('You get a lotus, lotus recover life + 5.')
	HP = HP + 5

def meet_dinasour():
	global HP
	global dinasour_pos
	# 遇到过的恐龙就从列表里移除
	
	# level 3的时候有两只恐龙
	if(current_level == 3):
		dinasour_pos.remove(player_pos)
	else:
		dinasour_pos = [0,0]
	print('You meet a dinasour! The dinasour attacks you, HP-5!')
	HP = HP - 5


def display_smell():							
	if(current_level == 3):
		for dinasour in dinasour_pos:
			if(abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) <= 1 ):
				print('I can feel that the dinasour is just beside me...')
				break
			
			elif(abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) == 2 ):
				print('The disgusting stench grew stronger as you approach forward...')
				break
			
			elif(abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) > 2 and abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) <= 4  ):
				print('A strange stench comes from far away...')
				break
	
	else:
		if(abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) <= 1 ):
			print('I can feel that the dinasour is just beside me...')
		
		elif(abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) == 2 ):
			print('The disgusting stench grew stronger as you approach forward...')
		
		elif(abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) > 2 and abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) <= 4  ):
			print('A strange stench comes from far away...')

def marked_visted():
	if(current_level == 1):
		global whole_board_lv1_for_update
		whole_board_lv1_for_update[player_pos[0]][player_pos[1]] = 'X'
	elif(current_level == 2):
		global whole_board_lv2_for_update
		whole_board_lv2_for_update[player_pos[0]][player_pos[1]] = 'X'
	elif(current_level == 3):
		global whole_board_lv3_for_update
		if(player_pos not in river_pos):
			whole_board_lv3_for_update[player_pos[0]][player_pos[1]] = 'X'
		else:
			whole_board_lv3_for_update[player_pos[0]][player_pos[1]] = '~'

def get_key():
	global level_complete
	print('Congradulation! You get the key!')
	level_complete = True

# player_pos = [1,1]
def move(direction):	
	global player_pos
	global energy
	
	marked_visted()
	
	if(direction == 'right'):
		player_pos[1] += 1
	elif(direction == 'left'):
		player_pos[1] -= 1
	elif(direction == 'up'):
		player_pos[0] -= 1
	else:
		player_pos[0] += 1
	energy -= 1
	
	print('Your current position: ',player_pos)
	

# level 1 [4x4]
def level_1_board():
	global dinasour_pos
	global lotus_pos
	global key_pos
	global first_time_to_level_1
	
	
	if(first_time_to_level_1 == True):
		# level 1 game init
		dinasour_pos = [2,3]
		key_pos = [4,4]
		lotus_pos = [2,2]
	
	first_time_to_level_1 = False
	
	global first_line_lv1
	global second_line_lv1
	global third_line_lv1
	global forth_line_lv1
	global whole_board_lv1_display
	global whole_board_lv1_for_update
	
	whole_board_lv1_for_update = [upper_bound_lv1,first_line_lv1,second_line_lv1,third_line_lv1,forth_line_lv1,lower_bound_lv1]
	
	upper_bound_lv1_display = ' '.join(upper_bound_lv1)
	first_line_lv1_display = ' '.join(first_line_lv1)
	second_line_lv1_display = ' '.join(second_line_lv1)
	third_line_lv1_display = ' '.join(third_line_lv1)
	forth_line_lv1_display = ' '.join(forth_line_lv1)
	lower_bound_lv1_display = ' '.join(lower_bound_lv1)

	whole_board_lv1 = [upper_bound_lv1_display,first_line_lv1_display,second_line_lv1_display,third_line_lv1_display,forth_line_lv1_display,lower_bound_lv1_display]
	
	whole_board_lv1_display = '\n'.join(whole_board_lv1)
	
	print()
	print(whole_board_lv1_display)

# level 2 [6x6]
def level_2_board():
	global lotus_pos
	global dinasour_pos
	global key_pos
	global broken_tree_pos
	global overwatch_tree_pos
	global fruit_tree_pos
	global first_time_to_level_2
	
	if(first_time_to_level_2 == True):
		lotus_pos = [3,2]
		dinasour_pos = [5,5]
		key_pos = [5,6]
		broken_tree_pos = [[2,1],[2,4]]
		overwatch_tree_pos = [[5,2],[3,3],[4,4]]
		fruit_tree_pos = [[2,3],[6,3],[3,5],[2,6]]
	
	first_time_to_level_2 = False
	
	global first_line_lv2
	global second_line_lv2
	global third_line_lv2
	global forth_line_lv2
	global fifth_line_lv2
	global sixth_line_lv2
	global whole_board_lv2_display
	global whole_board_lv2_for_update
	
	whole_board_lv2_for_update = [upper_bound_lv2,first_line_lv2,second_line_lv2,third_line_lv2,forth_line_lv2,fifth_line_lv2,sixth_line_lv2,lower_bound_lv2]

	upper_bound_lv2_display = ' '.join(upper_bound_lv2)
	first_line_lv2_display = ' '.join(first_line_lv2)
	second_line_lv2_display = ' '.join(second_line_lv2)
	third_line_lv2_display = ' '.join(third_line_lv2)
	forth_line_lv2_display = ' '.join(forth_line_lv2)
	fifth_line_lv2_display = ' '.join(fifth_line_lv2)
	sixth_line_lv2_display = ' '.join(sixth_line_lv2)
	lower_bound_lv2_display = ' '.join(lower_bound_lv2)

	whole_board_lv2 = [upper_bound_lv2_display,first_line_lv2_display,second_line_lv2_display,third_line_lv2_display,forth_line_lv2_display,fifth_line_lv2_display,sixth_line_lv2_display,lower_bound_lv2_display]

	whole_board_lv2_display = '\n'.join(whole_board_lv2)

	print()
	print(whole_board_lv2_display)

def meet_river():
	global energy
	if(item['boat']>0):
		print('You used one boat to cross the river, no energy cost.')
		energy += 1
		item['boat'] = item['boat'] - 1
		if(item['boat'] == 0):
			print('You run out of boat...')
	else:
		print('You are step into a river, and you need to swim to across the river... (swim will cost 1 more energy than on the ground)')
		energy -= 1

def meet_river_god():
	global item
	global fruit_tree_pos
	global overwatch_tree_pos
	global broken_tree_pos
	global already_meet_river_god
	already_meet_river_god = True
	print('You have met the god of river!')
	# use slow print to print what god of river said
	
	print('God of river: I can satisfy one of your dream, what is your wish?')
	wish = input('1.I want to have lots of food to recover energy!\n2.I want to light up the dark forest!\n3.I am fine, I don\'t need anything!\n')
	# all the trees becomes fruit tree
	if(wish == '1'):
		print('God of river: As you wish, I already make all the trees in the forest full of fruit! You can enjoy endless fruits!')
		slow_print_text = 'All the trees in the forest becomes fruit tree!'
		slow_print(slow_print_text)
		fruit_tree_pos = fruit_tree_pos + overwatch_tree_pos + broken_tree_pos
		del overwatch_tree_pos[:]
		del broken_tree_pos[:]
	elif(wish == '2'):
		print('God of river: As you wish, I will light up the forest!')
		
		if(fruit_tree_pos[0] != 0):
			fruit_tree_num = len(fruit_tree_pos)
		else:
			fruit_tree_num = 0
		if(overwatch_tree_pos[0] != 0):
			overwatch_tree_num = len(overwatch_tree_pos)
		else:
			overwatch_tree_num = 0
		if(broken_tree_pos[0] != 0):
			broken_tree_num = len(broken_tree_pos)
		else:
			broken_tree_num = 0
		if(lotus_pos[0] != 0):
			lotus_num = len(lotus_pos)
		else:
			lotus_num = 0
		dinasour_num = len(dinasour_pos)
		
		light_up_text = 'A huge thunder suddenly appear in the sky, the whole forest has been light up at that moment!\nfruit tree: ' + str(fruit_tree_num) + '\nbroken tree: ' + str(broken_tree_num) + '\noverwatch tree: ' + str(overwatch_tree_num) + '\nlotus: ' + str(lotus_num) + '\ndinasour: ' + str(dinasour_num)
		
		slow_print(light_up_text)
		
		tree_shocked_text = '\nWait, but the thunder is so powerful that some trees in the forest has been hit and fall down!'
		slow_print(tree_shocked_text)
		
		
		# random some of the trees fall down
		all_trees = fruit_tree_pos + overwatch_tree_pos + broken_tree_pos
		shocked_tree = random.sample(all_trees,5)
		for tree in shocked_tree:
			if(tree in fruit_tree_pos):
				fruit_tree_pos.remove(tree)
			elif(tree in overwatch_tree_pos):
				overwatch_tree_pos.remove(tree)
			else:
				broken_tree_pos.remove(tree)
	elif(wish == '3'):
		print('God of river: Oh! You don\'t have any wish from me! I am so touched, hardly have a people like you! I want to cry!\nGod of river give you a boat.')
		slow_print_text = 'You get two boat. (boat only last for one ride, after one ride the boat will be damaged.)'
		slow_print(slow_print_text)
		# a boat can save your extra energy in river
		item['boat'] = 2
	else:
		print('Invalid choice! please enter again!')
		meet_river_god()
		
				

# level 3 [8x8]
def level_3_board():
	global dinasour_pos
	global key_pos
	global lotus_pos
	global overwatch_tree_pos
	global broken_tree_pos
	global fruit_tree_pos
	global river_pos
	global first_time_to_level_3
	
	
	
	if(first_time_to_level_3 == True):
		dinasour_pos = [[3,4],[6,8]]
		key_pos = [7,6]
		lotus_pos = [[3,5],[5,7]]
		overwatch_tree_pos = [[3,3],[6,6],[2,8]]
		broken_tree_pos = [[2,2],[2,6],[8,8]]
		fruit_tree_pos = [[3,2],[2,3],[2,4],[1,5],[1,8],[5,3],[6,1],[6,5],[8,5],[7,8]]
		
		river_pos = [[7,1],[7,2],[7,3],[7,4],[6,4],[5,4],[4,4],[4,5],[5,5],[4,6],[3,6],[3,7],[3,8]]
	
	first_time_to_level_3 = False

	global first_line_lv3
	global second_line_lv3
	global third_line_lv3
	global forth_line_lv3
	global fifth_line_lv3
	global sixth_line_lv3
	global seventh_line_lv3
	global eight_line_lv3
	global whole_board_lv3_display
	global whole_board_lv3_for_update
	
	whole_board_lv3_for_update = [upper_bound_lv3,first_line_lv3,second_line_lv3,third_line_lv3,forth_line_lv3,fifth_line_lv3,sixth_line_lv3,seventh_line_lv3,eight_line_lv3,lower_bound_lv3]

	upper_bound_lv3_display = ' '.join(upper_bound_lv3)
	first_line_lv3_display = ' '.join(first_line_lv3)
	second_line_lv3_display = ' '.join(second_line_lv3)
	third_line_lv3_display = ' '.join(third_line_lv3)
	forth_line_lv3_display = ' '.join(forth_line_lv3)
	fifth_line_lv3_display = ' '.join(fifth_line_lv3)
	sixth_line_lv3_display = ' '.join(sixth_line_lv3)
	seventh_line_lv3_display = ' '.join(seventh_line_lv3)
	eight_line_lv3_display = ' '.join(eight_line_lv3)
	lower_bound_lv3_display = ' '.join(lower_bound_lv3)

	whole_board_lv3 = [upper_bound_lv3_display,first_line_lv3_display,second_line_lv3_display,third_line_lv3_display,forth_line_lv3_display,fifth_line_lv3_display,sixth_line_lv3_display,seventh_line_lv3_display,eight_line_lv3_display,lower_bound_lv3_display]

	whole_board_lv3_display = '\n'.join(whole_board_lv3)

	print()
	print(whole_board_lv3_display)


def update_player_position():
	# with player_pos [1,1] -> [1,2]
	# how to update the display?
	if(current_level == 1):
		global whole_board_lv1_for_update
		whole_board_lv1_for_update[player_pos[0]][player_pos[1]] = 'Y'
	elif(current_level == 2):
		global whole_board_lv2_for_update
		whole_board_lv2_for_update[player_pos[0]][player_pos[1]] = 'Y'
	elif(current_level == 3):
		global whole_board_lv3_for_update
		whole_board_lv3_for_update[player_pos[0]][player_pos[1]] = 'Y'






def level_1_game():
	display_smell()
	# display the game board, arrange everything position
	print('\n')
	print('Which direction you want to go?')
	
	all_direction = ['up','down','left','right']
	# 如果在最下面一行，就不显示down选项
	if(player_pos[0] == 4):
		all_direction.remove('down')
	# 如果在最上面一行，就不显示up选项
	if(player_pos[0] == 1):
		all_direction.remove('up')
	if(player_pos[1] == 1):
		all_direction.remove('left')
	if(player_pos[1] == 4):
		all_direction.remove('right')
	
	all_direction_choice = '\n'.join(all_direction)
	print(all_direction_choice)
	direction_raw = input('>')
	direction = direction_raw.lower()
	while(direction not in all_direction):
		print('Invalid direction, please enter again.\n')
		direction_raw = input('up\ndown\nleft\nright\n>')
		direction = direction_raw.lower()
	
	move(direction)
	update_player_position()
	if(player_pos == lotus_pos):
		meet_lotus()
	elif(player_pos == dinasour_pos):
		meet_dinasour()
	elif(player_pos == key_pos):
		get_key()
	# print('after move')
	level_1_board()
	print('energy [',energy,']')
	print('HP [',HP,']')




def level_2_game():
	display_smell()
	# display the game board, arrange everything position
	print('\n')
	print('Which direction you want to go?')
		
	all_direction = ['up','down','left','right']
	# 如果在最下面一行，就不显示down选项
	if(player_pos[0] == 6):
		all_direction.remove('down')
	# 如果在最上面一行，就不显示up选项
	if(player_pos[0] == 1):
		all_direction.remove('up')
	if(player_pos[1] == 1):
		all_direction.remove('left')
	if(player_pos[1] == 6):
		all_direction.remove('right')
	
	all_direction_choice = '\n'.join(all_direction)
	print(all_direction_choice)
	direction_raw = input('>')
	direction = direction_raw.lower()
	
	while(direction not in all_direction):
		print('Invalid direction, please enter again.\n')
		direction_raw = input('up\ndown\nleft\nright\n>')
		direction = direction_raw.lower()
		
	move(direction)
	update_player_position()
	if(player_pos == lotus_pos):
		meet_lotus()
	elif(player_pos == dinasour_pos):
		meet_dinasour()
	elif(player_pos == key_pos):
		get_key()
	elif(player_pos in fruit_tree_pos):
		meet_fruit_tree()
	elif(player_pos in broken_tree_pos):
		meet_fall_tree()
	elif(player_pos in overwatch_tree_pos):
		meet_overwatch_tree()
	# print('after move')
	level_2_board()
	print('energy [',energy,']')
	print('HP [',HP,']')

def level_3_game():
	
	display_smell()
	# display the game board, arrange everything position
	print('\n')
	print('Which direction you want to go?')
	
	all_direction = ['up','down','left','right']
	# 如果在最下面一行，就不显示down选项
	if(player_pos[0] == 8):
		all_direction.remove('down')
	# 如果在最上面一行，就不显示up选项
	if(player_pos[0] == 1):
		all_direction.remove('up')
	if(player_pos[1] == 1):
		all_direction.remove('left')
	if(player_pos[1] == 8):
		all_direction.remove('right')
	
	all_direction_choice = '\n'.join(all_direction)
	print(all_direction_choice)
	direction_raw = input('>')
	direction = direction_raw.lower()
	
	while(direction not in all_direction):
		print('Invalid direction, please enter again.\n')
		direction_raw = input('up\ndown\nleft\nright\n>')
		direction = direction_raw.lower()
		
	move(direction)
	update_player_position()
	if(player_pos in lotus_pos):
		meet_lotus()
	elif(player_pos in dinasour_pos):
		meet_dinasour()
	elif(player_pos == key_pos):
		get_key()
	elif(player_pos in fruit_tree_pos):
		meet_fruit_tree()
	elif(player_pos in broken_tree_pos):
		meet_fall_tree()
	elif(player_pos in overwatch_tree_pos):
		meet_overwatch_tree()
	elif(player_pos in river_pos):
		if(already_meet_river_god == False):
			meet_river_god()
		meet_river()
	# print('after move')
	level_3_board()
	print('energy [',energy,']')
	print('HP [',HP,']')


if(current_level == 1):
	print('\n==================================================')
	print('LEVEL 1')
	print('energy [',energy,']')
	print('HP [',HP,']')
	level_1_board()
	print()
	# display_smell()
	while(level_complete == False and energy > 0 and HP > 0):
		level_1_game()
	if(energy == 0):
		print('Game over! You fail to escape from the dark forest, you run out of energy...')
	elif(HP == 0):
		print('Game over! You fail to escape from the dark forest, you are killed...')
	else:
		# if level 1 is complete
		print('Congradulation on complete level 1!')
		print('Entering level 2...')
		time.sleep(5)
		current_level = 2

if(current_level == 2):
	# reset the game init
	level_complete = False
	energy = 10
	HP = 5
	player_pos = [1,1]
	
	print('\n==================================================')
	print('LEVEL 2')
	print('energy [',energy,']')
	print('HP [',HP,']')
	level_2_board()
	print()
	# display_smell()
	while(level_complete == False and energy > 0 and HP > 0):
		level_2_game()
		
	if(energy == 0):
		print('Game over! You fail to escape from the dark forest, you run out of energy...')
	elif(HP == 0):
		print('Game over! You fail to escape from the dark forest, you are killed...')
	else:
		# if level 1 is complete
		print('Congradulation on complete level 2!')
		print('Entering level 3...')
		time.sleep(5)
		current_level = 3


if(current_level == 3):
	# reset the game init
	level_complete = False
	energy = 10
	HP = 5
	player_pos = [1,1]
	
	print('\n==================================================')
	print('LEVEL 3')
	print('energy [',energy,']')
	print('HP [',HP,']')
	level_3_board()
	print()
	# display_smell()
	while(level_complete == False and energy > 0 and HP > 0):
		level_3_game()
		
	if(energy == 0):
		print('Game over! You fail to escape from the dark forest, you run out of energy...')
	elif(HP == 0):
		print('Game over! You fail to escape from the dark forest, you are killed...')
	else:
		# if level 1 is complete
		print('Congradulation on complete level 3!')
		print('You have escape from the dark forest!')
		time.sleep(2)
		
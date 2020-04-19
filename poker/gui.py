from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import pygame
from itertools import repeat
import random
import time


# 初始化
global AI1_card
global AI2_card
global AI3_card
global player_card
AI1_card = []
AI2_card = []
AI3_card = []
player_card = []

global other_pass
other_pass = []

suits_symbols = ['♠', '♦', '♥', '♣']

global first_round
first_round = True

# 卡堆，四种不同花色，红桃黑桃方片梅花
cards = {'Hearts_3':3,'Spades_3':3,'Diamonds_3':3,'Clubs_3':3,
		'Hearts_4':4,'Spades_4':4,'Diamonds_4':4,'Clubs_4':4,
		'Hearts_5':5,'Spades_5':5,'Diamonds_5':5,'Clubs_5':5,
		'Hearts_6':6,'Spades_6':6,'Diamonds_6':6,'Clubs_6':6,
		'Hearts_7':7,'Spades_7':7,'Diamonds_7':7,'Clubs_7':7,
		'Hearts_8':8,'Spades_8':8,'Diamonds_8':8,'Clubs_8':8,
		'Hearts_9':9,'Spades_9':9,'Diamonds_9':9,'Clubs_9':9,
		'Hearts_10':10,'Spades_10':10,'Diamonds_10':10,'Clubs_10':10,
		'Hearts_J':11,'Spades_J':11,'Diamonds_J':11,'Clubs_J':11,
		'Hearts_Q':12,'Spades_Q':12,'Diamonds_Q':12,'Clubs_Q':12,
		'Hearts_K':13,'Spades_K':13,'Diamonds_K':13,'Clubs_K':13,
		'Hearts_A':14,'Spades_A':14,'Diamonds_A':14,'Clubs_A':14,
		'Hearts_2':15,'Spades_2':15,'Diamonds_2':15,'Clubs_2':15}

# mapping card to picture
mapping_card = {'Hearts_3':'红桃3.png','Spades_3':'黑桃3.png','Diamonds_3':'方块3.png',					'Clubs_3':'草花3.png',
				'Hearts_4':'红桃4.png','Spades_4':'黑桃4.png','Diamonds_4':'方块4.png','Clubs_4':'草花4.png',
				'Hearts_5':'红桃5.png','Spades_5':'黑桃5.png','Diamonds_5':'方块5.png','Clubs_5':'草花5.png',
				'Hearts_6':'红桃6.png','Spades_6':'黑桃6.png','Diamonds_6':'方块6.png','Clubs_6':'草花6.png',
				'Hearts_7':'红桃7.png','Spades_7':'黑桃7.png','Diamonds_7':'方块7.png','Clubs_7':'草花7.png',
				'Hearts_8':'红桃8.png','Spades_8':'黑桃8.png','Diamonds_8':'方块8.png','Clubs_8':'草花8.png',
				'Hearts_9':'红桃9.png','Spades_9':'黑桃9.png','Diamonds_9':'方块9.png','Clubs_9':'草花9.png',
				'Hearts_10':'红桃10.png','Spades_10':'黑桃10.png','Diamonds_10':'方块10.png','Clubs_10':'草花10.png',
				'Hearts_J':'红桃J.png','Spades_J':'黑桃J.png','Diamonds_J':'方块J.png','Clubs_J':'草花J.png',
				'Hearts_Q':'红桃Q.png','Spades_Q':'黑桃Q.png','Diamonds_Q':'方块Q.png','Clubs_Q':'草花Q.png',
				'Hearts_K':'红桃K.png','Spades_K':'黑桃K.png','Diamonds_K':'方块K.png','Clubs_K':'草花K.png',
				'Hearts_A':'红桃A.png','Spades_A':'黑桃A.png','Diamonds_A':'方块A.png','Clubs_A':'草花A.png',
				'Hearts_2':'红桃2.png','Spades_2':'黑桃2.png','Diamonds_2':'方块2.png','Clubs_2':'草花2.png'}

def waithere_long():
	var = IntVar()
	root.after(4000, var.set, 1)
	print("waiting...")
	root.wait_variable(var)

def waithere_short():
	var = IntVar()
	root.after(2000, var.set, 1)
	print("waiting...")
	root.wait_variable(var)

# convert dict to list of tuples
all_cards_list = random.sample(cards.items(),52)

# 玩家列表,用其所持有的手牌组来代表
order = ['AI 1','AI 2','AI 3','You']


def sort_cards(card_list):
	# keyorder提取卡堆里的卡片名来排序
	keyorder = list(cards.keys())
	sorted_card_list = sorted(card_list,key = lambda x: (keyorder.index(x[0]),x[1]),reverse = True)
	return sorted_card_list

# 游戏开始，发牌
def give_card(card_list,already_given):	# already_given是上一回合发的牌
	# 从卡堆里随意抽选13张牌
	
	# 如果不是第一回合，就需要考虑上一回合发过的牌
	if(already_given != ''):	
		# remove those already given to other players
		for given_card in already_given:
			remove = all_cards_list.remove(given_card)
		# 从剩余的牌堆里任意抽取13张给一个玩家
	card_list = card_list + random.sample(all_cards_list,13)
	return card_list
	
def remove_card(current_cards,card_list):
	removed_list = []
	if(card_list == player_card):
		# 如果是玩家出牌然后需要移除，那么这里的current_cards就是list of 牌型
		for card in card_list:
			# 找出手牌里所有出过的牌
			if(card[0] in current_cards):
				removed_list.append(card)
				current_cards.remove(card[0])
				# print('to be removed',card)
		# first read all cards need to be removed into removed_list,then removed at once
		
		new_card_list = [x for x in card_list if x not in removed_list]
		
		# print('Your remaining card:',new_card_list)
		# print('Your remaining cards length:',len(new_card_list))

	else:
		if(type(current_cards)==list):
			for card in card_list:
				# print('card list',card_list)
				# 这里的current_cards就是list of values
				# 找出手牌里所有出过的牌
				# print('to be removed:',current_cards)
				# print('whole card',card)
				if(card[1] in current_cards):
					# print('go in')
					removed_list.append(card)
					# print('stored removed list',removed_list)
					# card_list.remove(card)
					current_cards.remove(card[1])
		else:
			for card in card_list:
				if(card[1] == current_cards):
					removed_list.append(card)
					card_list.remove(card)
					break
		
		new_card_list = [x for x in card_list if x not in removed_list]

		# print('AI remaining cards length:',len(new_card_list))
	
	i = 0
	while(i < len(card_list)):
		# print('ever enter before')
		# print('card_list[i])',card_list[i])
		# print('remove list is ',removed_list)
		if(card_list[i] in removed_list):
			card_list.remove(card_list[i])
			i = i - 1
		i = i + 1
	# print('card_list here here here',card_list)
	return new_card_list

#===================================tkinter page==================================
game_pygame = False
pygame_start = False
# when user press EXIT at the introduction page, the pygame window will not be executed
game = True
# this start_player will be set in tkinter page and used by pygame portion
start_player = ''

# introduction page
root = Tk()
root.title("Poker - Run Faster!")
# width and height for the main introduction page
w = 840
h = 480
# in order to use the background image, use canvas in the root page
canvas = Canvas(root, width=w, height=h)
canvas.pack(side = LEFT)
background_img = Image.open('bg.jpg')
bg = background_img.resize((840,480),Image.ANTIALIAS)
bg_img = ImageTk.PhotoImage(bg)

canvas.create_image(0,0,image=bg_img,anchor="nw")
root.resizable(False,False)

# color chart
light_blue = '#00ffff'
light_red = '#ff3333'
light_green = '#33ff33'

# 默认的头像是player3,犬夜叉
profile_pic = 'player3.png'

canvas.create_text(w/2,h/2-50,fill="black",font=("Forte",55),text='Poker - Run Faster!')

def destroy_page(page):
	page.destroy()

def display_profile(character,profile_page):
	confirm_profile_page = Toplevel(root)
	confirm_profile_page.title('Confirm your profile')
	w = 650
	h = 450
	
	canvas = Canvas(confirm_profile_page, width=w, height=h)
	canvas.pack(side = LEFT)
	
	background_img = Image.open('bg.jpg')
	bg = background_img.resize((700,500),Image.ANTIALIAS)
	bg_image = ImageTk.PhotoImage(bg)
	canvas.create_image(0,0,image=bg_image,anchor="nw")
	
	canvas.create_text(320,100,fill="black",font=("Forte",25),text='Confirm to choose character profile?')
	
	# 在人物旁边显示台词
	conversation_img = Image.open('dialog.png')
	conversation = conversation_img.resize((470,200),Image.ANTIALIAS)
	conversation_image = ImageTk.PhotoImage(conversation)
	canvas.create_image(150,200,image=conversation_image,anchor="nw")
	
	
	if(character == 'player1'):
		profile_img = Image.open('choose_player1.png')
		profile = profile_img.resize((200,350),Image.ANTIALIAS)
		profile_image = ImageTk.PhotoImage(profile)
		canvas.create_image(10,180,image=profile_image,anchor="nw")
		
		canvas.create_text(390,300,fill="black",font=("Forte",15),text='There are words keeping say be I endure the way!')
		
	elif(character == 'player2'):
		profile_img = Image.open('choose_player2.png')
		profile = profile_img.resize((200,350),Image.ANTIALIAS)
		profile_image = ImageTk.PhotoImage(profile)
		canvas.create_image(10,180,image=profile_image,anchor="nw")
		
		canvas.create_text(400,300,fill="black",font=("Forte",15),text='I\'m the man who\'ll become the pirate king!')
		
	else:
		profile_img = Image.open('choose_player3.png')
		profile = profile_img.resize((300,360),Image.ANTIALIAS)
		profile_image = ImageTk.PhotoImage(profile)
		canvas.create_image(-15,180,image=profile_image,anchor="nw")
	
		canvas.create_text(400,300,fill="black",font=("Forte",15),text='I am wind, wind of freedom.')
	
	def start_game():
		global profile_pic
		
		if(character == 'player1'):
			profile_pic = 'player1.png'
		elif(character == 'player2'):
			profile_pic = 'player2.png'
		else:
			profile_pic = 'player3.png'
		destroy_page(profile_page)
		destroy_page(confirm_profile_page)
		gameloop()
	
	def back():
		destroy_page(confirm_profile_page)
	
	# 两个button,开始游戏或者重新选择形象
	start = Button(canvas, font=("Forte",15),text = "confirm", command = start_game, anchor = W)
	start.configure(width = 10, bg="#33B5E5",activebackground = light_blue, relief = FLAT)
	start_window = canvas.create_window(250, 400, anchor=NW, window=start)
	
	back = Button(canvas, font=("Forte",15),text = "back", command = back, anchor = W)
	back.configure(width = 10, bg="#33B5E5",activebackground = light_blue, relief = FLAT)
	back_window = canvas.create_window(400, 400, anchor=NW, window=back)
	
	confirm_profile_page.mainloop()

def choose_profile():
	profile_page = Toplevel(root)
	profile_page.title('Choose your own profile')
	w = 650
	h = 450
	
	canvas = Canvas(profile_page, width=w, height=h)
	canvas.pack(side = LEFT)
	background_img = Image.open('bg.jpg')
	bg = background_img.resize((680,520),Image.ANTIALIAS)
	bg_image = ImageTk.PhotoImage(bg)
	canvas.create_image(0,0,image=bg_image,anchor="nw")
	
	# display three profile to be choose
	player_img_1 = Image.open('player1.png')
	player_image_1 = player_img_1.resize((150,150),Image.ANTIALIAS)
	player1 = ImageTk.PhotoImage(player_image_1)
	canvas.create_image(40,150,image=player1,anchor="nw")
	
	player_img_2 = Image.open('player2.png')
	player_image_2 = player_img_2.resize((150,150),Image.ANTIALIAS)
	player2 = ImageTk.PhotoImage(player_image_2)
	canvas.create_image(240,150,image=player2,anchor="nw")
	
	player_img_3 = Image.open('player3.png')
	player_image_3 = player_img_3.resize((150,150),Image.ANTIALIAS)
	player3 = ImageTk.PhotoImage(player_image_3)
	canvas.create_image(450,150,image=player3,anchor="nw")
	
	# three label for different profile
	def choose_profile_1(event=None):
		display_profile('player1',profile_page)
		
	def choose_profile_2(event=None):
		display_profile('player2',profile_page)
		
	def choose_profile_3(event=None):
		display_profile('player3',profile_page)

	canvas.create_text(w/2,100,fill="black",font=("Forte",20),text='There are 3 profile that you can choose:')

	button1 = Button(canvas, text = "Uzumaki Naruto", command = choose_profile_1, anchor = W)
	button1.configure(width = 15, activebackground = "#33B5E5", relief = FLAT)
	button1_window = canvas.create_window(60, 320, anchor=NW, window=button1)
	
	button2 = Button(canvas, text = "Monkey·D·Luffy", command = choose_profile_2, anchor = W)
	button2.configure(width = 15, activebackground = "#33B5E5", relief = FLAT)
	button2_window = canvas.create_window(260, 320, anchor=NW, window=button2)
	
	button3 = Button(canvas, text = "Inuyasha", command = choose_profile_3, anchor = W)
	button3.configure(width = 15, activebackground = "#33B5E5", relief = FLAT)
	button3_window = canvas.create_window(460, 320, anchor=NW, window=button3)
	
	profile_page.mainloop()

# before start of actual gameloop, direct to a rule intro page
def before_start():
	intro_page = Toplevel(root)
	intro_page.title("Game Introduction")
	w = 750
	h = 450
	
	def on_configure(event):
		# update scrollregion after starting 'mainloop'
		# when all widgets are in canvas
		canvas.configure(scrollregion=canvas.bbox('all'))
	
	# background image
	canvas = Canvas(intro_page, width=w, height=h)
	canvas.pack(side = LEFT)
	background_img = Image.open('bg.jpg')
	bg = background_img.resize((840,980),Image.ANTIALIAS)
	intro_image = ImageTk.PhotoImage(bg)
	canvas.create_image(0,0,image=intro_image,anchor="nw")
	scrollbar = Scrollbar(intro_page, command=canvas.yview)
	scrollbar.pack(side=LEFT, fill='y')
	canvas.configure(yscrollcommand = scrollbar.set)
	# update scrollregion after starting 'mainloop'
	# when all widgets are in canvas
	canvas.bind('<Configure>', on_configure)
	intro_page.resizable(False,False)
	
	# greeting
	greet = 'Hi welcome to Poker - Run Faster!'
	canvas.create_text(w/2,h/2-150,fill="black",font=("Forte",25),text=greet)
	
	# rule introduction
	intro_file = open('intro.txt','r+')
	intro_text = intro_file.read()
	intro_file.close()
	canvas.create_text(w/2,h/2+180,fill="black",font=("helvetica",12),text=intro_text)
	canvas.create_text(w/2-200,h/2+550,fill="black",font=("helvetica",12),text='If you are ready, let\'s go!')
	
	def proceed():
		# display character choosing
		destroy_page(intro_page)
		choose_profile()
	
	# GO button proceed to the gameloop
	GO_bt = Button(intro_page, text = "GO!",font='forte',command = proceed,anchor = 'nw',width = 12,bg=light_green,activebackground = light_green)
	GO_window = canvas.create_window(210, 850, anchor='nw', window=GO_bt)
	
	# switch account button
	switch_bt = Button(intro_page, text = "BACK",font='forte',command = lambda:destroy_page(intro_page),anchor = 'nw',width = 12,bg=light_blue,activebackground =light_blue)
	switch_window = canvas.create_window(400, 850, anchor='nw', window=switch_bt)
	
	intro_page.grab_set()
	# in order for displaying the background image
	intro_page.mainloop()
	
def exit():
	global game
	game = False
	destroy_page(root)

# choice button
start_bt = Button(root, text = "GO!",font=('forte',20),command = before_start,width = 10,bg=light_blue,activebackground = light_blue)
start_window = canvas.create_window(250, 380, anchor='nw', window=start_bt)

exit_bt = Button(root, text = "EXIT",font=('forte',20),command = exit,width = 10,bg=light_red,activebackground = light_red)
exit_window = canvas.create_window(450, 380, anchor='nw', window=exit_bt)








def game_init():
	# 发牌的时候要从卡堆里移除发过的牌
	# 第一次发牌不需要考虑已经给过的牌
	global AI1_card
	AI1_card = give_card(AI1_card,'')
	
	global AI2_card
	# 第二次发牌要除掉第一次发给AI1的牌
	AI2_card = give_card(AI2_card,AI1_card)
	
	global AI3_card
	# 第三次发牌要除掉第二次发给AI2的牌
	AI3_card = give_card(AI3_card,AI2_card)

	global player_card
	# 第四次发牌要除掉第三次发给AI3的牌
	player_card = give_card(player_card,AI3_card)
	
	# 给手牌排序
	AI1_card = sort_cards(AI1_card)
	AI2_card = sort_cards(AI2_card)
	AI3_card = sort_cards(AI3_card)
	player_card = sort_cards(player_card)


# AI出的牌返回的是[1,2,3,4]数字
def int_to_name(decide_card,card_list):
	name_list = []
	try:
		# print('its a list')
		# print('for compare, its card list is ',card_list)
		decide_card_temp = decide_card.copy()
		for card in card_list:
			# print('card[1]',card[1])
			# print('decide_card_temp',decide_card_temp)
			if(card[1] in decide_card_temp):
				name_list.append(card[0])
				decide_card_temp.remove(card[1])
	except AttributeError:	# 如果返回的只有一张牌了,not a list anymore
		# print('its a string')
		
		for card in card_list:
			# print('card[1]',card[1])
			# print('decide card',decide_card)
			if(card[1] == decide_card):
				name_list.append(card[0])
	return name_list


def name_to_int(last_used_card):
	# print('last used card',last_used_card)
	int_list = []
	decide_card_temp = last_used_card.copy()
	for card in decide_card_temp:
		value = card.split('_')
		try:
			if(value[1] == '2'):
				int_list.append(15)
			else:
				int_list.append(int(value[1]))
		except ValueError:
			if(value[1] == 'J'):
				int_list.append(11)
			elif(value[1] == 'Q'):
				int_list.append(12)
			elif(value[1] == 'K'):
				int_list.append(13)
			elif(value[1] == 'A'):
				int_list.append(14)
			
	return int_list









def check_respond(current_cards_value):
	# int_list = name_to_int(previous_card)
	int_list = current_cards
	ok_2 = False
	# 1. 如果上一回合出的是单张
	if(len(int_list) == 1):
		# print('last time is one card')
		if(len(current_cards_value) == 1):
			if(current_cards_value[0] > int_list[0]):
				ok_2 = True
	elif(len(int_list) == 2):	# 对子
		# print('last time is two card')
		if(len(current_cards_value) == 2):
			if(current_cards_value[0] == current_cards_value[1] and current_cards_value[0] > int_list[0]):
				ok_2 = True
	else:	# 上一回合出的牌大于两张
		if(len(int_list) == 0):
			print('error, zero length')
		if(int_list[0] == int_list[1] and int_list[1] == int_list[2]):
			# print('last time is three continue')
			# 三连
			if(len(int_list) == len(current_cards_value)):
				current_cards_value_set = set(current_cards_value)
				current_cards_value_list = list(current_cards_value_set)
				continue_three_index_1 = 0
				continue_three_index_2 = 1
				three_len = 1
				while(continue_three_index_2 < len(current_cards_value_list)):
					if(current_cards_value_list[continue_three_index_1] - current_cards_value_list[continue_three_index_2] == 1):
						three_len = three_len + 1
						continue_three_index_1 = continue_three_index_1 + 1
						continue_three_index_2 = continue_three_index_2 + 1
				if(three_len*3 == len(int_list)):
					ok_2 = True
		# 连对
		elif(int_list[0] == int_list[1] and int_list[1] != int_list[2]):
			# print('last time is continue couple')
			if(len(int_list) == len(current_cards_value)):
				current_cards_value_set = set(current_cards_value)
				current_cards_value_list = list(current_cards_value_set)
				continue_couple_index_1 = 0
				continue_couple_index_2 = 1
				couple_len = 1
				while(continue_couple_index_2 < len(current_cards_value_list)):
					if(current_cards_value_list[continue_couple_index_1] - current_cards_value_list[continue_couple_index_2] == 1):
						couple_len = couple_len + 1
						continue_couple_index_1 = continue_couple_index_1 + 1
						continue_couple_index_2 = continue_couple_index_2 + 1
				if(couple_len*2 == len(int_list)):
					ok_2 = True
		# 顺子
		elif(int_list[0] != int_list[1]):
			# print('last time is sequence')
			if(len(int_list) == len(current_cards_value)):
				continue_sequence_index_1 = 0
				continue_sequence_index_2 = 1
				sequence_len = 1
				while(continue_sequence_index_2 < len(current_cards_value)):
					if(current_cards_value[continue_sequence_index_1] - current_cards_value[continue_sequence_index_2] == 1):
						sequence_len = sequence_len + 1
						continue_sequence_index_1 = continue_sequence_index_1 + 1
						continue_sequence_index_2 = continue_sequence_index_2 + 1
				if(sequence_len == len(int_list)):
					ok_2 = True

	if(ok_2 == False and 'You' not in other_pass):
		ok_2 = False
		messagebox.showinfo('Invalid cards','Invalid card pattern, please check your input and enter again.')
	
	return ok_2
	# if(ok_2 == True):
		# del other_pass[:]
		# respond_card_value_unsort = []
		# for card in wish_to_used_list_name:
			# card_split = card.split('_')
			# try:
				# if(card_split[1] == '2'):
					# respond_card_value_unsort.append(15)
				# else:
					# respond_card_value_unsort.append(int(card_split[1]))
			# except ValueError:
				# if(card_split[1] == 'J'):
					# respond_card_value_unsort.append(11)
				# elif(card_split[1] == 'Q'):
					# respond_card_value_unsort.append(12)
				# elif(card_split[1] == 'K'):
					# respond_card_value_unsort.append(13)
				# elif(card_split[1] == 'A'):
					# respond_card_value_unsort.append(14)
	

	# respond_card_value = sorted(respond_card_value_unsort,reverse = True)
	# # print('wish to respond card',respond_card_value)
	# new_card_list = remove_card(wish_to_used_list_name,card_list)


def check_free_play(current_cards_value):
	ok = True
	is_in = 0
	is_continue = 1	
	# get a list of all values of player card
	test_value_list = []
	test_name_list = []
	for card in player_card:
		test_value_list.append(card[1])
		test_name_list.append(card[0])
	# 单张不用检查
	if(len(current_cards_value) > 1):
		# 1. 如果出的是两张，只可能是对子，检查若不是对子，报错
		if(len(current_cards_value) == 2):
			# print('是对子')
			if(current_cards_value[0] != current_cards_value[1]):
				ok = False
				
		# 4. 如果出的是三张以上，就有可能是连对，顺子或者三连
		elif(len(current_cards_value) > 2):
			# 三连
			if(current_cards_value[0] == current_cards_value[1] and current_cards_value[1] == current_cards_value[2]):
				test_int_set = set(current_cards_value)
				# 如果出的都是正确的三连，那么list的长度应该是set的三倍
				if(len(current_cards_value) != 3*len(test_int_set)):
					ok = False
			# 连对
			elif(current_cards_value[0] == current_cards_value[1] and current_cards_value[1] != current_cards_value[2]):
				value_len = len(current_cards_value)
				if(value_len % 2 == 0):
					test_int_set = set(current_cards_value)
					test_int_list = list(test_int_set)
					# 如果出的都是正确的连对，那么list里面的值应该都是连续的
					i_test_1 = 0
					i_test_2 = 1
					while(i_test_2 < len(test_int_list)):
						if(test_int_list[i_test_1] - test_int_list[i_test_2] == 1):
							is_continue = is_continue + 1
						i_test_1 = i_test_1 + 1
						i_test_2 = i_test_2 + 1
					if(is_continue != (len(test_int_list) - 1)):
						ok = False
				else:
					ok = False
			# 顺子
			elif(current_cards_value[0] - current_cards_value[1] == 1):
				print('value 1 -',current_cards_value[0])
				print('value 2 -',current_cards_value[1])
				i_test_1 = 0
				i_test_2 = 1
				while(i_test_2 < len(current_cards_value)):
					if(current_cards_value[i_test_1] - current_cards_value[i_test_2] == 1):
						is_continue = is_continue + 1
					else:
						break
					i_test_1 = i_test_1 + 1
					i_test_2 = i_test_2 + 1
				print('actual continue len ',is_continue)
				print('theory continue len ',current_cards_value)
				if(is_continue != len(current_cards_value)):
					ok = False
			else:
				print('Error occured')
				ok = False

	return ok




def get_next_player(current_player):
	if(current_player == AI1_card):
		current_player_name = 'AI 1'
	elif(current_player == AI2_card):
		current_player_name = 'AI 2'
	elif(current_player == AI3_card):
		current_player_name = 'AI 3'
	elif(current_player == player_card):
		current_player_name = 'You'
	else:
		print('ERROR! NO VALID CURRENT PLAYER NAME')
	# print('new current player is:',current_player_name)	
	current_index = order.index(current_player_name)
	if((current_index + 1) >= len(order)):
		current_index = 0
		next_player_name = order[current_index]
	else:
		next_player_name = order[current_index+1]
	print('\n')
	print('next_player',next_player_name)
	# get next_player by next_player_name
	if(next_player_name == 'AI 1'):
		next_player = AI1_card
	elif(next_player_name == 'AI 2'):
		next_player = AI2_card
	elif(next_player_name == 'AI 3'):
		next_player = AI3_card
	else:
		next_player = player_card
	return next_player


def gameloop():
	# create a new page
	game_page = Toplevel(root)
	game_page.title("Run Faster")
	w = 900
	h = 550
	
	# 发牌
	game_init()
	
	# 打牌背景图
	canvas = Canvas(game_page, width=w, height=h)
	canvas.pack(side = LEFT)
	background_img = Image.open('game_bg.jpg')
	bg = background_img.resize((920,580),Image.ANTIALIAS)
	bg_image = ImageTk.PhotoImage(bg)
	canvas.create_image(0,0,image=bg_image,anchor="nw")
	
	# display AI 1 name and AI 1 profile
	AI_1_img = Image.open('AI1.png')
	AI_1 = AI_1_img.resize((100,100),Image.ANTIALIAS)
	AI_1_image = ImageTk.PhotoImage(AI_1)
	canvas.create_image(w/2-50,10,image=AI_1_image,anchor="nw")
	
	canvas.create_text(w/2,130,fill="white",font=("forte",15),text='AI 1')
	
	# display AI 2 name and AI 1 profile
	AI_2_img = Image.open('AI2.png')
	AI_2 = AI_2_img.resize((100,100),Image.ANTIALIAS)
	AI_2_image = ImageTk.PhotoImage(AI_2)
	canvas.create_image(0,h/2-50,image=AI_2_image,anchor="nw")
	
	canvas.create_text(50,h/2+80,fill="white",font=("forte",15),text='AI 2')
	
	# display AI 1 name and AI 1 profile
	AI_3_img = Image.open('AI3.png')
	AI_3 = AI_3_img.resize((100,100),Image.ANTIALIAS)
	AI_3_image = ImageTk.PhotoImage(AI_3)
	canvas.create_image(w-100,h/2-50,image=AI_3_image,anchor="nw")
	
	canvas.create_text(w-50,h/2+80,fill="white",font=("forte",15),text='AI 3')
	
	# display player name and profile
	player_img = Image.open(profile_pic)
	player_profile = player_img.resize((100,100),Image.ANTIALIAS)
	player_image = ImageTk.PhotoImage(player_profile)
	player_picture = canvas.create_image(w/2-50,h-100,image=player_image,anchor="nw")
	
	canvas.create_text(w/2-80,h-50,fill="white",font=("forte",15),text='You')
	
	# 用一张背面牌来显示电脑的手牌，图片是不变的，之后变的是手牌数量
	card_back_img = Image.open('黑牌背面.png')
	card_back = card_back_img.resize((40,50),Image.ANTIALIAS)
	card_back_image = ImageTk.PhotoImage(card_back)

	card_back_picture_1 = canvas.create_image(w/2+90,35,image=card_back_image,anchor="nw")
	
	card_back_picture_2 = canvas.create_image(100,h/2,image=card_back_image,anchor="nw")
	
	card_back_picture_3 = canvas.create_image(w-140,h/2,image=card_back_image,anchor="nw")
	
	# 红桃三玩家先出牌
	def who_first():
		global first_player_display_text
		if(('Hearts_3',3) in AI1_card):
			current_player = AI1_card
		elif(('Hearts_3',3) in AI2_card):
			current_player = AI2_card
		elif(('Hearts_3',3) in AI3_card):
			current_player = AI3_card
		elif(('Hearts_3',3) in player_card):
			current_player = player_card
		else:
			print('error, ♥_3 not in any player')
		# 出牌
		# 记下这次出的牌,和该玩家剩下的手牌
		if(current_player == AI1_card):
			current_player_name = 'AI 1'

		elif(current_player == AI2_card):
			current_player_name = 'AI 2'

		elif(current_player == AI3_card):
			current_player_name = 'AI 3'

		elif(current_player == player_card):
			current_player_name = 'You'
			
		else:
			current_player_name = ''
		
		if(current_player == 'You'):
			first_player_script = 'You are holding ♥_3\nIt\'s your turn to play.'
			first_player_display_text = canvas.create_text(w/2,h/2,fill="white",font=("forte",15),text=first_player_script)
			# 如果是玩家第一个出牌，就等着玩家按下respond按钮到下一步
		else:
			first_player_script = 'Holding ♥_3 first player is ' + current_player_name + '.'
			first_player_display_text = canvas.create_text(w/2,h/2,fill="white",font=("forte",15),text=first_player_script)
			
		return current_player
		
	def AI_play(card_list):
		# 如果是AI自由出牌，那么AI会优先选择最长的牌型来出
		# print(card_list)
		
		# 检查顺子长度， 2和A在顺子里的值分别是1 和 2
		sequence_len = 1
		max_sequence_len = 1
		
		# all_sequence这个列表是为了存下所有顺子，包括三个以及以上
		all_sequence = []
		
		temp_sequence = []
		
		value_list = []	# 只存卡牌的值
		# 检查完整个List
		for card_sequence in card_list:
			value_list.append(card_sequence[1])
		# print('his cards:',value_list)
		i = 0
		while(i < len(card_list)-2):
			sequence_len = 1
			for j in range(1,len(card_list)):
				first_sequence_card = value_list[i]
				second_sequence_card = value_list[j]
				if(first_sequence_card - second_sequence_card == 1):
					i = j
					sequence_len = sequence_len + 1
					if(sequence_len > max_sequence_len):
						max_sequence_len = sequence_len
					# 先把两个连续的放进暂时列表
					temp_sequence.append(first_sequence_card)
					temp_sequence.append(second_sequence_card)					
			i = i + 1
		# 最后得到的temp_sequence要移除重复的卡牌
		all_sequence_reverse = list(set(temp_sequence))
		all_sequence = sorted(all_sequence_reverse,reverse = True)
		# print('all_sequence',all_sequence)
		
		# print('max sequence len:',max_sequence_len)
		

		
		# 检查连对长度
		# 在连对里，A和2的值分别为1和2
		
		# all_continue_couple这个列表是为了存下所有连对，包括一个对子
		all_continue_couple = []
		
		temp_continue_couple = []
		
		# value_list 用跟前面一样的就好
		
		m = 0
		n = 1
		# print('for continue_couple',value_list)
		while(m < len(card_list)-1):
			while(n < len(card_list)):
				first_couple_card = value_list[m]
				second_couple_card = value_list[n]
				if(first_couple_card == second_couple_card):
					m = m + 2
					n = n + 2
					# 先把两个连续的放进暂时列表
					temp_continue_couple.append(first_couple_card)
					temp_continue_couple.append(second_couple_card)
				else:
					m = n
					n = n + 1

		# 最后得到的temp_continue_couple要移除重复的卡牌
		# print('temp_continue_couple',temp_continue_couple)
		all_continue_couple = list(set(temp_continue_couple))
		# print('all_continue_couple',all_continue_couple)
		sorted_all_continue_couple = sorted(all_continue_couple,reverse = True)
		# print('sorted all_continue_couple',sorted_all_continue_couple)
		index_couple_1 = 0
		index_couple_2 = 1
		if(len(sorted_all_continue_couple) == 0):
			continue_couple_len = 0
			max_continue_couple_len = 0
		elif(len(sorted_all_continue_couple) == 1):
			continue_couple_len = 2
			max_continue_couple_len = 2
		else:
			continue_couple_len = 2
			max_continue_couple_len = 2
			while(index_couple_2 < len(sorted_all_continue_couple)):
				if(sorted_all_continue_couple[index_couple_1] - sorted_all_continue_couple[index_couple_2] == 1):
					continue_couple_len = continue_couple_len + 2
					if(continue_couple_len > max_continue_couple_len):
						max_continue_couple_len = continue_couple_len
				else:
					continue_couple_len = 2
					
				index_couple_1 = index_couple_1 + 1
				index_couple_2 = index_couple_2 + 1
		
		
		# # 检查三连
		
		# all_continue_couple这个列表是为了存下所有连对，包括一个对子
		all_continue_three = []
		
		temp_continue_three = []
		
		# value_list 用跟前面一样的就好
		
		x = 0
		y = 1
		z = 2
		# print('for continue_three',value_list)
		while(x < len(card_list)-2):
			while(y < len(card_list)-1):
				while(z < len(card_list)):
					first_three_card = value_list[x]
					second_three_card = value_list[y]
					third_three_card = value_list[z]
					if(first_three_card == second_three_card == third_three_card):
						x = x + 3
						y = y + 3
						z = z + 3
						# 先把三个相同的的放进暂时列表
						temp_continue_three.append(first_three_card)
						temp_continue_three.append(second_three_card)
						temp_continue_three.append(third_three_card)
					else:
						x = x + 1
						y = y + 1
						z = z + 1

		# 最后得到的temp_sequence要移除重复的卡牌
		# print('temp_continue_three',temp_continue_three)
		all_continue_three = list(set(temp_continue_three))
		# print('all_continue_three',all_continue_three)
		sorted_all_continue_three = sorted(all_continue_three)
		
		# 在all_continue_three里
		three_index_1 = 0
		three_index_2 = 1
		if(len(sorted_all_continue_three) == 0):	# 如果没有三连
			continue_three_len = 0
			max_continue_three_len = 0
		elif(len(sorted_all_continue_three) == 1):	# 如果只有一个三连
			continue_three_len = 3
			max_continue_three_len = 3
		else:	# 如果有两个以上，就需要考虑它们是连续的还是分开的
			continue_three_len = 3
			max_continue_three_len = 3
			while(three_index_2 < len(sorted_all_continue_three)):
				# 因为在all_continue_three里存的是所有三连的数值，所以只用看是否连续就行
				if(sorted_all_continue_three[three_index_1] - sorted_all_continue_three[three_index_2]==1):
					# 如果是连续的，长度加一，如果不连续，就不用加
					continue_three_len = continue_three_len + 3
					if(continue_three_len > max_continue_three_len):
						max_continue_three_len = continue_three_len
				else:
					# 如果不连续，清零，注意这里的清零是指清掉大于三个的
					continue_three_len = 3
					

				three_index_1 = three_index_1 + 1
				three_index_2 = three_index_2 + 1
			
				
		# 现在有了三个会比较长的牌型的长度
		max_len = max(max_continue_couple_len,max_continue_three_len,max_sequence_len)
		# print('max continue couple',max_continue_couple_len)
		# print('max continue three',max_continue_three_len)
		# print('max sequence',max_sequence_len)
		# print('final max len',max_len)
		
		sublist = []
		sublist_1 = []
		sublist_2 = []
		has_break = False
		
		if(max_len > 1):
			# 在三种牌型长度相同的情况下，默认把连对放第一位，三连放第二位，顺子放第三位
			if(max_len == max_continue_couple_len):
				if(max_len == 2):
					# 但是如果只有一个对子
					if(len(sorted_all_continue_couple) == 1):
						sublist = sorted_all_continue_couple
					else:
						sublist = min(sorted_all_continue_couple)
				else:
					# 找出那个最长的连对 (sorted_all_continue_couple)
					check_1 = 0
					check_2 = 1
					check_len = 2	# 至少一个对子
					while(check_2 < len(sorted_all_continue_couple)):
						if(sorted_all_continue_couple[check_1]-sorted_all_continue_couple[check_2]==1):
							check_len = check_len + 2
							check_1 = check_1 + 1
							check_2 = check_2 + 1
						else:	# 一旦碰到断点，检查左右是否符合最长长度
							has_break = True
							sublist_1 = sorted_all_continue_couple[:check_2]
							sublist_2 = sorted_all_continue_couple[check_2:]
							check_1 = 0
							check_2 = 1
							
							# print('sublist_1',sublist_1)
							# print('sublist_2',sublist_2)
							if(len(sublist_1)*2 == max_len):
								sublist = sublist_1
								break
							elif(len(sublist_2)*2 == max_len):
								sublist = sublist_2
								break
							# 只取右边部分，因为左边如果不符合，就永远不可能符合了
							# sorted_all_continue_couple.remove(sorted_all_continue_couple[check_1])
							sorted_all_continue_couple = sublist_2
							
					
					if(has_break == False):
						sublist = sorted_all_continue_couple
				
				if(type(sublist) == int):
					to_sublist = []
					to_sublist.append(sublist)
					# print('sublist',to_sublist)
					decide_card_unsort = [x for item in to_sublist for x in repeat(item, 2)]
				else:
					decide_card_unsort = sublist + sublist
					
				decide_card = sorted(decide_card_unsort)

				
			elif(max_len == max_continue_three_len):
				# 找出那个最长的三连 (sorted_all_three_couple)
				check_1 = 0
				check_2 = 1
				check_len = 3	# 至少一个三连
				if(max_len == 3):	# 如果只有一个三连
					temp_three = min(all_continue_three)
					to_sublist = []
					to_sublist.append(temp_three)
					# print('temp_three',to_sublist)
					decide_card = [x for item in to_sublist for x in repeat(item, 3)]
				else:
					while(check_2 < len(sorted_all_continue_three)):
						if(sorted_all_continue_three[check_1]-sorted_all_continue_three[check_2]==1):
							check_len = check_len + 3
							check_1 = check_1 + 1
							check_2 = check_2 + 1
						else:	# 一旦碰到断点，检查左右是否符合最长长度
							has_break = True
							# print('sorted_all_continue_three',sorted_all_continue_three)
							sublist_1 = sorted_all_continue_three[:check_2]
							sublist_2 = sorted_all_continue_three[check_2:]
							check_1 = 0
							check_2 = 1
							# print('sublist_1',sublist_1)
							# print('sublist_2',sublist_2)
							if(len(sublist_1)*3 == max_len):
								sublist = sublist_1
								break
							elif(len(sublist_2)*3 == max_len):
								sublist = sublist_2
								break
							else:
								sublist = min(sorted_all_continue_three)
							
							# sorted_all_continue_three.remove(sorted_all_continue_three[check_1])
							sorted_all_continue_three = sublist_2
								
						
					if(has_break == False):
						sublist = sorted_all_continue_three
					# 如果list里只有一个element
					if(type(sublist) == int):
						to_sublist = []
						to_sublist.append(sublist)
						# print('sublist',to_sublist)
						decide_card_unsort = [x for item in to_sublist for x in repeat(item, 3)]
					else:
						decide_card_unsort = sublist + sublist + sublist
						
					decide_card = sorted(decide_card_unsort)

			
			# 找出最长的那个顺子
			elif(max_len == max_sequence_len):
				if(max_len > 2):	# if max_len < 3 then it's not a valid sequence
					# sorted_all_three_couple
					check_1 = 0
					check_2 = 1
					check_len = 0	
					while(check_2 < len(all_sequence)):
						if(all_sequence[check_1]-all_sequence[check_2]==1):
							check_len = check_len + 2
							check_1 = check_1 + 1
							check_2 = check_2 + 1
						else:	# 一旦碰到断点，检查左右是否符合最长长度
							has_break = True
							# print('check all sequence',all_sequence)
							sublist_1 = all_sequence[:check_2]
							sublist_2 = all_sequence[check_2:]
							check_1 = 0
							check_2 = 1
							# print('sublist_1',sublist_1)
							# print('sublist_2',sublist_2)
							if(len(sublist_1) == max_len):
								sublist = sublist_1
							elif(len(sublist_2) == max_len):
								sublist = sublist_2
								
							# 不连续的直接从列表里移除
							all_sequence = sublist_2
									
								
					if(has_break == False):
						sublist = all_sequence
						
					decide_card = sublist	
				
				else:	# 如果顺子只有两个连着，不能出
					decide_card = []
				
			else:
				print('error happened!!!!!!!!!!!!!!!')
					
		else:
			# 因为长度为二的肯定是一个对子，那个在连对里也包含了，所以最后只用考虑单张
			decide_card = min(value_list)
		
		global AI_turn_text		
		try:
			canvas.delete(AI_turn_text)
		except:
			print('AI turn script not exist')
		# 显示哪个AI出的牌
		if(card_list == AI1_card):
			name = 'AI 1'
		elif(card_list == AI2_card):
			name = 'AI 2'
		else:
			name = 'AI 3'
		AI_turn_script = name + ' turn :'
		AI_turn_text = canvas.create_text(100,100,fill="white",font=("Forte",30),text=AI_turn_script)

		# AI 和 player分开return
		# 显示出的牌，然后调用remove_card方法，最后回到主方法
		
		# convert int list to card name list
		name_list = int_to_name(decide_card,card_list)
		decide_card_backup_2 = []
		
		# use name list to get the image list and display
		display_play_card(name_list)
		
		try:
			decide_card_backup_2 = decide_card.copy()
		except AttributeError:
			decide_card_backup_2.append(decide_card)
		new_card_list = remove_card(decide_card_backup_2,card_list)
		# print('new card list:',new_card_list)
		# print('decide card has been removed...',decide_card)
		return (new_card_list,decide_card)


	def respond(card_list,last_used_card):
		try:
			if(type(last_used_card[0]) == str):
				last_used_card = name_to_int(last_used_card)
		except TypeError:
			print('no need for conversion.')
		# print('pass过来的card list 是',card_list)
		# print('last used card 原来的current_cards是',last_used_card)
		respond_card = []
		respond_card_value = []
		int_list = []
		# 如果是玩家回合，那就让玩家决定出牌
		new_card_list = []
		wish_to_used_list = []
		try:
			int_list = last_used_card.copy()
		except AttributeError:
			int_list.append(last_used_card)

		# 如果是AI的回合
		
		# 重复利用上面play方法里，把所有牌型都存到相应的列表里
		# all_sequence这个列表是为了存下所有顺子，包括三个以及以上
		all_sequence = []
		temp_sequence = []
		value_list = []	# 只存卡牌的值
		# 检查完整个List
		for card_sequence in card_list:
			value_list.append(card_sequence[1])
		# print('his cards:',value_list)
		i = 0
		max_sequence_len = 1
		while(i < len(card_list)-2):
			sequence_len = 1
			for j in range(1,len(card_list)):
				first_sequence_card = value_list[i]
				second_sequence_card = value_list[j]
				if(first_sequence_card - second_sequence_card == 1):
					i = j
					sequence_len = sequence_len + 1
					if(sequence_len > max_sequence_len):
						max_sequence_len = sequence_len
					# 先把两个连续的放进暂时列表
					temp_sequence.append(first_sequence_card)
					temp_sequence.append(second_sequence_card)					
			i = i + 1
		# 最后得到的temp_sequence要移除重复的卡牌
		all_sequence_reverse = list(set(temp_sequence))
		all_sequence = sorted(all_sequence_reverse,reverse = True)
		# print('all_sequence',all_sequence)
		
		
		
		# all_continue_couple这个列表是为了存下所有连对，包括一个对子
		all_continue_couple = []
		temp_continue_couple = []
		# value_list 用跟前面一样的就好
		m = 0
		n = 1
		# print('for continue_couple',value_list)
		while(m < len(card_list)-1):
			while(n < len(card_list)):
				first_couple_card = value_list[m]
				second_couple_card = value_list[n]
				if(first_couple_card == second_couple_card):
					m = m + 2
					n = n + 2
					# 先把两个连续的放进暂时列表
					temp_continue_couple.append(first_couple_card)
					temp_continue_couple.append(second_couple_card)
				else:
					m = n
					n = n + 1
		# 最后得到的temp_continue_couple要移除重复的卡牌
		# print('temp_continue_couple',temp_continue_couple)
		all_continue_couple = list(set(temp_continue_couple))
		
		sorted_all_continue_couple = sorted(all_continue_couple,reverse = True)
		# print('sorted_all_continue_couple',sorted_all_continue_couple)
		
		
		
		# all_continue_couple这个列表是为了存下所有连对，包括一个对子
		all_continue_three = []
		temp_continue_three = []
		# value_list 用跟前面一样的就好
		x = 0
		y = 1
		z = 2
		# print('for continue_three',value_list)
		while(x < len(card_list)-2):
			while(y < len(card_list)-1):
				while(z < len(card_list)):
					first_three_card = value_list[x]
					second_three_card = value_list[y]
					third_three_card = value_list[z]
					if(first_three_card == second_three_card == third_three_card):
						x = x + 3
						y = y + 3
						z = z + 3
						# 先把三个相同的的放进暂时列表
						temp_continue_three.append(first_three_card)
						temp_continue_three.append(second_three_card)
						temp_continue_three.append(third_three_card)
					else:
						x = x + 1
						y = y + 1
						z = z + 1
		# 最后得到的temp_continue_three要移除重复的卡牌
		# print('temp_continue_three',temp_continue_three)
		all_continue_three = list(set(temp_continue_three))
	
		sorted_all_continue_three = sorted(all_continue_three,reverse = True)
		# print('sorted_all_continue_three',sorted_all_continue_three)
		
		
		
		
		
		last_used_card_list = []
		# if last_used_card have more than 1 element
		if(type(last_used_card) == list):
			if(type(last_used_card[0]) == str):
				# 如果上一个出牌的是玩家，那么为了比较大小需要把牌名换成数值
				int_list = name_to_int(last_used_card)
			need_len = len(last_used_card)
		else:	# if last_used_card have only one element
			last_used_card_list.append(last_used_card)
			if(type(last_used_card) == str):
				int_list = name_to_int(last_used_card_list)
			need_len = len(last_used_card_list)
		
		# print('need_len now!!!!!!!!!!!!!!!!!',need_len)
		if(need_len == 1):	# 单张，只比大小
			single_greater = []
			for card in card_list:
				# print('=======card[1]',card[1])
				# print(type(card[1]))
				# print('=======int_list',int_list)
				# print('=======int_list[0]',int_list[0])
				# print(type(int_list[0]))
				if(card[1] > int_list[0]):
					single_greater.append(card[1])
			if(len(single_greater)>1):
				respond_card_value.append(min(single_greater))
			else:
				respond_card_value = single_greater
			
			
		elif(need_len == 2):	# 对子
			respond_card_value_temp = []
			# respond_card_value = min(sorted_all_continue_couple)
			for card in sorted_all_continue_couple:
				if(card > int_list[0]):	# 一旦找到那个符合条件的对子，直接break
					respond_card_value_temp.append(card)
					break
			respond_card_value = [x for item in respond_card_value_temp for x in repeat(item, 2)]
		else:	# 大于2张牌，有可能是三连，有可能是顺子，也有可能是连对
			has_break = False
			# test是哪种牌型
			index_test1 = 0
			index_test2 = 1
			index_test3 = 2
			if(int_list[0]-int_list[1] == 1 and int_list[1]-int_list[2] == 1):
				# 顺子
				# print('[inside sequence]')
				# print('max sequence len',max_sequence_len)
				# print('need len',need_len)
				if(max_sequence_len > need_len):
					check_1 = 0
					check_2 = 1
					check_len = 1	
					while(check_2 < len(all_sequence)):
						if(all_sequence[check_1]-all_sequence[check_2]==1):
							check_len = check_len + 1
							check_1 = check_1 + 1
							check_2 = check_2 + 1
						else:	# 一旦碰到断点，检查左右是否符合所需长度
							has_break = True
							# print('check all sequence',all_sequence)
							sublist_1 = all_sequence[:check_2]
							sublist_2 = all_sequence[check_2:]
							check_1 = 0
							check_2 = 1
							# print('sublist_1',sublist_1)
							# print('sublist_2',sublist_2)
							if(len(sublist_1) >= need_len):
								# 要出的顺子第一张牌值必须大于last_used_card的第一张牌值
								if(sublist_1[0] > last_used_card[0]):
								# 你可能会有比所需牌型更长的顺子，只需要取同等长度
									respond_card_value = sublist_1[0:need_len]
									break
							elif(len(sublist_2) >= need_len):
								if(sublist_2[0] > last_used_card[0]):
									respond_card_value = sublist_2[0:need_len]
									break
								
							# 不符合的直接从列表里移除
							all_sequence = sublist_2
										
					if(has_break == False):
						if(all_sequence[0] > last_used_card[0]):
							if(len(all_sequence) > need_len):
								respond_card_value = all_sequence[0:need_len]
							else:
								respond_card_value = all_sequence
						
				# 符合要求，找到相对应的牌名并返回
				# print('respond_card_value',respond_card_value)
				
			elif(int_list[0] == int_list[1] and int_list[1] == int_list[2]):
				# 三连
				# 找出那个最长的三连 (sorted_all_three_couple)
				# print('[inside continue three]')
				check_1 = 0
				check_2 = 1
				check_len = 3	# 至少一个三连
				if(len(sorted_all_continue_three) == 0):	# 如果没有三连
					pass
				elif(len(sorted_all_continue_three) == 1):	# 如果只有一个三连
					if(need_len == 3):	# 如果上个玩家只出了一个三连
						if(last_used_card[0] < sorted_all_continue_three[0]):
							respond_card_value = [x for item in sorted_all_continue_three for x in repeat(item, 3)]

				else:	# 上个玩家出了多于一个三连
					while(check_2 < len(sorted_all_continue_three)):
						if(sorted_all_continue_three[check_1]-sorted_all_continue_three[check_2]==1):
							check_len = check_len + 3
							check_1 = check_1 + 1
							check_2 = check_2 + 1
						else:	# 一旦碰到断点，检查左右是否符合最长长度
							has_break = True
							# print('sorted_all_continue_three',sorted_all_continue_three)
							sublist_1 = sorted_all_continue_three[:check_2]
							sublist_2 = sorted_all_continue_three[check_2:]
							check_1 = 0
							check_2 = 1
							# print('sublist_1',sublist_1)
							# print('sublist_2',sublist_2)
							if(len(sublist_1)*3 == need_len and check_len >= need_len):
								if(sublist_1[0] > last_used_card[0]):
									# print('sublist_1 first value:',sublist_1[0])
									respond_card_value = sublist_1
									break
							elif(len(sublist_2)*3 == need_len and check_len >= need_len):
								if(sublist_2[0] > last_used_card[0]):
									# print('sublist_2 first value:',sublist_2[0])
									respond_card_value = sublist_2
									break

							# sorted_all_continue_three.remove(sorted_all_continue_three[check_1])
							sorted_all_continue_three = sublist_2
								
					# 如果所有三连都是连续的
					if(has_break == False):
						# 从前往后找, sorted_all_continue_three 是倒序的
						index_three = 0
						index_last = 0
						len_three = 3
						satisfied_three = []
						while(sorted_all_continue_three[index_three] > last_used_card[index_last] and index_three < (len(sorted_all_continue_three)-1)):
							index_three = index_three + 1
							index_last = index_last + 1
							len_three = len_three + 3
							satisfied_three.append(sorted_all_continue_three[index_three])
							if(len_three == need_len):
								respond_card_value = satisfied_three
								break

						
					# 如果list里只有一个element
					if(type(respond_card_value) == int):
						to_sublist = []
						to_sublist.append(respond_card_value)
						decide_card_unsort = [x for item in to_sublist for x in repeat(item, 3)]
					else:
						decide_card_unsort = respond_card_value + respond_card_value + respond_card_value
					respond_card_value = sorted(decide_card_unsort)
					# print('respond_card_value',respond_card_value)
				
			elif(int_list[0] == int_list[1] and int_list[1] != int_list[2]):
				# 连对
				# print('[inside continue couple]')
				if(len(sorted_all_continue_couple) == 0):
					pass
				elif(len(sorted_all_continue_couple) == 1):
					if(need_len == 1):
						if(sorted_all_continue_couple[0] > last_used_card[0]):
							respond_card_value = sorted_all_continue_couple
				else:
					# 找出那个符合的连对 (sorted_all_continue_couple)
					check_1 = 0
					check_2 = 1
					check_len = 2	# 至少一个对子
					while(check_2 < len(sorted_all_continue_couple)):
						if(sorted_all_continue_couple[check_1]-sorted_all_continue_couple[check_2]==1):
							check_len = check_len + 2
							check_1 = check_1 + 1
							check_2 = check_2 + 1
						else:	# 一旦碰到断点，检查左右是否符合最长长度
							has_break = True
							sublist_1 = sorted_all_continue_couple[:check_2]
							sublist_2 = sorted_all_continue_couple[check_2:]
							check_1 = 0
							check_2 = 1
							
							# print('sublist_1',sublist_1)
							# print('sublist_2',sublist_2)
							if(len(sublist_1)*2 == need_len and check_len >= need_len):
								if(sublist_1[0] > last_used_card[0]):
									respond_card_value = sublist_1
									break
							elif(len(sublist_2)*2 == need_len and check_len >= need_len):
								if(sublist_2[0] > last_used_card[0]):
									respond_card_value = sublist_2
									break
							# 只取右边部分，因为左边如果不符合，就永远不可能符合了
							sorted_all_continue_couple = sublist_2
								
						
					if(has_break == False):
						# 从前往后找, sorted_all_continue_couple 是倒序的
						index_couple = 0
						index_last = 0
						len_couple = 2
						satisfied_couple = []
						while(sorted_all_continue_couple[index_couple] > last_used_card[index_last] and index_couple < (len(sorted_all_continue_couple)-1)):
							index_couple = index_couple + 1
							index_last = index_last + 1
							len_couple = len_couple + 2
							satisfied_couple.append(sorted_all_continue_couple[index_couple])
							if(len_couple == need_len):
								respond_card_value = satisfied_couple
								break
					
					if(type(respond_card_value) == int):
						to_sublist = []
						to_sublist.append(respond_card_value)
						decide_card_unsort = [x for item in to_sublist for x in repeat(item, 2)]
					else:
						decide_card_unsort = respond_card_value + respond_card_value
						
					respond_card_value = sorted(decide_card_unsort)
					# print('respond_card_value',respond_card_value)
				
			else:
				print('error occured')
		# print('respond_card_value',respond_card_value)
		# print('len of respond_card_value',len(respond_card_value))
		if(card_list == AI1_card):
			this_player = 'AI 1'
		elif(card_list == AI2_card):
			this_player = 'AI 2'
		elif(card_list == AI3_card):
			this_player = 'AI 3'
		else:
			this_player = 'error'
		
		waithere_short()
		global AI_turn_text		
		try:
			canvas.delete(AI_turn_text)
		except:
			print('AI turn script not exist')
		# 显示哪个AI出的牌
		if(card_list == AI1_card):
			name = 'AI 1'
		elif(card_list == AI2_card):
			name = 'AI 2'
		else:
			name = 'AI 3'
		AI_turn_script = name + ' turn :'
		AI_turn_text = canvas.create_text(100,100,fill="white",font=("Forte",30),text=AI_turn_script)
		
		
		if(len(respond_card_value) == 0):
			global pass_text
			other_pass.append(this_player)
			try:
				canvas.delete(pass_text)
			except NameError:
				print('pass text not exist yet.')
			pass_words = this_player + 'pass'
			pass_text = canvas.create_text(w/2,h/2,fill="white",font=("forte",15),text=pass_words)
			new_card_list = card_list
		else:	# 如果出了牌，那么就需要从手牌中移除出过的牌
			# respond_card_value is the value of respond card, need to get the card name
			del other_pass[:]
			respond_card = int_to_name(respond_card_value,card_list)
			
			display_play_card(respond_card)
			
			print(this_player,':',respond_card)
			respond_card_value_backup = respond_card_value.copy()
			new_card_list = remove_card(respond_card_value_backup,card_list)
			# 每回合出牌结束要做三件事，1.移除出过的牌 2.显示出的牌 3.返回剩余手牌和出过的
			# 还有第四件，如果这回合有人要的起并出了牌，重置other_pass list
			
				
		
		if(len(respond_card_value) > 0):	# 如果本回合选择了出牌，那么返回本回合出的牌
			return (new_card_list,respond_card_value)
		else:	# 如果本回合选择pass,那么返回上回合用的牌
			return (new_card_list,last_used_card)



	def draw_play_card(card_image,gap):
		global play_card_image_display
		image_name = canvas.create_image(w/2-100+gap,h/2-100,image=card_image,anchor='nw')
		play_card_image_display.append(image_name)


	def display_play_card(name_list):
		clear_AI_cards_num()
		display_AI_cards_num()
		global play_card_image_display
		play_card_image_display = []
		global card_img_list
		card_img_list = []
		global card_pic_list
		card_pic_list = []
		global card_image_list
		card_image_list = []
		gap = 0
		try:
			waithere_short()
			canvas.delete(first_player_display_text)
		except NameError:
			print('display text is not exist')
		try:
			canvas.delete(pass_text)
		except NameError:
			print('pass message not exist.')
		try:
			# try to delete previous card images
			for previous_AI_card in play_card_image_display:
				canvas.delete(previous_AI_card)
		except NameError:
			print('no previous card images.')
		# try to delete player's card
		for card in name_list:
			card_img = Image.open(mapping_card[card])
			card_img_list.append(card_img)
			# print(mapping_card[card])
			card_pic = card_img.resize((60,80),Image.ANTIALIAS)
			card_pic_list.append(card_pic)
			card_image = ImageTk.PhotoImage(card_pic)
			card_image_list.append(card_image)
			# draw_player_card('card_image_'+str(i),card_image,gap)
			draw_play_card(card_image,gap)
			gap = gap + 30
	
	
	
	# 选中的牌会上升一些
	def select_card(event,selected_card):
		global final_decide_card_image
		# print('You click me!!!',selected_card)
		# canvas.delete(selected_card)
		coords = canvas.coords(selected_card)
		# print(coords)
		if(coords[1] == 365):
			# 这个coords有可能是取消选中的，所以要从选中牌组里移除
			if(selected_card in final_decide_card_image):
				final_decide_card_image.remove(selected_card)
			shift = -15
		elif(coords[1] == 380):
			# 如果被选中了的牌，加进选中牌组里
			final_decide_card_image.append(selected_card)
			# print('current list:',final_decide_card_image)
			shift = 15
		try:
			canvas.coords(selected_card,coords[0],coords[1]-shift)
		except UnboundLocalError:
			print('Cannot select this card.')
	
	def draw_player_card(player_card_image,gap):
		global player_card_image_list
		image_name = canvas.create_image(250+gap,h-170,image=player_card_image,anchor='nw')
		player_card_image_list.append(image_name)
	
	
	def clear_AI_cards_num():
		global AI1_card_num_text
		global AI2_card_num_text
		global AI3_card_num_text
		canvas.delete(AI1_card_num_text)
		canvas.delete(AI2_card_num_text)
		canvas.delete(AI3_card_num_text)
	
	def display_AI_cards_num():
		global AI1_card_num_text
		global AI2_card_num_text
		global AI3_card_num_text
		# display 各个玩家的手牌
		# display AI1 的手牌数量
		AI1_card_num = 'x' + str(len(AI1_card))
		AI1_card_num_text = canvas.create_text(w/2+70,60,fill="white",font=("forte",15),text=AI1_card_num)
		
		# display AI2 的手牌数量
		AI2_card_num = 'x' + str(len(AI2_card))
		AI2_card_num_text = canvas.create_text(120,h/2-10,fill="white",font=("forte",15),text=AI2_card_num)
		
		# display AI3 的手牌数量
		AI3_card_num = 'x' + str(len(AI3_card))
		AI3_card_num_text = canvas.create_text(w-120,h/2-10,fill="white",font=("forte",15),text=AI3_card_num)
	
	
	
	# 显示玩家手牌
	display_AI_cards_num()
	global player_card_image_list
	player_card_image_list = []
	gap = 0
	player_card_name = []
	for card in player_card:
		player_card_name.append(card[0])
	for card in player_card_name:
		player_card_img = Image.open(mapping_card[card])
		# card_img_list.append(card_img)
		print(mapping_card[card])
		player_card_pic = player_card_img.resize((60,80),Image.ANTIALIAS)
		# card_pic_list.append(card_pic)
		player_card_image = ImageTk.PhotoImage(player_card_pic)
		player_card_image_list.append(player_card_image)
		draw_player_card(player_card_image,gap)
		gap = gap + 30
	
	# 玩家的所有手牌图片
	global final_decide_card_image
	global new_player_card_image_list
	final_decide_card_image = []
	new_player_card_image_list = []
	# print('all player cards image list',player_card_image_list)
	for images in player_card_image_list:
		if(type(images) == int):
			new_player_card_image_list.append(images)
	# print('all player cards image list',new_player_card_image_list)
	# print('ITS LENGTH IS ',len(new_player_card_image_list))
	
	for card_image_in in player_card_image_list:
		# 每次画完所有的手牌，因为选中牌 手牌图片要上升一点，所以要bind to event
		canvas.tag_bind(card_image_in, '<ButtonPress-1>', lambda event, selected_card = card_image_in :select_card(event,selected_card))
	
	
	
		
	def play():
		global player_card
		print('每次出牌前，先显示所剩余手牌',player_card)
		try:
			canvas.delete(your_turn_display_text)
		except NameError:
			print('no your_turn_display_text yet.')
		global first_round
		
		global var2
		# 如果不是自由出牌的回合，需要记下之前的current_cards
		# global previous_card
		# if(len(other_pass) != 3 or first_round == False):
			# previous_card = current_cards.copy()
			
		# 玩家的回合，选择好了要出的牌，按了play之后
		# 这些选中的牌会被存到另一个list里，并从player_card中移除
		index = 0
		global index_list
		index_list = []
		global current_card_value_and_name
		current_card_value_and_name = []
		global current_cards_name
		global current_cards_value
		current_cards_name = []
		
		# based on the index in card_image_list
		# print('final_decide_card_image',final_decide_card_image)
		for card in new_player_card_image_list:
			if(card in final_decide_card_image):
				index_list.append(index)
			index = index + 1
		# print('index list is : ',index_list)
		# print('player cards : ',player_card)
		# having all selected_card index
		
		# print('new player card image list',new_player_card_image_list)
		# print('final decide card image',final_decide_card_image)
		# print('index list',index_list)
		# print('current player card',player_card)
		
		# 从player_card里用index找到所出的牌
		for index_in in index_list:
			current_card_value_and_name.append(player_card[index_in])
		# print('player final decide card: ',current_card_value_and_name)
		
		# current_cards 是
		for card in current_card_value_and_name:
			current_cards_name.append(card[0])
			# 这个current_cards就是玩家出的牌的牌名
		current_cards_value = name_to_int(current_cards_name)
		
		# 自由出牌
		if(len(other_pass) == 3 or first_round == True):
			# check
			ok_1 = check_free_play(current_cards_value)
			# ok_1 = True
			if(ok_1 == True):
				first_round = False
				del other_pass[:]
				# 打牌之前，先尝试删除之前出过的牌
				try:
					for play_card_image in play_card_image_display:
						canvas.delete(play_card_image)
				except NameError:
					print('screen already clear')
				# 如果检查自由出牌正确，把牌打出去，然后从玩家手牌里移除
				try:
					canvas.delete(your_turn_display_text)
				except NameError:
					print('your turn display text is not exist yet.')
				canvas.delete(first_player_display_text)
				play_gap = 0
				for image_display in final_decide_card_image:
					canvas.coords(image_display,w/2-100+play_gap,h/2-50)
					play_gap = play_gap + 30
				
				
				# 把打出去的牌从 new_player_card_image_list 里面移除
				
				for final_card_image in final_decide_card_image:
					try:
						new_player_card_image_list.remove(final_card_image)
					except ValueError:
						print('already delete')
				
				waithere_short()
				for final_card_image in final_decide_card_image:
					canvas.delete(final_card_image)
				
				del final_decide_card_image[:]
				
				# remove cards from player_card
				
				player_card = remove_card(current_cards_name,player_card)
				var2.set(1)
			else:
				# 用messagebox 来显示出牌无效
				messagebox.showinfo("Invalid cards", "Invalid card pattern, please check your input and enter again")
		else:
			# check 打上一回合的牌
			ok_2 = check_respond(current_cards_value)
			if(ok_2 == True):
				del other_pass[:]
				# 打牌之前，先尝试删除之前出过的牌
				for play_card_image in play_card_image_display:
					try:
						canvas.delete(play_card_image)
					except NameError:
						print('screen already clear')
				# 如果检查自由出牌正确，把牌打出去，然后从玩家手牌里移除
				canvas.delete(first_player_display_text)
				play_gap = 0
				for image_display in final_decide_card_image:
					canvas.coords(image_display,w/2-200+play_gap,h/2-120)
					play_gap = play_gap + 30
				
				# 把打出去的牌从 new_player_card_image_list 里面移除
				print('new_player_card_image_list',new_player_card_image_list)
				print('final_decide_card_image',final_decide_card_image)
				for final_card_image in final_decide_card_image:
					try:
						new_player_card_image_list.remove(final_card_image)
					except ValueError:
						print('already delete')
				
				
				waithere_short()
				for final_card_image in final_decide_card_image:
					canvas.delete(final_card_image)	
					
				del final_decide_card_image[:]
				
				
				
				# remove cards from player_card
				player_card = remove_card(current_cards_name,player_card)
				var2.set(1)
				
		
	def PASS():
		canvas.delete(your_turn_display_text)
		global var2
		global pass_text
		pass_text = canvas.create_text(w/2,h/2,fill="white",font=("forte",15),text='You : pass')
		other_pass.append('You')
		var2.set(1)
	
	current_player = who_first()
	
	# print('first current player is ',current_player)
	global var2
	var2 = IntVar()
	# 先把第一回合的牌打了
	global current_cards
	if(current_player == player_card):	
		
		# button
		play_bt = Button(canvas, font=("Forte",15),text = "play", command = play, anchor = W)
		play_bt.configure(width = 10, bg="#33B5E5",activebackground = light_blue, relief = FLAT)
		play_window = canvas.create_window(w/2-150, h/2+50, anchor=NW, window=play_bt)
		
		# pass_bt = Button(canvas, font=("Forte",15),text = "pass", command = PASS, anchor = W)
		# pass_bt.configure(width = 10, bg="#33B5E5",activebackground = light_blue, relief = FLAT)
		# pass_window = canvas.create_window(w/2+50, h/2+50, anchor=NW, window=pass_bt)
		
		play_bt.wait_variable(var2)
		next_player = AI1_card
		current_cards = current_cards_value
		# current_cards = int_to_name(current_cards_value,current_player_back_up)
		# game_page.mainloop()
	else:
		global first_round
		first_round = False
		(current_player,current_cards) = AI_play(current_player)
		print(current_player,' : ',current_cards)
		clear_AI_cards_num()
		display_AI_cards_num()
	
		# print('current player is HEY LOOKHERE!!!!!',current_player)
		next_player = get_next_player(current_player)
	
	
	while(len(AI1_card) != 0 and len(AI2_card) != 0 and len(AI3_card) != 0 and len(player_card) != 0):
		if(next_player == player_card):
			# button			
			# print('HEY YOU ARE IN PLAYER ROUND.')
			# try to clear previous pass text
			waithere_short()
			try:
				canvas.delete(pass_text)
			except NameError:
				print('pass text is not exist yet.')
			try:
				canvas.delete(AI_turn_text)
			except NameError:
				print('AI_turn_text is not exist yet.')
			global your_turn_display_text
	
			your_turn_display_text = canvas.create_text(w/2,h/2,fill="white",font=("forte",15),text='It is your turn to play:')
			play_bt = Button(canvas, font=("Forte",15),text = "play", command = play, anchor = W)
			play_bt.configure(width = 10, bg="#33B5E5",activebackground = light_blue, relief = FLAT)
			play_window = canvas.create_window(w/2-150, h/2+50, anchor=NW, window=play_bt)
			
			if(len(other_pass) != 3):
				pass_bt = Button(canvas, font=("Forte",15),text = "pass", command = PASS, anchor = W)
				pass_bt.configure(width = 10, bg="#33B5E5",activebackground = light_blue, relief = FLAT)
				pass_window = canvas.create_window(w/2+50, h/2+50, anchor=NW, window=pass_bt)
			
			# game_page.mainloop()
			if(var2 != 1):
				play_bt.wait_variable(var2)
			else:
				pass_bt.wait_variable(var2)
			
			
			
			next_player = AI1_card
			# print('current_cards_value',current_cards_value)
			# current_cards = int_to_name(current_cards_value,current_player_back_up)
			# print('after convert to name ',current_cards)
			if('You' not in other_pass):
				current_cards = current_cards_value
			# print('current player back up list',current_player_back_up)
			print('track current cards:     ',current_cards)
			print('track other pass:        ',other_pass)
			
		else:
			print('I GOT CURRENT CARD FROM PLAYER:',current_cards)
			try:
				canvas.delete(play_window)
			except NameError:
				print('play bt window is not exist')
			try:
				canvas.delete(pass_window)
			except NameError:
				print('pass window is not exist')
			# print('在while loop里的next_player是',next_player)
			if(len(other_pass) == 3):
				del other_pass[:]
				(current_player,current_cards) = AI_play(next_player)
			else:
				(current_player,current_cards) = respond(next_player,current_cards)
			
			clear_AI_cards_num()
			display_AI_cards_num()
			
			print('track current cards:     ',current_cards)
			print('track other pass:        ',other_pass)
	
		
			next_player = get_next_player(current_player)
	
	print('AI1_card length',len(AI1_card))
	print('AI2_card length',len(AI2_card))
	print('AI3_card length',len(AI3_card))
	print('player card length',len(player_card))
	
	
	# game_page.grab_set()
	game_page.resizable(False,False)
	game_page.mainloop()

root.mainloop()
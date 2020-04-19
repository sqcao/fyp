from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import pygame
import sys
import time
import random

# the code consist of two different GUI implementation
# 1. tkinter (for the introduction and login or sign up page)
# 2. pygame (for actual game loop)

#===================================tkinter page==================================

# when user press EXIT at the introduction page, the pygame window will not be executed
game = True
# this start_player will be set in tkinter page and used by pygame portion
start_player = ''

# introduction page
root = Tk()
root.title("Incredible Snake")
# width and height for the main introduction page
w = 840
h = 480
# in order to use the background image, use canvas in the root page
canvas = Canvas(root, width=w, height=h)
canvas.pack(side = LEFT)
background_img = Image.open('bg1.png')
bg_img = ImageTk.PhotoImage(background_img)
canvas.create_image(0,0,image=bg_img,anchor="nw")
root.resizable(False,False)

# color chart
light_blue = '#00ffff'
light_red = '#ff3333'
light_green = '#33ff33'

# GAME TITLE displayed in the introduction page
img = Image.open('snake.ico')
snake_title = img.resize((50,50),Image.ANTIALIAS)
title_img = ImageTk.PhotoImage(snake_title)
canvas.create_image(w/2-330,h/2-80,image=title_img,anchor="nw")
canvas.create_text(w/2,h/2-50,fill="black",font=("Forte",55),text='Incredible Snake')

# use to destroy all kinds of toplevel pages
def destroy_page(page):
	page.destroy()

# before start of actual gameloop, direct to a rule intro page
def before_start(username):
	intro_page = Toplevel(root)
	intro_page.title("Game Introduction")
	w = 750
	h = 450
	
	# background image
	canvas = Canvas(intro_page, width=w, height=h)
	canvas.pack(side = LEFT)
	intro_bg = Image.open('bg1.png')
	intro_image = ImageTk.PhotoImage(intro_bg)
	canvas.create_image(0,0,image=intro_image,anchor="nw")
	intro_page.resizable(False,False)
	
	# greeting
	greet = 'Hi welcome,' + username + '!'
	canvas.create_text(w/2,h/2-150,fill="black",font=("Forte",20),text=greet)
	
	# rule introduction
	canvas.create_text(w/2,h/2,fill="black",font=("helvetica",15),text='Unlike the traditional snake game,\nIncredible Snake added few new items to increase the fun and challenges.\n1.thunder (get killed once touched)\n2.cutter (no score, reduce snake length by one)\n3.diamond (one score, enter the special mode)\n4.apple (one score)')
	
	def proceed():
		global start_player
		start_player = username
		destroy_page(root)
	
	# GO button proceed to the gameloop
	GO_bt = Button(intro_page, text = "GO!",font='forte',command = proceed,anchor = 'nw',width = 12,bg=light_green,activebackground = light_green)
	GO_window = canvas.create_window(210, 350, anchor='nw', window=GO_bt)
	
	# switch account button
	switch_bt = Button(intro_page, text = "Switch account",font='forte',command = lambda:destroy_page(intro_page),anchor = 'nw',width = 12,bg=light_blue,activebackground =light_blue)
	switch_window = canvas.create_window(400, 350, anchor='nw', window=switch_bt)
	
	intro_page.grab_set()
	# in order for displaying the background image
	intro_page.mainloop()

# validation method for login
def validation(name,password,login_page):
	found_user = False
	username = name
	pw = password
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
		# validation pass, pass the username to the game introduction page
		destroy_page(login_page)
		before_start(username)
	else:
		messagebox.showerror('Login fail','username not exists or incorrect password.')

def login():
	# create a new window display the login form
	login_page = Toplevel(root)
	login_page.title("Login")
	login_page.geometry("280x250")
	login_frame = Frame(login_page)
	login_frame.grid()
	login_page.resizable(False,False)
	
	# form
	Label(login_frame, text='username',font='forte').grid(row=0,column=0,columnspan=2,pady=10)
	username_entry = ttk.Entry(login_frame)
	username_entry.grid(row=1,column=0,columnspan=2)
	Label(login_frame, text='password',font='forte').grid(row=2,column=0,columnspan=2,pady=10)
	password_entry = ttk.Entry(login_frame)
	password_entry.grid(row=3,column=0,columnspan=2)
	
	# back button and confirm button
	back = Button(login_frame,text="Back",font='forte',command=lambda:destroy_page(login_page),bg='#659EC7',activebackground='#659EC7',width = 10)
	confirm = Button(login_frame,text='Confirm',font='forte',command=lambda:validation(username_entry.get(),password_entry.get(),login_page),bg='#659EC7',activebackground='#659EC7',width = 10)
	back.grid(row=4,column=0,padx=10,pady=10)
	confirm.grid(row=4,column=1,padx=10,pady=10)
	
	# grab
	login_page.grab_set()

def signUp_checking(name,password,signUp_page):
	# check the username exitsed or not and constrain applies to the password
	user_list = []
	username = name
	pw = password
	# print('username:',username)
	# print(pw)
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
		# display a message box, press ok return to the previous page
		messagebox.showerror('Error','Username already exists, please enter another one.')
	else:
		if(re.match(r'[A-Za-z0-9@#$%^&*]{8,}',pw) == None):
			messagebox.showerror("Error","password pattern is incorrect, password must be 8 characters long, and can mix with characters(upper case/lower case) or digits or special characters in '@#$%^&*'")
		else:
			account_info = 'username:' + username + '\npassword:' + pw + '\n---------------------\n'
			with open('account.txt','a+') as account_file:
				account_file.write(account_info)
			messagebox.showinfo('Account created successfully','Create account successful, please log in.')
			# if account created successfully, destroy current sign up page
			destroy_page(signUp_page)

def signUp():
	# create a new window display the sign up form
	signUp_page = Toplevel(root)
	signUp_page.title("Sign Up Form")	
	signUp_page.geometry("280x250")
	signUp_frame = Frame(signUp_page)
	signUp_frame.grid()
	signUp_page.resizable(False,False)
	
	# form
	Label(signUp_frame, text='please enter your username',font='forte').grid(row=0,column=0,columnspan=2,pady=10)
	username_entry = ttk.Entry(signUp_frame)
	username_entry.grid(row=1,column=0,columnspan=2)
	Label(signUp_frame, text='please enter your password',font='forte').grid(row=2,column=0,columnspan=2,pady=10)
	password_entry = ttk.Entry(signUp_frame)
	password_entry.grid(row=3,column=0,columnspan=2)
	
	
	
	# back button and confirm button
	back = Button(signUp_frame,text="Back",font='forte',command=lambda:destroy_page(signUp_page),bg='#659EC7',activebackground='#659EC7',width = 10)
	submit = Button(signUp_frame,text='Submit',font='forte',command=lambda:signUp_checking(username_entry.get(),password_entry.get(),signUp_page),bg='#659EC7',activebackground='#659EC7',width = 10)
	back.grid(row=4,column=0,padx=10,pady=10)
	submit.grid(row=4,column=1,padx=10,pady=10)
	
	
	# grab
	signUp_page.grab_set()

def exit():
	global game
	game = False
	destroy_page(root)


		
# choice button
login_bt = Button(root, text = "Log in",font=('forte',20),command = login,width = 10,bg=light_blue,activebackground = light_blue)
login_window = canvas.create_window(150, 350, anchor='nw', window=login_bt)

signUp_bt = Button(root, text = "Sign up",font=('forte',20),command = signUp,width = 10,bg=light_blue,activebackground = light_blue)
signUp_window = canvas.create_window(350, 350, anchor='nw', window=signUp_bt)

exit_bt = Button(root, text = "Exit",font=('forte',20),command = exit,width = 10,bg=light_red,activebackground = light_red)
exit_window = canvas.create_window(550, 350, anchor='nw', window=exit_bt)

root.mainloop()








#====================================pygame====================================


# method field
def create_food(snake):
	food = None
	while(food == None):
		food = [random.randint(1,(width-1)//20)*delta,random.randint(1,(height-1)//20)*delta]
		if(food in snake):
			food = None
	return food

def create_cutter(snake,food):
	cutter = None
	while(cutter == None):
		cutter = [random.randint(3,(width-3)//20)*delta,random.randint(3,(height-3)//20)*delta]
		if(cutter in snake):
			cutter = None
		elif(cutter == food):
			cutter = None
	return cutter

def create_thunder(snake,food,cutter):
	thunder = None
	while(thunder == None):
		thunder = [random.randint(1,(width-1)//20)*delta,random.randint(1,(height-1)//20)*delta]
		if(thunder in snake):
			thunder = None
		elif(thunder == food):
			thunder = None
		elif(thunder == cutter):
			thunder = None
	return thunder

# no need update dollar, once eat the dollar enter the speical mode
def create_dollar(snake,food,cutter,thunder_list):
	dollar = None
	while(dollar == None):
		dollar = [random.randint(1,(width-1)//20)*delta,random.randint(1,(height-1)//20)*delta]
		if(dollar in snake):
			dollar = None
		elif(dollar == food):
			dollar = None
		elif(dollar == cutter):
			dollar = None
		elif(dollar in thunder_list):
			dollar = None
	return dollar

def update_thunder(snake,food,cutter,thunder_list,k):
	# create a new thunder list
	while(k > 0):
		thunder = create_thunder(snake,food,cutter)
		thunder_list.append(thunder)
		k -= 1
	return thunder_list
	
def update_dollar(snake,food,cutter,thunder_list,dollar_list,num_dollar):
	# create a new dollar list	
	n = num_dollar
	while(n > 0):
		dollar = create_dollar(snake,food,cutter,thunder_list)
		dollar_list.append(dollar)
		n -= 1
	return dollar_list

def special_mode(snake,food,cutter,thunder_list,dollar_list,num_dollar):
	# clear the screen and stop generating other items
	# how to clear the screen: set everything to false
	
	# need to clear the current items in the screen
	pygame.draw.rect(playSurface, black, pygame.Rect(food[0], food[1], delta, delta))
	pygame.draw.rect(playSurface, black, pygame.Rect(cutter[0], cutter[1], delta, delta))
	
	# set all items to be False
	food = None
	cutter = None
	dollar_list[:] = []
	thunder_list[:] = []

	# generate dollars
	dollar_list = update_dollar(snake,food,cutter,thunder_list,dollar_list,num_dollar)
	return dollar_list

# end of method field


# Game Over
def gameOver(go_reason):
	myFont = pygame.font.SysFont('monaco', 72)
	# This creates a new Surface with the specified text rendered on it. pygame provides no way to directly draw text on an existing Surface: instead you must use Font.render() to create an image (Surface) of the text, then blit this image onto another Surface.
	# render(text, antialias, color, background=None)
	reason_dict = {'thunder':'You are killed by thunder!','body':'You hit the snake body!','boder':'You hit the boder!'}
	reason = reason_dict[go_reason]
	GOsurf = myFont.render(reason, True, red)
	GOrect = GOsurf.get_rect()
	GOrect.midtop = (width//2, height//2)
	playSurface.blit(GOsurf, GOrect)
	showScore(0)
	pygame.display.flip()
	# update the game record
	record_dict = {}
	try:	# try to open the record file
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
	except:	# if record file not exists, just create a new one and write the current record
		log_game_record(score)

	time.sleep(4)
	pygame.quit()
	sys.exit()

# a special ending if the snake length becomes zero
def special_end():
	myFont = pygame.font.SysFont('monaco', 72)
	SEsurf = myFont.render("OMG, the snake disappear!", True, red)
	SErect = SEsurf.get_rect()
	SErect.midtop = (width//2, height//2)
	playSurface.blit(SEsurf, SErect)
	showScore(0)
	pygame.display.flip()
	time.sleep(4)
	pygame.quit()
	sys.exit()


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
		else:	# if it's new player
			print('writing new record')
			# just store the record
			record_file = open('game_record.txt','a+')
			write_in_newfile = search_user_str + str(max_score) + '\n'
			record_file.write(write_in_newfile)
			record_file.close()

	except IOError:	# if file not exists
		record_file = open('game_record.txt','w+')
		write_in_newfile = search_user_str + str(max_score) + '\n'
		record_file.write(write_in_newfile)
		record_file.close()

# display part

# display current score and max score
def showScore(choice=1):
    SFont = pygame.font.SysFont('monaco', 32)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, white)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (width//2, 0)
    else:
        Srect.midtop = (width//2, height//2-50)
    playSurface.blit(Ssurf, Srect)

def showMaxScore():
	record_dict = {}
	try:
		with open('game_record.txt','rt') as game_record:
			for line in game_record:
				(player,score) = line.rstrip('\n').split(':')
				record_dict[player] = score
		result = max(zip(record_dict.values(), record_dict.keys()))
		max_score = str(result[0])
		player = result[1]
	except:
		player = ''
		max_score = '0'
	SFont = pygame.font.SysFont('monaco', 32)
	max_record = max_score + ' [' + player + ']'
	Ssurf = SFont.render("Max Score  :  {0}".format(max_record), True, white)
	Srect = Ssurf.get_rect()
	Srect.topleft = (0, 0)
	playSurface.blit(Ssurf, Srect)

def draw_food(food):
	foodImg_big = pygame.image.load('apple.jpg')
	foodImg = pygame.transform.scale(foodImg_big, (delta, delta))
	playSurface.blit(foodImg,(food[0],food[1]))

def draw_cutter(cutter):
	cutterImg_big = pygame.image.load('cutter.jpg')
	cutterImg = pygame.transform.scale(cutterImg_big, (delta, delta))
	playSurface.blit(cutterImg,(cutter[0],cutter[1]))

def draw_thunder(thunder_list):
	thunderImg_big = pygame.image.load('thunder.jpg')
	thunderImg = pygame.transform.scale(thunderImg_big, (delta, delta))
	for thunders in thunder_list:
		playSurface.blit(thunderImg,(thunders[0],thunders[1]))

def draw_dollar(dollar_list):
	dollarImg_big = pygame.image.load('dollar.jpg')
	dollarImg = pygame.transform.scale(dollarImg_big, (delta, delta))
	for dollars in dollar_list:
		playSurface.blit(dollarImg,(dollars[0],dollars[1]))

# end of display part



if(game == True):
	# Pygame Init
	init_status = pygame.init()
	if init_status[1] > 0:
		print("Had {0} initialising errors, exiting... ".format(init_status[1]))
		sys.exit()
	else:
		print("Pygame initialised successfully ")

	# Play Surface
	size = width, height = 840, 480
	playSurface = pygame.display.set_mode(size)
	pygame.display.set_caption("Snake Game")

	# Colors
	red = pygame.Color(255, 0, 0)
	green = pygame.Color(0, 255, 0)
	black = pygame.Color(0, 0, 0)
	white = pygame.Color(255, 255, 255)
	brown = pygame.Color(165, 42, 42)
	yellow = pygame.Color(255,185,15)

	# FPS controller
	fpsController = pygame.time.Clock()

	# Game settings
	delta = 20	# the unit cell size of the game
	head = [width//2,height//2]
	snake = [[width//2,height//2], [width//2-delta,height//2], [width//2-2*delta,height//2]]


	# before start of game, some initialization
	mode = False
	food = create_food(snake)
	cutter = create_cutter(snake,food)
	direction = 'RIGHT'	# initialize the direction
	changeto = ''	# changto is the direction that change by user keyboard input
	score = 0	# initialize the score
	thunder = False
	thunder_list = []	# the thunder will only appear after 3000 ticks
	dollar = False
	dollar_list = []	# the dollar will only appear after 4000 ticks
	num_thunder = 4	# the number of thunder will increased as game goes on
	num_dollar = 15 # the number of dollars in the special mode


	# we need to get the different ticks in order to decide when refresh the items on the screen
	cutter_appear_time = pygame.time.get_ticks()
	thunder_appear_time = pygame.time.get_ticks()
	last_time_increase = pygame.time.get_ticks()
	dollar_appear_time = pygame.time.get_ticks()


	
# main game loop start
while(game==True):
	# keyboard change to direction
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				changeto = 'RIGHT'
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				changeto = 'LEFT'
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				changeto = 'UP'
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				changeto = 'DOWN'
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

	# Validate direction
	if changeto == 'RIGHT' and direction != 'LEFT':
		direction = changeto
	if changeto == 'LEFT' and direction != 'RIGHT':
		direction = changeto
	if changeto == 'UP' and direction != 'DOWN':
		direction = changeto
	if changeto == 'DOWN' and direction != 'UP':
		direction = changeto

	# Update snake position, move the snake
	if direction == 'RIGHT':
		head[0] += delta
	if direction == 'LEFT':
		head[0] -= delta
	if direction == 'DOWN':
		head[1] += delta
	if direction == 'UP':
		head[1] -= delta
	
	# update the cutter every 3500 ticks
	update_cutter_duration = pygame.time.get_ticks() - cutter_appear_time
	if(update_cutter_duration > 3500 and mode == False):
		cutter = None
		cutter = create_cutter(snake,food)
		cutter_appear_time = pygame.time.get_ticks()	# get the new tick time
	
	# increase number of thunder every 10000 ticks
	increase_thunder_duration = pygame.time.get_ticks() - last_time_increase
	if(increase_thunder_duration > 15000 and mode == False):
		num_thunder += 1
		last_time_increase = pygame.time.get_ticks()	# get the new tick time
	
	# when reach 3000 ticks start to create thunder
	# and update the thunder every 3000 ticks
	update_thunder_duration = pygame.time.get_ticks() - thunder_appear_time
	if(update_thunder_duration > 3000 and mode == False):
		thunder_list[:] = []	# clear the list
		k = num_thunder	# use k to get the number of thunders need to create
		thunder_list = update_thunder(snake,food,cutter,thunder_list,k)
		thunder_appear_time = pygame.time.get_ticks()	# get the new tick time
	
	# when reach 4000 ticks start to create dollar
	# and update the dollar every 3000 ticks
	update_dollar_duration = pygame.time.get_ticks() - dollar_appear_time
	if(update_dollar_duration > 4000 and mode == False):
		dollar_list[:] = []
		dollar = create_dollar(snake,food,cutter,thunder_list)
		dollar_list.append(dollar)	# in normal mode, only create one dollar
		dollar_appear_time = pygame.time.get_ticks()	# get the new tick time
	
	# the special mode will only last for 20000 ticks long
	if(mode == True):
		special_mode_duration = pygame.time.get_ticks() - special_mode_start_time
		if(special_mode_duration > 10000):
			dollar_list[:] = []	# clear all remaining dollars
			mode = False	# set the mode back to False, so that the items will generate as usual
			
	
	# only when snake eat food or dollar will increase the score
	
	# Snake body mechanism
	snake.insert(0, list(head))	# append one unit to the snake
	if head == food:
		food = None	# if food has been eaten, set food to None
		score += 1
	elif head == cutter:
		cutter = None	# if food has been eaten, set food to None
		snake.pop()	# pop the added unit
		snake.pop()	# pop one more means cut the snake length by 1
	elif head in dollar_list:
		score += 1
		dollar_list.remove(head)	#remove the eaten dollar
		if(mode == False):	# record down the start time in the normal mode
			mode = True
			special_mode_start_time = pygame.time.get_ticks()	# get the mode start time
			dollar_list = special_mode(snake,food,cutter,thunder_list,dollar_list,num_dollar)	# enter the special mode
	else:
		snake.pop()	# if never eat anything, just pop the added unit from snake
		
	# food and cutter need to be created if they been eaten
	# thunder and dollar need not to be re-create

	# create new item if they are eaten
	if(food == None and mode == False):
		food = create_food(snake)
	if(cutter == None and mode == False):
		cutter = create_cutter(snake,food)

	# start to draw items to the playsurface
	playSurface.fill(black)	# set the playSurface background color
	
	for pos in snake:	# draw the snake body
		pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], delta, delta))
	
	# draw the food
	if(food != None and mode == False):
		draw_food(food)	# pass the created food
	
	# draw the cutter
	if(cutter != None and mode == False):
		draw_cutter(cutter)	# pass the created cutter
	
	# draw the thunder
	if(len(thunder_list) != 0):
		draw_thunder(thunder_list)

	# draw the dollar
	if(len(dollar_list) != 0):
		draw_dollar(dollar_list)

	# various ending:
	if len(snake) == 0:	# if snake length is zero, trigger special ending
		special_end()
	
	if head in thunder_list:	# if snake hit by thunder, game over
		gameOver('thunder')
	if head[0] >= width or head[0] < 0:	# if snake hit the border, game over
		gameOver('boder')
	if head[1] >= height or head[1] < 0:
		gameOver('boder')

	for block in snake[1:]:	# if snake hit itself, game over
		if head == block:
			gameOver('body')

	# display the score while game play
	showScore()
	showMaxScore()
	# refresh the game screen
	pygame.display.flip()
	# control the game speed
	fpsController.tick(12)
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import pygame
import random
from threading import Timer
import time

#===================================tkinter page==================================

# when user press EXIT at the introduction page, the pygame window will not be executed
game = True
start = False
# this start_player will be set in tkinter page and used by pygame portion
start_player = ''

# introduction page
root = Tk()
root.title("Back To School")
# width and height for the main introduction page
w = 550
h = 480
# in order to use the background image, use canvas in the root page
canvas = Canvas(root, width=w, height=h)
canvas.pack(side = LEFT)
background_img = Image.open('bg2.jpg')
bg_img = ImageTk.PhotoImage(background_img)
canvas.create_image(0,0,image=bg_img,anchor="nw")
root.resizable(False,False)

# color chart
blue = (0,200,200)
bright_blue = (0,255,255)
light_blue = '#00ffff' 
light_red = '#ff3333'
light_green = '#33ff33'


# use to destroy all kinds of toplevel pages
def destroy_page(page):
	page.destroy()

def waithere_short():
	var = IntVar()
	root.after(1500, var.set, 1)
	print("waiting...")
	root.wait_variable(var)

def waithere_long():
	var = IntVar()
	root.after(4500, var.set, 1)
	print("waiting...")
	root.wait_variable(var)

# before start of actual gameloop, direct to a rule intro page
def before_start(username):
	intro_page = Toplevel(root)
	intro_page.title("Game Introduction")
	w = 900
	h = 500
	
	def on_configure(event):
		# update scrollregion after starting 'mainloop'
		# when all widgets are in canvas
		canvas.configure(scrollregion=canvas.bbox('all'))
	
	# background image
	canvas = Canvas(intro_page, width=w, height=h)
	canvas.pack(side = LEFT)
	intro_bg = Image.open('bg5.png')
	intro_image = ImageTk.PhotoImage(intro_bg)
	canvas.create_image(0,0,image=intro_image,anchor="nw")
	scrollbar = Scrollbar(intro_page, command=canvas.yview)
	scrollbar.pack(side=LEFT, fill='y')

	canvas.configure(yscrollcommand = scrollbar.set)
	# update scrollregion after starting 'mainloop'
	# when all widgets are in canvas
	canvas.bind('<Configure>', on_configure)
	intro_page.resizable(False,False)
	
	# greeting
	greet = 'Hi welcome, ' + username + '!'
	canvas.create_text(w/2,h/2-180,fill="white",font=("Forte",25),text=greet)
	
	# read the game intro and rule until [Background] part
	empty_line = 0
	part1 = []
	intro = ''
	try:
		with open('intro.txt','rt') as intro_file:
			for line in intro_file:
				# from welcome to background_part have 3 empty line
				if(line == '\n'):
					empty_line += 1
				# welcome and rule are stored inside the part1 list
				if(empty_line < 3):
					part1.append(line)
	except IOError:
		messagebox('Error','Introduction file not exists or has been deleted')
	
	for part in part1:
		intro = intro + part
	
	# rule introduction
	canvas.create_text(w/2,h/2+130,fill="black",font=("helvetica",15),text=intro)
	
	def proceed():
		global start_player
		start_player = username
		destroy_page(root)
	
	# GO button proceed to the gameloop
	GO_bt = Button(intro_page, text = "GO!",font='forte',command = proceed,anchor = 'nw',width = 12,bg=light_green,activebackground = light_green)
	GO_window = canvas.create_window(w/2-150, 650, anchor='nw', window=GO_bt)
	
	# switch account button
	switch_bt = Button(intro_page, text = "Switch account",font='forte',command = lambda:destroy_page(intro_page),anchor = 'nw',width = 12,bg=light_blue,activebackground =light_blue)
	switch_window = canvas.create_window(w/2+50, 650, anchor='nw', window=switch_bt)
	
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
login_bt = Button(root, text = "Log in",font=('forte',15),command = login,width = 10,bg=light_blue,activebackground = light_blue)
login_window = canvas.create_window(50, 350, anchor='nw', window=login_bt)

signUp_bt = Button(root, text = "Sign up",font=('forte',15),command = signUp,width = 10,bg=light_blue,activebackground = light_blue)
signUp_window = canvas.create_window(200, 350, anchor='nw', window=signUp_bt)

exit_bt = Button(root, text = "Exit",font=('forte',15),command = exit,width = 10,bg=light_red,activebackground = light_red)
exit_window = canvas.create_window(350, 350, anchor='nw', window=exit_bt)

root.mainloop()







#============================pygame loop==================================

# after press GO button, then display the background of game in the new page
# then in the background page, press any key to continue

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)
yellow = pygame.Color(255,185,15)

def wrap_text(message, wraplimit):
    return textwrap.fill(message, wraplimit)

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
	pygame.display.set_caption("Back To School")
	
	# FPS controller
	fpsController = pygame.time.Clock()

	# first display the background
	background = pygame.image.load("classroom.jpg")
	picture = pygame.transform.scale(background, (840, 480))
	playSurface.blit(picture,(0,0))
	
	# background introductions
	empty_line = 0
	part2 = []
	intro_background = ''
	try:
		with open('intro.txt','rt') as intro_file:
			for line in intro_file:
				if(line == '\n'):
					empty_line += 1
				# the background part is within 3 empty line
				if(empty_line == 3):
					part2.append(line)
	except IOError:
		print('Introduction file not exists or has been deleted')
	
	for part in part2:
		intro_background = intro_background + part
		
	# print(intro_background)
	
	def blit_text(surface, text, pos, font, color=pygame.Color('black')):
		words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
		space = font.size(' ')[0]  # The width of a space.
		max_width, max_height = surface.get_size()
		x, y = pos
		for line in words:
			for word in line:
				word_surface = font.render(word, 0, color)
				word_width, word_height = word_surface.get_size()
				if x + word_width >= max_width-150:
					x = pos[0]  # Reset the x.
					y += word_height  # Start on new row.
				surface.blit(word_surface, (x, y))
				x += word_width + space
			x = pos[0]  # Reset the x.
			y += word_height  # Start on new row
			
	myFont = pygame.font.SysFont('monaco', 35)
	blit_text(playSurface,intro_background,(100, 60), myFont)
		
	pygame.display.flip()
	# control the game speed
	fpsController.tick(12)





# in order to proceed while player press any key, we stored all the background_img into list
# and all the background introductions into another list also


# the background image will stay the same at introduction
# we change only the characters image
# characters images are all png, so can just put in front of backgroud image

# change the character image based on the intro_list
img_dict = {'Teacher':'teacher.png','Jandon':'jandon.png','You':'you.png'}
intro = []

# read everything into intro_list
# separate them by empty line
empty_line = 0
try:
	with open('intro.txt','rt') as intro_file:
		for line in intro_file:
			if(line == '\n'):
				empty_line += 1
			# append everything beyond 3 empty line into the intro_parts
			if(empty_line >3):
				intro.append(line)
except IOError:
	print('Introduction file not exists or has been deleted')
# first convert the list into string
# intro_string = intro_list
# then split the string by empty line and covert back to list
# intro_list = intro_string.split('\n')
intro_list = []
for element in intro:
	element = element.rstrip('\n')
	intro_list.append(element)



intro_list.pop(0)
# remove can only remove one element
# so using filter to remove all empty element
intro_list_new = list(filter(lambda a: a != '', intro_list))
intro_str = str(intro_list_new)








# this is introduction loop
i = 0
while(game==True and start == False):
	# press any key to continue
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			# increase when press
			i = i + 1
			print(i)
			# clear the previous  image
			playSurface.fill((255,255,255))
			# get intro script from the list
			try:
				next_intro = intro_list_new[i-1]
			except IndexError:
				start = True
				break
			# load new image based on the intro script
			background = pygame.image.load('background1.png')
			playSurface.blit(background,(0,0))
			
			# display the dialog box
			dialog = pygame.image.load('dialog.png')
			dialog_image = pygame.transform.scale(dialog, (770, 200))
			playSurface.blit(dialog_image,(50,270))
			blit_text(playSurface,next_intro,(205, 300), myFont)
			# fetch teacher, jandon and your image, the rest left with empty character image
			if(':' in next_intro):
				split_intro = next_intro.split(':')
				character = split_intro[0]
				character_img = img_dict[character]
				character_image = pygame.image.load(character_img)
				# resize the character image, only teacher image need to be resize
				if(character == 'Teacher'):
					character_image = pygame.transform.scale(character_image, (320, 480))
					playSurface.blit(character_image,(-50,120))
				elif(character == 'Jandon'):
					playSurface.blit(character_image,(-110,0))
				else:
					playSurface.blit(character_image,(-10,0))
	
	
			pygame.display.flip()
			# fpsController.tick(12)
	if(start == True):
		break


	
			

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def get_rule(type):
	rule_type = type
	rule_found = False
	rule = []
	
	rule_type_to_search = '[' + rule_type + ']'
	with open('rule.txt','rt') as rule_file:
		for line in rule_file:
			if(rule_type_to_search in line):
				rule_found = True
			if(rule_found == True):
				if(line != '\n'):
					rule.append(line)
				# if reach empty line, just break
				if(line == '\n'):
					break
	rule_string = ('').join(rule)
	return rule_string

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(playSurface, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(playSurface, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    playSurface.blit(textSurf, textRect)






# ================================actual competition=============================

global win_first_time_list_player
global win_more_than_one_time_list_player
global lost_first_time_list_player
global lost_more_than_one_time_list_player
win_first_time_player = False
win_more_than_one_time_player = False
lost_first_time_player = False
lost_more_than_one_time_player = False
win_first_time_list_player = []
win_more_than_one_time_list_player = []
lost_first_time_list_player = []
lost_more_than_one_time_list_player = []

global win_first_time_list_jandon
global win_more_than_one_time_list_jandon
global lost_first_time_list_jandon
global lost_more_than_one_time_list_jandon
win_first_time_jandon = False
win_more_than_one_time_jandon = False
lost_first_time_jandon = False
lost_more_than_one_time_jandon = False
win_first_time_list_jandon = []
win_more_than_one_time_list_jandon = []
lost_first_time_list_jandon = []
lost_more_than_one_time_list_jandon = []


global win_result
global lost_result
win_result = 0
lost_result = 0



# get all the scripts first and store in list
with open('player_script.txt','rt') as player_script_file:
	for line in player_script_file:
		if('[win first time]' in line):
			win_first_time_player = True
		if('[win more than one time]' in line):
			win_more_than_one_time_player = True
		if('[lost first time]' in line):
			lost_first_time_player = True
		if('[lost more than one time]' in line):
			lost_more_than_one_time_player = True
			
		if(win_first_time_player == True and win_more_than_one_time_player == False):
			win_first_time_list_player.append(line.rstrip('\n'))
			
		if(win_more_than_one_time_player == True and lost_first_time_player == False):
			win_more_than_one_time_list_player.append(line.rstrip('\n'))
			
		if(lost_first_time_player == True and lost_more_than_one_time_player == False):
			lost_first_time_list_player.append(line.rstrip('\n'))
			
		if(lost_more_than_one_time_player == True):
			lost_more_than_one_time_list_player.append(line.rstrip('\n'))
			
with open('Jandon_script.txt','rt') as player_script_file:
	for line in player_script_file:
		if('[win first time]' in line):
			win_first_time_jandon = True
		if('[win more than one time]' in line):
			win_more_than_one_time_jandon = True
		if('[lost first time]' in line):
			lost_first_time_jandon = True
		if('[lost more than one time]' in line):
			lost_more_than_one_time_jandon = True
			
		if(win_first_time_jandon == True and win_more_than_one_time_jandon == False):
			win_first_time_list_jandon.append(line.rstrip('\n'))
			
		if(win_more_than_one_time_jandon == True and lost_first_time_jandon == False):
			win_more_than_one_time_list_jandon.append(line.rstrip('\n'))
			
		if(lost_first_time_jandon == True and lost_more_than_one_time_jandon == False):
			lost_first_time_list_jandon.append(line.rstrip('\n'))
			
		if(lost_more_than_one_time_jandon == True):
			lost_more_than_one_time_list_jandon.append(line.rstrip('\n'))

win_first_time_list_player.remove('[win first time]')
win_more_than_one_time_list_player.remove('[win more than one time]')
lost_first_time_list_player.remove('[lost first time]')
lost_more_than_one_time_list_player.remove('[lost more than one time]')

win_first_time_list_jandon.remove('[win first time]')
win_more_than_one_time_list_jandon.remove('[win more than one time]')
lost_first_time_list_jandon.remove('[lost first time]')
lost_more_than_one_time_list_jandon.remove('[lost more than one time]')	

# print('BELOW IS ALL SCRITPS')
# print('player: win one time:')
# print(win_first_time_list_player)
# print('player: win more than one:')
# print(win_more_than_one_time_list_player)
# print('player: lost one time:')
# print(lost_first_time_list_player)
# print('player: lost more than one:')
# print(lost_more_than_one_time_list_player)

# print('======================================')
# print('jandon: win one time:')
# print(win_first_time_jandon)
# print('jandon: win more than one:')
# print(win_more_than_one_time_jandon)
# print('jandon: lost one time:')
# print(lost_first_time_jandon)
# print('jandon: lost more than one')
# print(lost_more_than_one_time_jandon)

# print('======================================')


root = Tk()
root.title("Choosing Competition")
root.configure(bg='black')
# width and height for the main introduction page
w = 650
h = 500
# in order to use the background image, use canvas in the root page
# canvas = Canvas(root, width=w, height=h)
# canvas.pack(side = LEFT)

global wordbrain_done
wordbrain_done = False
global reaction_done
reaction_done = False
global country_done
country_done = False
global math_done
math_done = False
global language_done
language_done = False

global var2
var2 = IntVar()

# 显示可以选择的比赛项目
def red_text(event=None):
	lab.config(fg="grey")

def black_text(event=None):
	lab.config(fg="white")

def red_text_2(event=None):
	lab_2.config(fg="grey")

def black_text_2(event=None):
	lab_2.config(fg="white")

def red_text_3(event=None):
	lab_3.config(fg="grey")

def black_text_3(event=None):
	lab_3.config(fg="white")

def red_text_4(event=None):
	lab_4.config(fg="grey")

def black_text_4(event=None):
	lab_4.config(fg="white")

def red_text_5(event=None):
	lab_5.config(fg="grey")

def black_text_5(event=None):
	lab_5.config(fg="white")

def display_competition_rule(type):
	global win_num
	global lost_num
	win_num = 0
	lost_num = 0
	
	rule_page = Toplevel(root)
	rule_page.title(type)
	w = 750
	h = 500
	canvas = Canvas(rule_page, width=w, height=h)
	canvas.pack(side = LEFT)
	
	rule_background_img = Image.open('question_background.jpg')
	rule_bg = rule_background_img.resize((750,500),Image.ANTIALIAS)
	rule_background_image = ImageTk.PhotoImage(rule_bg)
	canvas.create_image(0,0,image=rule_background_image,anchor="nw")
	
	rule = get_rule(type)
	# display the competition rule
	canvas.create_text(w/2,h/2,fill="white",font=("Forte",20),text=rule)
	
	def start_competition():
		# close rule page and create a new competition page
		destroy_page(rule_page)
		competition(type)
	
	# button to start the competition
	start_bt = Button(rule_page, text = "Start",font='forte',command = start_competition,anchor = 'n',width = 12,bg=light_green,activebackground = light_green,relief = FLAT)
	start_window = canvas.create_window(w/2+100, h/2+100, anchor='nw', window=start_bt)
	
	rule_page.grab_set()
	rule_page.resizable(False,False)
	rule_page.mainloop()


def competition(type):
	# create a new page for display the questions, and later return to the root page to choose other type of competition
	competition_page = Toplevel(root)
	competition_page.title(type)
	w = 750
	h = 500
	canvas = Canvas(competition_page, width=w, height=h)
	canvas.pack(side = LEFT)
	
	def ask_question(question_type):
		var = IntVar()
		var_2 = IntVar()
		# I need to ask 10 questions in this function
		# and summarize the 10 times wins and losts, return the final result
		num_win = 0
		num_lost = 0
		easy_question = {}
		diff_question = {}
		# string concatenation
		question_type_to_find = '[' + question_type + ']'
		# read all specific type of question into a dict {question:answer}
		found = False
		easy = False
		diff = False
		end = False
		with open('questions_unicode.txt','rt',encoding = 'utf-16') as question_file:
				linenum = 0
				for line in question_file:
					linenum += 1
					if(question_type_to_find in line):
						# find each type of question
						line_to_find = linenum + 1
						found = True
					# line that larger than the current type title
					if(found == True):
						if('(easy)' in line):
							easy_line = linenum
							easy = True
						elif('(diff)' in line):
							diff_line = linenum
							diff = True
						elif(line == '\n'):
							end_line = linenum
							end = True
						if(easy == True and diff != True):
							if(linenum > easy_line):
								(easyQ,easyA) = line.rstrip('\n').split(':')
								easy_question[easyQ] = easyA
						elif(diff == True and end != True):
							if(linenum > diff_line):
								(diffQ,diffA) = line.rstrip('\n').split(':')
								diff_question[diffQ] = diffA
		# now we have one full set of questions with given type		
		easy_question_options = list(easy_question.keys())
		diff_question_options = list(diff_question.keys())
		all_question_options = easy_question_options + diff_question_options
		i = 0
		
		# after times up Jandon will answer the question, so need to show Jandon	
		def time_ran_out(answer):			
			Jandon_dialog_img = Image.open('dialog.png')
			Jandon_dialog_bg = Jandon_dialog_img.resize((400,120),Image.ANTIALIAS)
			Jandon_dialog_image = ImageTk.PhotoImage(Jandon_dialog_bg)
			dialog_jadon_display = canvas.create_image(200,h-250,image=Jandon_dialog_image,anchor="nw")
			
			
			Jandon_img = Image.open('jandon.png')
			Jandon_bg = Jandon_img.resize((450,500),Image.ANTIALIAS)
			Jandon_image = ImageTk.PhotoImage(Jandon_bg)
			jandon_image_display = canvas.create_image(50,h-400,image=Jandon_image,anchor="nw")
			
			global Jandon_answer_text
			Jandon_answer = 'Jandon: ' + answer
			Jandon_answer_text = canvas.create_text(w/2,h/2+50,fill="black",font=("Forte",15),text=Jandon_answer)
			def next_question():
				# clear the ok button and Jandon's answer
				canvas.delete(OK_window)
				canvas.delete(Jandon_answer_text)
				canvas.delete(jandon_image_display)
				canvas.delete(dialog_jadon_display)
				var_2.set(1)
			
			# button to continue
			OK_bt = Button(competition_page, text = "OK",font='forte',command = next_question,anchor = 'n',width = 6,bg=light_blue,activebackground = light_blue,relief = FLAT)
			OK_window = canvas.create_window(w/2+80, h-180, anchor='nw', window=OK_bt)
			
			OK_bt.wait_variable(var_2)
		
		global q_num_text
		global question_text
		global entry_window
		global answer_window
		# we will ask 10 question in total (for each round)
		while(i < 10):
			if(i > 0):
				canvas.delete(q_num_text)
				canvas.delete(question_text)
				canvas.delete(entry_window)
				canvas.delete(answer_window)
				try:
					canvas.delete(Jandon_answer_text)
				except NameError:
					print('Jandon did not answer last time.')
			i += 1
			easy = False
			# randomly select question from options
			question = random.choice(all_question_options)
			all_question_options.remove(question)
			# get the answer for that randomly selected question
			if(question in easy_question_options):
				answer = easy_question[question]
				easy = True
			else:
				answer = diff_question[question]
			question_num_text = 'Question ' + str(i)
			q_num_text = canvas.create_text(130,80,fill="white",font=("helvetica",20),text=question_num_text)
			
			question_str = str(question)
			print('question is ',question)
			print('question str is ',question_str)
			question_text = canvas.create_text(w/2,h/2-110,fill="white",font=("helvetica",15),text=question_str,width=450)
			if(easy == True):
				limit = 15
			else:
				limit = 30
			
			t=Timer(limit,time_ran_out,(answer,))
			t.start()
			# user_input = input('\n>')
			# change 回答问题的方式，在GUI里，是给一个text box
			answer_entry = Entry(competition_page)
			entry_window = canvas.create_window(w/2,h/2-80,window=answer_entry)
			
			def answering():
				global user_input
				user_input = answer_entry.get()
				
				var.set(1)
			
			
			
			answer_bt = Button(competition_page, text = "Answer",font='forte',command = answering,anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue,relief = FLAT)
			answer_window = canvas.create_window(w/2-70, h/2-50, anchor='nw', window=answer_bt)
			
			answer_bt.wait_variable(var)
			# 等待answer button 被按下，如果限定时间过了，显示输了
			
			
			
			# decide the score result
			timer_str = str(t)
			# print('outside answer method, user_input get',user_input)
			# print('answer is ',answer)
			# print('timer string is ',timer_str)
			# if timer not expire and answer correct
			if('stopped' not in timer_str and user_input.lower() == answer):
				win_text = 'You win! You are faster than Jandon and your answer is correct!'
				# canvas.create_text(w/2,h/2-130,fill="white",font=("helvetica",15),win_text)
				messagebox.showinfo('Win',win_text,parent = competition_page)
				num_win += 1
			# I need to have two cases for lost game: 1. time up 2. wrong answer
			elif('stopped' not in timer_str and user_input.lower() != answer):
				lost_text = 'You lost, your answer is wrong.'
				messagebox.showinfo('Lost',lost_text,parent = competition_page)
				num_lost += 1
			elif('stopped' in timer_str):
				lost_text = 'You lost, Jandon is faster than you.'
				messagebox.showinfo('Lost',lost_text, parent = competition_page)
				num_lost += 1
			t.cancel()
		
		def clear_page():
			canvas.delete(q_num_text)
			# canvas.delete(dialog_jadon_display)
			# canvas.delete(jandon_image_display)
			canvas.delete(question_text)
			canvas.delete(entry_window)
			canvas.delete(answer_window)
		
		# 问完十个问题后，clear page, 
		waithere_short()
		clear_page()
		# display this round result and you or Jandon script
		
		try:
			canvas.delete(player_script_str_text)
		except NameError:
			print('player script not exists')
		try:
			canvas.delete(Jandon_script_str_text)
		except NameError:
			print('Jandon script not exists')
		try:
			canvas.delete(match_script_str_text)
		except NameError:
			print('match script not exists')

		canvas.delete(answer_window)
		canvas.delete(entry_window)
		
		
		dialog_image_win_img = Image.open('dialog.png')
		dialog_image_win_pic = dialog_image_win_img.resize((600,150),Image.ANTIALIAS)
		dialog_image_win_image = ImageTk.PhotoImage(dialog_image_win_pic)
		dialog_image_win_picture = canvas.create_image(100,h/2-100,image=dialog_image_win_image,anchor="nw")
		
		# return this round result
		if(num_win > num_lost):
			result = 'win'
			if(win_result > 1):
				player_img = Image.open('you.png')
				player_pic = player_img.resize((450,550),Image.ANTIALIAS)
				player_image = ImageTk.PhotoImage(player_pic)
				player_picture = canvas.create_image(w/2,h/2-200,image=player_image,anchor="nw")
				
				player_script_str = '\n'.join(win_more_than_one_time_list_player)
				player_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=player_script_str)
				
				# 换下一个台词
				waithere_long()
				canvas.delete(player_script_str_text)
				canvas.delete(player_picture)
				
				Jandon_img = Image.open('jandon.png')
				Jandon_pic = Jandon_img.resize((450,550),Image.ANTIALIAS)
				Jandon_image = ImageTk.PhotoImage(Jandon_pic)
				Jandon_picture = canvas.create_image(10,h/2-200,image=Jandon_image,anchor="nw")
				
				Jandon_script_str = '\n'.join(lost_more_than_one_time_list_jandon)
				Jandon_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=Jandon_script_str)
				
			else:
				player_img = Image.open('you.png')
				player_pic = player_img.resize((450,550),Image.ANTIALIAS)
				player_image = ImageTk.PhotoImage(player_pic)
				player_picture = canvas.create_image(w/2,h/2-200,image=player_image,anchor="nw")
				
				player_script_str = '\n'.join(win_first_time_list_player)
				player_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=player_script_str)
				
				# 换下一个台词
				waithere_long()
				canvas.delete(player_script_str_text)
				canvas.delete(player_picture)
				
				Jandon_img = Image.open('jandon.png')
				Jandon_pic = Jandon_img.resize((450,550),Image.ANTIALIAS)
				Jandon_image = ImageTk.PhotoImage(Jandon_pic)
				Jandon_picture = canvas.create_image(10,h/2-200,image=Jandon_image,anchor="nw")
				
				Jandon_script_str = '\n'.join(lost_first_time_list_jandon)
				Jandon_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=Jandon_script_str)
												
		elif(num_win == num_lost):
			result = 'match'
			match_script = 'Match!You and Jandon have same score!'
			match_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=match_script_str)
			
		else:
			result = 'lost'
			if(lost_result > 1):
				player_img = Image.open('you.png')
				player_pic = player_img.resize((450,550),Image.ANTIALIAS)
				player_image = ImageTk.PhotoImage(player_pic)
				player_picture = canvas.create_image(w/2,h/2-200,image=player_image,anchor="nw")
				
				player_script_str = '\n'.join(lost_more_than_one_time_list_player)
				player_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=player_script_str)
				
				waithere_long()
				canvas.delete(player_script_str_text)
				canvas.delete(player_picture)
				
				Jandon_img = Image.open('jandon.png')
				Jandon_pic = Jandon_img.resize((450,550),Image.ANTIALIAS)
				Jandon_image = ImageTk.PhotoImage(Jandon_pic)
				Jandon_picture = canvas.create_image(10,h/2-200,image=Jandon_image,anchor="nw")
				
				Jandon_script_str = '\n'.join(win_more_than_one_time_list_jandon)
				Jandon_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=Jandon_script_str)
				
			else:
				player_img = Image.open('you.png')
				player_pic = player_img.resize((450,550),Image.ANTIALIAS)
				player_image = ImageTk.PhotoImage(player_pic)
				player_picture = canvas.create_image(w/2,h/2-200,image=player_image,anchor="nw")
				
				player_script_str = '\n'.join(lost_first_time_list_player)
				player_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=player_script_str)
				
				waithere_long()
				canvas.delete(player_script_str_text)
				canvas.delete(player_picture)
				
				Jandon_img = Image.open('jandon.png')
				Jandon_pic = Jandon_img.resize((450,550),Image.ANTIALIAS)
				Jandon_image = ImageTk.PhotoImage(Jandon_pic)
				Jandon_picture = canvas.create_image(10,h/2-200,image=Jandon_image,anchor="nw")
				
				Jandon_script_str = '\n'.join(win_first_time_list_jandon)
				Jandon_script_str_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=Jandon_script_str)
		
		
		
		
		def back_to_main():
			if(result == 'win'):
				current_result = 'Current round end, your score + 1'
			elif(result == 'lost'):
				current_result = 'Current round end, Jandon score + 1'
			else:
				current_result = 'Current round end, draw.'
			messagebox.showinfo('Round end',current_result)
			var2.set(1)
			destroy_page(competition_page)
			
		
		back_bt = Button(competition_page, text = "back",font='forte',command =back_to_main,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		back_window = canvas.create_window(w/2, h-80, anchor='n', window=back_bt)
		
		back_bt.wait_variable(var2)
		
		return result
	
	# 答题背景
	question_background_img = Image.open('question_background.jpg')
	question_bg = question_background_img.resize((750,500),Image.ANTIALIAS)
	question_background_image = ImageTk.PhotoImage(question_bg)
	canvas.create_image(0,0,image=question_background_image,anchor="nw")
	
	# load 题目
	global win_result
	global lost_result
	result = ask_question(type)
	if(result == 'win'):
		win_result = win_result + 1
	elif(result == 'lost'):
		lost_result = lost_result + 1
	else:
		print('draw')
	
	# if all competition is done, close competition window and display the ending
	if(wordbrain_done == True and reaction_done == True and country_done == True and language_done == True and math_done == True):
		if(win_result > lost_result):
			ending_result = 'win'
		elif(win_result < lost_result):
			ending_result = 'lost'
		else:
			ending_result = 'draw'
		waithere_short()
		destroy_page(competition_page)
		ending(ending_result)
	
	competition_page.grab_set()
	competition_page.resizable(False,False)
	competition_page.mainloop()

def already_compete(type):
	already_compete_text = 'You have already complete the competition on' + type
	messagebox.showinfo('Already complete',already_compete_text)

def wordbrain(event=None):
	global wordbrain_done
	if(wordbrain_done == False):
		wordbrain_done = True
		display_competition_rule('wordbrain')
	else:
		already_compete('wordbrain')

def reaction(event=None):
	global reaction_done
	if(reaction_done == False):
		reaction_done = True
		display_competition_rule('reaction')
	else:
		already_compete('reaction')
	

def country(event=None):
	global country_done
	if(country_done == False):
		country_done = True
		display_competition_rule('country')
	else:
		already_compete('country')

def math(event=None):
	global math_done
	if(math_done == False):
		math_done = True
		display_competition_rule('math')
	else:
		already_compete('math')

def language(event=None):
	global language_done
	if(language_done == False):
		language_done = True
		display_competition_rule('language')
	else:
		already_compete('language')

desc = Label(root,text="There are 5 different competition you can choose:",font = 'forte',fg = 'white',bg = 'black')

lab = Label(root,text="1. wordbrain",font = 'forte',fg = 'white',bg = 'black')

lab_2 = Label(root,text='2. reaction',font = 'forte',fg = 'white',bg = 'black')

lab_3 = Label(root,text='3. country',font = 'forte',fg = 'white',bg = 'black')

lab_4 = Label(root,text='4. math',font = 'forte',fg = 'white',bg = 'black')

lab_5 = Label(root,text='5. language',font = 'forte',fg = 'white',bg = 'black')

lab.bind("<Button-1>",wordbrain)
lab.bind("<Enter>",red_text)
lab.bind("<Leave>",black_text)

lab_2.bind("<Button-1>",reaction)
lab_2.bind("<Enter>",red_text_2)
lab_2.bind("<Leave>",black_text_2)

lab_3.bind("<Button-1>",country)
lab_3.bind("<Enter>",red_text_3)
lab_3.bind("<Leave>",black_text_3)

lab_4.bind("<Button-1>",math)
lab_4.bind("<Enter>",red_text_4)
lab_4.bind("<Leave>",black_text_4)

lab_5.bind("<Button-1>",language)
lab_5.bind("<Enter>",red_text_5)
lab_5.bind("<Leave>",black_text_5)

desc.grid(padx=15,pady=30)
lab.grid(pady=10)
lab_2.grid()
lab_3.grid(pady=10)
lab_4.grid()
lab_5.grid(pady=10)

def ending(ending_result):
	ending_page = Toplevel(root)
	ending_page.title(ending_result)
	w = 700
	h = 500
	canvas = Canvas(ending_page, width=w, height=h)
	canvas.pack(side = LEFT)
	
	ending_img = Image.open('applause.png')
	ending_bg = ending_img.resize((700,500),Image.ANTIALIAS)
	ending_image = ImageTk.PhotoImage(ending_bg)
	ending_display = canvas.create_image(0,0,image=ending_image,anchor="nw")
	
	ending_dialog_img = Image.open('dialog.png')
	ending_dialog_bg = ending_dialog_img.resize((600,200),Image.ANTIALIAS)
	ending_dialog_image = ImageTk.PhotoImage(ending_dialog_bg)
	dialog_ending_display = canvas.create_image(200,h-250,image=ending_dialog_image,anchor="nw")
	
	win_ending = False
	lost_ending = False
	win_ending_script = []
	lost_ending_script = []
	
	
	with open('ending.txt','rt') as ending_file:
		for line in ending_file:
			if(line == '[win ending]' and lost_ending == False):
				win_ending = True
				win_ending_script.append(line)
			if(line == '[lost ending]'):
				lost_ending = True
				lost_ending_script.append(line)
	
	
	if(ending_result == 'win'):
		canvas.create_text(w/2,h/2-130,fill="white",font=("Forte",15),text=win_ending_script,width = 500)
	elif(ending_result == 'lost'):
		canvas.create_text(w/2,h/2-130,fill="white",font=("Forte",15),text=lost_ending_script,width = 500)
	else:
		draw_text = 'You and Jandon have the same scores in the competition,\n' + 'and Jandon give this class rep to you.\n' + 'Jandon: It is first time that I have draw with others.\n Keep your hardworking\n next time I will win!'
		canvas.create_text(w/2,h/2-130,fill="white",font=("Forte",15),text=draw_text,width = 500)
	
	def end_game():
		messagebox.showinfo('ENDING','Thanks for playing Back To School!')
		destroy_page(root)
	
	ending_bt = Button(ending_page, text = "QUIT",font='forte',command =end_game,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
	ending_window = canvas.create_window(w/2, h-100, anchor='n', window=ending_bt)
				

root.mainloop()


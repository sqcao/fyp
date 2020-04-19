from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import pygame
import sys
import time
import random




# game init
energy = 10
HP = 5
player_pos = [1,1]
item = {'boat':0}
first_meet_river_god = True

i = 1

global visited_display_list
visited_display_list = []

smell_display_list = []



# ==========================================================================

# introduction page
root = Tk()
root.title("Dark Forest")
# width and height for the main introduction page
w = 450
h = 600
# in order to use the background image, use canvas in the root page
canvas = Canvas(root, width=w, height=h)
canvas.pack(side = LEFT)
background_img = Image.open('bg2.jpg')
bg = background_img.resize((450,600),Image.ANTIALIAS)
bg_img = ImageTk.PhotoImage(bg)
canvas.create_image(0,0,image=bg_img,anchor="nw")
root.resizable(False,False)


# color chart
light_blue = '#00ffff'
light_red = '#ff3333'
light_green = '#33ff33'

current_level = 1



		
def destroy_page(page):
	page.destroy()
	
	

def continue_game(event=None):
	# 创建一个新的界面，然后显示游戏规则
	game_page = Toplevel(root)
	game_page.title("Dark Forest")
	w = 450
	h = 600
	
	canvas = Canvas(game_page,width=w, height=h)
	canvas.pack(side = LEFT)
	
	background_img_2 = Image.open('bg2.jpg')
	bg_2 = background_img_2.resize((450,600),Image.ANTIALIAS)
	bg_img_2 = ImageTk.PhotoImage(bg_2)
	canvas.create_image(0,0,image=bg_img_2,anchor="nw")
	game_page.resizable(False,False)
	
	
	
	
	global intro_text
	global start_text
	canvas.unbind("<Button-1>")
	
	intro_file = open('intro.txt','r')
	intro = intro_file.read()
	intro_file.close()
	intro_text = canvas.create_text(w/2,h/2-50,fill="white",font=("Forte",15),text=intro,width=380)
	
	
	
	def start_game(event=None):
		# 删除游戏简介，显示第一关
		canvas.delete(intro_text)
		canvas.delete(start_text)
		canvas.unbind("<Button-1>")
		
		def display_smell():
			global smell_display_list
			
			try:
				for smell_display in smell_display_list:
					canvas.delete(smell_display)
			except NameError:
					print('smell_display not exist')
									
			if(current_level == 3):
				for dinasour in dinasour_pos:
					if(abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) <= 1 ):
						smell_text = 'I can feel that the dinasour is just beside me...'
						smell_display = canvas.create_text(w/2,h/2+130,fill="white",font=("Forte",15),text=smell_text,width=380)
						break
					
					elif(abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) == 2 ):
						smell_text = 'The disgusting stench grew stronger as you approach forward...'
						smell_display = canvas.create_text(w/2,h/2+130,fill="white",font=("Forte",15),text=smell_text,width=380)
						break
					
					elif(abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) > 2 and abs(player_pos[0] - dinasour[0]) + abs(player_pos[1] - dinasour[1]) <= 4  ):
						smell_text = 'A strange stench comes from far away...'
						smell_display = canvas.create_text(w/2,h/2+130,fill="white",font=("Forte",15),text=smell_text,width=380)
						break
			
			else:
				if(abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) <= 1 ):
					smell_text = 'I can feel that the dinasour is just beside me...'
					smell_display = canvas.create_text(w/2,h/2+130,fill="white",font=("Forte",15),text=smell_text,width=380)
				
				elif(abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) == 2 ):
					smell_text = 'The disgusting stench grew stronger as you approach forward...'
					smell_display = canvas.create_text(w/2,h/2+130,fill="white",font=("Forte",15),text=smell_text,width=380)
				
				elif(abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) > 2 and abs(player_pos[0] - dinasour_pos[0]) + abs(player_pos[1] - dinasour_pos[1]) <= 4  ):
					smell_text = 'A strange stench comes from far away...'
					smell_display = canvas.create_text(w/2,h/2+130,fill="white",font=("Forte",15),text=smell_text,width=380)
			try:
				smell_display_list.append(smell_display)
			except UnboundLocalError:
				print('smell_display not displayed yet.')
		
		def clear_meet_item():
			try:
				canvas.delete(get_key_display)
			except NameError:
				 print('get_key_display not exist')
			
			try:
				canvas.delete(get_lotus_display)
			except NameError:
				print('get_lotus_display not exist')
			
			try:
				canvas.delete(meet_dinasour_display)
			except NameError:
				print('meet_dinasour_display not exist')
				
			try:
				canvas.delete(meet_fruit_tree_display)
			except NameError:
				print('meet_fruit_tree_display not exist')
			
			try:
				canvas.delete(meet_broken_tree_display)
			except NameError:
				print('meet_broken_tree_display not exist')
			
			try:
				canvas.delete(meet_overwatch_tree_display)
			except NameError:
				print('meet_overwatch_tree_display not exist')
			
		
		def get_key():
			global get_key_display
			# clear_meet_item()
			get_key_text = 'Congradulation! You get the key!'
			get_key_display = canvas.create_text(w/2,h/2+200,fill="white",font=("Forte",15),text=get_key_text,width=380)
			game_over('key')
		
		def meet_lotus():
			# clear_meet_item()
			global HP
			global get_lotus_display
			global lotus_pos
			
			if(current_level == 3):
				if(len(lotus_pos) == 2):
					lotus_pos.remove(player_pos)
				else:
					lotus_pos = [0,0]
			else:
				lotus_pos = [0,0]
			
			get_lotus_text = 'You get a lotus, lotus recover life + 5.'
			get_lotus_display = canvas.create_text(w/2,h/2+170,fill="white",font=("Forte",15),text=get_lotus_text,width=380)
			HP = HP + 5
		
		def meet_dinasour():
			# clear_meet_item()
			global HP
			global dinasour_pos
			global meet_dinasour_display
			if(current_level == 3):
				dinasour_pos.remove(player_pos)
			else:
				dinasour_pos = [-10,-10]
			meet_dinasour_text = 'You meet a dinasour! The dinasour attacks you, HP-5!'
			meet_dinasour_display = canvas.create_text(w/2,h/2+160,fill="white",font=("Forte",15),text=meet_dinasour_text,width=380)
			HP = HP - 5
		
		def meet_tree(tree_type):
			global energy
			global overwatch_tree_pos
			global fruit_tree_pos
			global broken_tree_pos
			
			if(tree_type == 'fruit'):
				fruit_tree_pos.remove(player_pos)
			elif(tree_type == 'broken'):
				broken_tree_pos.remove(player_pos)
			else:
				overwatch_tree_pos.remove(player_pos)
			
			choice = messagebox.askyesno('meet huge tree','There is a huge tree in front of you, do you want to climb it or walk away? (climb tree will cost 1 energy.)',parent = game_page)
			if(choice == False):
				messagebox.showinfo('walk away','You walk away...',parent = game_page)
			else:
				energy -= 1
				if(tree_type == 'fruit'):
					meet_fruit_tree()
				elif(tree_type == 'broken'):
					meet_broken_tree()
				else:
					meet_overwatch_tree()
			
		
		def meet_broken_tree():
			global HP
			messagebox.showinfo('you fall down','The tree is broken! You fall down from the tree! HP -1',parent = game_page)
			HP = HP - 1
		
		def meet_fruit_tree():
			global energy
			messagebox.showinfo('found a fruit','You found a fruit on the tree! You eat the fruit. Energy +5',parent = game_page)
			energy = energy + 5
		
		def over_watch(direction_view):
			view = {'tree':0,'dinasour':0,'lotus':0,'key':0}
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
					if(dinasour_pos[0] == player_pos[0] and dinasour_pos[1] < player_pos[1]):
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
			messagebox.showinfo('watch result',view,parent = game_page)
		
		def meet_overwatch_tree():
			# watch_direction = messagebox.askquestion('choose direction','ou are standing on top of the tree, and you can choose one direction to see what is there. Which direction you wish to see? (up/down/left/right)',parent = game_page)
			watch_direction = simpledialog.askstring(title = 'Choose view direction',prompt='up/down/left/right',parent = game_page)
			if(watch_direction == 'up'):
				over_watch('up')
			elif(watch_direction == 'down'):
				over_watch('down')
			elif(watch_direction == 'left'):
				over_watch('left')
			elif(watch_direction == 'right'):
				over_watch('right')
			else:
				messagebox.showinfo('error','invalid choice.')
				meet_overwatch_tree()
		
		def meet_river_god():
			global item
			global fruit_tree_pos
			global overwatch_tree_pos
			global broken_tree_pos
			
			messagebox.showinfo('River God','You have met the god of river!',parent = game_page)
			messagebox.showinfo('River God','God of river: I can satisfy one of your dream, just tell me what you want.',parent = game_page)
			
			prompt_text = '1.I want to have lots of food to recover energy!\n2.I want to light up the dark forest!\n3.I am fine, I don\'t need anything!'
			wish = simpledialog.askstring(title = 'Choose a wish',prompt=prompt_text,parent = game_page)
			
				
			# all the trees becomes fruit tree
			if(wish == '1'):
				messagebox.showinfo('endless fruits','God of river: As you wish,\n I already make all the trees in the forest full of fruit!\n You can enjoy endless fruits!',parent = game_page)
				messagebox.showinfo('endless fruits','All the trees in the forest becomes fruit tree!',parent = game_page)
				fruit_tree_pos = fruit_tree_pos + overwatch_tree_pos + broken_tree_pos
				del overwatch_tree_pos[:]
				del broken_tree_pos[:]
			elif(wish == '2'):
				messagebox.showinfo('light up forest','God of river: As you wish, I will light up the forest!',parent = game_page)
				
				# what is left in the forest
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
				
				light_up_text = 'A huge thunder suddenly appear in the sky,\n the whole forest has been light up at that moment!\nfruit tree: ' + str(fruit_tree_num) + '\nbroken tree: ' + str(broken_tree_num) + '\noverwatch tree: ' + str(overwatch_tree_num) + '\nlotus: ' + str(lotus_num) + '\ndinasour: ' + str(dinasour_num)
				
				messagebox.showinfo('light up forest',light_up_text,parent = game_page)
				messagebox.showinfo('tree been shocked','Wait, but the thunder is so powerful\n that some trees in the forest has been shocked and fall down!',parent = game_page)
				
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
				messagebox.showinfo('no wish','God of river: Oh! You don\'t have any wish from me!\n I am so touched, hardly have a people like you!\n I want to cry!\nGod of river give you two boat.',parent = game_page)
				messagebox.showinfo('get boat','You get two boat. (boat only last for one ride, after one ride the boat will be damaged.)',parent = game_page)
				# a boat can save your extra energy in river
				item['boat'] = 2
			else:
				messagebox.showinfo('error','Invalid choice! please enter again!',parent = game_page)
				meet_river_god()
		
		def meet_river():
			global first_meet_river_god
			global item
			global energy
			
			if(first_meet_river_god == True):
				meet_river_god()
				first_meet_river_god = False
			
			# check if have boat
			if(item['boat']==2):
				messagebox.showinfo('cross river','You use a boat to cross the river, no energy cost.',parent = game_page)
				item['boat'] = 1
				# recover the consumed energy by move action
				energy += 1
			elif(item['boat']==1):
				messagebox.showinfo('cross river','You use a boat to cross the river, no energy cost.',parent = game_page)
				item['boat'] = 0
				energy += 1
			elif(item['boat']==0):
				messagebox.showinfo('cross river','No boat to use, extra 1 energy cost.',parent = game_page)
				energy -= 1
		
		def display_energy_HP():
			global energy_display
			global HP_display
			energy_text = 'energy: [' + str(energy) + ']'
			HP_text = 'HP: [' + str(HP) + ']'
			
			energy_display = canvas.create_text(w/2+100,20,fill="black",font=("Forte",20),text=energy_text,width=380)
			HP_display = canvas.create_text(w/2-100,20,fill="black",font=("Forte",20),text=HP_text,width=380)
		
		def clear_current_level():
			# clear the board
			canvas.delete(board_display)
			# clear the energy_display
			canvas.delete(energy_display)
			# clear the HP_display
			canvas.delete(HP_display)
			# clear the character_display
			canvas.delete(character_display)
			# clear all directions button
			canvas.delete(up_window)
			canvas.delete(down_window)
			canvas.delete(left_window)
			canvas.delete(right_window)
			
		
		def game_over(reason):
			global over_pic
			global over_display
			global restart_window
			clear_current_level()
			# use a escape background image to cover the game background_img
			over_img = Image.open('escape.png')
			over = over_img.resize((450,600),Image.ANTIALIAS)
			over_image = ImageTk.PhotoImage(over)
			over_pic = canvas.create_image(0,0,image=over_image,anchor="nw")
			# if one level is completed, clear the whole screen 
			if(reason == 'energy'):
				over_text = 'You fail to escape from the dark forest, your energy has been run out...'
			elif(reason == 'HP'):
				over_text = 'You fail to escape from the dark forest, you get killed...'
			elif(reason == 'key'):
				over_text = 'You have successfully escape from the dark forest!'
			over_display = canvas.create_text(w/2,h/2,fill="white",font=("Forte",20),text=over_text,width=380)
			
			def go_next_level():
				global current_level
				# delete the game over background
				canvas.delete(over_pic)
				canvas.delete(over_display)
				for footprint in visited_display_list:
					canvas.delete(footprint)
				del visited_display_list[:]
				try:
					canvas.delete(next_window)
				except NameError:
					print('next level button is not exist')
				try:
					canvas.delete(restart_window)
				except NameError:
					print('restart button is not exist')
				canvas.delete(get_key_display)
				if(current_level == 1):
					current_level = 2
					display_level_2()
				elif(current_level == 2):
					current_level = 3
					display_level_3()
				elif(current_level == 3):
					end_page = Toplevel(game_page)
					end_page.title("Thanks for playing")
					w = 550
					h = 500
					
					canvas_2 = Canvas(end_page,width=w, height=h)
					canvas_2.pack(side = LEFT)
					end_page.resizable(False,False)
					
					end_img = Image.open('end.jpg')
					end = end_img.resize((550,500),Image.ANTIALIAS)
					end_image = ImageTk.PhotoImage(end)
					end_pic = canvas_2.create_image(0,0,image=end_image,anchor="nw")
					
					end_text = 'Follow the light in your heart, and you will escape from the dark forest...'
					canvas_2.create_text(w/2,h/2,fill="white",font=("Forte",20),text=end_text,width=380)
					
					def exit():
						destroy_page(root)
					
					exit_bt = Button(end_page, text = "exit",font='forte',command = exit,anchor = 'nw',width = 7,bg=light_green,activebackground = light_green)
					exit_window = canvas_2.create_window(w/2, h/2+100, anchor='c', window=exit_bt)
					
					end_page.grab_set()
					end_page.mainloop()
			
			def restart_game():
				global visited_display_list
				for footprint in visited_display_list:
					canvas.delete(footprint)
				del visited_display_list[:]
				
				global first_meet_river_god
				first_meet_river_god = True
				global item
				item['boat'] = 0
				global energy
				global HP
				global player_pos
				energy = 10
				HP = 5
				player_pos = [1,1]
				canvas.delete(over_pic)
				canvas.delete(over_display)
				canvas.delete(restart_window)
				if(current_level == 1):
					display_level_1()
				elif(current_level == 2):
					display_level_2()
				else:
					display_level_3()
			if(reason == 'key'):
				if(current_level == 3):
					end_bt = Button(game_page, text = "end",font='forte',command = go_next_level,anchor = 'nw',width = 10,bg=light_green,activebackground = light_green)
					next_window = canvas.create_window(w/2, h/2+100, anchor='c', window=end_bt)
				else:
					next_bt = Button(game_page, text = "next level",font='forte',command = go_next_level,anchor = 'nw',width = 10,bg=light_green,activebackground = light_green)
					next_window = canvas.create_window(w/2, h/2+100, anchor='c', window=next_bt)
			else:
				restart_bt = Button(game_page, text = "restart",font='forte',command = restart_game,anchor = 'nw',width = 10,bg=light_green,activebackground = light_green)
				restart_window = canvas.create_window(w/2, h/2+100, anchor='c', window=restart_bt)
			
			game_page.mainloop()
		

		def check_meeting():
			if(current_level == 1):
				if(player_pos == lotus_pos):
					meet_lotus()
				elif(player_pos == dinasour_pos):
					meet_dinasour()
				elif(player_pos == key_pos):
					get_key()
			elif(current_level == 2):
				if(player_pos == lotus_pos):
					meet_lotus()
				elif(player_pos == dinasour_pos):
					meet_dinasour()
				elif(player_pos == key_pos):
					get_key()
				elif(player_pos in fruit_tree_pos):
					meet_tree('fruit')
				elif(player_pos in broken_tree_pos):
					meet_tree('broken')
				elif(player_pos in overwatch_tree_pos):
					meet_tree('overwatch')
			elif(current_level == 3):
				if(player_pos in lotus_pos):
					meet_lotus()
				elif(player_pos in dinasour_pos):
					meet_dinasour()
				elif(player_pos == key_pos):
					get_key()
				elif(player_pos in fruit_tree_pos):
					meet_tree('fruit')
				elif(player_pos in broken_tree_pos):
					meet_tree('broken')
				elif(player_pos in overwatch_tree_pos):
					meet_tree('overwatch')
				elif(player_pos in river_pos):
					meet_river()
				
		
		
		def move(direction):
			global i 
			i += 1
			try:
				clear_meet_item()
			except NameError:
				print('no meet item display exist')
			
			try:
				canvas.delete(energy_display)
			except NameError:
				print('energy_display not exist yet.')
			
			try:
				canvas.delete(HP_display)
			except NameError:
				print('HP_display not exist yet.')
			
			try:
				for smell_display in smell_display_list:
					canvas.delete(smell_display)
					del smell_display_list[:]
			except NameError:
				print('smell_display not exist yet.')
			
			
			# before move, need to mark current position
			if(current_level == 1):
				foot_size = 60
			elif(current_level == 2):
				foot_size = 45
			else:
				foot_size = 30
			current_pos = canvas.coords(character_display)
			visited_img = Image.open('visited.png')
			visited_pic = visited_img.resize((foot_size,foot_size),Image.ANTIALIAS)
			visited_image = ImageTk.PhotoImage(visited_pic)
			visited_display = canvas.create_image(current_pos[0],current_pos[1],image=visited_image,anchor="nw")
			visited_display_list.append(visited_display)
			
			print('before move action, back to here, no',i)
			
			if(current_level == 1):
				lower_bound = 4
				right_bound = 4
				shift = 90
			elif(current_level == 2):
				lower_bound = 6
				right_bound = 6
				shift = 60
			else:
				lower_bound = 8
				right_bound = 8
				shift = 45
			
			if(direction == 'up'):
				if(player_pos[0] == 1):
					messagebox.showinfo('error','cannot go up.',parent=game_page)
				else:
					move_up(shift)
					display_smell()
			elif(direction == 'down'):
				if(player_pos[0] == lower_bound):
					messagebox.showinfo('error','cannot go down.',parent=game_page)
				else:
					move_down(shift)
					display_smell()
			elif(direction == 'left'):
				if(player_pos[1] == 1):
					messagebox.showinfo('error','cannot go left.',parent=game_page)
				else:
					move_left(shift)
					display_smell()
			elif(direction == 'right'):
				if(player_pos[1] == right_bound):
					messagebox.showinfo('error','cannot go right.',parent=game_page)
				else:
					move_right(shift)
					display_smell()
			
			print('after move action, back to here')


			display_energy_HP()
			if(energy == 0):
				game_over('energy')
			elif(HP == 0):
				game_over('HP')
			
			# for display_smell in display_smell_list:
				# canvas.delete(display_smell)
			
			
			game_page.mainloop()
		
		def move_up(shift):
			global player_pos
			player_pos[0] -= 1
			global energy
			energy -= 1
			global press
			press = True
			
			canvas.move(character_display,0,-shift)
			check_meeting()
		
		def move_down(shift):
			global player_pos
			player_pos[0] += 1
			global energy
			energy -= 1
			global press
			press = True
			
			canvas.move(character_display,0,shift)
			check_meeting()

			
		
		def move_left(shift):
			global player_pos
			player_pos[1] -= 1
			global energy
			energy -= 1
			global press
			press = True
			
			canvas.move(character_display,-shift,0)
			check_meeting()
		
		def move_right(shift):
			global player_pos
			player_pos[1] += 1
			global energy
			energy -= 1
			global press
			press = True
			
			canvas.move(character_display,shift,0)
			check_meeting()
		
		
		def display_level_1():
			global dinasour_pos
			global lotus_pos
			global key_pos
			
			global board_display
			global character_display
			
			global up_window
			global down_window
			global left_window
			global right_window

			dinasour_pos = [2,3]
			key_pos = [4,4]
			lotus_pos = [2,2]
			
			# 在loop之前先显示board, HP and energy， 以及皮卡丘
			board_img = Image.open('board.png')
			board_pic = board_img.resize((360,360),Image.ANTIALIAS)
			board_image = ImageTk.PhotoImage(board_pic)
			board_display = canvas.create_image(w/2-175,h/2-250,image=board_image,anchor="nw")
			
			display_energy_HP()
			display_smell()
			
			character_img = Image.open('character1.png')
			character_pic = character_img.resize((80,80),Image.ANTIALIAS)
			character_image = ImageTk.PhotoImage(character_pic)
			character_display = canvas.create_image(w/2-170,h/2-245,image=character_image,anchor="nw")
			

			
			up_bt = Button(game_page, text = "up",font='forte',command = lambda: move('up'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			up_window = canvas.create_window(w/2, h-100, anchor='c', window=up_bt)
			
			down_bt = Button(game_page, text = "down",font='forte',command = lambda: move('down'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			down_window = canvas.create_window(w/2, h-20, anchor='c', window=down_bt)
			
			left_bt = Button(game_page, text = "left",font='forte',command = lambda: move('left'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			left_window = canvas.create_window(w/2-50, h-60, anchor='c', window=left_bt)
			
			right_bt = Button(game_page, text = "right",font='forte',command = lambda: move('right'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			right_window = canvas.create_window(w/2+50, h-60, anchor='c', window=right_bt)

			game_page.mainloop()
				
			
				
			
		
		def display_level_2():
			global energy
			global HP
			global player_pos
			player_pos = [1,1]
			HP = 5
			energy = 10
			global board_display
			global character_display
			
			global up_window
			global down_window
			global left_window
			global right_window

			global lotus_pos
			global dinasour_pos
			global key_pos
			global broken_tree_pos
			global overwatch_tree_pos
			global fruit_tree_pos
			
			lotus_pos = [3,2]
			dinasour_pos = [5,5]
			key_pos = [5,6]
			broken_tree_pos = [[2,1],[2,4]]
			overwatch_tree_pos = [[5,2],[3,3],[4,4]]
			fruit_tree_pos = [[2,3],[6,3],[3,5],[2,6]]
			
			# 在loop之前先显示board, HP and energy， 以及皮卡丘
			board_img = Image.open('board2.png')
			board_pic = board_img.resize((360,360),Image.ANTIALIAS)
			board_image = ImageTk.PhotoImage(board_pic)
			board_display = canvas.create_image(w/2-175,h/2-250,image=board_image,anchor="nw")
			
			display_energy_HP()
			display_smell()
			
			character_img = Image.open('character1.png')
			character_pic = character_img.resize((50,50),Image.ANTIALIAS)
			character_image = ImageTk.PhotoImage(character_pic)
			character_display = canvas.create_image(w/2-170,h/2-245,image=character_image,anchor="nw")
			

			
			up_bt = Button(game_page, text = "up",font='forte',command = lambda: move('up'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			up_window = canvas.create_window(w/2, h-100, anchor='c', window=up_bt)
			
			down_bt = Button(game_page, text = "down",font='forte',command = lambda: move('down'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			down_window = canvas.create_window(w/2, h-20, anchor='c', window=down_bt)
			
			left_bt = Button(game_page, text = "left",font='forte',command = lambda: move('left'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			left_window = canvas.create_window(w/2-50, h-60, anchor='c', window=left_bt)
			
			right_bt = Button(game_page, text = "right",font='forte',command = lambda: move('right'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			right_window = canvas.create_window(w/2+50, h-60, anchor='c', window=right_bt)

			game_page.mainloop()
		
		
		def display_level_3():
			global energy
			global HP
			global player_pos
			player_pos = [1,1]
			HP = 5
			energy = 10
			
			global board_display
			global character_display
			
			global up_window
			global down_window
			global left_window
			global right_window

			global dinasour_pos
			global key_pos
			global lotus_pos
			global overwatch_tree_pos
			global broken_tree_pos
			global fruit_tree_pos
			global river_pos
			
			dinasour_pos = [[3,4],[6,8]]
			key_pos = [7,6]
			lotus_pos = [[3,5],[5,7]]
			overwatch_tree_pos = [[3,3],[6,6],[2,8]]
			broken_tree_pos = [[2,2],[2,6],[8,8]]
			fruit_tree_pos = [[3,2],[2,3],[2,4],[1,5],[1,8],[5,3],[6,1],[6,5],[8,5],[7,8]]
			
			river_pos = [[7,1],[7,2],[7,3],[7,4],[6,4],[5,4],[4,4],[4,5],[5,5],[4,6],[3,6],[3,7],[3,8]]
			
			# 在loop之前先显示board, HP and energy， 以及皮卡丘
			board_img = Image.open('board3.png')
			board_pic = board_img.resize((360,360),Image.ANTIALIAS)
			board_image = ImageTk.PhotoImage(board_pic)
			board_display = canvas.create_image(w/2-175,h/2-250,image=board_image,anchor="nw")
			
			# display the river on the map
			river_img = Image.open('river.png')
			river_pic = river_img.resize((30,30),Image.ANTIALIAS)
			river_image = ImageTk.PhotoImage(river_pic)
			river1_display = canvas.create_image(w/2-170,h/2-245+6*45,image=river_image,anchor="nw")
			river2_display = canvas.create_image(w/2-170+45,h/2-245+6*45,image=river_image,anchor="nw")
			river3_display = canvas.create_image(w/2-170+45*2,h/2-245+6*45,image=river_image,anchor="nw")
			river4_display = canvas.create_image(w/2-170+45*3,h/2-245+6*45,image=river_image,anchor="nw")
			river5_display = canvas.create_image(w/2-170+45*3,h/2-245+5*45,image=river_image,anchor="nw")
			river6_display = canvas.create_image(w/2-170+45*3,h/2-245+4*45,image=river_image,anchor="nw")
			river7_display = canvas.create_image(w/2-170+45*3,h/2-245+3*45,image=river_image,anchor="nw")
			river8_display = canvas.create_image(w/2-170+45*4,h/2-245+3*45,image=river_image,anchor="nw")
			river9_display = canvas.create_image(w/2-170+45*4,h/2-245+4*45,image=river_image,anchor="nw")
			river10_display = canvas.create_image(w/2-170+45*5,h/2-245+3*45,image=river_image,anchor="nw")
			river11_display = canvas.create_image(w/2-170+45*5,h/2-245+2*45,image=river_image,anchor="nw")
			river12_display = canvas.create_image(w/2-170+45*6,h/2-245+2*45,image=river_image,anchor="nw")
			river13_display = canvas.create_image(w/2-170+45*7,h/2-245+2*45,image=river_image,anchor="nw")
			
			display_energy_HP()
			display_smell()
			
			character_img = Image.open('character1.png')
			character_pic = character_img.resize((30,30),Image.ANTIALIAS)
			character_image = ImageTk.PhotoImage(character_pic)
			character_display = canvas.create_image(w/2-170,h/2-245,image=character_image,anchor="nw")
			

			
			up_bt = Button(game_page, text = "up",font='forte',command = lambda: move('up'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			up_window = canvas.create_window(w/2, h-100, anchor='c', window=up_bt)
			
			down_bt = Button(game_page, text = "down",font='forte',command = lambda: move('down'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			down_window = canvas.create_window(w/2, h-20, anchor='c', window=down_bt)
			
			left_bt = Button(game_page, text = "left",font='forte',command = lambda: move('left'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			left_window = canvas.create_window(w/2-50, h-60, anchor='c', window=left_bt)
			
			right_bt = Button(game_page, text = "right",font='forte',command = lambda: move('right'),anchor = 'nw',width = 6,bg=light_green,activebackground = light_green)
			right_window = canvas.create_window(w/2+50, h-60, anchor='c', window=right_bt)

			game_page.mainloop()
		
		
		if(current_level == 1):
			display_level_1()
		
		
	
	start_text = canvas.create_text(w/2+100,h/2+250,fill="white",font=("Forte",15),text='Click to start...')
	# 看完游戏规则之后，Click 界面进入游戏
	canvas.bind("<Button-1>", start_game)
	
	game_page.mainloop()
	

def waithere_long():
	var = IntVar()
	root.after(1500, var.set, 1)
	print("loading...")
	root.wait_variable(var)
	


title = canvas.create_text(w/2,h/2-50,fill="black",font=("Forte",55),text='Dark Forest')
waithere_long()
proceed_text = canvas.create_text(w/2+100,h/2+150,fill="black",font=("Forte",15),text='Click to proceed...')
canvas.bind("<Button-1>", continue_game)




root.mainloop()
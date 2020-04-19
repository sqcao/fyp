from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import pygame
import time
import random

#===================================tkinter page==================================
game_pygame = False
# when user press EXIT at the introduction page, the pygame window will not be executed
game = True
# this start_player will be set in tkinter page and used by pygame portion
start_player = ''

# introduction page
root = Tk()
root.title("Rover Diary")
# width and height for the main introduction page
w = 840
h = 480
# in order to use the background image, use canvas in the root page
canvas = Canvas(root, width=w, height=h)
canvas.pack(side = LEFT)
background_img = Image.open('bg1.jpg')
bg = background_img.resize((840,480),Image.ANTIALIAS)
bg_img = ImageTk.PhotoImage(bg)

canvas.create_image(0,0,image=bg_img,anchor="nw")
root.resizable(False,False)

# color chart
light_blue = '#00ffff'
light_red = '#ff3333'
light_green = '#33ff33'

canvas.create_text(w/2,h/2-50,fill="black",font=("Forte",55),text='Rover Diary')


# ===============================all global attributes==================================

# 小白的特效，每次探索必获得资源
full_explore_list = ['$1','$2','unknown fruit','wormwood','flax','healing grass','wood']
# 默认的，有几率探索不到任何资源
not_full_explore_list = ['$1','$2','unknown fruit','','wormwood','flax','healing grass','','wood']

food_dict = {'unknown fruit':0,'bbq meat':0}

medicine_dict = {'healing grass':0,'magic medicine':0}

manufacture_resouces_dict = {'wormwood':0,'flax':0,'wood':0,'raw meat':0}

food_list = list(food_dict.keys())
medicine_list = list(medicine_dict.keys())
manufacture_resouces_list = list(manufacture_resouces_dict.keys())

# price tag
price_tag = {'unknown fruit':3,'bbq meat':8,'healing grass':5,'magic medicine':10,'wood':1,'flax':2,'raw meat':2,'wormwood':2}

# 探索的过程中可能会触发战斗
# 战斗随着时间变化而增加难度

normal_reward = ['raw meat','unknown fruit','healing grass']
# magic blade can increase crit chance by 5,lucky ring can increase defend chance by 5
challenge_reward = ['magic blade','lucky ring','magic medicine','bbq meat']

normal_enermy = ['crazy dog','rogue','snake']
special_enermy = ['thief','cat']
# 挑战怪物每十天出现一次，挑战成功会有稀有奖励
challenge_enermy = ['shadow','killer']




# 每十天提升一次怪物等级
# 普通怪物
level = 1

normal_enermy_HP = {'crazy dog':45*level,'rogue':80*level,'snake':60*level}
normal_enermy_attack = {'crazy dog':15*level,'rogue':15*level,'snake':20*level}
normal_enermy_desc = {'crazy dog':'A crazy dog is chased after you!!!','rogue':'A rogue stops you and want to take your money!!!','snake':'A snake is going to attack you at the back!!!'}

# 特殊怪物
# 小偷没有攻击力，但是每次攻击会偷取你0.1金币
# 流浪猫，没有攻击力，每次攻击有几率偷取食物，如果没有食物它就会逃跑
special_enermy_HP = {'thief':50*level,'cat':50*level}
special_enermy_attack = {'thief':0,'cat':0}
special_enermy_desc = {'thief':'A thief is going to steal your money but you notice him already...','cat':'A homeless cat is staring you at the corner...'}

# 挑战怪物
challenge_enermy_HP = {'shadow':150*level,'killer':100*level}
challenge_enermy_attack = {'shadow':50,'killer':80}
challenge_enermy_desc = {'shadow':'A man standing in the shadow, it\'s too dark to see his face...','killer':'You discover a killer is aiming at a innocent girl...'}


# 所有制造用品， 木头，亚麻，生肉和 艾草，也标记为全局变量
wood = 0
flax = 0
raw_meat = 0
wormwood = 0


# 游戏初始化
enermy_HP = 0
enermy_attack = 0
explore_list = not_full_explore_list

# 初始，生命值30，血量50，精力50，饥饿100，攻击力10，防御力0，金币10
life = 30
player_HP = 50
max_player_HP = 50
energy = 50
max_energy = 50
hungry = 100
max_hungry = 100
attack = 20
defence = 0
crit_chance = 0
defend_chance = 0
money = 10
trap_number = 0
# 游戏从第一天开始
day = 1

# 富二代角色属性，每天获得金币
money_increase = False


# 制造等级以及物品属性，所需材料
# 所需材料和物品属性随着制造等级提升

# 木剑，增加攻击力，可触发暴击2% （需要木头）
wood_sword_level = 0
attack_increase = [0,10,15,20,25,30,35,40,45,50,55]
trigger_crit = [0,0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2]
sword_need_wood = [3,6,9,12,15,18,21,24,27,30]	# up to level 10

# 帐篷，增加精力上限 （需要木头和亚麻）
tent_level = 0
max_energy_increase = [10,20,30,40,50,60,70,80,90,100]
tent_need_wood = [2,4,6,8,10,12,14,16,18,20]
tent_need_flax = [6,10,14,18,22,26,30,34,38,42]

# 制造神奇药水 （需要艾草）
magic_medicine_need_wormwood = 2

# 制造烤肉 （需要生肉和木头）
meat_need_raw = 1
meat_need_wood = 1

# 亚麻布衣，增加生命上限，可触发格挡2%
flax_clothing_level = 0
HP_increase = [0,30,60,90,120,150,180,210,240,270,300]
trigger_defend = [0,0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2]
flax_clothing_need_flax = [6,10,14,18,22,26,30,34,38,42]

# 陷阱，睡觉时有几率获得资源，获得数量随着等级提升
trap_level = 0
trap_get_item_num = [0,1,2,3,4,5,6,7,8,9,10]
trap_chance = 0.3
trap_need_wood = [4,8,12,16,20,24,28,32,36,40]

# 篝火，睡觉后恢复生命值， 恢复数值随着等级提升
bonfire_level = 0
sleep_recover_HP = [0,20,30,40,50,60,70,80,90,100,110]
bonfire_need_wood = [10,15,20,25,30,35,40,45,50,55]



# use to destroy all kinds of toplevel pages
def destroy_page(page):
	page.destroy()

def waithere_long():
	var = IntVar()
	root.after(4000, var.set, 1)
	print("waiting...")
	root.wait_variable(var)

def waithere_short():
	var = IntVar()
	root.after(1500, var.set, 1)
	print("waiting...")
	root.wait_variable(var)

def background_intro():
	game_background_page = Toplevel(root)
	game_background_page.title("Rover Diary")
	w = 500
	h = 500
	
	
	canvas = Canvas(game_background_page, bg="black",width=w, height=h)
	canvas.pack(side = LEFT)
	bg_intro_1 = 'After yesterday argument with dad, \nI run out of home...'
	bg_intro_2 = 'I had enough with him already!'
	bg_intro_3 = 'I want to prove to everyone!\nI will be the greatest man in the world!'
	canvas.create_text(w/2-15,h/2-60,fill="grey",font=("Forte",15),text=bg_intro_1)
	waithere_short()
	canvas.create_text(w/2-32,h/2,fill="grey",font=("Forte",15),text=bg_intro_2)
	waithere_short()
	canvas.create_text(w/2,h/2+60,fill="grey",font=("Forte",15),text=bg_intro_3)
	waithere_short()
	canvas.create_text(w/2+100,h/2+180,fill="white",font=("Forte",15),text='Click the screen to continue...')
	
	def continue_game(event=None):
		destroy_page(game_background_page)
		gameloop()
	
	canvas.bind("<Button-1>", continue_game)
	
	game_background_page.mainloop()



	

# 选完角色，开始游戏循环
def gameloop():
	game_page = Toplevel(root)
	game_page.title("Rover Diary")
	w = 550
	h = 600
	
	canvas = Canvas(game_page, bg="black",width=w, height=h)
	canvas.pack(side = LEFT)
	
	def fight(enermy_choose,enermy_info_HP,enermy_info_attack,meet_enermy_page):
		global attack
		global defence
		global your_HP_text
		global monster_HP_text
		
		destroy_page(meet_enermy_page)
		# 战斗界面显示玩家血量，玩家攻击力和防御力，怪物血量和攻击力
		fight_page = Toplevel(root)
		fight_page.title("Fight")
		w = 550
		h = 600
		
		canvas = Canvas(fight_page, bg="black",width=w, height=h)
		canvas.pack(side = LEFT)
		
		player_info = 'Your attack : ' + str(attack) + '   Your defence : ' + str(defence)
		enermy_info = 'Enermy attack : ' + str(enermy_info_attack)
		
		your_HP = 'Your HP : [' + str(player_HP) + '/' + str(max_player_HP) + ']'
		max_enermy_HP = enermy_info_HP
		monster_HP = enermy_choose + ' HP : [' + str(enermy_info_HP) + '/' + str(max_enermy_HP) + ']'
		
		canvas.create_text(w/2,h/2-200,fill="white",font=("Forte",15),text=player_info)
		canvas.create_text(w/2,h/2-180,fill="white",font=("Forte",15),text=enermy_info)
		your_HP_text = canvas.create_text(w/2,h/2-150,fill="white",font=("Forte",15),text=your_HP)
		monster_HP_text = canvas.create_text(w/2,h/2-130,fill="white",font=("Forte",15),text=monster_HP)
		
		# 用个框框框住玩家和怪物信息
		fight_frame = Image.open('fight_frame.png')
		fight_frame_pic = fight_frame.resize((450,500),Image.ANTIALIAS)
		fight_frame_image = ImageTk.PhotoImage(fight_frame_pic)
		fight_frame_picture = canvas.create_image(50,0,image=fight_frame_image,anchor="nw")
		
		fight_icon = Image.open('fight.png')
		fight_pic = fight_icon.resize((100,100),Image.ANTIALIAS)
		fight_image = ImageTk.PhotoImage(fight_pic)
		fight_picture = canvas.create_image(w/2-30,0,image=fight_image,anchor="nw")
		
		def attack_action():
			global player_HP
			global enermy_info_HP
			global attack
			global defence
			global life
			global crit_chance
			global defend_chance
			global food_dict
			global money
			global max_player_HP
			global your_HP_text
			global monster_HP_text
			
			global attack_display_text
			global be_attack_display_text
			
			# 每次按了攻击键以后要清空上回合display的信息
			try:
				canvas.delete(be_attack_display_text)
			except NameError:
				print('first attack, next time can be deleted.')
			
			# 注意布甲和木剑的特效
			# crit chance * 100  (0 ~ 0.2)
			if(wood_sword_level > 0):
				crit_num = random.randint(0,20)
				if(crit_chance*100 > crit_num):
					attack_text = 'You crit the enermy!\nenermy HP - ' + str(2*attack)
					enermy_info_HP = enermy_info_HP - attack*2
				else:
					attack_text = 'You attack ' + enermy_choose + '\nenermy HP - ' + str(attack)
					enermy_info_HP = enermy_info_HP - attack
			else:
				attack_text = 'You attack ' + enermy_choose + '\nenermy HP - ' + str(attack)
				enermy_info_HP = enermy_info_HP - attack
			attack_display_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=attack_text)
			if(enermy_info_HP < 0):
				enermy_info_HP = 0
			
			canvas.delete(monster_HP_text)
			monster_HP = enermy_choose + ' HP : [' + str(enermy_info_HP) + '/' + str(max_enermy_HP) + ']'
			monster_HP_text = canvas.create_text(w/2,h/2-130,fill="white",font=("Forte",15),text=monster_HP)
			
			waithere_short()
			
			steal_food = False
			steal_money = False
			# if enermy not dead, enermy will attack
			if(enermy_info_HP > 0):
				if(enermy_choose == 'cat'):
					steal_food = True
				elif(enermy_choose == 'thief'):
					steal_money = True
					
				if(flax_clothing_level > 0):
					defend_num = random.randint(0,20)
					if(defend_chance*100 > defend_num):
						be_attack_text = 'You defend the attack from enermy!'
					else:
						if(steal_money == True):
							if(money > 0):
								be_attack_text = 'The enermy steal your money! money - 1'
							else:
								be_attack_text = 'The enermy stabs you!\nYour HP - 10'
								player_HP = player_HP - 10
						elif(steal_food == True):
							if(food_dict['unknown fruit'] > 0):
								be_attack_text = 'The enermy steal your unknown fruit!'
								food_dict['unknown fruit'] = food_dict['unknown fruit'] - 1
							elif(food_dict['bbq meat'] > 0):
								be_attack_text = 'The enermy steal your bbq meat!'
								food_dict['bbq meat'] = food_dict['bbq meat'] - 1
							else:
								be_attack_text = 'The enermy bites you!\nYour HP - 10'
								player_HP = player_HP - 10
						if(steal_food == False and steal_money == False):	
							be_attack_text = 'The enermy attacks you!\nYour HP - ' + str(enermy_info_attack)
							player_HP = player_HP - enermy_info_attack + defence
						if(player_HP < 0):
							player_HP = 0
				else:
					if(steal_money == True):
						if(money > 0):
							be_attack_text = 'The enermy steal your money! money - 1'
						else:
							be_attack_text = 'The enermy stabs you!\nYour HP - 10'
							player_HP = player_HP - 10
					if(steal_food == True):
						if(food_dict['unknown fruit'] > 0):
							be_attack_text = 'The enermy steal your unknown fruit!'
							food_dict['unknown fruit'] = food_dict['unknown fruit'] - 1
						elif(food_dict['bbq meat'] > 0):
							be_attack_text = 'The enermy steal your bbq meat!'
							food_dict['bbq meat'] = food_dict['bbq meat'] - 1
						else:
							be_attack_text = 'The enermy bites you!\nYour HP - 10'
							player_HP = player_HP - 10
					if(steal_food == False and steal_money == False):	
						be_attack_text = 'The enermy attacks you!\nYour HP - ' + str(enermy_info_attack)
						player_HP = player_HP - enermy_info_attack + defence
					if(player_HP < 0):
						player_HP = 0
				canvas.delete(attack_display_text)
				be_attack_display_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=be_attack_text)
				
				canvas.delete(your_HP_text)
				your_HP = 'Your HP : [' + str(player_HP) + '/' + str(max_player_HP) + ']'
				your_HP_text = canvas.create_text(w/2,h/2-150,fill="white",font=("Forte",15),text=your_HP)
				
				waithere_short()
			else:	# 战斗胜利，返回主界面
				canvas.delete(attack_display_text)
				print(attack)
				print('attack type:',type(attack))
				# 战斗胜利随机增益一个玩家属性，然后获得1-2个材料
				# 属性增益
				if(enermy_choose in challenge_enermy):
					reward_attribute_increase = 5
					reward_list = challenge_reward
				else:
					reward_attribute_increase_HP = 2
					reward_attribute_increase = 1
					reward_list = normal_reward
				reward_type = ['max_player_HP','attack','defence']
				increase_attribute = random.choice(reward_type)
				if(increase_attribute == 'max_player_HP'):
					max_player_HP = max_player_HP + reward_attribute_increase_HP
					increase_attribute_text = 'max HP + ' + str(reward_attribute_increase_HP)
				elif(increase_attribute == 'attack'):
					attack = attack + reward_attribute_increase
					increase_attribute_text = 'attack + ' + str(reward_attribute_increase)
				else:
					defence = defence + reward_attribute_increase
					increase_attribute_text = 'defence + ' + str(reward_attribute_increase)
				# 获得材料
				reward = random.choice(reward_list)
				if(reward in normal_reward):
					if(reward in food_list):
						food_dict[reward] = food_dict[reward] + 2
					elif(reward in medicine_list):
						medicine_dict[reward] = medicine_dict[reward] + 2
					else:
						manufacture_resouces_dict[reward] = manufacture_resouces_dict[reward] + 2
					reward_text = 'You found ' + reward + ' x2 from ' + enermy_choose
				else:
					if(reward == 'magic blade'):
						crit_chance = crit_chance + 0.1
						reward_text = 'You found ' + reward + ' from ' + enermy_choose
					elif(reward == 'lucky ring'):
						defend_chance = defend_chance + 0.1
						reward_text = 'You found ' + reward + ' from ' + enermy_choose
					elif(reward == 'magic medicine'):
						medicine_dict[reward] = medicine_dict[reward] + 5
						reward_text = 'You found ' + reward + ' x5 from ' + enermy_choose
					else:
						food_dict[reward] = food_dict[reward] + 5
						reward_text = 'You found ' + reward + ' x5 from ' + enermy_choose
					
				
				all_reward = 'Victory! ' + '\n' + increase_attribute_text + '\n' + reward_text
				canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=all_reward)
				waithere_long()
				
				destroy_page(fight_page)
				clear_screen()
				display_day()
				display_action()
			# 如果怪物攻击完后玩家死亡，生命值-1，如果生命值不为零，回到主界面
			if(player_HP <= 0):
				life = life - 1
				if(life <= 0):
					gameover()
				else:
					canvas.delete(be_attack_display_text)
					canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='Defeat! You are dead.')
					player_HP = 1
					waithere_long()
					destroy_page(fight_page)
					clear_screen()
					display_day()
					display_action()
				
		def run_in_fight():
			pass
		
		# display two actions
		attack_bt = Button(fight_page, text = "attack",font='forte',command =attack_action,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		attack_window = canvas.create_window(w/2-100, h-80, anchor='n', window=attack_bt)
		
		run_bt = Button(fight_page, text = "run",font='forte',command = run_in_fight,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		run_window = canvas.create_window(w/2+100, h-80, anchor='n', window=run_bt)
		
		fight_page.grab_set()
		fight_page.resizable(False,False)
		fight_page.mainloop()
		
		
	
	def run(enermy_choose,enermy_info_HP,enermy_info_attack,meet_enermy_page):
		# challenge_enermy is 100%
		if(enermy_choose in challenge_enermy):
			# 如果成功逃跑了，返回主界面，然后显示You run away
			canvas.delete(finding)
			finding = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='You run away...')
			destroy_page(meet_enermy_page)
		else:
			# 如果是普通怪物，50%逃跑几率
			choice_num = [1,2]
			run_random = random.choice(choice_num)
			if(run_random == 0):
				# 逃跑失败，进入战斗
				# 在遭遇怪物的界面display fail to escape, entering the fight...
				# delete the text from previous page
				canvas.delete(enermy_text)
				canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='Fail to escape, entering the fight...')
				# wait for a while then delete the meet_enermy_page
				waithere_long()
				destroy_page(meet_enermy_page)
				fight(enermy_choose,enermy_info_HP,enermy_info_attack,meet_enermy_page)
			else:
				# 如果成功逃跑了，返回主界面，然后显示You run away
				destroy_page(meet_enermy_page)
				# 清除探索信息，然后显示成功逃跑
				canvas.delete(finding)
				finding = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='You run away...')
	
	
	
	def meet_enermy():
		global enermy_info_HP
		# meet enermy use new page
		meet_enermy_page = Toplevel(root)
		meet_enermy_page.title("Meet Enermy")
		w = 600
		h = 400
			
		canvas = Canvas(meet_enermy_page, bg="black",width=w, height=h)
		canvas.pack(side = LEFT)
		
		no_challenge = normal_enermy + special_enermy
		have_challenge = normal_enermy + special_enermy + challenge_enermy
		if(day % 10 == 0):
			enermy_choose = random.choice(challenge_enermy)
		else:
			enermy_choose = random.choice(no_challenge)
		# 随机选择怪物之后，display怪物信息，显示 战斗或者逃跑
		# 得到怪物信息
		if(enermy_choose in normal_enermy):
			enermy_info_HP = normal_enermy_HP[enermy_choose]
			enermy_info_attack = normal_enermy_attack[enermy_choose]
			enermy_info_desc = normal_enermy_desc[enermy_choose]
		elif(enermy_choose in special_enermy):
			enermy_info_HP = special_enermy_HP[enermy_choose]
			enermy_info_attack = special_enermy_attack[enermy_choose]
			enermy_info_desc = special_enermy_desc[enermy_choose]
		elif(enermy_choose in challenge_enermy):
			enermy_info_HP = challenge_enermy_HP[enermy_choose]
			enermy_info_attack = challenge_enermy_attack[enermy_choose]
			enermy_info_desc = challenge_enermy_desc[enermy_choose]
		
		pk_img = Image.open('pk.png')
		pk = pk_img.resize((250,250),Image.ANTIALIAS)
		pk_image = ImageTk.PhotoImage(pk)
		pk_pic = canvas.create_image(w/2-140,h/2-250,image=pk_image,anchor="nw")
		
		global enermy_text
		enermy_info = '[' + enermy_choose + ']' + ' HP : ' + str(enermy_info_HP) + '\nattack: ' + str(enermy_info_attack) + '\n' + enermy_info_desc
		enermy_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=enermy_info)
		
		
		# display two actions
		fight_bt = Button(meet_enermy_page, text = "fight",font='forte',command = lambda: fight(enermy_choose,enermy_info_HP,enermy_info_attack,meet_enermy_page),anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		fight_window = canvas.create_window(w/2-100, h-50, anchor='n', window=fight_bt)
		
		run_bt = Button(meet_enermy_page, text = "run",font='forte',command = lambda: run(enermy_choose,enermy_info_HP,enermy_info_attack,meet_enermy_page),anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		run_window = canvas.create_window(w/2+100, h-50, anchor='n', window=run_bt)
		
		meet_enermy_page.grab_set()
		meet_enermy_page.resizable(False,False)
		meet_enermy_page.mainloop()
	
	def clear_screen():
		# clear the screen and re-print all images
		try:
			canvas.delete(finding)
			
		except NameError:
			print('First time not define the text object. Next time will be ok.')
		
		canvas.delete(day_text)
		canvas.delete(energy_text)
		canvas.delete(life_text)
		canvas.delete(attack_text)
		canvas.delete(hungry_text)
		canvas.delete(defence_text)
		canvas.delete(HP_text)
		canvas.delete(money_text)
		canvas.delete(medicine_text)
		canvas.delete(food_text)
		try:
			canvas.delete(trap_resouces_display_text)
		except:
			print('First time not define the text object. Next time will be ok.')
		try:
			canvas.delete(sleep_money_increase_text)
		except:
			print('First time not define the text object. Next time will be ok.')
		try:
			canvas.delete(sleep_HP_text)
		except:
			print('First time not define the text object. Next time will be ok.')
		try:
			canvas.delete(sleep_energy_text)
		except NameError:
			print('First time not define the text object. Next time will be ok.')
		try:
			canvas.delete(sleep_hungry_text)
		except NameError:
			print('First time not define the text object. Next time will be ok.')
		try:
			canvas.delete(no_food_text)
		except NameError:
			print('Still have enough food and hungry.')
		
	def display_day():
		global day_text
		global energy_text
		global hungry_text
		global life_text
		global attack_text
		global defence_text
		global HP_text
		global money_text
		global medicine_text
		global food_text
		
		day_display = 'Day  ' + str(day)
		day_text = canvas.create_text(110,20,fill="white",font=("Forte",15),text=day_display)
		energy_display = '[' + str(energy) + '/' + str(max_energy) + ']'
		energy_text = canvas.create_text(280,20,fill="white",font=("Forte",15),text=energy_display)
		hungry_display = '[' + str(hungry) + '/' + str(max_hungry) + ']'
		hungry_text = canvas.create_text(460,20,fill="white",font=("Forte",15),text=hungry_display)
		
		# 显示玩家基本属性
		life_display = 'life ' + str(life)
		life_text = canvas.create_text(130,80,fill="white",font=("Forte",15),text=life_display)
		
		attack_display = 'attack ' + str(attack)
		attack_text = canvas.create_text(260,80,fill="white",font=("Forte",15),text=attack_display)
		
		defence_display = 'defence ' + str(defence)
		defence_text = canvas.create_text(390,80,fill="white",font=("Forte",15),text=defence_display)
		
		HP_display = 'HP [' + str(player_HP) + '/' + str(max_player_HP) + ']'
		HP_text = canvas.create_text(130,110,fill="white",font=("Forte",15),text=HP_display)
		
		money_display = 'money ' + str(money)
		money_text = canvas.create_text(260,110,fill="white",font=("Forte",15),text=money_display)
		
		medicine_dict_display = 'medicine ' + str(medicine_dict)
		medicine_text = canvas.create_text(280,140,fill="white",font=("Forte",15),text=medicine_dict_display)
		
		food_dict_display = 'food ' + str(food_dict)
		food_text = canvas.create_text(230,170,fill="white",font=("Forte",15),text=food_dict_display)
	
	def gameover():
		gameover_page = Toplevel(root)
		gameover_page.title("Game Over")
		w = 500
		h = 400
		
		canvas = Canvas(gameover_page, bg="black",width=w, height=h)
		canvas.pack(side = LEFT)
		
		if(life > 0):
			canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='Game over, you made it and you are the greatest man in the world!')
		else:
			canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='Game over, you did not made to 100 days, try your luck next time!')
		
		def over():
			destroy_page(root)
		
		over_bt = Button(gameover_page, text = "ok",font='forte',command = over,anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
		over_window = canvas.create_window(w/2,h-50, anchor='n', window=over_bt)
		
		gameover_page.grab_set()
		gameover_page.resizable(False,False)
		gameover_page.mainloop()
	
	def explore():
		global money
		global finding
		global energy
		global hungry
		
			
		clear_screen()
		
		
		if(life <= 0 or day >= 100):
			gameover()
			
			
		if(energy > 0):
			# deduct energy and hungry
			energy = energy - 10
			hungry = hungry - 5
			if(hungry < 0):
				hungry = 0
			
			item_get = random.choice(explore_list)
			if('$' in item_get):	# 如果探索到的是钱
				money_get = float(item_get.replace('$',''))
				money = money + money_get
				found_script = 'You found ' + item_get
				# create text
				finding = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=found_script)
			else:
				item_num = random.randint(1,3)
				if(item_get == ''):
					found_script = 'You did not found anything...'
					finding = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=found_script)
				else:
					found_script = 'You found ' + item_get + ' x ' + str(item_num)
					finding = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=found_script)
					global food_dict
					global medicine_dict
					global manufacture_resouces_dict
					if(item_get in food_list):
						food_dict[item_get] = food_dict[item_get] + item_num
					elif(item_get in medicine_list):
						medicine_dict[item_get] = medicine_dict[item_get] + item_num
					else:
						manufacture_resouces_dict[item_get] = manufacture_resouces_dict[item_get] + item_num
			
			# 有一定几率碰到怪物
			meet_enermy_num = [0,1,2,3,4,5,6,7,8,9]
			random_num = random.randint(0,9)
			if(random_num > 6):
				meet_enermy()
			
		else:
			finding = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='Energy not enough, please go sleep!')
	
		# refresh
		display_day()
		display_action()
	
	def manufacture():
		global display_resources
		global wood_sword_text
		global tent_text
		global magic_medicine_text
		global bbq_meat_text
		global clothing_text
		global trap_text
		global bonfire_text
		
		manufacture_page = Toplevel(root)
		manufacture_page.title("Manufacture")
		w = 700
		h = 600
		
		def on_configure(event):
			# update scrollregion after starting 'mainloop'
			# when all widgets are in canvas
			canvas.configure(scrollregion=canvas.bbox('all'))
		
		canvas = Canvas(manufacture_page, bg="black",width=w, height=h)
		canvas.pack(side = LEFT)
		
		scrollbar = Scrollbar(manufacture_page, command=canvas.yview)
		scrollbar.pack(side=LEFT, fill='y')
		canvas.configure(yscrollcommand = scrollbar.set)
		# update scrollregion after starting 'mainloop'
		# when all widgets are in canvas
		canvas.bind('<Configure>', on_configure)
		
		canvas.create_text(w/2,50,fill="white",font=("Forte",20),text='click the picture to manufacture')
		
		global display_resources
		# display the current resources
		resources = str(manufacture_resouces_dict)
		display_resources = canvas.create_text(w/2,80,fill=light_blue,font=("Forte",20),text=resources)
		
		wood_sword_img = Image.open('wood_sword.png')
		wood_sword_pic = wood_sword_img.resize((100,100),Image.ANTIALIAS)
		wood_sword_image = ImageTk.PhotoImage(wood_sword_pic)
		wood_sword_picture = canvas.create_image(100,100,image=wood_sword_image,anchor="nw")
		
		wood_sword_desc = 'wood sword level[' + str(wood_sword_level) + ']\nattack increase [' + str(attack_increase[wood_sword_level]) + ']\nupgrade need wood [' + str(sword_need_wood[wood_sword_level]) + ']'
		wood_sword_text = canvas.create_text(400,150,fill="white",font=("Forte",15),text=wood_sword_desc)
		
		tent_img = Image.open('tent.png')
		tent_pic = tent_img.resize((130,130),Image.ANTIALIAS)
		tent_image = ImageTk.PhotoImage(tent_pic)
		tent_picture = canvas.create_image(80,300,image=tent_image,anchor="nw")
		
		tent_desc = 'tent level[' + str(tent_level) + ']\nmax energy increase [' + str(max_energy_increase[tent_level]) + ']\nupgrade need wood [' + str(tent_need_wood[tent_level]) + ']' + '\nupgrade need flax [' + str(tent_need_flax[tent_level]) + ']'
		tent_text = canvas.create_text(400,350,fill="white",font=("Forte",15),text=tent_desc)
		
		magic_medicine_img = Image.open('magic medicine.jpg')
		magic_medicine = magic_medicine_img.resize((100,100),Image.ANTIALIAS)
		magic_medicine_image = ImageTk.PhotoImage(magic_medicine)
		magic_medicine_pic = canvas.create_image(100,500,image=magic_medicine_image,anchor="nw")
		
		magic_medicine_desc = 'magic medicine\nHP + 50\nmake need wormwood [' + str(magic_medicine_need_wormwood) + ']'
		magic_medicine_text = canvas.create_text(400,550,fill="white",font=("Forte",15),text=magic_medicine_desc)
		
		bbq_meat_img = Image.open('bbq_meat.png')
		bbq_meat = bbq_meat_img.resize((100,100),Image.ANTIALIAS)
		bbq_meat_image = ImageTk.PhotoImage(bbq_meat)
		bbq_meat_pic = canvas.create_image(100,700,image=bbq_meat_image,anchor="nw")
		
		bbq_meat_desc = 'bbq meat\nhungry + 40\nmake need raw meat [' + str(meat_need_raw) + ']\nmake need wood [' + str(meat_need_wood) + ']'
		bbq_meat_text = canvas.create_text(400,750,fill="white",font=("Forte",15),text=bbq_meat_desc)
		
		clothing_img = Image.open('clothing.png')
		clothing = clothing_img.resize((130,130),Image.ANTIALIAS)
		clothing_image = ImageTk.PhotoImage(clothing)
		clothing_pic = canvas.create_image(80,900,image=clothing_image,anchor="nw")
		
		clothing_desc = 'flax clothing level[' + str(flax_clothing_level) + ']\nmax HP increase [' + str(HP_increase[flax_clothing_level]) + 'trigger defend chance [' + str(trigger_defend[flax_clothing_level]) + ']\nupgrade need flax [' + str(flax_clothing_need_flax[flax_clothing_level]) + ']'
		clothing_text = canvas.create_text(450,970,fill="white",font=("Forte",15),text=clothing_desc)
		
		trap_img = Image.open('trap.png')
		trap = trap_img.resize((100,100),Image.ANTIALIAS)
		trap_image = ImageTk.PhotoImage(trap)
		trap_pic = canvas.create_image(100,1100,image=trap_image,anchor="nw")
		
		trap_desc = 'trap level[' + str(trap_level) + ']\ntrap get item number [' + str(trap_get_item_num[trap_level]) + ']\nupgrade need wood [' + str(trap_need_wood[trap_level]) + ']'
		trap_text = canvas.create_text(400,1150,fill="white",font=("Forte",15),text=trap_desc)
		
		bonfire_img = Image.open('bonfire.png')
		bonfire = bonfire_img.resize((100,100),Image.ANTIALIAS)
		bonfire_image = ImageTk.PhotoImage(bonfire)
		bonfire_pic = canvas.create_image(100,1300,image=bonfire_image,anchor="nw")
		
		bonfire_desc = 'bonfire level[' + str(bonfire_level) + ']\nsleep recover HP [' + str(sleep_recover_HP[bonfire_level]) + ']\nupgrade need wood [' + str(bonfire_need_wood[bonfire_level]) + ']'
		bonfire_text = canvas.create_text(400,1350,fill="white",font=("Forte",15),text=bonfire_desc)
		
		def manufacture_back():
			destroy_page(manufacture_page)
			# refresh the previous page
			clear_screen()
			display_day()
			display_action()
		
		# exit manufacture page
		manufacture_back_bt = Button(manufacture_page, text = "back",font='forte',command = manufacture_back,anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
		manufacture_back_window = canvas.create_window(w-70,20, anchor='n', window=manufacture_back_bt)
		
		def ok(make_item_page):
			global display_resources
			global wood_sword_text
			global tent_text
			global magic_medicine_text
			global bbq_meat_text
			global clothing_text
			global trap_text
			global bonfire_text
			canvas.delete(display_resources)
			canvas.delete(wood_sword_text)
			canvas.delete(tent_text)
			canvas.delete(magic_medicine_text)
			canvas.delete(bbq_meat_text)
			canvas.delete(clothing_text)
			canvas.delete(trap_text)
			canvas.delete(bonfire_text)
			
			resources = str(manufacture_resouces_dict)
			display_resources = canvas.create_text(w/2,80,fill=light_blue,font=("Forte",20),text=resources)
			
			wood_sword_desc = 'wood sword level[' + str(wood_sword_level) + ']\nattack increase [' + str(attack_increase[wood_sword_level]) + ']\nupgrade need wood [' + str(sword_need_wood[wood_sword_level]) + ']'
			wood_sword_text = canvas.create_text(400,150,fill="white",font=("Forte",15),text=wood_sword_desc)
			
			tent_desc = 'tent level[' + str(tent_level) + ']\nmax energy increase [' + str(max_energy_increase[tent_level]) + ']\nupgrade need wood [' + str(tent_need_wood[tent_level]) + ']' + '\nupgrade need flax [' + str(tent_need_flax[tent_level]) + ']'
			tent_text = canvas.create_text(400,350,fill="white",font=("Forte",15),text=tent_desc)
			
			magic_medicine_desc = 'magic medicine\nHP + 50\nmake need wormwood [' + str(magic_medicine_need_wormwood) + ']'
			magic_medicine_text = canvas.create_text(400,550,fill="white",font=("Forte",15),text=magic_medicine_desc)
			
			bbq_meat_desc = 'bbq meat\nhungry + 40\nmake need raw meat [' + str(meat_need_raw) + ']\nmake need wood [' + str(meat_need_wood) + ']'
			bbq_meat_text = canvas.create_text(400,750,fill="white",font=("Forte",15),text=bbq_meat_desc)
			
			clothing_desc = 'flax clothing level[' + str(flax_clothing_level) + ']\nmax HP increase [' + str(HP_increase[flax_clothing_level]) + '\ntrigger defend chance [' + str(trigger_defend[flax_clothing_level]) + ']\nupgrade need flax [' + str(flax_clothing_need_flax[flax_clothing_level]) + ']'
			clothing_text = canvas.create_text(450,970,fill="white",font=("Forte",15),text=clothing_desc)
			
			trap_desc = 'trap level[' + str(trap_level) + ']\ntrap get item number [' + str(trap_get_item_num[trap_level]) + ']\nupgrade need wood [' + str(trap_need_wood[trap_level]) + ']'
			trap_text = canvas.create_text(400,1150,fill="white",font=("Forte",15),text=trap_desc)
			
			bonfire_desc = 'bonfire level[' + str(bonfire_level) + ']\nsleep recover HP [' + str(sleep_recover_HP[bonfire_level]) + ']\nupgrade need wood [' + str(bonfire_need_wood[bonfire_level]) + ']'
			bonfire_text = canvas.create_text(400,1350,fill="white",font=("Forte",15),text=bonfire_desc)
			
			destroy_page(make_item_page)
		
		def make_item(item_to_do):
			make_item_page = Toplevel(root)
			make_item_page.title("Manufacture")
			w = 400
			h = 300
			
			canvas = Canvas(make_item_page, bg="black",width=w, height=h)
			canvas.pack(side = LEFT)
			
			# display the item picture and level up effect
			if(item_to_do == 'wood sword'):
				item_level_up = 'wood_sword.png'
			elif(item_to_do == 'tent'):
				item_level_up = 'tent.png'
			elif(item_to_do == 'trap'):
				item_level_up = 'trap.png'
			elif(item_to_do == 'bbq meat'):
				item_level_up = 'bbq_meat.png'
			elif(item_to_do == 'magic medicine'):
				item_level_up = 'magic medicine.png'
			elif(item_to_do == 'flax clothing'):
				item_level_up = 'clothing.png'
			elif(item_to_do == 'bonfire'):
				item_level_up = 'bonfire.png'
			
			# effect
			effect_img = Image.open('level_up.png')
			effect = effect_img.resize((200,200),Image.ANTIALIAS)
			effect_image = ImageTk.PhotoImage(effect)
			effect_pic = canvas.create_image(0,50,image=effect_image,anchor="nw")
			
			# item picture
			item_img = Image.open(item_level_up)
			item = item_img.resize((120,120),Image.ANTIALIAS)
			item_image = ImageTk.PhotoImage(item)
			item_pic = canvas.create_image(w/2-140,h/2-50,image=item_image,anchor="nw")
			
			if(item_to_do == 'magic medicine' or item_to_do == 'bbq meat'):
				level_up_text = 'You made a ' + item_to_do + '!'
			else:
				level_up_text = item_to_do + ' level up!'
			canvas.create_text(w/2+50,h/2,fill="white",font=("Forte",15),text=level_up_text)
			
				
			
			ok_bt = Button(make_item_page, text = "ok",font='forte',command = lambda: ok(make_item_page),anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
			buy_ok_window = canvas.create_window(w/2,h-50, anchor='n', window=ok_bt)
			
			make_item_page.grab_set()
			make_item_page.resizable(False,False)
			make_item_page.mainloop()
		
		def resources_not_enough():
			resources_not_enough_page = Toplevel(root)
			resources_not_enough_page.title("resources not enough")
			w = 300
			h = 300
			
			canvas = Canvas(resources_not_enough_page, bg="black",width=w, height=h)
			canvas.pack(side = LEFT)
			
			canvas.create_text(w/2,h/2,fill="white",font=("Forte",20),text='Resources not enough!')
			
			def ok():
				destroy_page(resources_not_enough_page)
			
			ok_bt = Button(resources_not_enough_page, text = "ok",font='forte',command = ok,anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
			buy_ok_window = canvas.create_window(w/2,h-50, anchor='n', window=ok_bt)
			
			resources_not_enough_page.grab_set()
			resources_not_enough_page.resizable(False,False)
			resources_not_enough_page.mainloop()
		
		# make method
		def make_wood_sword(event=None):
			global wood_sword_level
			global attack
			global crit_chance
			global manufacture_resouces_dict
			
			if(manufacture_resouces_dict['wood'] >= sword_need_wood[wood_sword_level]):
				# level up
				wood_sword_level = wood_sword_level + 1
				# update player attributes
				attack = attack + attack_increase[wood_sword_level]
				crit_chance = crit_chance + trigger_crit[wood_sword_level]
				# remove used resources
				manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - sword_need_wood[wood_sword_level-1]
				# display result
				make_item('wood sword')
			else:
				resources_not_enough()
		
		def make_tent(event=None):
			global tent_level
			global max_energy
			global manufacture_resouces_dict
			
			if(manufacture_resouces_dict['wood'] >= tent_need_wood[tent_level] and manufacture_resouces_dict['flax'] >= tent_need_flax[tent_level]):
				# level up
				tent_level = tent_level + 1
				# update player attributes
				max_energy = max_energy + max_energy_increase[tent_level]
				# remove used resources
				manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - tent_need_wood[tent_level-1]
				manufacture_resouces_dict['flax'] = manufacture_resouces_dict['flax'] - tent_need_flax[tent_level-1]
				# display result
				make_item('tent')
			else:
				resources_not_enough()
		
		def make_magic_medicine(event=None):
			global medicine_dict
			global manufacture_resouces_dict
			
			if(manufacture_resouces_dict['wormwood'] >= magic_medicine_need_wormwood):
				# update medicine dict
				medicine_dict['magic medicine'] = medicine_dict['magic medicine'] + 1
				# remove used resources
				manufacture_resouces_dict['wormwood'] = manufacture_resouces_dict['wormwood'] - magic_medicine_need_wormwood
				# display result
				make_item('magic medicine')
			else:
				resources_not_enough()
		
		def make_bbq_meat(event=None):
			global food_dict
			global manufacture_resouces_dict
			
			if(manufacture_resouces_dict['raw meat'] >= meat_need_raw and manufacture_resouces_dict['wood'] >= meat_need_wood):
				# update medicine dict
				food_dict['bbq meat'] = food_dict['bbq meat'] + 1
				# remove used resources
				manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - meat_need_wood
				manufacture_resouces_dict['raw meat'] = manufacture_resouces_dict['raw meat'] - meat_need_raw
				# display result
				make_item('bbq meat')
			else:
				resources_not_enough()
		
		def make_clothing(event=None):
			global flax_clothing_level
			global max_player_HP
			global defend_chance
			global manufacture_resouces_dict
			
			if(manufacture_resouces_dict['flax'] >= flax_clothing_need_flax[flax_clothing_level]):
				# level up
				flax_clothing_level = flax_clothing_level + 1
				# update player attributes
				max_player_HP = max_player_HP + HP_increase[flax_clothing_level]
				defend_chance = defend_chance + trigger_defend[flax_clothing_level]
				# remove used resources
				manufacture_resouces_dict['flax'] = manufacture_resouces_dict['flax'] - flax_clothing_need_flax[flax_clothing_level - 1]
				# display result
				make_item('flax clothing')
			else:
				resources_not_enough()
		
		def make_trap(event=None):
			global trap_level
			global trap_number
			global manufacture_resouces_dict
			
			if(manufacture_resouces_dict['wood'] >= trap_need_wood[trap_level]):
				# level up
				trap_level = trap_level + 1
				# update trap 
				trap_number = trap_get_item_num[trap_level]
				# remove used resources
				manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - trap_need_wood[trap_level - 1]
				# display result
				make_item('trap')
			else:
				resources_not_enough()
		
		def make_bonfire(event=None):
			global bonfire_level
			global recover_HP
			global manufacture_resouces_dict
			
			if(manufacture_resouces_dict['wood'] >= bonfire_need_wood[bonfire_level]):
				# level up
				bonfire_level = bonfire_level + 1
				# update trap 
				recover_HP = sleep_recover_HP[bonfire_level]
				# remove used resources
				manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - bonfire_need_wood[bonfire_level-1]
				# display result
				make_item('bonfire')
			else:
				resources_not_enough()
		
		
		# bind different manufacture item with manufacture functions
		canvas.tag_bind(wood_sword_picture, '<ButtonPress-1>', make_wood_sword)
		canvas.tag_bind(tent_picture, '<ButtonPress-1>', make_tent)
		canvas.tag_bind(magic_medicine_pic, '<ButtonPress-1>', make_magic_medicine)
		canvas.tag_bind(bbq_meat_pic, '<ButtonPress-1>', make_bbq_meat)
		canvas.tag_bind(clothing_pic, '<ButtonPress-1>', make_clothing)
		canvas.tag_bind(trap_pic, '<ButtonPress-1>', make_trap)
		canvas.tag_bind(bonfire_pic, '<ButtonPress-1>', make_bonfire)
		
		
		manufacture_page.grab_set()
		manufacture_page.resizable(False,False)
		manufacture_page.mainloop()
	
	def shopping():
		shopping_page = Toplevel(root)
		shopping_page.title("Shops")
		w = 700
		h = 600
		canvas = Canvas(shopping_page, bg="black",width=w, height=h)
		canvas.pack(side = LEFT)
		
		canvas.create_text(w/2,50,fill="white",font=("Forte",25),text='click the picture to buy')
		
		# display all items pic
		# unknown fruit
		fruit_img = Image.open('fruit.png')
		unknown_fruit = fruit_img.resize((100,100),Image.ANTIALIAS)
		unknown_fruit_image = ImageTk.PhotoImage(unknown_fruit)
		unknown_fruit_pic = canvas.create_image(80,100,image=unknown_fruit_image,anchor="nw")
		
		canvas.create_text(130,210,fill="white",font=("Forte",15),text='unknown fruit [$3]\nhungry+15')
		
		# bbq meat
		bbq_meat_img = Image.open('bbq_meat.png')
		bbq_meat = bbq_meat_img.resize((100,100),Image.ANTIALIAS)
		bbq_meat_image = ImageTk.PhotoImage(bbq_meat)
		bbq_meat_pic = canvas.create_image(280,100,image=bbq_meat_image,anchor="nw")
		
		canvas.create_text(330,210,fill="white",font=("Forte",15),text='bbq meat [$8]\nhungry+40')
		
		# raw meat
		raw_meat_img = Image.open('raw meat.png')
		raw_meat = raw_meat_img.resize((100,100),Image.ANTIALIAS)
		raw_meat_image = ImageTk.PhotoImage(raw_meat)
		raw_meat_picture = canvas.create_image(480,100,image=raw_meat_image,anchor="nw")
		
		canvas.create_text(530,210,fill="white",font=("Forte",15),text='raw meat [$2]')
		
		# healing grass
		healing_grass_img = Image.open('healing grass.png')
		healing_grass = healing_grass_img.resize((100,100),Image.ANTIALIAS)
		healing_grass_image = ImageTk.PhotoImage(healing_grass)
		healing_grass_pic = canvas.create_image(80,260,image=healing_grass_image,anchor="nw")
		
		canvas.create_text(125,380,fill="white",font=("Forte",15),text='healing grass [$5]\nHP+15')
		
		# magic medicine
		magic_medicine_img = Image.open('magic medicine.jpg')
		magic_medicine = magic_medicine_img.resize((100,100),Image.ANTIALIAS)
		magic_medicine_image = ImageTk.PhotoImage(magic_medicine)
		magic_medicine_pic = canvas.create_image(280,260,image=magic_medicine_image,anchor="nw")
		
		canvas.create_text(315,380,fill="white",font=("Forte",15),text='magic medicine [$10]\nHP+50')
		
		# wood
		wood_img = Image.open('wood.png')
		wood_pic = wood_img.resize((100,100),Image.ANTIALIAS)
		wood_image = ImageTk.PhotoImage(wood_pic)
		wood_picture = canvas.create_image(80,450,image=wood_image,anchor="nw")
		
		canvas.create_text(125,560,fill="white",font=("Forte",15),text='wood [$1]')
		
		# flax
		flax_img = Image.open('flax.png')
		flax_pic = flax_img.resize((100,100),Image.ANTIALIAS)
		flax_image = ImageTk.PhotoImage(flax_pic)
		flax_picture = canvas.create_image(280,440,image=flax_image,anchor="nw")
		
		canvas.create_text(330,560,fill="white",font=("Forte",15),text='flax [$2]')
		
		# wormwood
		wormwood_img = Image.open('wormwood.png')
		wormwood = wormwood_img.resize((100,100),Image.ANTIALIAS)
		wormwood_image = ImageTk.PhotoImage(wormwood)
		wormwood_picture = canvas.create_image(480,450,image=wormwood_image,anchor="nw")
		
		canvas.create_text(530,560,fill="white",font=("Forte",15),text='wormwood [$2]')
		
		def buy_item(item):
			buy_item_page = Toplevel(root)
			buy_item_page.title("Buy item")
			w = 500
			h = 300
			canvas = Canvas(buy_item_page, bg="black",width=w, height=h)
			canvas.pack(side = LEFT)
			
			buy_item_img = Image.open('buy_ok.png')
			buy_item_pic = buy_item_img.resize((500,300),Image.ANTIALIAS)
			buy_item_image = ImageTk.PhotoImage(buy_item_pic)
			buy_item_picture = canvas.create_image(0,0,image=buy_item_image,anchor="nw")
			
			global money
			global food_dict
			global medicine_dict
			global manufacture_resouces_dict
			if(money >= price_tag[item]):
				buy_text = 'you have bought a ' + item
				canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=buy_text)
				money = money - price_tag[item]
				if(item in food_list):
					food_dict[item] = food_dict[item] + 1
				elif(item in medicine_list):
					medicine_dict[item] = medicine_dict[item] + 1
				else:
					manufacture_resouces_dict[item] = manufacture_resouces_dict[item] + 1
			else:
				canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text='Not enough money')
			
			def buy_ok():
				destroy_page(buy_item_page)
			
			buy_ok_bt = Button(buy_item_page, text = "ok",font='forte',command = buy_ok,anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
			buy_ok_window = canvas.create_window(w/2,h-50, anchor='n', window=buy_ok_bt)
		
			buy_item_page.grab_set()
			buy_item_page.resizable(False,False)
			buy_item_page.mainloop()
		
		def buy_unknown_fruit(event=None):
			buy_item('unknown fruit')
		
		def buy_bbq_meat(event=None):
			buy_item('bbq meat')
		
		def buy_raw_meat(event=None):
			buy_item('raw meat')
			
		def buy_healing_grass(event=None):
			buy_item('healing grass')
		
		def buy_magic_medicine(event=None):
			buy_item('magic medicine')
		
		def buy_wood(event=None):
			buy_item('wood')
		
		def buy_flax(event=None):
			buy_item('flax')
		
		def buy_wormwood(event=None):
			buy_item('wormwood')
		
		# bind each pic with buy function
		canvas.tag_bind(unknown_fruit_pic, '<ButtonPress-1>', buy_unknown_fruit)
		canvas.tag_bind(bbq_meat_pic, '<ButtonPress-1>', buy_bbq_meat)
		canvas.tag_bind(raw_meat_picture, '<ButtonPress-1>', buy_raw_meat)
		canvas.tag_bind(healing_grass_pic, '<ButtonPress-1>', buy_healing_grass)
		canvas.tag_bind(magic_medicine_pic, '<ButtonPress-1>', buy_magic_medicine)
		canvas.tag_bind(wood_picture, '<ButtonPress-1>', buy_wood)
		canvas.tag_bind(flax_picture, '<ButtonPress-1>', buy_flax)
		canvas.tag_bind(wormwood_picture, '<ButtonPress-1>', buy_wormwood)
		
		
		def finish_shopping():
			# refresh the previous page
			clear_screen()
			# refresh
			display_day()
			display_action()
			
			destroy_page(shopping_page)
		
		# back button
		shopping_back_bt = Button(shopping_page, text = "back",font='forte',command = finish_shopping,anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
		shopping_back_window = canvas.create_window(w-80,20, anchor='n', window=shopping_back_bt)
	
		shopping_page.grab_set()
		shopping_page.resizable(False,False)
		shopping_page.mainloop()
		
	
	def use_medicine():
		# new page
		medicine_page = Toplevel(root)
		medicine_page.title("Use medicine")
		w = 550
		h = 550
		canvas = Canvas(medicine_page, bg="black",width=w, height=h)
		canvas.pack(side = LEFT)
		
		# load medicine pic
		# healing grass
		healing_grass_img = Image.open('healing grass.png')
		healing_grass = healing_grass_img.resize((150,150),Image.ANTIALIAS)
		healing_grass_image = ImageTk.PhotoImage(healing_grass)
		healing_grass_pic = canvas.create_image(w/2-220,50,image=healing_grass_image,anchor="nw")
		# magic medicine
		magic_medicine_img = Image.open('magic medicine.jpg')
		magic_medicine = magic_medicine_img.resize((130,130),Image.ANTIALIAS)
		magic_medicine_image = ImageTk.PhotoImage(magic_medicine)
		magic_medicine_pic = canvas.create_image(w/2-200,250,image=magic_medicine_image,anchor="nw")
		
		canvas.create_text(w/2,30,fill="white",font=("Forte",20),text='Click the picture to use the medicine.')
		
		def ok(medicine_used_page):
			global medicine_1_text
			global medicine_2_text
						
			canvas.delete(medicine_1_text)
			canvas.delete(medicine_2_text)
			
			medicine_1 = 'Healing grass: ' + str(medicine_dict['healing grass']) + '\nAn wild grass, can eat.\nHP+15.'
			medicine_2 = 'Magic medicine :' + str(medicine_dict['magic medicine']) + '\nAn special medicine, have magic power.\nHP+50.'
			medicine_1_text = canvas.create_text(w/2+30,150,fill="white",font=("Forte",15),text=medicine_1)
			medicine_2_text = canvas.create_text(w/2+100,320,fill="white",font=("Forte",15),text=medicine_2)
			
			destroy_page(medicine_used_page)
			
		
		def use_healing_grass(event=None):
			# update HP
			global player_HP
			global medicine_dict
			if(medicine_dict['healing grass'] > 0):
				player_HP = player_HP + 15
				if(player_HP > max_player_HP):
					player_HP = max_player_HP
				# consume healing grass
				
			# messagebox to show player that HP updates and consumption of medicine
			medicine_used_page = Toplevel(root)
			medicine_used_page.title("Use medicine")
			w = 400
			h = 300
			canvas = Canvas(medicine_used_page, bg="black",width=w, height=h)
			canvas.pack(side = LEFT)
			
			use_medicine_img = Image.open('use_medicine.jpg')
			use_medicine_pic = use_medicine_img.resize((400,300),Image.ANTIALIAS)
			use_medicine_image = ImageTk.PhotoImage(use_medicine_pic)
			use_medicine_picture = canvas.create_image(0,0,image=use_medicine_image,anchor="nw")
			if(medicine_dict['healing grass'] > 0):
				canvas.create_text(w/2,150,fill="white",font=("Forte",15),text='You used one healing grass\n HP + 15')
			else:
				canvas.create_text(w/2,150,fill="white",font=("Forte",15),text='You do not have enough healing grass!')
		
			if(medicine_dict['healing grass'] > 0):
				medicine_dict['healing grass'] = medicine_dict['healing grass'] - 1
			
			# ok button
			ok_bt = Button(medicine_used_page, text = "ok",font='forte',command =lambda: ok(medicine_used_page),anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
			ok_window = canvas.create_window(w/2,250, anchor='n', window=ok_bt)
			
			medicine_used_page.grab_set()
			medicine_used_page.resizable(False,False)
			medicine_used_page.mainloop()
			
		
		def use_magic_medicine(event=None):
			# update HP
			global player_HP
			global medicine_dict
			if(medicine_dict['magic medicine'] > 0):
				player_HP = player_HP + 50
				if(player_HP > max_player_HP):
					player_HP = max_player_HP
				
			# messagebox to show player that HP updates and consumption of medicine
			medicine_used_page = Toplevel(root)
			medicine_used_page.title("Use medicine")
			w = 400
			h = 300
			canvas = Canvas(medicine_used_page, bg="black",width=w, height=h)
			canvas.pack(side = LEFT)
			
			use_medicine_img = Image.open('use_medicine.jpg')
			use_medicine_pic = use_medicine_img.resize((400,300),Image.ANTIALIAS)
			use_medicine_image = ImageTk.PhotoImage(use_medicine_pic)
			use_medicine_picture = canvas.create_image(0,0,image=use_medicine_image,anchor="nw")
			if(medicine_dict['magic medicine'] > 0):
				canvas.create_text(w/2,150,fill="white",font=("Forte",15),text='You used one magic medicine\nHP + 50')
			else:
				canvas.create_text(w/2,150,fill="white",font=("Forte",15),text='You do not have enough magic medicine!')
			
			if(medicine_dict['magic medicine'] > 0):
				# consume healing grass
				medicine_dict['magic medicine'] = medicine_dict['magic medicine'] - 1
			
			
			
			# ok button
			ok_bt = Button(medicine_used_page, text = "ok",font='forte',command = lambda: ok(medicine_used_page),anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
			ok_window = canvas.create_window(w/2,250, anchor='n', window=ok_bt)
			
			medicine_used_page.grab_set()
			medicine_used_page.resizable(False,False)
			medicine_used_page.mainloop()
			
		
		# bind events to pic
		canvas.tag_bind(healing_grass_pic, '<ButtonPress-1>', use_healing_grass)
		canvas.tag_bind(magic_medicine_pic, '<ButtonPress-1>', use_magic_medicine)
		
		# display medicine text
		global medicine_1_text
		global medicine_2_text
		medicine_1 = 'Healing grass: ' + str(medicine_dict['healing grass']) + '\nAn wild grass, can eat.\nHP+15.'
		medicine_2 = 'Magic medicine :' + str(medicine_dict['magic medicine']) + '\nAn special medicine, have magic power.\nHP+50.'
		medicine_1_text = canvas.create_text(w/2+30,150,fill="white",font=("Forte",15),text=medicine_1)
		medicine_2_text = canvas.create_text(w/2+100,320,fill="white",font=("Forte",15),text=medicine_2)
		
		def back():
			# 回到之前的界面前，再refresh一下之前的界面信息
			clear_screen()
			# refresh
			display_day()
			display_action()
			destroy_page(medicine_page)
		
		# back button
		medicine_back_bt = Button(medicine_page, text = "back",font='forte',command = back,anchor = 'n',width = 12,bg=light_blue,activebackground = light_blue)
		medicine_back_window = canvas.create_window(w/2,500, anchor='n', window=medicine_back_bt)
		
		medicine_page.grab_set()
		medicine_page.resizable(False,False)
		medicine_page.mainloop()
		
		
		# after finish medicine page, return to previous page, update HP display
	
	def sleep():
		global energy
		global sleep
		global day
		global hungry
		global money
		global sleep_energy_text
		global sleep_hungry_text
		global sleep_HP_text
		global food_dict
		global life
		global no_food_text
		global player_HP
		global level
		global food_dict
		global medicine_dict
		global manufacture_resouces_dict
		global sleep_money_increase_text
		global trap_resouces_display_text
		
		clear_screen()
		
		day = day + 1
		if(money_increase == True):
			money = money + 1
		if(day % 10 == 0):
			level = level + 1
		if(bonfire_level > 0):
			sleep_HP = 'HP + ' + str(sleep_recover_HP[bonfire_level])
			player_HP = player_HP + sleep_recover_HP[bonfire_level]
			if(player_HP > max_player_HP):
				player_HP = max_player_HP
		sleep_recover = 'Energy + ' + str(max_energy - energy)
		sleep_hungry = 'hungry - 20'
		sleep_money_increase = 'Money + 1'
		
		if(trap_level > 0):
			# 30% chance to trap some resources
			trap_random_num = random.randint(0,9)
			if(trap_random_num > 6):
				trap_resouces = random.choice(full_explore_list)
				trap_resouces_text = 'Your trap get ' + trap_resouces + ' x ' + str(trap_number)
				if(trap_resouces in food_dict):
					food_dict[trap_resouces] = food_dict[trap_resouces] + trap_number
				elif(trap_resouces in medicine_dict):
					medicine_dict[trap_resouces] = medicine_dict[trap_resouces] + trap_number
				else:
					manufacture_resouces_dict[trap_resouces] = manufacture_resouces_dict[trap_resouces] + trap_number
			trap_resouces_display_text = canvas.create_text(w/2,h/2+90,fill="white",font=("Forte",15),text=trap_resouces_text)
		
		# recover the energy
		energy = max_energy
		hungry = hungry - 20
		if(hungry < 0):
			hungry = 0
			
		# eat food if there is food
		while(hungry < 100 and food_dict['unknown fruit'] != 0):
			food_dict['unknown fruit'] = food_dict['unknown fruit'] - 1
			hungry = hungry + 15
			if(hungry > max_hungry):
				hungry = max_hungry
		
		while(hungry < 100 and food_dict['bbq meat'] != 0):
			food_dict['bbq meat'] = food_dict['bbq meat'] - 1
			hungry = hungry + 40
			if(hungry > max_hungry):
				hungry = max_hungry
		
		if(hungry == 0 and food_dict['unknown fruit'] == 0 and food_dict['bbq meat'] == 0):
			no_food_text = canvas.create_text(w/2,h/2+90,fill="white",font=("Forte",15),text='not enough food, \nlife will decrease by 1 each day.')
			life = life - 1
		
		
		sleep_energy_text = canvas.create_text(w/2,h/2-30,fill="white",font=("Forte",15),text=sleep_recover)
		sleep_hungry_text = canvas.create_text(w/2,h/2,fill="white",font=("Forte",15),text=sleep_hungry)
		if(bonfire_level > 0):
			sleep_HP_text = canvas.create_text(w/2,h/2+30,fill="white",font=("Forte",15),text=sleep_HP)
		if(money_increase == True):
			sleep_money_increase_text = canvas.create_text(w/2,h/2+60,fill="white",font=("Forte",15),text=sleep_money_increase)
		
		# refresh
		display_day()
		display_action()
	
	def exit():
		print('game exit.')
		destroy_page(root)
	
	def display_action():
		global explore_bt
		global manufacture_bt
		global shopping_bt
		global use_medicine_bt
		global exit_bt
		# use button to show all actions
		explore_bt = Button(game_page, text = "explore",font='forte',command = explore,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		explore_window = canvas.create_window(w/2, 560, anchor='n', window=explore_bt)
		
		manufacture_bt = Button(game_page, text = "manufacture",font='forte',command = manufacture,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		explore_window = canvas.create_window(w/2-150, 510, anchor='n', window=manufacture_bt)
		
		shopping_bt = Button(game_page, text = "shopping",font='forte',command = shopping,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		explore_window = canvas.create_window(w/2, 460, anchor='n', window=shopping_bt)
		
		use_medicine_bt = Button(game_page, text = "use medicine",font='forte',command = use_medicine,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
		explore_window = canvas.create_window(w/2, 510, anchor='n', window=use_medicine_bt)
		
		exit_bt = Button(game_page, text = "Exit",font='forte',command = exit,anchor = 'nw',width = 12,bg='red',activebackground = 'red')
		exit_window = canvas.create_window(w/2+180, 560, anchor='n', window=exit_bt)
		
		# when energy == 0, can choose to sleep
		if(energy == 0):
			sleep_bt = Button(game_page, text = "sleep",font='forte',command = sleep,anchor = 'nw',width = 12,bg=light_blue,activebackground = light_blue)
			sleep_window = canvas.create_window(w/2+150, 510, anchor='n', window=sleep_bt)
		
		
	
	
		
	# 每天都要display玩家基本信息
	
	# =======================================================================
	# 用一个框框来框住所有的玩家属性
	day_frame_img = Image.open('day_frame2.png')
	day_frame = day_frame_img.resize((450,160),Image.ANTIALIAS)
	day_frame_image = ImageTk.PhotoImage(day_frame)
	canvas.create_image(w/2-225,50,image=day_frame_image,anchor="nw")
	
	# 小图标
	# day icon
	day_img = Image.open('day.png')
	day_icon = day_img.resize((40,40),Image.ANTIALIAS)
	day_image = ImageTk.PhotoImage(day_icon)
	canvas.create_image(40,5,image=day_image,anchor="nw")
	
	# energy icon
	energy_img = Image.open('energy.png')
	energy_icon = energy_img.resize((45,45),Image.ANTIALIAS)
	energy_image = ImageTk.PhotoImage(energy_icon)
	canvas.create_image(195,0,image=energy_image,anchor="nw")
	
	# food icon
	food_img = Image.open('food.png')
	food_icon = food_img.resize((50,50),Image.ANTIALIAS)
	food_image = ImageTk.PhotoImage(food_icon)
	canvas.create_image(365,0,image=food_image,anchor="nw")
	
	# =======================================================================
	
	
	
	# 显示所有可执行动作
	# 每次完成一个操作都要清空屏幕，并重新运行这两个方法
	display_day()
	display_action()
	
	
	game_page.grab_set()
	game_page.resizable(False,False)
	game_page.mainloop()

def character_choosing():
	# create a new toplevel
	character_page = Toplevel(root)
	character_page.title("Choose character")
	w = 550
	h = 650
	character_page.configure(background='black')
	
	def game_init_green_hand(event=None):
		global explore_list
		global player_HP
		global game_pygame
		# green hand attributes initialization
		player_HP = player_HP + 30
		explore_list = full_explore_list
		game_pygame = True
		destroy_page(character_page)
		background_intro()
		
	
	def game_init_rich_man(event=None):
		global explore_list
		global money
		global money_increase
		global game_pygame
		# rich man attributes initialization
		money = 25
		money_increase = True
		explore_list = not_full_explore_list
		game_pygame = True
		destroy_page(character_page)
		background_intro()
		
	
	def game_init_solider(event=None):
		global explore_list
		global game_pygame
		global attack
		# solider attributes initialization
		attack = attack + 20
		explore_list = not_full_explore_list
		game_pygame = True
		destroy_page(character_page)
		background_intro()
		

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
	
	desc = Label(character_page,text="There are 3 different character you can choose:",font = 'forte',fg = 'white',bg = 'black')
	
	lab = Label(character_page,text="1. Green hand: initial HP +30,\n explore will get resources for sure.",font = 'forte',fg = 'white',bg = 'black')

	lab_2 = Label(character_page,text='2. Rich man: start money+$20,\n everyday gain $1.',font = 'forte',fg = 'white',bg = 'black')

	lab_3 = Label(character_page,text='3. solider: attack+15.',font = 'forte',fg = 'white',bg = 'black')

	lab.bind("<Button-1>",game_init_green_hand)
	lab.bind("<Enter>",red_text)
	lab.bind("<Leave>",black_text)

	lab_2.bind("<Button-1>",game_init_rich_man)
	lab_2.bind("<Enter>",red_text_2)
	lab_2.bind("<Leave>",black_text_2)

	lab_3.bind("<Button-1>",game_init_solider)
	lab_3.bind("<Enter>",red_text_3)
	lab_3.bind("<Leave>",black_text_3)

	desc.grid(padx=15,pady=30)
	lab.grid()
	lab_2.grid(pady=10)
	lab_3.grid()
	
	character_page.grab_set()
	character_page.resizable(False,False)
	character_page.mainloop()

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
	background_img = Image.open('bg2.jpg')
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
	greet = 'Hi welcome to Rover Diary!'
	canvas.create_text(w/2,h/2-150,fill="black",font=("Forte",20),text=greet)
	
	# rule introduction
	intro_file = open('intro_gui.txt','r+')
	intro_text = intro_file.read()
	intro_file.close()
	canvas.create_text(w/2,h/2+200,fill="black",font=("helvetica",15),text=intro_text)
	canvas.create_text(w/2-200,h/2+550,fill="white",font=("helvetica",15),text='If you are ready, let\'s go!')
	
	def proceed():
		# display character choosing
		destroy_page(intro_page)
		character_choosing()
		
	
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
login_bt = Button(root, text = "GO!",font=('forte',20),command = before_start,width = 10,bg=light_blue,activebackground = light_blue)
login_window = canvas.create_window(250, 380, anchor='nw', window=login_bt)

exit_bt = Button(root, text = "EXIT",font=('forte',20),command = exit,width = 10,bg=light_red,activebackground = light_red)
exit_window = canvas.create_window(450, 380, anchor='nw', window=exit_bt)



root.mainloop()



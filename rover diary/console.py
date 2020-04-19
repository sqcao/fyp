import random
import time
import sys

# 总共一百天
# 目标是活到一百天并打败最终BOSS

# 探索可能会获得：
# 1. 制造用的资源
# 2. 食物
# 3. 金钱
# 4. 伤药

# 小白的特效，每次探索必获得资源
full_explore_list = ['$1','$2','unknown fruit','wormwood','flax','healing grass','wood']
# 默认的，有几率探索不到任何资源
not_full_explore_list = ['$1','$2','unknown fruit','','wormwood','flax','healing grass','','wood']

food_dict = {'unknown fruit':0,'meat':0}

medicine_dict = {'healing grass':0,'magic medicine':0}

manufacture_resouces_dict = {'wormwood':0,'flax':0,'wood':0,'raw meat':0}

food_list = list(food_dict.keys())
medicine_list = list(medicine_dict.keys())
manufacture_resouces_list = list(manufacture_resouces_dict.keys())

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

normal_enermy_HP = {'crazy dog':30*level,'rogue':25*level,'snake':50*level}
normal_enermy_attack = {'crazy dog':10*level,'rogue':15*level,'snake':5*level}
normal_enermy_desc = {'crazy dog':'A crazy dog is chased after you!!!','rogue':'A rogue stops you and want to take your money!!!','snake':'A snake is going to attack you at the back!!!'}

# 特殊怪物
# 小偷没有攻击力，但是每次攻击会偷取你0.1金币
# 流浪猫，没有攻击力，每次攻击有几率偷取食物，如果没有食物它就会逃跑
special_enermy_HP = {'thief':50*level,'cat':50*level}
special_enermy_attack = {'thief':0,'cat':0}
special_enermy_desc = {'thief':'A thief is going to steal your money but you notice him already...','cat':'A homeless cat is staring you at the corner...'}

# 挑战怪物
challenge_enermy_HP = {'shadow':100*level,'killer':80*level}
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
hungary = 100
max_hungary = 100
attack = 20
defence = 0
crit_chance = 0
defend_chance = 0
money = 10
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

def game_intro():
	intro_file = open('intro.txt','r+')
	intro = intro_file.read()
	print(intro)
	intro_file.close()

def slowprint(s):
	for c in s + '\n':
		sys.stdout.write(c)
		sys.stdout.flush() # defeat buffering
		time.sleep(random.random() * 0.08)

def game_init():
	# 游戏开始玩家可选择三种不同职业
	# 小白， 富二代， 战士
	print('\n')
	choice = input('There are 3 different character you can choose:\n1. Green hand: initial HP +30, explore will get resources for sure.\n2. Rich man: start money +$20,everyday gain $10.\n3. solider: attack +15.\n>')
	
	global player_HP
	global max_player_HP
	global explore_list
	global money
	global money_increase
	global attack
	# 不同角色属性初始化
	if(choice == '1'):
		player_HP = player_HP + 30
		max_player_HP = max_player_HP + 30
		explore_list = full_explore_list
	elif(choice == '2'):
		money = 35
		money_increase = True
		explore_list = not_full_explore_list
	elif(choice == '3'):
		attack = attack + 25
		explore_list = not_full_explore_list


	# 游戏故事背景
	print('\n')
	bg_1 = 'After yesterday argument with dad, I run out of home...'
	slowprint(bg_1)
	bg_2 = 'I had enough with him already! I want to prove to everyone that I am the greatest man in the world!'
	slowprint(bg_2)
	time.sleep(1)
	continue_press = input('Press any key to continue...')

# 玩家属性
def display_player_info():
	print('\n*Day',day,'*','energy[',energy,'/',max_energy,']','hungary[',hungary,'/',max_hungary,']')
	print('='*50)
	print('life',life)
	print('attack',attack)
	print('defence',defence)
	print('HP',player_HP,'/',max_player_HP)
	print('money',money)
	print('medicine',medicine_dict)
	print('food',food_dict)
	print('='*50)

def display_enermy_in_fight(HP):
	print('Enermy HP:',HP)

def display_player_in_fight():
	print('Your HP:',player_HP,'/',max_player_HP)
	
def explore():
	# 随机获得探索结果
	global money
	item_get = random.choice(explore_list)
	if('$' in item_get):	# 如果探索到的是钱
		money_get = float(item_get.replace('$',''))
		money = money + money_get
		found_script = 'You found ' + item_get
		slowprint(found_script)
		time.sleep(1)
	else:
		item_num = random.randint(1,3)
		if(item_get == ''):
			found_script = 'You did not found anything...'
			slowprint(found_script)
			time.sleep(1)
		else:
			found_script = 'You found ' + item_get + ' x ' + str(item_num)
			slowprint(found_script)
			time.sleep(1)
			global food_dict
			global medicine_dict
			global manufacture_resouces_dict
			if(item_get in food_list):
				food_dict[item_get] = food_dict[item_get] + item_num
			elif(item_get in medicine_list):
				medicine_dict[item_get] = medicine_dict[item_get] + item_num
			else:
				manufacture_resouces_dict[item_get] = manufacture_resouces_dict[item_get] + item_num

def display_enermy_info(HP,attack,desc):
	# desc 是怪物登场介绍
	print('\n')
	print('-'*len(desc))
	print(desc)
	# 然后再显示怪物基本信息，血量以及攻击力
	print('enermy HP:',HP)
	print('enermy attack:',attack)
	print('-'*len(desc))
	print('\n')

	
def run_in_fight(round):
	# 战斗中随着回合数增加，逃跑几率逐渐增加
	run_init = 0.5
	run = run_init + round*0.1
	random_num = 0.1*(random.randint(0,9))
	if(random_num < run):
		# 逃跑成功
		return True
	else:
		# 逃跑失败
		print('Fail to escape!')
		return False

def player_attack_turn(selected_enermy,HP):
	print('You attack the',selected_enermy)
	print(selected_enermy,'HP -',attack)
	HP = HP - attack
	return HP

def enermy_attack_turn(selected_enermy,enermyAttack):
	global money
	global food_dict
	global player_HP
	if(selected_enermy in special_enermy):
		if(selected_enermy == 'thief'):
			# 不攻击，偷取0.1金币
			print('thief steal your $1 !')
			money = money - 1
		elif(selected_enermy == 'cat'):
			# 不攻击，偷取一个食物
			if(food_dict['unknown fruit'] != 0):
				food_dict['unknown fruit'] = food_dict['unknown fruit'] - 1
				print('cat steal your unknown fruit!')
			elif(food_dict['meat'] != 0):
				food_dict['meat'] = food_dict['meat'] - 1
				print('cat steal your meat!')
			else:
				print('The cat want to steal your food but you have no food.')
				print('The cat bite you!')
				print('HP -10')
				player_HP = player_HP - 10
	else:
		player_HP = player_HP - enermyAttack + defence
		print(selected_enermy,'attacks you, HP -',(enermyAttack-defence))

	

def fight(selected_enermy,HP,enermyAttack):
	global attack
	global defence
	global player_HP
	global max_player_HP
	global life
	# 每回合display怪物的信息，和玩家信息
	round = 1
	attr_increase = 1
	run_result = False
	if(day % 10 == 0):
		attr_increase = attr_increase + 1
	while(HP > 0 and player_HP > 0):
		print('='*18)
		print('*round',round,'*')
		display_enermy_in_fight(HP)
		display_player_in_fight()
		print('='*18)
		# 玩家先选择
		print('\n')
		print('1. Attack\n2. Run')
		choice = input('>')
		choice_valid = False
		while(choice_valid == False):
			if(choice == '1'):
				choice_valid = True
				HP = player_attack_turn(selected_enermy,HP)
			elif(choice == '2'):
				choice_valid = True
				run_result = run_in_fight(round)
			else:
				choice = input('Invalid choice, please check and enter again.')
		if(choice == '2'):
			if(run_result == True):
				break
		if(HP > 0):
			enermy_attack_turn(selected_enermy,enermyAttack)
		round = round + 1
	# 如果逃跑了，那么break之后什么都不用做
	if(run_result == True):
		print('You run away...')
	else:
		if(player_HP <= 0):
			print('Defeat! Life - 1')
			life = life - 1 
		else:
			print('\n')
			print('- '*30)
			print('Victory!')
			if(selected_enermy in challenge_enermy):
				reward = random.choice(challenge_reward)
				print('Congradulation! You have found',reward,'from',selected_enermy)
				special_items.append(reward)
				print('- '*30)
			else:
				reward = random.choice(normal_reward)
				print('You have found',reward,'x3 from',selected_enermy)
				if(reward in food_list):
					food_dict[reward] = food_dict[reward] + 3
				elif(reward in medicine_list):
					medicine_dict[reward] = medicine_dict[reward] + 3
				else:
					manufacture_resouces_dict[reward] = manufacture_resouces_dict[reward] + 3
			attribute_list = ['attack','defence','player_HP']
			attribute = random.choice(attribute_list)

			if(attribute == 'attack'):
				attack = attack + attr_increase
				print('attack + 1')
			elif(attribute == 'defence'):
				defence = defence + attr_increase
				print('defence + 1')
			else:
				max_player_HP = max_player_HP + 10*attr_increase
				print('HP + 10')
			print(' -'*20)

def ask_for_action():
	print('This is a challenge enermy, the enermy is very strong but after victory you will received valueable rewards, do you want to accept the challenge? (y/n)')
	choice_valid = False
	while(choice_valid == False):
		choice = input('>')
		if(choice == 'y'):
			choice_valid = True
			return True
		elif(choice == 'n'):
			choice_valid = True
			return False
		else:
			print('Invalid choice, please check and enter again. Enter (y/n)!')
	
		

def trigger_event():
	# 第十天出现挑战怪物
	if(day % 10 == 0):
		selected_enermy = random.choice(challenge_enermy)
	else:
		normal_special = normal_enermy + special_enermy
		selected_enermy = random.choice(normal_special)
	
	if(selected_enermy in normal_enermy):
		HP = normal_enermy_HP[selected_enermy]
		enermyAttack = normal_enermy_attack[selected_enermy]
		desc = normal_enermy_desc[selected_enermy]
	elif(selected_enermy in special_enermy):
		HP = special_enermy_HP[selected_enermy]
		enermyAttack = special_enermy_attack[selected_enermy]
		desc = special_enermy_desc[selected_enermy]
	else:
		HP = challenge_enermy_HP[selected_enermy]
		enermyAttack = challenge_enermy_attack[selected_enermy]
		desc = challenge_enermy_desc[selected_enermy]
	
	display_enermy_info(HP,enermyAttack,desc)
	# 挑战怪物出现，需要玩家确认是否选择挑战
	if(selected_enermy in challenge_enermy):
		action = ask_for_action(selected_enermy)
		if(action == True):
			# pass HP to fight for ease
			fight(selected_enermy,HP,enermyAttack)
		# 不挑战
		else:
			pass
	else: # 如果不是挑战怪物，直接进入战斗
		fight(selected_enermy,HP,enermyAttack)

def display_manufacture():
	print('\n')
	print('- '*20)
	print('*wood sword* level',wood_sword_level)
	print('attack increase',attack_increase[wood_sword_level])
	print('chance to crit',trigger_crit[wood_sword_level])
	print('To upgrade: (to increase attack and chance to crit)')
	print('[wood] :',sword_need_wood[wood_sword_level])
	print('- '*20)
	print('*tent* level',tent_level)
	print('max energy increase',max_energy_increase[tent_level])
	print('To upgrade: (to increase max energy)')
	print('[wood] :',tent_need_wood[tent_level])
	print('[flax] :',tent_need_flax[tent_level])
	print('- '*20)
	print('*magic medicine* (HP + 100)')
	print('To make:')
	print('[wormwood] :,magic_medicine_need_wormwood')
	print('- '*20)
	print('*meat* (energy + 40)')
	print('To make:')
	print('[raw meat] :',meat_need_raw)
	print('[wood] :',meat_need_wood)
	print('- '*20)
	print('*flax clothing* level',flax_clothing_level)
	print('HP increase',HP_increase[flax_clothing_level])
	print('chance to defend',trigger_defend[flax_clothing_level])
	print('To upgrade: (increase defend chance and max HP)')
	print('[flax] :',flax_clothing_need_flax[flax_clothing_level] )
	print('- '*20)
	print('*trap* level',trap_level)
	print('number of resources trap can get',trap_get_item_num[trap_level])
	print('chance to get resources',trap_chance)
	print('To upgrade: (get more resources at one time)')
	print('[wood] :',trap_need_wood[trap_level])
	print('- '*20)
	print('*bonfire* level',bonfire_level)
	print('recover HP while sleep',sleep_recover_HP[bonfire_level])
	print('To upgrade: (increase amount of HP recover)')
	print('[wood] :',bonfire_need_wood[bonfire_level])
	print('- '*20)
	print('\n')

def manufacture():
	global wood_sword_level
	global manufacture_resouces_dict
	global attack
	global crit_chance
	global tent_level
	global max_energy
	global medicine_dict
	global food_dict
	global flax_clothing_level
	global max_player_HP
	global defend_chance
	global trap_level
	global bonfire_level
	
	item_list = ['wood sword','tent','magic medicine','meat','flax clothing','trap','bonfire']
	print('enter the item that you wish to manufacture:')
	print('If you want to exit the manufacture, please enter exit')
	item = input('>')
	if(item == 'exit'):
		pass
	else:
		if(item in item_list):
			# 选择升级木剑
			if(item == 'wood sword'):
				# 如果所拥有的木材足够了
				if(manufacture_resouces_dict['wood'] >= sword_need_wood[wood_sword_level]):
					# 扣除木材
					manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - sword_need_wood[wood_sword_level]
					# 升级木剑
					wood_sword_level = wood_sword_level + 1
					# 更新玩家属性
					attack = attack + attack_increase[wood_sword_level]
					crit_chance = trigger_crit[wood_sword_level]
				else:
					print('resources is not enough')
			elif(item == 'tent'):
				if(manufacture_resouces_dict['wood'] >= tent_need_wood[tent_level] and manufacture_resouces_dict['flax'] >= tent_need_flax[tent_level]):
					# 扣除材料
					manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - tent_need_wood[tent_level]
					manufacture_resouces_dict['flax'] = manufacture_resouces_dict['flax'] - tent_need_flax[tent_level]
					# 升级帐篷
					tent_level = tent_level + 1
					# 更新玩家属性
					max_energy = max_energy + max_energy_increase
				else:
					print('resources is not enough')
			elif(item == 'magic medicine'):
				if(manufacture_resouces_dict['wormwood'] >= magic_medicine_need_wormwood):
					manufacture_resouces_dict['wormwood'] = manufacture_resouces_dict['wormwood'] - magic_medicine_need_wormwood
					medicine_dict['magic medicine'] = medicine_dict['magic medicine'] + 1
				else:
					print('resources is not enough')
			elif(item == 'meat'):
				if(manufacture_resouces_dict['raw meat'] >= meat_need_raw and manufacture_resouces_dict['wood'] >= meat_need_wood):
					manufacture_resouces_dict['raw_meat'] = manufacture_resouces_dict['raw_meat'] - meat_need_raw
					manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - meat_need_wood
					food_dict['meat'] = food_dict['meat'] + 1
				else:
					print('resources is not enough')
			elif(item == 'flax clothing'):
				if(manufacture_resouces_dict['flax'] >= flax_clothing_need_flax[flax_clothing_level]):
					manufacture_resouces_dict['flax'] = manufacture_resouces_dict['flax'] - flax_clothing_need_flax[flax_clothing_level]
					# 升级麻布衣
					flax_clothing_level = flax_clothing_level + 1
					# 更新玩家属性
					max_player_HP = max_player_HP + HP_increase[flax_clothing_level]
					defend_chance = trigger_defend[flax_clothing_level]
				else:
					print('resources is not enough')
			elif(item == 'trap'):
				if(manufacture_resouces_dict['wood'] >= trap_need_wood[trap_level]):
					manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - trap_need_wood[trap_level]
					trap_level = trap_level + 1
				else:
					print('resources is not enough')
			elif(item == 'bonfire'):
				if(manufacture_resouces_dict['wood'] >= bonfire_need_wood[bonfire_level]):
					manufacture_resouces_dict['wood'] = manufacture_resouces_dict['wood'] - bonfire_need_wood[bonfire_level]
					bonfire_level = bonfire_level + 1
				else:
					print('resources is not enough')
			else:
				print('TBA...')
					
					
		else:
			print('Invalid item name, please try again.')

def get_trap_item():
	global food_dict
	global medicine_dict
	global money
	# 根据陷阱的等级来决定会获得多少个资源
	item = random.choice(full_explore_list)
	print('While sleeping, your trap help you get',item,'x',trap_get_item_num[trap_level])
	if(item in food_list):
		food_dict[item] = food_dict[item] + 1
	elif(item in medicine_list):
		medicine_dict[item] = medicine_dict[item] + 1
	else:
		get_money = int(item.replace('$',''))
		money = money + item

def bonfire_recover_HP():
	global player_HP
	player_HP = player_HP + sleep_recover_HP[bonfire_level]
	if(player_HP > max_player_HP):
		player_HP = max_player_HP

def medicine_manual():
	print(' -'*13)
	print('|healing grass:  HP + 50  |')
	print('|magic medicine: HP + 100 |')
	print(' -'*13)

# price tag
food_price = {'unknown fruit':3,'meat':8}
medicine_price = {'healing grass':5,'magic medicine':10}
manufacture_price = {'wood':1,'flax':2,'raw_meat':2,'wormwood':2}

def shopping():
	global money
	global food_dict
	global medicine_dict
	global manufacture_resouces_dict
	print('Enter the item that you want to buy:')
	print('Enter exit if you wish to exit the shop.')
	buy_item = input('>')
	if(buy_item == 'exit'):
		print('You exit the shop.')
		pass
	else:
		if(buy_item in food_list or buy_item in medicine_list or buy_item in manufacture_resouces_list):
			print('Enter the number of items that you want to buy:')
			buy_num_temp = input('>')
			# check whether enter the valid int
			try:
				buy_num = int(buy_num_temp)
				# if buy food
				if(buy_item in food_list):
					# check whether money is enough
					if(money >= (food_price[buy_item]*buy_num) ):
						money = money - (food_price[buy_item]*buy_num)
						food_dict[buy_item] = food_dict[buy_item] + buy_num
						print('You have bought',buy_num,buy_item)
					else:
						print('money not enough')
				elif(buy_item in medicine_list):
					if(money >= (medicine_price[buy_item]*buy_num) ):
						money = money - (medicine_price[buy_item]*buy_num)
						medicine_dict[buy_item] = medicine_dict[buy_item] + buy_num
						print('You have bought',buy_num,buy_item)
					else:
						print('money not enough')
				else:
					if(money >= (manufacture_price[buy_item]*buy_num) ):
						money = money - (manufacture_price[buy_item]*buy_num)
						manufacture_resouces_dict[buy_item] = manufacture_resouces_dict[buy_item] + buy_num
						print('You have bought',buy_num,buy_item)
					else:
						print('money not enough')
				
			except:
				print('Invalid input, please enter an integer.')
		else:
			print('Invalid input, please enter valid item name.')
					

def display_shops():
	# 商店里卖食物，伤药，制造物资
	print('Your resources: ',manufacture_resouces_dict)
	print('Your money: ',money)
	print('\n')
	print('price in dollar:')
	print(food_price)
	print(medicine_price)
	print(manufacture_price)

def game_loop():
	global energy
	global hungary
	global level
	global day
	global life
	global food_dict
	global player_HP
	global money
	# 游戏主循环
	# when HP or hungary decrease to 0 or when more than 100 days, game over
	while(life > 0 and day <= 100):
		if(day % 10 == 0):	# 每十天提升一次怪物等级
			level = level + 1
		# 每天刚开始，显示玩家属性
		display_player_info()
		# 给出每天可以做的事情
		print('You can:')
		print('1. explore')
		# 开启制造功能
		print('2. manufacture')
		print('3. shopping')
		print('4. use medicine')
		if(energy == 0):
			print('5. sleep')
		
		
		print('\n')
		print('Please enter your choice (enter the number such as 1)')
		choice_valid = False
		while(choice_valid == False):
			choice = input('>')
			if(choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice == '5'):
				choice_valid = True
			else:
				print('Invalid choice, please check and enter again.')
		# 探索
		if(choice == '1'):
			if(energy > 0):
				# 在探索过程中玩家可以获得物品
				# 探索获得普通物品
				explore()
				# 探索过程中也可以触发一些事件
				# 80%的几率随机触发事件
				meet_event_num = [1,2,4,5,6,8,9,10]
				num = random.randint(0,10)
				if(num in meet_event_num):
					trigger_event()
				# 每次探索都扣除10精力和5饥饿
				energy = energy - 10
				hungary = hungary - 5
			else:
				print('Energy is not enough! Please go sleep!')
		
		# 制造
		elif(choice == '2'):
			display_manufacture()
			manufacture()
		
		# 购物
		elif(choice == '3'):
			display_shops()
			shopping()
		
		# 吃药
		elif(choice == '4'):
			medicine_manual()
			print(medicine_dict)
			
			print('please enter the medicine that you want to take.')
			print('Enter back if you wish to go back.')
			take_medicine = input('>')
			if(take_medicine == 'back'):
				pass
			else:
				if(take_medicine in medicine_list):
					if(medicine_dict[take_medicine] != 0):
						medicine_dict[take_medicine] = medicine_dict[take_medicine] - 1
						if(take_medicine == 'healing grass'):
							player_HP = player_HP + 15
							if(player_HP > max_player_HP):
								player_HP = max_player_HP
							print('You take a',take_medicine,'HP + 15.')
						elif(take_medicine == 'magic medicine'):
							player_HP = player_HP + 50
							if(player_HP > max_player_HP):
								player_HP = max_player_HP
							print('You take a',take_medicine,'HP + 50.')
					else:
						print('Not enough',take_medicine,'!')
				else:
					print('Invalid medicine name.')
		
		# 睡觉
		else:
			energy = max_energy
			hungary = hungary - 20
			if(hungary <= 0):
				hungary = 0
				life = life - 1
			day = day + 1
			# everyday increase 1 dollar, for rich man character
			if(money_increase == True):
				money = money + 5
			# 食物是每天自动使用的，如果食物不足会提示
			while(hungary < max_hungary):
				# 优先使用果子，然后使用肉
				if(food_dict['unknown fruit'] != 0):
					food_dict['unknown fruit'] = food_dict['unknown fruit'] - 1
					hungary = hungary + 15
					if(hungary > max_hungary):
						hungary = max_hungary
				elif(food_dict['meat'] != 0):
					food_dict['meat'] = food_dict['meat'] - 1
					hungary = hungary + 40
					if(hungary > max_hungary):
						hungary = max_hungary
				else:
					print('Auto use food: No food to eat.')
					break
			# 如果有升级陷阱，睡觉的时候有30%的几率获得资源
			if(trap_level > 0):
				trap_num = random.randint(0,9)
				# [0,1,2,3,4,5,6,7,8,9]
				if(trap_num == 1 or 5 or 9):
					get_trap_item()
			# 如果有升级篝火，睡觉的时候能恢复生命值
			if(bonfire_level > 0):
				bonfire_recover_HP()
			print('Day',day)
			print('energy +',max_energy,'[',energy,'/',max_energy,']')
			print('hungary - 20 [',hungary,'/',max_hungary,']')
			input('Press to continue...')
		
		
		
		
		

game_intro()
game_init()
game_loop()


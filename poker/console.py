from itertools import repeat
import random
import time

# 最后一次发牌没有remove,player_card没有remove，暂时不用管


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

# convert dict to list of tuples
all_cards_list = random.sample(cards.items(),52)

# 玩家列表,用其所持有的手牌组来代表
order = ['AI 1','AI 2','AI 3','You']

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
	# print('Hey in here!!!!!!')
	print('last used card',last_used_card)
	int_list = []
	decide_card_temp = last_used_card.copy()
	# print('!!!!last_used_card',decide_card_temp)
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

# 自由出牌
def play(card_list):
	current_cards = []
	# print('HEY, HERE IS PLAY')
	# 我只用设计AI的出牌逻辑
	if(card_list == player_card):
		print('It\'s your turn to play, please enter the card you want to use,seperate by comma.')
		ok = False
		display_card()
		while(ok == False):
			is_in = 0
			is_continue = 0
			# 把玩家要出的牌加进一个list里
			current_card = input('>')	# string
			
			# get a list of all values of player card
			test_value_list = []
			test_name_list = []
			for card in card_list:
				test_value_list.append(card[1])
				test_name_list.append(card[0])
			# 单张的话，先看看是否是valid的牌名
			if(',' not in current_card):
				if(current_card in test_name_list):
					ok = True			
			
			else:
				test = current_card.split(',')
				# 确保每个牌名都有'_'
				valid_card_len = 0
				for test_card in test:
					if('_' in test_card):
						valid_card_len = valid_card_len + 1
				if(valid_card_len == len(test)):
					test_int = name_to_int(test)
					# 1. 首先test是否所出的每一张牌都在手牌里
					for card_name in test:
						if(card_name in test_name_list):
							is_in = is_in + 1	# 如果每一张都在，那么ok = True
					# print('how many satisfied',is_in)
					if(is_in == len(test)):
						ok = True
					# print(ok)
					# 如果所出的每一张牌都在手牌里才检查下面的
					if(ok == True):
						# 3. 如果出的是两张，只可能是对子，检查若不是对子，报错
						if(len(test_int) == 2):
							# print('是对子')
							if(test_int[0] != test_int[1]):
								ok = False
						
						# 4. 如果出的是三张以上，就有可能是连对，顺子或者三连
						elif(len(test_int) > 2):
							# 三连
							if(test_int[0] == test_int[1] and test_int[1] == test_int[2]):
								test_int_set = set(test_int)
								# 如果出的都是正确的三连，那么list的长度应该是set的三倍
								if(len(test_int) != 3*len(test_int_set)):
									ok = False
							# 连对
							elif(test_int[0] == test_int[1] and test_int[1] != test_int[2]):
								test_int_set = set(test_int)
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
							# 顺子
							elif(test_int[0] - test_int[1] == 1):
								test_int_set = set(test_int)
								test_int_list = list(test_int_set)
								i_test_1 = 0
								i_test_2 = 1
								while(i_test_2 < len(test_int_list)):
									if(test_int[i_test_1] - test_int[i_test_2] == 1):
										is_continue = is_continue + 1
									i_test_1 = i_test_1 + 1
									i_test_2 = i_test_2 + 1
								if(is_continue != (len(test_int)-1)):
									ok = False
							else:
								print('Error occured')
								ok = False
			
			if(ok == False):
				print('Invalid card pattern, please check your input and enter again')
					
		
		decide_card = current_card.split(',')	# list
		
		# AI 和 player分开return
		# 显示出的牌，然后调用remove_card方法，最后回到主方法
		
		# # convert int list to card name list
		# player_value_list = name_to_int(decide_card)
		
		# print('decide to use cards:',player_value_list)
		print(decide_card)
		decide_card_backup = decide_card.copy()
		new_card_list = remove_card(decide_card,card_list)
		# print('new card list:',new_card_list)
		# print('decide_card has been back up!!!',decide_card_backup)
		# convert decide_card_backup to int list
		decide_card_int_list = name_to_int(decide_card_backup)
		return (new_card_list,decide_card_int_list)
		
	else:
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
					
		
		# 显示哪个AI出的牌
		if(card_list == AI1_card):
			name = 'AI 1'
		elif(card_list == AI2_card):
			name = 'AI 2'
		else:
			name = 'AI 3'
		print(name,'turn :')
	
		# AI 和 player分开return
		# 显示出的牌，然后调用remove_card方法，最后回到主方法
		
		# convert int list to card name list
		name_list = int_to_name(decide_card,card_list)
		decide_card_backup_2 = []
		# print('decide to use cards:',decide_card)
		print(name_list)
		try:
			decide_card_backup_2 = decide_card.copy()
		except AttributeError:
			decide_card_backup_2.append(decide_card)
		new_card_list = remove_card(decide_card_backup_2,card_list)
		# print('new card list:',new_card_list)
		# print('decide card has been removed...',decide_card)
		return (new_card_list,decide_card)

def sort_cards(card_list):
	# keyorder提取卡堆里的卡片名来排序
	keyorder = list(cards.keys())
	sorted_card_list = sorted(card_list,key = lambda x: (keyorder.index(x[0]),x[1]),reverse = True)
	return sorted_card_list

def to_list(input_string):
	# if there is only one card name
	return_list = []
	if(',' not in input_string):
		return_list.append(input_string)
	else:
		return_list = input_string.split(',')
	return return_list



def respond(card_list,last_used_card):
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

	if(card_list == player_card):
		print('\n')
		print('It\'s your turn, please enter cards that you wish to used,if you do not want to use any card, please enter pass instead.')
		print('\n')
		display_card()
		ok_1 = False
		ok_2 = False
		while(ok_1 == False or ok_2 == False):
			len_wish_card = 0
			wish_to_used = input('>')
			if(wish_to_used == 'pass'):
				other_pass.append('You')
				new_card_list = card_list
				break
			else:
				card_name_list = []
				for card_in_list in card_list:
					card_name_list.append(card_in_list[0])
			
				# 输入的是一个string,要转化为列表
				wish_to_used_list_name = to_list(wish_to_used)
				
				
				# card_list is (Hearts_2,15), need to convert to Hearts_2
				for card_wish in wish_to_used_list_name:
					if(card_wish in card_name_list):
						len_wish_card = len_wish_card + 1
				if(len_wish_card == len(wish_to_used_list_name)):
					ok_1 = True
				
							
				if(ok_1 == True):	# 如果所有出的牌都在手牌里，检查下一步
					wish_to_used_list = name_to_int(wish_to_used_list_name)	
					# 1. 如果上一回合出的是单张
					if(len(int_list) == 1):
						# print('last time is one card')
						if(len(wish_to_used_list) == 1):
							if(wish_to_used_list[0] > int_list[0]):
								ok_2 = True
					elif(len(int_list) == 2):	# 对子
						# print('last time is two card')
						if(len(wish_to_used_list) == 2):
							if(wish_to_used_list[0] == wish_to_used_list[1] and wish_to_used_list[0] > int_list[0]):
								ok_2 = True
					else:	# 上一回合出的牌大于两张
						if(len(int_list) == 0):
							print('error, zero length')
						if(int_list[0] == int_list[1] and int_list[1] == int_list[2]):
							# print('last time is three continue')
							# 三连
							if(len(int_list) == len(wish_to_used_list)):
								wish_to_used_set = set(wish_to_used_list)
								new_wish_to_used_list = list(wish_to_used_set)
								continue_three_index_1 = 0
								continue_three_index_2 = 1
								three_len = 1
								while(continue_three_index_2 < len(new_wish_to_used_list)):
									if(new_wish_to_used_list[continue_three_index_1] - new_wish_to_used_list[continue_three_index_2] == 1):
										three_len = three_len + 1
										continue_three_index_1 = continue_three_index_1 + 1
										continue_three_index_2 = continue_three_index_2 + 1
								if(three_len*3 == len(int_list)):
									ok_2 = True
						# 连对
						elif(int_list[0] == int_list[1] and int_list[1] != int_list[2]):
							# print('last time is continue couple')
							if(len(int_list) == len(wish_to_used_list)):
								wish_to_used_set = set(wish_to_used_list)
								new_wish_to_used_list = list(wish_to_used_set)
								continue_couple_index_1 = 0
								continue_couple_index_2 = 1
								couple_len = 1
								while(continue_couple_index_2 < len(new_wish_to_used_list)):
									if(new_wish_to_used_list[continue_couple_index_1] - new_wish_to_used_list[continue_couple_index_2] == 1):
										couple_len = couple_len + 1
										continue_couple_index_1 = continue_couple_index_1 + 1
										continue_couple_index_2 = continue_couple_index_2 + 1
								if(couple_len*2 == len(int_list)):
									ok_2 = True
						# 顺子
						elif(int_list[0] != int_list[1]):
							# print('last time is sequence')
							if(len(int_list) == len(wish_to_used_list)):
								continue_sequence_index_1 = 0
								continue_sequence_index_2 = 1
								sequence_len = 1
								while(continue_sequence_index_2 < len(wish_to_used_list)):
									if(wish_to_used_list[continue_sequence_index_1] - wish_to_used_list[continue_sequence_index_2] == 1):
										sequence_len = sequence_len + 1
										continue_sequence_index_1 = continue_sequence_index_1 + 1
										continue_sequence_index_2 = continue_sequence_index_2 + 1
								if(sequence_len == len(int_list)):
									ok_2 = True
			
			if(ok_1 == False or ok_2 == False and 'You' not in other_pass):
				ok_1 = False
				ok_2 = False
				print('Invalid card pattern, please check your input and enter again.')
		
		if(ok_1 == True and ok_2 == True):
			del other_pass[:]
			respond_card_value_unsort = []
			for card in wish_to_used_list_name:
				card_split = card.split('_')
				try:
					if(card_split[1] == '2'):
						respond_card_value_unsort.append(15)
					else:
						respond_card_value_unsort.append(int(card_split[1]))
				except ValueError:
					if(card_split[1] == 'J'):
						respond_card_value_unsort.append(11)
					elif(card_split[1] == 'Q'):
						respond_card_value_unsort.append(12)
					elif(card_split[1] == 'K'):
						respond_card_value_unsort.append(13)
					elif(card_split[1] == 'A'):
						respond_card_value_unsort.append(14)
					
				
			respond_card_value = sorted(respond_card_value_unsort,reverse = True)
			# print('wish to respond card',respond_card_value)
			new_card_list = remove_card(wish_to_used_list_name,card_list)
		
			
	else:	# 如果是AI的回合
	
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
		if(len(respond_card_value) == 0):
			other_pass.append(this_player)
			print(this_player,': pass.')
			new_card_list = card_list
		else:	# 如果出了牌，那么就需要从手牌中移除出过的牌
			# respond_card_value is the value of respond card, need to get the card name
			respond_card = int_to_name(respond_card_value,card_list)
			print(this_player,':',respond_card)
			respond_card_value_backup = respond_card_value.copy()
			new_card_list = remove_card(respond_card_value_backup,card_list)
			# 每回合出牌结束要做三件事，1.移除出过的牌 2.显示出的牌 3.返回剩余手牌和出过的
			# 还有第四件，如果这回合有人要的起并出了牌，重置other_pass list
			del other_pass[:]
			
	
	if(len(respond_card_value) > 0):	# 如果本回合选择了出牌，那么返回本回合出的牌
		return (new_card_list,respond_card_value)
	else:	# 如果本回合选择pass,那么返回上回合用的牌
		return (new_card_list,last_used_card)


# 每回合来显示各个玩家手牌
def display_card():
	# 玩家的手牌直接显示,只显示牌名不用显示数值
	player_card_display = []
	for card in player_card:
		player_card_display.append(card[0])
	print('=  '*37)
	print('You:',player_card_display)
	print('=  '*37)
	# AI的手牌用X表示
	print('AI 1:','X '*len(AI1_card))
	print('=  '*37)
	print('AI 2:','X '*len(AI2_card))
	print('=  '*37)
	print('AI 3:','X '*len(AI3_card))
	print('=  '*37)
	print('\n')

# 开始打牌直到有一方的手牌出完为止
def game_start():
	# 游戏的第一回合由谁持有红桃3开始出牌
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
	
	print('\n')
	print('Holding ♥_3 first player is',current_player_name,'.')
	print('\n')
	
	
	display_card()
	# current_player is card list, current_player_name is the name of player
	(current_player,current_cards) = play(current_player)

	# 手里有红桃三的玩家已经出完牌了，现在该开始游戏了
	
	first_round = True
	# 如果有一方的手牌出完 游戏结束
	while(len(AI1_card) != 0 and len(AI2_card) != 0 and len(AI3_card) != 0 and len(player_card) != 0):
		
		# display_card(AI1_card,AI2_card,AI3_card,player_card)
		# 得到下一个出牌的玩家
		
		if(current_player == AI1_card):
			current_player_name = 'AI 1'
		elif(current_player == AI2_card):
			current_player_name = 'AI 2'
		elif(current_player == AI3_card):
			current_player_name = 'AI 3'
		elif(current_player == player_card):
			current_player_name = 'You'
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
	
		
		
		
		if(len(other_pass) != 3 or first_round == True):	# 如果有人要的起牌，下个人就必须按照上个人出的牌
			# current_player在上面用来找next player
			first_round = False
			(current_player,current_cards) = respond(next_player,current_cards)
			
			if(current_player == AI1_card):
				name_temp = 'AI 1'
			elif(current_player == AI2_card):
				name_temp = 'AI 2'
			elif(current_player == AI3_card):
				name_temp = 'AI 3'
			elif(current_player == player_card):
				name_temp = 'You'
			else:
				print('ERROR IN PROCEED')
				
			# print('!!!!!!!return current player',name_temp)
			# print('!!!!!!!return current_player card_list',current_player)
			# print('!!!!!!!return current_cards',current_cards)
		else:	# 如果所有其他人都选择了pass，那么该人继续自由出牌
			# print('has other_pass changed?',other_pass)
			# 每次自由出牌都会重置 other_pass
			del other_pass[:]
			(current_player,current_cards) = play(next_player)
			
	
	if(len(AI1_card) == 0):
		winner = 'AI 1'
	elif(len(AI2_card) == 0):
		winner = 'AI 2'
	elif(len(AI3_card) == 0):
		winner = 'AI 3'
	elif(len(player_card) == 0):
		winner = 'You'
	else:
		print('error occured, game over before player finished their cards.')
	print('Game Over,winner is',winner,'!')
	
def game_intro():
	# game intro stored in txt file
	file = open('intro.txt','r')
	print(file.read())
	print('\n')
	input('Press any key to continue...')

def game_init():
	# game intro
	game_intro()
	
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
	
	# 发完牌，游戏开始
	game_start()

game_init()


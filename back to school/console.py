from threading import Timer
import random
import sys
import time

# this will only be called 5 times to get different type of question
def ask_question(question_type):
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
	def time_ran_out(answer):
		print('Jandon:',answer,'\n')
	# we will ask 10 question in total (for each round)
	while(i < 10):
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
		print(' -----------')
		print('|Question',i,'|')
		print(' -----------')
		print(question)
		if(easy == True):
			limit = 15
		else:
			limit = 30
		t=Timer(limit,time_ran_out,(answer,))
		t.start()
		user_input = input('\n>')
		# decide the score result
		timer_str = str(t)
		# if timer not expire and answer correct
		if('stopped' not in timer_str and user_input.lower() == answer):
			print('\nYou win! You are faster than Jandon and your answer is correct!\n')
			num_win += 1
		# I need to have two cases for lost game: 1. time up 2. wrong answer
		elif('stopped' not in timer_str and user_input.lower() != answer):
			print('\nYou lost, your answer is wrong.\n')
			num_lost += 1
		elif('stopped' in timer_str):
			print('\nYou lost, Jandon is faster than you.\n')
			num_lost += 1
		t.cancel()
	if(num_win > num_lost):
		result = 'win'
	elif(num_win == num_lost):
		result = 'match'
	else:
		result = 'lost'
	return result

# i need to separate the whole intro into few parts
# wait user press anykey to continue display next part
def introduction():
	empty_line = 0
	part1 = []
	part2 = []
	part3 = []
	part4 = []
	part5 = []
	part6 = []
	part7 = []
	part8 = []
	part9 = []
	part10 = []
	part11 = []
	part12 = []
	part13 = []
	with open('intro.txt','rt') as intro_file:
		for line in intro_file:
			# from welcome to background_part have 3 empty line
			if(line == '\n'):
				empty_line += 1
			# welcome and rule
			if(empty_line < 3):
				part1.append(line)
			# Background
			elif(empty_line < 4):
				part2.append(line)
			# morning to applause
			elif(empty_line < 6):
				part3.append(line)
			# after you thinking
			elif(empty_line < 8):
				part4.append(line)
			# Jandon self intro
			elif(empty_line < 10):
				part5.append(line)
			# cocky people **************
			elif(empty_line < 11):
				part6.append(line)
			# teacher ask jandon to sit
			elif(empty_line < 12):
				part7.append(line)
			# Jandon walk to you ***************
			elif(empty_line < 13):
				part8.append(line)
			# teacher announce election for class rep
			elif(empty_line < 14):
				part9.append(line)
			# classmates are watching at you ***********
			elif(empty_line < 15):
				part10.append(line)
			# teacher and Jandon say
			elif(empty_line < 17):
				part11.append(line)
			# classmates are watching at Jandon **********
			elif(empty_line < 18):
				part12.append(line)
			else:
				part13.append(line)

	script1 = ('').join(part1)
	script2 = ('').join(part2)
	script3 = ('').join(part3)
	script4 = ('').join(part4)
	script5 = ('').join(part5)
	script6 = ('').join(part6)
	script7 = ('').join(part7)
	script8 = ('').join(part8)
	script9 = ('').join(part9)
	script10 = ('').join(part10)
	script11 = ('').join(part11)
	script12 = ('').join(part12)
	script13 = ('').join(part13)
	
	# create a dict for the script parts
	script_dict = {1:script1,2:script2,3:script3,4:script4,5:script5,6:script6,7:script7,8:script8,9:script9,10:script10,11:script11,12:script12,13:script13}
	# first print the welcome and rule
	print(script1)
	script_no = 2

	def slowprint(s):
		for c in s + '\n':
			sys.stdout.write(c)
			sys.stdout.flush() # defeat buffering
			time.sleep(random.random() * 0.08)


	# while waiting user input to continue the story
	while(script_no < 14):
		input('press enter to continue...')
		print('------------------------------------'*2)
		script_to_print = script_dict[script_no]
		# for the second script, background script, i need it slowly print
		slow_print_list = [2,4,6,8,10,12]
		if(script_no in slow_print_list):
			slowprint(script_to_print)
		# the rest just continue by press enter key
		else:
			print(script_to_print)
		script_no += 1


def game_over():
	print('Thanks for playing our game!')

def show_rule(type):
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
	print(rule_string)

def game():
	introduction()
	challenge_type_list = ['wordbrain','reaction','country','math','language']
	# challenge_type_string = ('\n').join(challenge_type_list)
	print('\n')
	print('------------------------------------'*2)
	print('\nPlease choose a question type to compete with Jandon:')
	for element in challenge_type_list:
		print('>',element)
	challenge_type_choice = input('\n>')
				
	# the type already selected will not be options again, pop out from list
	challenge_type_list.remove(challenge_type_choice)
	print('\nYou: Ok! Let\'s first compete on',challenge_type_choice,'!\n')
	print('------------------------------------'*2)
	print('\nBefore the competion, you need to understand the rule first:\n')
	show_rule(challenge_type_choice)
	input('press enter to start the competition')
	
	# 总共问50个题， take from txt file
	# 每十个做一个总结，谁输谁赢了，然后选下一个问题种类
	your_score = 0
	Jandon_score = 0
	num_type = 1
	
	win_first_time_player = False
	win_more_than_one_time_player = False
	lost_first_time_player = False
	lost_more_than_one_time_player = False
	win_first_time_list_player = []
	win_more_than_one_time_list_player = []
	lost_first_time_list_player = []
	lost_more_than_one_time_list_player = []
	
	win_first_time_jandon = False
	win_more_than_one_time_jandon = False
	lost_first_time_jandon = False
	lost_more_than_one_time_jandon = False
	win_first_time_list_jandon = []
	win_more_than_one_time_list_jandon = []
	lost_first_time_list_jandon = []
	lost_more_than_one_time_list_jandon = []
	# outside the while loop, get all the scripts first and store in list
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
				
	# game logic start from here
	while(num_type <= 5):
		# the first type is already selected
		if(num_type == 1):
			this_round_result = ask_question(challenge_type_choice)	
			# if the result is you win, select [win first time] from player
			# select [lost first time] from Jandon
			
			# if player win
			if(this_round_result == 'win'):
				player_script = random.choice(win_first_time_list_player)
				jandon_script = random.choice(lost_first_time_list_jandon)
				print('You:',player_script,'\n','\nJandon:',jandon_script)
			# if they match
			elif(this_round_result == 'match'):
				print('match.')
			else:
				player_script = random.choice(lost_first_time_list_player)
				jandon_script = random.choice(win_first_time_list_jandon)
				print('Jandon:',jandon_script,'\n','\nYou:',player_script)
				
		else:# 2 round, 3 round and so on
			challenge_type_string2 = ('\n>').join(challenge_type_list)
			print('\n',num_type,'round, which type of question do you want to choose for this round?\n',challenge_type_string2)
			type_choice = input('\n>')
			challenge_type_list.remove(type_choice)
			
			print('\nBefore the competion, you need to understand the rule first:\n')
			show_rule(type_choice)
			input('press enter to start the competition')
			
			this_round_result = ask_question(type_choice)
			# if player win
			if(this_round_result == 'win'):
				player_script = random.choice(win_more_than_one_time_list_player)
				jandon_script = random.choice(lost_more_than_one_time_list_jandon)
				print('You:',player_script,'\n','\nJandon:',jandon_script,'\n')
			# if they match			
			elif(this_round_result == 'match'):
				print('match.')
			else:
				player_script = random.choice(lost_more_than_one_time_list_player)
				jandon_script = random.choice(win_more_than_one_time_list_jandon)
				print('Jandon:',jandon_script,'\n','\nYou:',player_script,'\n')
		num_type += 1
		if(this_round_result == 'win'):
			your_score += 1
		elif(this_round_result == 'lost'):
			Jandon_score += 1
	
	print('--------------------------------')
	print('| 5 rounds competiton complete |')
	print('--------------------------------')
	
	print('--------------------')
	print('|  Your score:',your_score,'  |')
	print('|  Jandon score:',Jandon_score,'|')
	print('--------------------')
	
	win_ending = False
	if(your_score > Jandon_score):
		with open('ending.txt','rt') as ending_file:
			linenum = 0
			for line in ending_file:
				linenum += 1
				if('[win ending]' in line):
					ending_line = linenum
					win_ending = True
				if(win_ending == True and linenum == ending_line + 1):
					print(line)
	else:
		with open('ending.txt','rt') as ending_file:
			linenum = 0
			for line in ending_file:
				linenum += 1
				if('[lost ending]' in line):
					ending_line = linenum
					win_ending = True
				if(win_ending == True and linenum == ending_line + 1):
					print(line)
	game_over()	

game()			
				

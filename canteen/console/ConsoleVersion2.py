# datetime是Python处理日期和时间的标准库。
# datetime 是 module, datetime module 还包含一个datetime class
# 如果只导入import datetime, 那引用必须用全名 datetime.datetime
from datetime import datetime
import calendar

# I need to create my own switch since python don't provide one:
# here I am using dict to do that
def weekday_switcher(day):
	switcher = {
	0:'Monday',
	1:'Tuesday',
	2:'Wedsday',
	3:'Thursday',
	4:'Friday',
	5:'Saturday',
	6:'Sunday'
	}
	today = switcher[day]
	return today

# for get_weekday function and get_hour function
def get_datetime():
	now = datetime.now().replace(microsecond=0)
	return now

def get_weekday():
	# how to decide it's mon or sat only according to the date?
	# 0 is monday, 6 is sunday
	now = get_datetime()
	today = int(now.weekday())
	return today

def get_hour():
	now = get_datetime()
	current_hour = int(now.hour)
	return current_hour

def findDay(input_date):
	weekday = datetime.strptime(input_date,'%d%m%y').weekday()
	return(calendar.day_name[weekday])
	
# greeting function, comparison done by now.hour
def greeting():
	current_hour = get_hour()
	current_time = get_datetime()
	weekday = get_weekday()
	if(current_hour < 12 and current_hour >= 0):
		greet = "morning"
	elif(current_hour>=12 and current_hour<=18):
		greet = "afternoon"
	else:
		greet = "evening"
	# output is 2015-05-18 16:28:07.198690
	print("Hello, good %s !" %greet)
	print(get_datetime())
	print("Today is %s." %weekday_switcher(weekday))
	

	
def get_western_menu(today,current_time):
	weekday = today
	current_hour = current_time
	if(weekday == 'Sunday'):
		return ("Stall closed")
	elif(weekday == 'Saturday'):
		if(current_hour >= 7 and current_hour < 12):
			return (open('Western_bf.txt','r').read())
		elif(current_hour >= 12 and current_hour < 14):
			return (open('Western.txt','r').read())
		else:
			return ("Stall closed")
	else:
		if(current_hour >= 7 and current_hour < 12):
			return (open('Western_bf.txt','r').read())
		elif(current_hour >= 12 and current_hour < 20):
			return (open('Western.txt','r').read())
		else:
			return ("Stall closed")

def get_chicken_rice_menu(today,current_time):
	weekday = today
	current_hour = current_time
	if(weekday == 'Sunday'):
		return ("Stall closed")
	elif(weekday == 'Saturday'):
		if(current_hour >= 10 and current_hour < 14):
			return (open('Chicken_rice.txt','r').read())
		else:
			return ("Stall closed")
	else:
		if(current_hour >= 10 and current_hour < 20):
			return (open('Chicken_rice.txt','r').read())
		else:
			return ("Stall closed")

	
	
	
# now print those stall who have different menu on everyday
def get_malay_menu(today,current_time):
	weekday = today
	current_hour = current_time
	if(weekday == 'Monday' or weekday == 'Wedsday' or weekday == 'Friday'):
		if(current_hour >= 10 and current_hour < 20):
			return(open('Malay_mon.txt','r').read())
		else:
			return ("Stall closed")

	elif(weekday == 'Tuesday' or weekday == 'Thursday'):
		if(current_hour >= 10 and current_hour < 20):
			return(open('Malay_tue.txt','r').read())
		else:
			return ("Stall closed")
	
	elif(weekday == 'Saturday'):
		if(current_hour >= 10 and current_hour < 14):
			# saturday_menu = open('Malay_tue.txt','r')
			return(open('Malay_tue.txt','r').read())
		else:
			return ("Stall closed")
	# for sunday, all canteen stalls are closed
	else:
		return ("Stall closed")

	# now print fast food restaraunt 
	# MC weekday and saturday: 7am - 24pm
	# MC sunday: 10am - 22pm
	
def get_Mc_menu(today,current_time):
	weekday = today
	current_hour = current_time
	if(weekday == 'Sunday'):
		#Mc only sell normal meal on sunday, no breakfast
		if(current_hour >= 10 and current_hour < 22):
			return (open('Mc.txt','r').read())
		else:
			return ("Stall closed")
	else: # weekday and saturday
		if(current_hour >= 7 and current_hour < 11):
			return (open('Mc_bf.txt','r').read())
		elif(current_hour >=11 and current_hour < 24):
			return (open('Mc.txt','r').read())
		else:
			return ("Stall closed")



# Subway weekday: 8am-21pm
# Subway weekend: 11am-18pm		
# Subway only sell normal meal
def get_Subway_menu(today,current_time):
	weekday = today
	current_hour = current_time
	if(weekday == 'Sunday' or weekday == 'Saturday'):
		if(current_hour >= 11 and current_hour < 18):
			return (open('Subway.txt','r').read())
		else:
			return ("Stall closed")
	else: # weekdays
		if(current_hour >= 8 and current_hour < 21):
			return (open('Subway.txt','r').read())
		else:
			return ("Stall closed")

def print_menu():
	weekday = get_weekday()
	today = weekday_switcher(weekday)
	current_hour = get_hour()
	print()
	print("="*10,"Canteen Stall","="*10)
	print("\n")
	print("*"*5,"Western food","*"*5)
	print(get_western_menu(today,current_hour))
	print("\n")
	print("*"*5,"Chicken Rice","*"*5)
	print(get_chicken_rice_menu(today,current_hour))
	print("\n")
	print("*"*5,"Malay food","*"*5)
	print(get_malay_menu(today,current_hour))
	print("\n")
	print("="*10,"Fast Food Restaraunt","="*10)
	print("\n")
	print("*"*5,"Macdonald","*"*5)
	print(get_Mc_menu(today,current_hour))
	print("\n")
	print("*"*5,"Subway","*"*5)
	print(get_Subway_menu(today,current_hour))

def get_Western_OH():
	return (open('western_OH.txt','r').read())

def get_Macdonald_OH():
	return (open('mac_OH.txt','r').read())

def get_Subway_OH():
	return (open('subway_OH.txt','r').read())

def get_Chicken_rice_OH():
	return (open('chicken_rice_OH.txt','r').read())

def get_Malay_OH():
	return (open('malay_OH.txt','r').read())

def checkOH(OH_name):
	stall_name = OH_name
	if(stall_name == 'Western' or stall_name == 'western'):
		operating_hour = get_Western_OH()
	elif(stall_name == 'Macdonald' or stall_name == 'macdonald' or stall_name == 'Mac' or stall_name == 'mac'):
		operating_hour = get_Macdonald_OH()
	elif(stall_name == 'Chicken Rice' or stall_name == 'chicken rice' or stall_name == 'Chicken rice'):
		operating_hour = get_Chicken_rice_OH()
	elif(stall_name == 'Subway' or stall_name == 'subway'):
		operating_hour = get_Subway_OH()
	elif(stall_name == 'Malay' or stall_name == 'malay'):
		operating_hour = get_Malay_OH()
	else:
		operating_hour = "Invalid Stall Name"
	return operating_hour

def waitTime(time_per_pax,numPeople):
	time = time_per_pax
	number_people = numPeople
	waiting_time = number_people*time_per_pax
	return waiting_time

def get_time_per_pax(stall):
	stall_name = stall
	if(stall_name == 'Western' or stall_name == 'western'):
		time_per_pax = 2
	elif(stall_name == 'Macdonald' or stall_name == 'macdonald' or stall_name == 'Mac' or stall_name == 'mac'):
		time_per_pax = 1
	elif(stall_name == 'Chicken Rice' or stall_name == 'chicken rice'):
		time_per_pax = 2
	elif(stall_name == 'Subway' or stall_name == 'subway'):
		time_per_pax = 3
	elif(stall_name == 'Malay' or stall_name == 'malay'):
		time_per_pax = 2
	else:
		time_per_pax = -1
	return time_per_pax

def manualCheckTime(weekday,removed_zero_input_hour):

	if(weekday == 'Sunday'):
		if(removed_zero_input_hour >= 7 and removed_zero_input_hour < 11):
			opening = ">Macdonald"
		elif(removed_zero_input_hour >= 11 and removed_zero_input_hour < 18):
			opening = ">Macdonald\n>Subway"
		elif(removed_zero_input_hour >= 18 and removed_zero_input_hour < 22):
			opening = ">Macdonald"
		else:
			opening = "All stalls are closed"
	elif(weekday == 'Saturday'):
		if(removed_zero_input_hour >= 7 and removed_zero_input_hour < 10):
			opening = ">Macdonald\n>Western"
		elif(removed_zero_input_hour >= 10 and removed_zero_input_hour < 11):
			opening = ">Macdonald\n>Western\n>Chicken Rice\n>Malay"
		elif(removed_zero_input_hour >= 11 and removed_zero_input_hour < 14):
			opening = ">Macdonald\n>Western\n>Chicken Rice\n>Malay\n>Subway"
		elif(removed_zero_input_hour >= 14 and removed_zero_input_hour < 18):
			opening = ">Macdonald\n>Subway"
		elif(removed_zero_input_hour >= 18 and removed_zero_input_hour < 24):
			opening = ">Macdonald"
		else:
			opening = "All stalls are closed"
	else:
		if(removed_zero_input_hour >= 7 and removed_zero_input_hour < 8):
			opening = ">Macdonald"
		elif(removed_zero_input_hour >= 8 and removed_zero_input_hour < 10):
			opening = ">Macdonald\n>Subway\n>Western"
		elif(removed_zero_input_hour >= 10 and removed_zero_input_hour < 20):
			opening = ">Macdonald\n>Subway\n>Western\n>Chicken Rice\n>Malay"
		elif(removed_zero_input_hour >= 20 and removed_zero_input_hour < 21):
			opening = ">Macdonald\n>Subway"
		elif(removed_zero_input_hour >= 18 and removed_zero_input_hour < 24):
			opening = ">Macdonald"
		else:
			opening = "All stalls are closed"
	return opening

def print_choice():
	print('\nDo you want to:')
	print("1. View today's stores\n2. View Stores by other dates\n3. Check stall waiting time\n4. Check store's operating hours\n5. Exit")
	choice = input('>')
	return choice


def check_waiting_time():
	stallName = input("\n\nPlease enter the stall name which you wish to check the waiting time:\n>")
	time_per_pax = get_time_per_pax(stallName)
	if(time_per_pax > 0):
		numPeople = int(input("\nPlease enter the number of people in the queue:\n>"))
		wait_time = waitTime(time_per_pax,numPeople)
		if(wait_time == 1):
			suffix = "min"
		else:
			suffix = "mins"
		print("\nThe estimation waiting time is: ",wait_time,suffix,"\n")
	else:
		print("The stall name you entered is not exist, please re-enter again")
		check_waiting_time()

def check_operating_hour():
	print("="*80)
	OH_name = input("\nPlease enter the stall name which you wish to check the operating hours:\n>")
	operating_hour = checkOH(OH_name)
	if(operating_hour == 'Invalid Stall Name'):
		OH_name = input("Invalid stall name please enter again.\n>")
		check_operating_hour()
	else:
		flag2 = True
		print("\nThe operating hour of",OH_name,"is:\n",operating_hour)

def view_other_date():
	print("\n")
	print("="*80)
	input_date = input("\nPlease enter your desire date(format of date: \'ddmmyy\'):\n>")
	input_time = input("\nPlease enter your desire time in 24 hours format hh:mm(for example: 14:30 stands for 2pm past 30 mins)\n>")
	
	weekday = findDay(input_date)
	input_time_split = input_time.split(":")
	input_hour = input_time_split[0]
	removed_zero_input = input_hour.lstrip("0")
	removed_zero_input_hour = int(removed_zero_input)
	opening_stall = manualCheckTime(weekday,removed_zero_input_hour)
	
	if(opening_stall != "All stalls are closed"):
		opening_stall_split = opening_stall.split("\n")
		print("\n==========Opening stalls==========\n")
		# opening_stall_split_count = len(opening_stall_split)
		for stall in opening_stall_split:				
			if(stall == '>Macdonald'):
				name = '***Macdonald***'
				menu = get_Mc_menu(weekday,removed_zero_input_hour)
			elif(stall == '>Subway'):
				name = '***Subway***'
				menu = get_Subway_menu(weekday,removed_zero_input_hour)
			elif(stall == '>Western'):
				name = '***Western***'
				menu = get_western_menu(weekday,removed_zero_input_hour)	
			elif(stall == '>Chicken Rice'):
				name = '***Chicken rice***'
				menu = get_chicken_rice_menu(weekday,removed_zero_input_hour)
			elif(stall == '>Malay'):
				name = '***Malay***'
				menu = get_malay_menu(weekday,removed_zero_input_hour)
			else:
				menu = "Error occured"
			
			print(name,'\n')
			print(menu,'\n')
	else:
		print(opening_stall)

def start():
	print("="*10,"Canteen Master","="*10)
	print("Canteen Master is an application for student or \nschool faculty to reference daily menu of all\n stalls in the north spine foodcourt in NTU.\nIt also provides waiting time estimation feature.")
	print("="*36,"\n")
	greeting()
	print("\n")
	exit = False
	while(exit == False):
		choice = print_choice()
		if(choice == '1'):
			print_menu()
		elif(choice == '2'):
			view_other_date()
		elif(choice == '3'):
			check_waiting_time()
		elif(choice == '4'):
			check_operating_hour()
		else:
			exit = True
			print('program exiting...')
		
	
			
	
	
	
start()
print("="*80)
print("\n")
input("Press any key to exit...")

	
	


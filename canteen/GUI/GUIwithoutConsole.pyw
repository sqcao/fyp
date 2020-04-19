from tkinter import *
from tkinter import messagebox
import time
from datetime import datetime
import calendar
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import simpledialog
from tkcalendar import DateEntry
from datetime import date




# =========================
def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

root = Tk()
root.wm_title("Canteen Master")

# --- create canvas with scrollbar ---
canvas = Canvas(root, width=750, height=550)
canvas.pack(side = LEFT)
canvas.configure(bg = 'black')
scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=LEFT, fill='y')

canvas.configure(yscrollcommand = scrollbar.set)
# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
canvas.bind('<Configure>', on_configure)
# ==========================
root.resizable(False,False)




# resize the photo
image = Image.open('wall_paper.jpg')
# Image.ANTIALIAS to make the image more smooth
image = image.resize((800,500),Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
canvas.create_image(0,0,image=photo,anchor="nw")


image1 = Image.open('Intro_bg.png')
image1 = image1.resize((650,240),Image.ANTIALIAS)
photo1 = ImageTk.PhotoImage(image1)
canvas.create_image(70,300,image=photo1,anchor="nw")




# function 
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
	return (switcher[day])
	
def get_datetime():
	now = datetime.now().replace(microsecond=0)
	return now
	
def get_weekday():
	# how to decide it's mon or sat only according to the date?
	# 0 is monday, 6 is sunday
	now = get_datetime()
	today = int(now.weekday())
	return today

def findDay(input_date):
	weekday = datetime.strptime(input_date,'%Y %m %d').weekday()
	return(calendar.day_name[weekday])

def get_hour():
	now = get_datetime()
	current_hour = int(now.hour)
	return current_hour
	
def greeting():
	current_hour = get_hour()
	current_time = get_datetime()
	weekday = get_weekday()
	if(current_hour < 12 and current_hour > 0):
		greet = "morning"
	elif(current_hour>12 and current_hour<18):
		greet = "afternoon"
	else:
		greet = "evening"
	return greet

# get all date/time information
date = get_datetime().date()
# today get the value 0 - 6
today = get_weekday()
# weekday get the string value
weekday = weekday_switcher(today)
current_hour = get_hour()



canvas.create_text(170,380,fill="white",font=("Forte",15),
                        text=date)
canvas.create_text(170,410,fill="white",font=("Forte",15),
                        text=weekday)


frame = Frame(canvas)
canvas.create_window((130,430), window=frame, anchor='nw')


class Clock:
	
    def __init__(self):
        self.time1 = ''
		# define the format
        self.time2 = time.strftime('%H:%M:%S')
		# create a container to put the watch
        self.mFrame = Frame()
		# define the position
        self.mFrame.pack(side=TOP,fill=Y,expand=YES)
		
		# create a watch label, with the text updates the timing
        self.watch = Label(frame, text=self.time2, fg = 'white',font=('Forte',15),bg = "#52261D")
		# put at a appropriate position
        self.watch.pack(side=TOP,fill=Y,expand=YES)

        self.changeLabel() #first call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%H:%M:%S')
        self.watch.configure(text=self.time2)
        self.mFrame.after(200, self.changeLabel) #it'll call itself continuously

clock1 = Clock()

greet = greeting()
canvas.create_text(170,480,fill="white",font=("Forte",15),
                        text="Good " + greet + " !")


image2 = Image.open('arrow.png')
# Image.ANTIALIAS to make the image more smooth
image2 = image2.resize((50,50),Image.ANTIALIAS)
photo2 = ImageTk.PhotoImage(image2)
canvas.create_image(500,525,image=photo2,anchor="nw")

canvas.create_text(380,540,fill="white",font=("Forte",15),
                        text="Scroll down for restaurant Info!")



# ====================end of start page==========================


def getOperatingHour(stallName):
	searchStall = stallName.lower()
	stallInfo = []
	with open('all_OH.txt') as OH_file:
		found = False
		for line in OH_file:
			# read until the search stall is found
			if(line.lower().find(searchStall) != -1):
				# append the stall name title to the stallInfo list
				found = True
			# if it's after the search stall
			if(found == True):
				# if it's not the end of operating hour info
				if(line!="\n"):
					# append the info into the stallInfo list
					stallInfo.append(line.rstrip('\n'))
				else:
					break;	
	return stallInfo


# ====================print menu method==========================

# manual and auto all refer to this method
# the stallname and date/hour are passed in
# what this method need to do is compare the given date/time with OH

def get_menu(stallName,date,hour):
	searchStall = stallName.lower()
	current_day = date.lower()
	current_hour = hour
	has_bf = False
	openOnSunday = True
	
	# call getOperatingHour method to get all OH info	
	stallInfo = getOperatingHour(searchStall)
	# what we get from the getOperatingHour method is a list of OH info
	# so we need to separate the list to get individual info
	# check whether the search stall serves breakfast
	# check the second line in the list
	if("breakfast" in stallInfo[1]):
		breakfast1 = stallInfo[1]
		weekday1 = stallInfo[2]
		saturday1 = stallInfo[3]
		sunday2 = stallInfo[4]
		has_bf = True
	else:
		weekday1 = stallInfo[1]
		saturday1 = stallInfo[2]
		sunday2 = stallInfo[3]
	

	# since string is immutable, the only way is replace() and use new string
	if(has_bf == True):
		breakfast = breakfast1.replace('breakfast:','').replace('am','')
		split_breakfast = breakfast.split("-")
		breakfast_start = int(split_breakfast[0])
		breakfast_end = int(split_breakfast[1])
	# no matter has bf or not, below is necessary info
	weekday = weekday1.replace("weekday:","").replace('am','').replace('pm','')
	# the string left with 7-24 format
	# split by "-"
	split_weekday = weekday.split("-")
	weekday_start_OH = int(split_weekday[0])
	weekday_close_OH = int(split_weekday[1])
	
	saturday = saturday1.replace("saturday:","").replace('am','').replace('pm','')
	split_saturday = saturday.split("-")
	saturday_start_OH = int(split_weekday[0])
	saturday_close_OH = int(split_weekday[1])
	
	sunday1 = sunday2.replace("sunday:","")
	if(sunday1 == 'closed'):
		openOnSunday = False
	else:
		sunday = sunday1.replace("am","").replace('pm','')
		split_sunday = sunday.split("-")
		sunday_start_OH = int(split_sunday[0])
		sunday_close_OH = int(split_sunday[1])
	
	# now we have all date and time from OH ready
	# can compare the system/input date&time with OH already
	
	# apply date condition first
	# 135 24 67 three case 
	weekday = ['monday','tuesday','wedsday','thursday','friday']

	# now find out if stall serves different menu
	stallNameAppearTimes = 0
	# offer different menu
	hasDifferentMenu = False
	with open('all_menu.txt') as searchName_file:
		for line in searchName_file:
			if(line.lower().find(searchStall) != -1):
				# if appear times is more than 1, means it offer different menu
				if(line.lower().find("-bf") == -1):
					stallNameAppearTimes += 1
	if(stallNameAppearTimes > 1):
		hasDifferentMenu = True
	Mon_Wed_Fri = ['monday','wedsday','friday']
	Tue_Thur = ['tuesday','thursday']
	found1 = False
	stallMenu = []
	# treat stall with different menu specially, it checks 135 24 and weekend
	if(hasDifferentMenu):
	# so far only malay has different menu and it does not serve bf
		#============================135==============================
		if(current_day in Mon_Wed_Fri):
			if(current_hour >= weekday_start_OH and current_hour < weekday_close_OH):
				with open('all_menu.txt') as menu_file:
					searchStallMon = searchStall + "-135"
					for line in menu_file:
						if(line.lower().find(searchStallMon) != -1):
							found1 = True
						if(found1 == True):
							# if it's not the end of operating hour info
							if(line!="\n"):
								# append the menu into the stallMenu list
								stallMenu.append(line)
							else:
								break;	
			else:
				stallMenu.append("Stall closed")
		#============================24==============================
		elif(current_day in Tue_Thur):
			if(current_hour >= weekday_start_OH and current_hour < weekday_close_OH):
				with open('all_menu.txt') as menu_file:
					searchStallTue = searchStall + "-246"
					for line in menu_file:
						if(line.lower().find(searchStallTue) != -1):
							found1 = True
						if(found1 == True):
							# if it's not the end of operating hour info
							if(line!="\n"):
								# append the menu into the stallMenu list
								stallMenu.append(line)
							else:
								break;	
			else:
				stallMenu.append("Stall closed")
	#============================Saturday==============================		
	# saturday not serving breakfast, only normal meal
		elif(current_day == 'saturday'):
			if(current_hour >= saturday_start_OH and current_hour < saturday_close_OH):
				with open('all_menu.txt') as menu_file:
						searchStallTue = searchStall + "-246"
						for line in menu_file:
							if(line.lower().find(searchStallTue) != -1):
								found1 = True
							if(found1 == True):
								# if it's not the end of operating hour info
								if(line!="\n"):
									# append the menu into the stallMenu list
									stallMenu.append(line)
								else:
									break;	
			else:
				stallMenu.append("Stall closed")
	#============================Sunday==============================		
		else:
			if(openOnSunday == True):
				if(current_hour >= sunday_start_OH and current_hour < sunday_close_OH):
					with open('all_menu.txt') as menu_file:
						for line in menu_file:
							if(line.lower().find(searchStall) != -1):
								found1 = True
							if(found1 == True):
								# if it's not the end of operating hour info
								if(line!="\n"):
									# append the menu into the stallMenu list
									stallMenu.append(line)
								else:
									break;	
				else:
					stallMenu.append("Stall closed")
			# the stall is not open on sunday
			else:
				stallMenu.append("Stall closed")
	#================================================================
	# if the stall do not offer different menu
	else:
		if(current_day in weekday):
			if(has_bf == True):
				# if the search stall serve bf, attach the suffix to the stall name according to the format in menu text file
				searchStallBf = searchStall + "-bf"	# concatenation
				if(current_hour >= breakfast_start and current_hour < breakfast_end):
					with open('all_menu.txt') as menu_file:
						for line in menu_file:
							if(line.lower().find(searchStallBf) != -1):
								found1 = True
							if(found1 == True):
								# if it's not the end of operating hour info
								if(line!="\n"):
									# append the menu into the stallMenu list
									stallMenu.append(line)
								else:
									break;	
				elif(current_hour >= breakfast_end and current_hour < weekday_close_OH):
					with open('all_menu.txt') as menu_file:
						for line in menu_file:
							if(line.lower().find(searchStall) != -1):
								# only the normal menu will set found1 to true
								if(line.find("-bf") == -1):
									found1 = True
							if(found1 == True):
								if(line!="\n"):
									stallMenu.append(line)
								else:
									break;	
				else:
					stallMenu.append("Stall closed")
			# if the stall do not serves breakfast
			else:	
				if(current_hour >= weekday_start_OH and current_hour < weekday_close_OH):
					with open('all_menu.txt') as menu_file:
						for line in menu_file:
							if(line.lower().find(searchStall) != -1):
								# only the normal menu will set found1 to true
								if(line.find("-bf") == -1):
									found1 = True
							if(found1 == True):
								if(line!="\n"):
									stallMenu.append(line)
								else:
									break;	
				else:
					stallMenu.append("Stall closed")
		elif(current_day == 'saturday'):
			if(current_hour >= saturday_start_OH and current_hour < saturday_close_OH):
					with open('all_menu.txt') as menu_file:
						for line in menu_file:
							if(line.lower().find(searchStall) != -1):
								# only the normal menu will set found1 to true
								if(line.find("-bf") == -1):
									found1 = True
							if(found1 == True):
								if(line!="\n"):
									stallMenu.append(line)
								else:
									break;	
			else:
				stallMenu.append("Stall closed")
		#sunday
		else:
			if(openOnSunday == True):
				if(current_hour >= sunday_start_OH and current_hour < sunday_close_OH):
					with open('all_menu.txt') as menu_file:
						for line in menu_file:
							if(line.lower().find(searchStall) != -1):
								# only the normal menu will set found1 to true
								if(line.find("-bf") == -1):
									found1 = True
							if(found1 == True):
								if(line!="\n"):
									stallMenu.append(line)
								else:
									break;	
				else:
					stallMenu.append("Stall closed")
			else:
				stallMenu.append("Stall closed")
	
	# format the output menu
	print(current_hour)
	print(searchStall)
	print(stallMenu)
	stallMenu.pop(0)
	menu = ("\n").join(stallMenu)
	
	# clear for next method call
	stallMenu.clear()
	return menu
	

# ====================end of menu method==========================



# ================title for fastfood and canteen==================


image_fd1 = Image.open('title.png')
image_fd1 = image_fd1.resize((300,60),Image.ANTIALIAS)
photo_fd1 = ImageTk.PhotoImage(image_fd1)
canvas.create_image(250,620,image=photo_fd1,anchor="nw")
canvas.create_text(400,620,fill="white",font=("Forte",20),
                        text="Fast Food Restaraunt")

# title for canteen store
image_fd2 = Image.open('title.png')
image_fd2 = image_fd2.resize((300,60),Image.ANTIALIAS)
photo_fd2 = ImageTk.PhotoImage(image_fd2)
canvas.create_image(250,1800,image=photo_fd2,anchor="nw")
canvas.create_text(400,1800,fill="white",font=("Forte",20),
                        text="Canteen Stalls")

# ================end title fastfood and canteen==================


# ====================menu template field=========================
						
image_menu1 = Image.open('mac_menu.png')
# Image.ANTIALIAS to make the image more smooth
image_menu1 = image_menu1.resize((600,500),Image.ANTIALIAS)
photo_menu1 = ImageTk.PhotoImage(image_menu1)
canvas.create_image(100,680,image=photo_menu1,anchor="nw")

image_menu2 = Image.open('subway_menu.png')
# Image.ANTIALIAS to make the image more smooth
image_menu2 = image_menu2.resize((600,500),Image.ANTIALIAS)
photo_menu2 = ImageTk.PhotoImage(image_menu2)
canvas.create_image(100,1200,image=photo_menu2,anchor="nw")						
						
image_menu3 = Image.open('western_menu.png')
# Image.ANTIALIAS to make the image more smooth
image_menu3 = image_menu3.resize((600,500),Image.ANTIALIAS)
photo_menu3 = ImageTk.PhotoImage(image_menu3)
canvas.create_image(100,1900,image=photo_menu3,anchor="nw")

image_menu4 = Image.open('Chicken_rice_menu.png')
# Image.ANTIALIAS to make the image more smooth
image_menu4 = image_menu4.resize((600,500),Image.ANTIALIAS)
photo_menu4 = ImageTk.PhotoImage(image_menu4)
canvas.create_image(100,2460,image=photo_menu4,anchor="nw")

image_menu5 = Image.open('malay_menu.png')
# Image.ANTIALIAS to make the image more smooth
image_menu5 = image_menu5.resize((600,500),Image.ANTIALIAS)
photo_menu5 = ImageTk.PhotoImage(image_menu5)
canvas.create_image(100,3020,image=photo_menu5,anchor="nw")


# ==================end menu template field=======================



# ======================read menu field===========================

mc_menu = get_menu("Macdonald",weekday,current_hour)

canvas.create_text(545,920,fill="white",font=("Forte",12),
                        text=mc_menu)
						
subway_menu = get_menu("Subway",weekday,current_hour)

canvas.create_text(540,1450,fill="white",font=("Forte",12),
                        text=subway_menu)

western_menu = get_menu("Western",weekday,current_hour)

canvas.create_text(550,2080,fill="white",font=("Forte",12),
                        text=western_menu)

Chicken_rice_menu = get_menu("Chicken rice",weekday,current_hour)

canvas.create_text(540,2620,fill="white",font=("Forte",12),
                        text=Chicken_rice_menu)
						
Malay_menu = get_menu("Malay",weekday,current_hour)

canvas.create_text(540,3180,fill="white",font=("Forte",12),
                        text=Malay_menu)

# ========================end menu read===========================



# def manualCheckTime():
	# input_date = simpledialog.askstring("Input Date","Please enter your desire date(format of date: \'ddmmyy\'):",parent = root)
	# weekday = findDay(input_date)
	
	# input_time = simpledialog.askstring("Input Time","Please enter your desire time in 24 hours format hh:mm(for example: 14:30 stands for 2pm past 30 mins):",parent = root) # time string can be 1230 , divide 1230 by 100, get 12
	# input_time_split = input_time.split(":")
	# input_hour = input_time_split[0]
	# removed_zero_input = input_hour.lstrip("0")
	# removed_zero_input_hour = int(removed_zero_input)
	# # input_time = input_time_split[1]
	# # since the current operating hour is all exactly hour, minute is not used

	
	# if(weekday == 'Sunday'):
		# if(removed_zero_input_hour >= 7 and removed_zero_input_hour < 11):
			# opening = ">Macdonald"
		# elif(removed_zero_input_hour >= 11 and removed_zero_input_hour < 18):
			# opening = ">Macdonald\n>Subway"
		# elif(removed_zero_input_hour >= 18 and removed_zero_input_hour < 22):
			# opening = ">Macdonald"
		# else:
			# opening = "All stalls are closed"
	# elif(weekday == 'Saturday'):
		# if(removed_zero_input_hour >= 7 and removed_zero_input_hour < 10):
			# opening = ">Macdonald\n>Western"
		# elif(removed_zero_input_hour >= 10 and removed_zero_input_hour < 11):
			# opening = ">Macdonald\n>Western\n>Chicken Rice\n>Malay"
		# elif(removed_zero_input_hour >= 11 and removed_zero_input_hour < 14):
			# opening = ">Macdonald\n>Western\n>Chicken Rice\n>Malay\n>Subway"
		# elif(removed_zero_input_hour >= 14 and removed_zero_input_hour < 18):
			# opening = ">Macdonald\n>Subway"
		# elif(removed_zero_input_hour >= 18 and removed_zero_input_hour < 24):
			# opening = ">Macdonald"
		# else:
			# opening = "All stalls are closed"
	# else:
		# if(removed_zero_input_hour >= 7 and removed_zero_input_hour < 8):
			# opening = ">Macdonald"
		# elif(removed_zero_input_hour >= 8 and removed_zero_input_hour < 10):
			# opening = ">Macdonald\n>Subway\n>Western"
		# elif(removed_zero_input_hour >= 10 and removed_zero_input_hour < 20):
			# opening = ">Macdonald\n>Subway\n>Western\n>Chicken Rice\n>Malay"
		# elif(removed_zero_input_hour >= 20 and removed_zero_input_hour < 21):
			# opening = ">Macdonald\n>Subway"
		# elif(removed_zero_input_hour >= 18 and removed_zero_input_hour < 24):
			# opening = ">Macdonald"
		# else:
			# opening = "All stalls are closed"
			
	# if(opening != "All stalls are closed"):
		# opening_stall_split = opening.split("\n")
		# # opening_stall_split_count = len(opening_stall_split)
		# # name_list = []
		# menu_list = []
		# for stall in opening_stall_split:				
			# if(stall == '>Macdonald'):
				# name = '***Macdonald***'
				# menu = get_Mc_menu_manual(weekday,removed_zero_input_hour)
			# elif(stall == '>Subway'):
				# name = '***Subway***'
				# menu = get_Subway_menu_manual(weekday,removed_zero_input_hour)
			# elif(stall == '>Western'):
				# name = '***Western***'
				# menu = get_western_menu_manual(weekday,removed_zero_input_hour)	
			# elif(stall == '>Chicken Rice'):
				# name = '***Chicken rice***'
				# menu = get_chicken_rice_menu_manual(weekday,removed_zero_input_hour)
			# elif(stall == '>Malay'):
				# name = '***Malay***'
				# menu = get_malay_menu_manual(weekday,removed_zero_input_hour)
			# else:
				# menu = "Error occured"

			# menu_list.append(name)
			# menu_list.append("\n")
			# menu_list.append(menu)
			# menu_list.append("\n\n")
			# menu_string = "".join(menu_list)

		# messagebox.showinfo("Opening Stalls",menu_string)
	# else:
		# messagebox.showinfo("Opening Stalls","All stalls are closed")
	
	






# ====================check waiting time==========================

def waitTime(stall):
	stall_name = stall
	if(stall_name == 'Western'):
		time_per_pax = 2
	elif(stall_name == 'Macdonald'):
		time_per_pax = 1
	elif(stall_name == 'Chicken Rice'):
		time_per_pax = 2
	elif(stall_name == 'Subway'):
		time_per_pax = 3
	elif(stall_name == 'Malay'):
		time_per_pax = 2
	else:
		time_per_pax = -1
	number_people = simpledialog.askinteger("Input","Please enter the number of people in the queue:",parent = root)
	waiting_time = number_people*time_per_pax
	messagebox.showinfo("Waiting time",("Estimated waiting time is: %s mins" %waiting_time))

# wait time for Mac
button1 = Button(root, text = "Waiting Time",command = lambda: waitTime("Macdonald"),anchor = 'nw',width = 11,bg='white',activebackground = "white")
button_window1 = canvas.create_window(120, 665, anchor='nw', window=button1)

# wait time for Subway
button2 = Button(root, text = "Waiting Time",command = lambda: waitTime("Subway"),anchor = 'nw',width = 11,bg='white',activebackground = "white")
button_window2 = canvas.create_window(120, 1190, anchor='nw', window=button2)

# wait time for western
button3 = Button(root, text = "Waiting Time",command = lambda: waitTime("Subway"),anchor = 'nw',width = 11,bg='white',activebackground = "white")
button_window3 = canvas.create_window(115, 1880, anchor='nw', window=button3)

# wait time for Chicken rice
button4 = Button(root, text = "Waiting Time",command = lambda: waitTime("Chicken Rice"),anchor = 'nw',width = 11,bg='white',activebackground = "white")
button_window4 = canvas.create_window(115, 2440, anchor='nw', window=button4)

# wait time for Malay food
button5 = Button(root, text = "Waiting Time",command = lambda: waitTime("Malay"),anchor = 'nw',width = 11,bg='white',activebackground = "white")
button_window5 = canvas.create_window(120, 3010, anchor='nw', window=button5)

# ==================end of check waiting time=====================


# ====================get operating hours=========================


def printOperatingHour(stallName):
	stall_to_be_search = stallName
	stallInfo = getOperatingHour(stall_to_be_search)
	stallInfoFormatter = ("\n").join(stallInfo)
	messagebox.showinfo("operating hour",stallInfoFormatter)


# operating time for Mac
button11 = Button(root, text = "Operating Hours",command =lambda: printOperatingHour("Macdonald"),anchor = 'nw',width = 13,bg='white',activebackground = "white")
button_window11 = canvas.create_window(208, 665, anchor='nw', window=button11)

# operating time for Subway
button12 = Button(root, text = "Operating Hours",command =lambda: printOperatingHour("Subway"),anchor = 'nw',width = 13,bg='white',activebackground = "white")
button_window12 = canvas.create_window(208, 1190, anchor='nw', window=button12)

# operating time for Western
button13 = Button(root, text = "Operating Hours",command =lambda: printOperatingHour("Western"),anchor = 'nw',width = 13,bg='white',activebackground = "white")
button_window13 = canvas.create_window(203, 1880, anchor='nw', window=button13)

# operating time for Chicken rice
button14 = Button(root, text = "Operating Hours",command =lambda: printOperatingHour("Chicken Rice"),anchor = 'nw',width = 13,bg='white',activebackground = "white")
button_window14 = canvas.create_window(203, 2440, anchor='nw', window=button14)

# operating time for Malay food
button15 = Button(root, text = "Operating Hours",command =lambda: printOperatingHour("Malay"),anchor = 'nw',width = 13,bg='white',activebackground = "white")
button_window15 = canvas.create_window(208, 3010, anchor='nw', window=button15)


# ====================end of operating hours======================

def exitProgram():
	root.quit()

def autoViewMenu(t1):
	# if user choose to view menu by system time, we just close this toplevel
	t1.destroy()

def destroyt4(t4):
	t4.destroy()

def newWindow(selectedStoreMenu):
	storeMenu = selectedStoreMenu
	t4 = Toplevel(root)
	t4.title("Canteen System")
	t4.geometry("300x250+250+150")
	frame4 = Frame(t4)
	frame4.pack()
	Label(frame4, text=storeMenu,font='forte,10').pack(pady=30)
	back = Button(frame4,text="Back",command=lambda:destroyt4(t4),bg='#659EC7',activebackground='#659EC7',width = 30)
	back.pack()
	t4.grab_set()

def destroyt3(t3):
	t3.destroy()

def gotoDisplay(input_date,input_hour,input_minute):
	inputDate = str(input_date)
	inputHour = int(input_hour)
	inputHourStr = str(input_hour)
	if(len(inputHourStr)==1):
		inputHourStr = '0'+inputHourStr
	inputMinute = int(input_minute)
	inputMinuteStr = str(input_minute)
	if(len(inputMinuteStr)==1):
		inputMinuteStr = '0'+inputMinuteStr
	t3 = Toplevel(root)
	t3.title("Canteen System")
	t3.geometry("300x280+250+150")
	frame3 = Frame(t3)
	frame3.pack()
	
	
	# instead of direct print all the menu and stall name,
	# we list out all the opening stall name
	
	# first get all OH
	inputDateFormat = inputDate.replace('-',' ')
	# return the day in a week to decide which stall is open at the input date and time
	# since findDay method only take format as ddmmyy 
	# i need to convert the date format
	
	inputWeekday = findDay(inputDateFormat)
	
	showTime = Label(frame3,text=inputWeekday+','+inputDate+','+inputHourStr+':'+inputMinuteStr,font='forte,10',width=250)
	showTime.pack()
	showTime.configure(bg="yellow")
	Label(frame3, text='Choose a store',font='forte,10').pack(pady=10)
	
	# call call get_menu method
	# if the return value is not closed or stall closed
	# means the stall is opening at the given inputDate and time
	returnValue1 = get_menu('Macdonald',inputWeekday,inputHour)
	# the return value is the menu for the stall
	
	def showMenu(storeName):
		if(storeName == 'Macdonald'):
			displayInNewWindow = returnValue1
		elif(storeName == 'Subway'):
			displayInNewWindow = returnValue2
		elif(storeName == 'Western'):
			displayInNewWindow = returnValue3
		elif(storeName == 'Chicken rice'):
			displayInNewWindow = returnValue4
		elif(storeName == 'Malay'):
			displayInNewWindow = returnValue5
		newWindow(displayInNewWindow)
	
	# if the stall is open, display the button in the toplevel frame
	if(returnValue1 != ''):
		MacButton = ttk.Button(frame3,text="Macdonald",command=lambda:showMenu("Macdonald"),width = 30)
		MacButton.pack(pady=3)
	
	returnValue2 = get_menu('Subway',inputWeekday,inputHour)
	if(returnValue2 != ''):
		SubButton = ttk.Button(frame3,text="Subway",command=lambda:showMenu("Subway"),width = 30)
		SubButton.pack(pady=3)
	
	returnValue3 = get_menu('Western',inputWeekday,inputHour)
	if(returnValue3 != ''):
		WesButton = ttk.Button(frame3,text="Western",command=lambda:showMenu("Western"),width = 30)
		WesButton.pack(pady=3)
	
	returnValue4 = get_menu('Chicken rice',inputWeekday,inputHour)
	if(returnValue4 != ''):
		ChiButton = ttk.Button(frame3,text="Chicken rice",command=lambda: showMenu("Chicken rice"),width = 30)
		ChiButton.pack(pady=3)
	
	returnValue5 = get_menu('Malay',inputWeekday,inputHour)
	if(returnValue5 != ''):
		MalayButton = ttk.Button(frame3,text="Malay",command=lambda:showMenu("Malay"),width = 30)
		MalayButton.pack(pady=3)
	
	back = Button(frame3,text='back',command=lambda:destroyt3(t3),bg='#659EC7',activebackground='#659EC7',width=30)
	back.pack(pady=6)
	t3.grab_set()
	
	
def backFuntion1(t2):
	t2.destroy()
	

def viewByOtherDate(t1):
	t2= Toplevel(root)
	t2.title("Select date and time")
	t2.geometry("300x180+250+150")
	frame2 = Frame(t2)
	frame2.pack()
	# select date
	ttk.Label(frame2, text='Choose a date').grid(row=0,column=1,columnspan=2,pady=10)
	calendar = DateEntry(frame2, width=12, background='darkblue',foreground='white', borderwidth=2)
	calendar.grid(row=1,column=1,columnspan=2)
	
	
	# select time
	ttk.Label(frame2,text='Choose a time').grid(row=2,column=1,columnspan=2,pady=10)
	hourChosen = ttk.Combobox(frame2, width=12)
	hour = []
	for i in range(25):
		hour.append(i)
	hourChosen['values'] = hour 
	hourChosen.grid(row=3,column=1)
	hourChosen.set('hour')  
	
	minuteChosen = ttk.Combobox(frame2, width=12)
	minute = []
	for j in range(61):
		minute.append(j)
	minuteChosen['values'] = minute
	minuteChosen.grid(row=3,column=2)  
	minuteChosen.set('minute')  
	
	def timeSelect(virtualEventObject):
		confirmDateTimeBt['state'] = 'normal'
	
	hourChosen.bind("<<ComboboxSelected>>",timeSelect)
	
	def confirmDateTime():
		ok = False
		input_date = calendar.get_date()
		input_hour = hourChosen.get()
		input_minute = minuteChosen.get()
		gotoDisplay(input_date,input_hour,input_minute)

	# confirm button
	confirmDateTimeBt = ttk.Button(frame2,text="confirm",command=confirmDateTime,state = 'disabled')
	confirmDateTimeBt.grid(row=4,column=1,pady=18)
	
	# back button
	backBt = Button(frame2,text="back",command=lambda:backFuntion1(t2),bg='#659EC7',activebackground='#659EC7',width=10)
	backBt.grid(row=4,column=2,pady=18)
	t2.grab_set()


def startfunc():
	t1 = Toplevel(root)
	t1.title("Get Start")
	t1.geometry("300x220+250+150")
	frame1 = Frame(t1)
	frame1.pack()
	
	welcomeMsgbody = ttk.Label(frame1,text="Nanyang Technological University\n Welcome to Canteen A Menu System")
	welcomeMsgbody.pack(pady=25)
	autoViewMenuButton = ttk.Button(frame1,text="View today's stores",command=lambda: autoViewMenu(t1),width = 25)
	autoViewMenuButton.pack()
	manualViewMenuButton = ttk.Button(frame1,text="View Stores by other dates",command=lambda: viewByOtherDate(t1),width=25)
	manualViewMenuButton.pack(pady=5)
	exitButton = Button(frame1,text="Exit Program",width=21,command=exitProgram,bg='#F75D59',activebackground='#F75D59')
	exitButton.pack(pady=20)
	# get the focus
	t1.grab_set()

button_manualCheck = Button(root, text = "Home Menu",command = startfunc,anchor = 'n',width = 15,bg='white',activebackground = "white")
manual_window = canvas.create_window(10,10, anchor='nw', window=button_manualCheck)

startfunc()
# --- start program ---
root.mainloop()

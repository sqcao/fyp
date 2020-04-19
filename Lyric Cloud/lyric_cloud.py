from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import sys
import re
import os
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np
from lxml import etree
from textblob import TextBlob


## ========================word cloud part============================
headers = {
		'Referer'  :'http://music.163.com',
		'Host'     :'music.163.com',
		'Accept'   :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent':'Chrome/10'
		}
	
def get_song_lyric(headers,lyric_url):
	res = requests.request('GET', lyric_url, headers=headers)
	if 'lrc' in res.json():
		lyric = res.json()['lrc']['lyric']
		new_lyric = re.sub(r'[\d:.[\]]','',lyric)
		return new_lyric
	else:
		return ''
		print(res.json())

def remove_stop_words(f):
	# self-define stop words
	stop_words = ['Taylor Swift','周杰伦','方文山','工作室','立酱','作词', '作曲', '编曲', 'Arranger', '录音', '混音', '人声', 'Vocal', '弦乐', 'Keyboard', '键盘', '编辑', '助理', 'Assistants', 'Mixing', 'Editing', 'Recording', '音乐', '制作', 'Producer', '发行', 'produced', 'and', 'distributed']
	for stop_word in stop_words:
		f = f.replace(stop_word, '')
	return f

def create_lyric_cloud(f):
	print('finished word tokenization!')
	print('start to create lyric cloud...')
	# first remove the stop words
	f = remove_stop_words(f)
	# then use the jieba to tokenize the lyric sentences
	cut_text = " ".join(jieba.cut(f,cut_all=False, HMM=True))
	wc = WordCloud(
		font_path="simhei.ttf",
		max_words=100,
		width=2000,
		height=1200,
	)
	print(cut_text)
	wordcloud = wc.generate(cut_text)
	# create jpg file
	wordcloud.to_file("wordcloud.jpg")
	# # use matplotlib to display
	# plt.imshow(wordcloud)
	# plt.axis("off")
	# plt.show()	
	
	# just display the jpg file in a new window
	wordcloud_window = Toplevel(root)
	wordcloud_window.title("Lyric Cloud")
	canvas = Canvas(wordcloud_window, width=750, height=480)
	canvas.pack(side = LEFT)
	canvas.configure(bg = 'black')
	# resize the photo
	image = Image.open('wordcloud.jpg')
	# Image.ANTIALIAS to make the image more smooth
	image = image.resize((700,400),Image.ANTIALIAS)
	photo = ImageTk.PhotoImage(image)
	canvas.create_image(20,20,image=photo,anchor="nw")
	
	def check_sentiment(text):
		blob = TextBlob(text)
		combine_value = blob.sentiment
		sentiment_value = combine_value[0]
		subjective_value = combine_value[1]
		sentiment = 'positive' if sentiment_value > 0.5 else 'negative'
		subjective = 'subjective' if subjective_value > 0.5 else 'objective'
		messagebox.showinfo('sentiment analysis',"This singer's lyrics are tend to be "+sentiment+", this analysis result is quite "+subjective)
	
	# button to check the sentiment of overall lyric
	sentiment_button = Button(wordcloud_window, text = "check sentiment",command = lambda: check_sentiment(cut_text),anchor = 'nw',width = 14,bg='grey',fg = 'white',activebackground = "white")
	button_window_sentiment = canvas.create_window(600, 440, anchor='nw', window=sentiment_button)
	wordcloud_window.mainloop()
	
	wordcloud_window.grab_set()

def get_songs(artist_id):
	# official api
	page_url = 'https://music.163.com/artist?id=' + artist_id
	# get the HTML of website
	res = requests.request('GET', page_url, headers=headers)
	# get the hotsong list
	html = etree.HTML(res.text)
	href_xpath = "//*[@id='hotsong-list']//a/@href"
	name_xpath = "//*[@id='hotsong-list']//a/text()"
	hrefs = html.xpath(href_xpath)
	names = html.xpath(name_xpath)
	# get the id and name of the hot songs
	song_ids = []
	song_names = []
	for href, name in zip(hrefs, names):
		if name not in song_names:
			song_ids.append(href[9:])
			song_names.append(name)
			print(href, '  ', name)
	return song_ids, song_names


## method that called by button
def generate_cloud(singer):
	# set the singer ID
	# Jay Chou: 6452
	# Talor Swift: 44266
	# One Republic: 98105
	
	# create a dict to convert singer name to singer id
	singer_dict = {'Jay Chou': '6452','Taylor Swift':'44266','One Republic':'98105'}
	
	artist_id = singer_dict[singer]
	[song_ids, song_names] = get_songs(artist_id)
	# all the lyrics
	all_word = ''
	# get all the songs
	for (song_id, song_name) in zip(song_ids, song_names):
		# song API
		lyric_url = 'http://music.163.com/api/song/lyric?os=pc&id=' + song_id + '&lv=-1&kv=-1&tv=-1'
		lyric = get_song_lyric(headers, lyric_url)
		all_word = all_word + ' ' + lyric
		print(song_name)

	create_lyric_cloud(all_word)


## ========================Python GUI part============================

# build a simple UI
root = Tk()
root.wm_title("Lyric Cloud Generator")

# --- create canvas with scrollbar ---
canvas = Canvas(root, width=750, height=550)
canvas.pack(side = LEFT)
canvas.configure(bg = 'black')

root.resizable(False,False)


# resize the photo
image = Image.open('cloud.png')
# Image.ANTIALIAS to make the image more smooth
image = image.resize((120,80),Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
canvas.create_image(0,0,image=photo,anchor="nw")


image1 = Image.open('lyric.png')
image1 = image1.resize((50,50),Image.ANTIALIAS)
photo1 = ImageTk.PhotoImage(image1)
canvas.create_image(20,0,image=photo1,anchor="nw")

canvas.create_text(200,50,fill="white",font=("Forte",15),text="Lyric Cloud Generator")

# this project select three singers as demo purpose

# Jay Chou
canvas.create_text(170,100,fill="yellow",font=("Forte",15),text="Jay Chou")

image2 = Image.open('jay.jpg')
image2 = image2.resize((100,100),Image.ANTIALIAS)
photo2 = ImageTk.PhotoImage(image2)
canvas.create_image(130,120,image=photo2,anchor="nw")

with open('intro.txt') as intro_file:
	intro = intro_file.read()
	
intro_list = intro.split('\n')
print(len(intro_list))
intro_list.remove('')
intro_list.remove('')

jay_intro = intro_list[0]
oneRepublic_intro = intro_list[1]
swift_intro = intro_list[2]

canvas.create_text(480,150,fill="white",font=("Forte",15),text=jay_intro,width=450)

button1 = Button(root, text = "Lyric Cloud",command = lambda: generate_cloud("Jay Chou"),anchor = 'nw',width = 11,bg='grey',activebackground = "white")
button_window1 = canvas.create_window(30, 120, anchor='nw', window=button1)


# taylor-swift
canvas.create_text(170,250,fill="yellow",font=("Forte",15),text="Taylor Swift")

image3 = Image.open('taylor-swift.jpg')
image3 = image3.resize((100,100),Image.ANTIALIAS)
photo3 = ImageTk.PhotoImage(image3)
canvas.create_image(130,270,image=photo3,anchor="nw")

canvas.create_text(480,310,fill="white",font=("Forte",15),text=swift_intro,width=450)

button2 = Button(root, text = "Lyric Cloud",command = lambda: generate_cloud("Taylor Swift"),anchor = 'nw',width = 11,bg='grey',activebackground = "white")
button_window2 = canvas.create_window(30, 270, anchor='nw', window=button2) 


# one republic
canvas.create_text(170,400,fill="yellow",font=("Forte",15),text="One Republic")

image4 = Image.open('oneRepublic.png')
image4 = image4.resize((100,100),Image.ANTIALIAS)
photo4 = ImageTk.PhotoImage(image4)
canvas.create_image(130,420,image=photo4,anchor="nw")

canvas.create_text(480,450,fill="white",font=("Forte",15),text=oneRepublic_intro,width=450)

button3 = Button(root, text = "Lyric Cloud",command = lambda: generate_cloud("One Republic"),anchor = 'nw',width = 11,bg='grey',activebackground = "white")
button_window3 = canvas.create_window(30, 420, anchor='nw', window=button3)



root.mainloop()
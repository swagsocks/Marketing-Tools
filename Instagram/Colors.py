#The idea behind the process is to emulate a user looking at each photo, and when done with the page, moves on to the next. 
#The user communicates through the browser using HTTP requests which we emulate

#Imports

import requests
from bs4 import BeautifulSoup
from PIL import Image
from cStringIO import StringIO
import pandas as pd

#Empty List where post data will be stored
media_list = []

#HTTP requests and HTML Parsing -- WHILE LOOP, first iteration of 12
#Initial HTTP request to subject URL
coef_insta = requests.get('https://www.instagram.com/selenagomez/')
has_next_page = True
coef_html = coef_insta.text
soup = BeautifulSoup(coef_html, 'html.parser')
soup_info = soup.contents[10].contents[5].contents[3].contents[0][21:-1]
soup_info = soup_info.replace('null', 'None')
soup_info = soup_info.replace('false', 'False')
soup_info = soup_info.replace('true', 'True')
coef_dict = eval(soup_info)
user = coef_dict['entry_data']['ProfilePage'][0]['user']
media = user['media']
posts = media['nodes']

for x in posts:
	media_list.append([x['thumbnail_src'], x['likes'], x['comments']])

#WHILE LOOP and z counter for progress printout
z = 0
while has_next_page == True:	
	end_cursor = media['page_info']['end_cursor']
	has_next_page = media['page_info']['has_next_page']
	#Open Inspect on your Browser and look for HTTP requests, scroll down and new GET request is what we're emulating
	coef_insta = requests.get("https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=%7B%22id%22%3A%221998370222%22%2C%22first%22%3A12%2C%22after%22%3A%22"+ end_cursor + "%22%7D")
	coef_html = coef_insta.text
	z += 1
	print z
	soup = BeautifulSoup(coef_html, 'html.parser')
	soup_info = soup.contents[0]
	soup_info = soup_info.replace('null', 'None')
	soup_info = soup_info.replace('false', 'False')
	soup_info = soup_info.replace('true', 'True')
	coef_dict = eval(soup_info)
	media = coef_dict['data']['user']['edge_owner_to_timeline_media']
	for post in media['edges']:
		media_list.append([post['node']['thumbnail_src'], post['node']['edge_media_preview_like'], post['node']['edge_media_to_comment']])

#Color definitions by RGB values

def color(pixels):
	color_count = {'white':0, 'light_yellow':0, 'yellow':0, 'light_pink':0, 'light_red':0, 'orange':0, 'pink':0, 'magenta': 0, 'red':0, 'light_teal':0, 'light_lime':0, 'lime':0, 'light_blue':0, 'grey':0, 'dark_yellow':0, 'purple':0, 'dark_magenta':0, 'dark_red':0, 'teal':0, 'light_neon':0, 'neon':0, 'sky_blue':0, 'ocean_blue':0, 'dark_green':0,'blue':0, 'dark_blue':0, 'black':0}
	for x in pixels:
		red = 'high'
		green = 'high'
		blue = 'high'
		if x[0] < 170:
			red = 'medium'
		if x[1] < 170:
			green = 'medium'
		if x[2] < 170:
			blue = 'medium'
		if x[0] < 85:
			red = 'low'
		if x[1] < 85:
			green = 'low'
		if x[2] < 85:
			blue = 'low'
		if red == 'high' and green == 'high' and blue =='high':
			color = 'white'
		elif red == 'high' and green == 'high' and blue =='medium':
			color = 'light_yellow'
		elif red == 'high' and green == 'high' and blue =='low':
			color = 'yellow'
		elif red == 'high' and green == 'medium' and blue == 'high':
			color = 'light_pink'
		elif red == 'high' and green == 'medium' and blue == 'medium':
			color = 'light_red'
		elif red == 'high' and green == 'medium' and blue == 'low':
			color = 'orange'
		elif red == 'high' and green == 'low' and blue == 'high':
			color = 'pink'
		elif red == 'high' and green == 'low' and blue == 'medium':
			color = 'magenta'
		elif red == 'high' and green == 'low' and blue == 'low':
			color = 'red'
		elif red == 'medium' and green == 'high' and blue =='high':
			color = 'light_teal'	
		elif red == 'medium' and green == 'high' and blue =='medium':
			color = 'light_lime'
		elif red == 'medium' and green == 'high' and blue =='low':
			color = 'lime'
		elif red == 'medium' and green == 'medium' and blue == 'high':
			color = 'light_blue'
		elif red == 'medium' and green == 'medium' and blue == 'medium':
			color = 'grey'
		elif red == 'medium' and green == 'medium' and blue == 'low':
			color = 'dark_yellow'
		elif red == 'medium' and green == 'low' and blue == 'high':
			color = 'purple'
		elif red == 'medium' and green == 'low' and blue == 'medium':
			color = 'dark_magenta'
		elif red == 'medium' and green == 'low' and blue == 'low':
			color = 'dark_red'
		elif red == 'low' and green == 'high' and blue =='high':
			color = 'teal'	
		elif red == 'low' and green == 'high' and blue =='medium':
			color = 'light_neon'
		elif red == 'low' and green == 'high' and blue =='low':
			color = 'neon'
		elif red == 'low' and green == 'medium' and blue == 'high':
			color = 'sky_blue'
		elif red == 'low' and green == 'medium' and blue == 'medium':
			color = 'ocean_blue'
		elif red == 'low' and green == 'medium' and blue == 'low':
			color = 'dark_green'
		elif red == 'low' and green == 'low' and blue == 'high':
			color = 'blue'
		elif red == 'low' and green == 'low' and blue == 'medium':
			color = 'dark_blue'
		elif red == 'low' and green == 'low' and blue == 'low':
			color = 'black'
		color_count[color] += 1
	top_four = sorted(color_count, key=color_count.get, reverse = True)
	return [top_four[0], top_four[1], top_four[2], top_four[3]]
			

#Dictionary initialization

all_posts_likes = {'white':0, 'light_yellow':0, 'yellow':0, 'light_pink':0, 'light_red':0, 'orange':0, 'pink':0, 'magenta': 0, 'red':0, 'light_teal':0, 'light_lime':0, 'lime':0, 'light_blue':0, 'grey':0, 'dark_yellow':0, 'purple':0, 'dark_magenta':0, 'dark_red':0, 'teal':0, 'light_neon':0, 'neon':0, 'sky_blue':0, 'ocean_blue':0, 'dark_green':0,'blue':0, 'dark_blue':0, 'black':0}
all_posts_comments = {'white':0, 'light_yellow':0, 'yellow':0, 'light_pink':0, 'light_red':0, 'orange':0, 'pink':0, 'magenta': 0, 'red':0, 'light_teal':0, 'light_lime':0, 'lime':0, 'light_blue':0, 'grey':0, 'dark_yellow':0, 'purple':0, 'dark_magenta':0, 'dark_red':0, 'teal':0, 'light_neon':0, 'neon':0, 'sky_blue':0, 'ocean_blue':0, 'dark_green':0,'blue':0, 'dark_blue':0, 'black':0}

weight = {'white':0, 'light_yellow':0, 'yellow':0, 'light_pink':0, 'light_red':0, 'orange':0, 'pink':0, 'magenta': 0, 'red':0, 'light_teal':0, 'light_lime':0, 'lime':0, 'light_blue':0, 'grey':0, 'dark_yellow':0, 'purple':0, 'dark_magenta':0, 'dark_red':0, 'teal':0, 'light_neon':0, 'neon':0, 'sky_blue':0, 'ocean_blue':0, 'dark_green':0,'blue':0, 'dark_blue':0, 'black':0}

color_likes = {'white':0, 'light_yellow':0, 'yellow':0, 'light_pink':0, 'light_red':0, 'orange':0, 'pink':0, 'magenta': 0, 'red':0, 'light_teal':0, 'light_lime':0, 'lime':0, 'light_blue':0, 'grey':0, 'dark_yellow':0, 'purple':0, 'dark_magenta':0, 'dark_red':0, 'teal':0, 'light_neon':0, 'neon':0, 'sky_blue':0, 'ocean_blue':0, 'dark_green':0,'blue':0, 'dark_blue':0, 'black':0}

color_comments = {'white':0, 'light_yellow':0, 'yellow':0, 'light_pink':0, 'light_red':0, 'orange':0, 'pink':0, 'magenta': 0, 'red':0, 'light_teal':0, 'light_lime':0, 'lime':0, 'light_blue':0, 'grey':0, 'dark_yellow':0, 'purple':0, 'dark_magenta':0, 'dark_red':0, 'teal':0, 'light_neon':0, 'neon':0, 'sky_blue':0, 'ocean_blue':0, 'dark_green':0,'blue':0, 'dark_blue':0, 'black':0}

n = 0

# For images requested in media_list sources, count pixels, attribute likes and comments on post to dominant colors		
for x in media_list:
	pic = Image.open(StringIO(requests.get(x[0]).content))
	pixels = list(pic.getdata())
	likes = x[1]['count']
	comments = x[2]['count']
	top_four = color(pixels)
	for x in top_four:
		all_posts_likes[x] += likes
		all_posts_comments[x] += comments
		weight[x] += 1
	n= n + 1	
	print n

# Weigh the Total Likes and Total Comments by Usage

#WEIGHTED AVERAGE
for keys in all_posts_likes.iterkeys():
	if weight[keys] != 0:
		color_likes[keys] = all_posts_likes[keys]/weight[keys]
		color_comments[keys] = all_posts_comments[keys]/weight[keys]
	else:
		pass

#Top colors
top_colors_likes = sorted(color_likes, key=color_likes.get, reverse = True)
top_colors_comments = sorted(color_comments, key=color_comments.get, reverse = True)
most_used = sorted(weight, key=weight.get, reverse = True)

#To DataFrame	
color_likes_df = pd.DataFrame(color_likes, index = ['likes']).T
color_comments_df = pd.DataFrame(color_comments, index = ['comments']).T
weight_df = pd.DataFrame(weight, index = ['use']).T

final_frame = pd.concat([color_likes_df, color_comments_df, weight_df], axis = 1, join = 'inner')

#To CSV
final_frame.to_csv('Selena_Gomez_instagram_colors.csv')	

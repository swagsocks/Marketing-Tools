#The idea behind the process is to emulate a user looking at each photo, and when done with the page, moves on to the next. 
#The user communicates through the browser using HTTP requests which we emulate

#Imports

import requests
from bs4 import BeautifulSoup
import pandas as pd

#Empty List where post data will be stored
likes_list = []
likers_codes = []


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
	likes_list.append(x['likes']['count'])
	likers_codes.append(x['code']) 
		
followers = user['followed_by']['count']

#WHILE LOOP and z counter for progress printout
z = 11
while has_next_page == True and z < 100:	
	end_cursor = media['page_info']['end_cursor']
	has_next_page = media['page_info']['has_next_page']
	#Open Inspect on your Browser and look for HTTP requests, scroll down and new GET request is what we're emulating
	coef_insta = requests.get("https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=%7B%22id%22%3A%221998370222%22%2C%22first%22%3A12%2C%22after%22%3A%22"+ end_cursor + "%22%7D")
	coef_html = coef_insta.text
	soup = BeautifulSoup(coef_html, 'html.parser')
	soup_info = soup.contents[0]
	soup_info = soup_info.replace('null', 'None')
	soup_info = soup_info.replace('false', 'False')
	soup_info = soup_info.replace('true', 'True')
	coef_dict = eval(soup_info)
	media = coef_dict['data']['user']['edge_owner_to_timeline_media']
	for post in media['edges']:
		likes_count = post['node']['edge_media_preview_like']['count']
		likes_list.append(likes_count)
		likers_codes.append(x['code'])
		z += 1
		print z

#Engagement Rate = Average Likes per Post / Total Followers	
engagement_rate = (sum(likes_list[:100])/100)/float(followers)

#Limit to 100 posts
likers_codes = likers_codes[:100]

#Attribute likes to likers names
likers_usernames = {}
likers_followers_dict = {}
n = 0

#For all posts, scrape who liked the post using short_codes, attribute to followers
for short_code in likers_codes:
	n += 1
	print n
	http = "https://www.instagram.com/graphql/query/?query_hash=1cb6ec562846122743b61e492c85999f&variables=%7B%22shortcode%22%3A%22" + short_code + "%22%2C%22first%22%3A20%7D"
	raw = requests.get(http).text
	raw = raw.replace('null', 'None')
	raw = raw.replace('false', 'False')
	raw = raw.replace('true', 'True')
	likers_dict = eval(raw)
	likers_nodes = likers_dict['data']['shortcode_media']['edge_liked_by']['edges']
	for x in likers_nodes:
		liker_user = x['node']['username']
		if liker_user in likers_usernames:
			likers_usernames[liker_user] += 1
		else:
			likers_usernames[liker_user] = 1
			
#For each follower, scrape their following
for keys in likers_usernames.iterkeys():
	print keys
	liker_user = keys		
	liker_raw = requests.get('https://www.instagram.com/' + liker_user).text
	liker_soup = BeautifulSoup(liker_raw, 'html.parser')
	liker_soup_info = liker_soup.contents[10].contents[5].contents[3].contents[0][21:-1]
	liker_raw = liker_soup_info.replace('null', 'None')
	liker_raw = liker_raw.replace('false', 'False')
	liker_raw = liker_raw.replace('true', 'True')
	liker_prof = eval(liker_raw)
	liker_followers = liker_prof['entry_data']['ProfilePage'][0]['user']['followed_by']['count']
	likers_followers_dict[liker_user] = liker_followers

#Put into DataFrame			
likers_df = pd.DataFrame(likers_usernames, index = ['posts_liked']).T
likers_df.sort_values(by = 'posts_liked',True)
likers_df.sort_values(by = 'posts_liked', ascending = False)

likers_followers_df = pd.DataFrame(likers_followers_dict, index = ['follower']).T

final_df = pd.concat([likers_df, likers_followers_df], axis = 1, join = 'inner')
final_df.sort_values(by = 'posts_liked', ascending = False)

#To CSV
final_df.to_csv('Selena_Gomez_instagram_engagement.csv')
print engagement_rate

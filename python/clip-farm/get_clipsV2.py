import requests
import json

import pickle
import os

import datetime

import time
import random

import download_clip as dc
import get_directoryV2
import config

date=datetime.date.today()
database_path = config.database_path

#get clips info through pure post requests.
twich_request_url = 'https://gql.twitch.tv/gql'
headers = {
'Host': 'gql.twitch.tv',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
'Accept': '*/*',
'Accept-Language': 'en-US',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://www.twitch.tv/',
'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
'X-Device-Id': '75af88a3d423ca4a',
'Content-Type': 'text/plain;charset=UTF-8',
'Origin': 'https://www.twitch.tv',
'Content-Length': '265',
'DNT': '1',
'Connection': 'keep-alive'}
body = {
"operationName":"ClipsCards__Game",
"variables":{
			 "gameName":"Just Chatting",
			 "limit":50,
			 "criteria":{
			 			 "languages":[],
			 			 "filter":"LAST_DAY"}},
"extensions":
			 {"persistedQuery":{
			 					"version":1,
								"sha256Hash":"0d8d0eba9fc7ef77de54a7d933998e21ad7a1274c867ec565ac14ffdce77b1f9"}}}

class Clips_Information:
	def __init__(self):
		self.clips_list = []

	def get_clip_info(self, game, number): #string, int, response object
	#uses response object to download and make directory for clips and meta information
		data = body

		data['variables']['limit'] = number
		data['variables']['gameName'] = game

		data = json.dumps(data)
		print("Retrieving clip information for category ", str(game), '.')
		response = requests.post(twich_request_url, headers=headers, data=data)
	
		#convert response object to json dict and navigate to index with actual clip info
		#each clip in the directory navigated to here is a dictionary as part of a list
		#scratch.py has example_dict, with format of the dict each clip is in
		dic = json.loads(response.text)

		clips_info = dic['data']['game']['clips']['edges']
	
		#create folder for date of running if it doesn't exist
		today_folder = database_path + 'Twitch Clip Gen' + '/' + str(date) + '/'
		try:
			os.makedirs(today_folder + 'clips') #make subfolder for clips
			os.makedirs(today_folder + 'meta')  #and for info on clips
		except:
			print('Failed create dirs: ', today_folder + 'clips && meta', "-- May already exist.")
	
		for clip in clips_info:
			self.clips_list.append(clip)
	
		return print('Length of self.clips_list is ', len(self.clips_list))

def get_all_clips(number_of_games, number_of_clips): #gets all clip info from x number of
#						  games through top viewed in directory
	games = get_directoryV2.get_directory(number_of_games)
	clips = Clips_Information()
	for game in games:
		print(game, ' : ', number_of_clips, ' clips.')
		clips.get_clip_info(game,  number_of_clips)
		time.sleep(1.5 + random.random() * 5)

	return clips.clips_list

def sort_clips_views(clip_list): #takes list of clip dicts
	# print(clip_list)
	# quit()
	most_viewed = sorted(clip_list, key=lambda x: x['node']['viewCount'], reverse=True)

	def english_in_front(index): # recursive function to find first english title
		if (index == len(most_viewed)): #and shuffle it along to front of list
			return 0

		title = list(most_viewed[index]['node']['title'])
		title_string_list = [ord(x) for x in title if ord(x) < 124 and ord(x) > 31]

		if (len(title_string_list) < 2):
			english_in_front(index + 1)
			most_viewed[index], most_viewed[index + 1] = most_viewed[index + 1], most_viewed[index]

		return 0

	return most_viewed
	#returns list of clip dicts in order of most viewed

def get_datetime(date_str): #turns json 'createdAt' str entry from response into datetime object
	year=int(date_str[0:4])
	month=int(date_str[5:7])
	day=int(date_str[8:10])
	hour = int(date_str[11:13])
	minute = int(date_str[14:16])
	second = int(date_str[17:19])
	date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
	return date


def get_clip_files(clips_list, total_length): #takes list of clip dicts, and len in seconds ; downloads files
	global date
	folder = database_path + 'Twitch Clip Gen' + '/' + str(date) + '/'

	length = 0
	repeat_log = [] #to check for clips from same channel within a minute

	pickle_meta = open(folder + 'meta/' + 'clips_list', 'wb')
	pickle.dump(clips_list, pickle_meta)
	pickle_meta.close()

	for clip in clips_list[0:60]:
		if (length > total_length):
			break

		date = get_datetime(clip['node']['createdAt'])
		streamer = clip['node']['broadcaster']['id']

		for entry in repeat_log:
			if (entry[1] == streamer): #same streamer
				if (abs(entry[0] - date) < datetime.timedelta(minutes=1)): #clipped within a minute
					break

		path = folder + 'clips/'

		#name file will be downloaded as, and url used to download.
		name = clip['node']['slug']
		url = clip['node']['url']

		clipr_file = 'https:' + dc.make_clip(url)

		print('Downloading: ', clip['node']['title'], '...')
		download_check = dc.download_file(clipr_file, name, path)

		
		repeat_log.append((date, streamer))

		time.sleep(1.5 + random.random() * 5)

		if (download_check == True):
			length += clip['node']['durationSeconds']
		print("Current Length: ", length)
	return 0


def retrieve_download(number_of_directories, number_of_clips, length): #downloads clips totalling length < length param
	print('Gettings clips for downloads...')
	a = get_all_clips(number_of_directories, number_of_clips)
	print('Sorting clips...')
	b = sort_clips_views(a)
	print('Downloading clips...')
	get_clip_files(b, length)


print('--------------end-----------------')

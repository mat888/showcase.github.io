import requests
import pickle
import json
import os

headers = {'Host': 'gql.twitch.tv',
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
"operationName":"BrowsePage_AllDirectories",
"variables":{
		"limit":30, #how many categories to get
		"options":
				{"recommendationsContext":
								{
								"platform":"web"},
								"requestID":"JIRA-VXP-2397",
								"sort":"VIEWER_COUNT",
								"tags":[]}},
"extensions":
		{"persistedQuery":
				{"version":1,"sha256Hash":"78957de9388098820e222c88ec14e85aaf6cf844adf44c8319c545c75fd63203"}}}

request_url = "https://gql.twitch.tv/gql"

def get_directory(number): #retrieves list of game names that feed into
	#				  get_clip_info() in get_clipsV2.py 
	data = body
	data['variables']['limit'] = number

	data = json.dumps(data) #convert dict to json before requesting

	response = requests.post(request_url, headers=headers, data=data)
	print("get_directory.py, in function get_directory(), response code: ", response)

	dicts = json.loads(response.text) #convert json response object to dictionary
	dicts = dicts['data']['directoriesWithTags']['edges'] #navigate to list

	directories = []
	for directory in dicts: #add url ends to list
		directories.append(directory['node']['name'])

	return directories

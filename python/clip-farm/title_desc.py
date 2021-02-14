import datetime
import config
import pickle

date = datetime.date.today()
#date = datetime.date(month=4, year=2020, day=25) #date override for debugging
path = config.database_path + "Twitch Clip Gen/" + str(date) + '/'

with open(path + 'log', 'rb') as log_:
		log = pickle.load(log_)

desc = "See more of the streams featured in these clips! Follow and subscribe if you enjoyed their content! \n"
tags = []
title = "MOST VIEWED CLIPS OF THE DAY! " + str(datetime.date.today()) + ' | ' + log[0]['node']['title']

def desc_tag_writer():
	global desc; global tags

	time = datetime.datetime(2010, 1, 1, minute=0, second=0)
	for entry in log:
		entry = entry['node']
		desc += entry['title'] + " - From https://twitch.tv/" + entry['broadcaster']['login']
		
		time_str = str(time)[14:] #get rid of year, month, etc.
		if (time_str[0] == '0'):  #get rid of leading 10's place zero
			time_str = time_str[1:]

		desc += '\n' + time_str   #finally add timestamp
	
		#add clip length to current time
		seconds = entry['durationSeconds'] - 1.2 
		# - 1.2 accounts for clips fading in
		time = time + datetime.timedelta(seconds = seconds)

		################################################################################
		#Add 'tags' based on broadcaster and twitch directory

		tags.append(entry['broadcaster']['displayName'])
		tags.append(entry['game']['name'])
	
	return 0

desc_tag_writer()

print(title)
print(desc)
print(tags)
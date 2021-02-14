from moviepy.editor import *
#import multiprocessing
import os
import datetime
import pickle

import math
import random

import timeit

import config
database_path = config.database_path

date=datetime.date.today()

date = datetime.date(month=4, year=2020, day=25) #date override for debugging

path = database_path + 'Twitch Clip Gen/' + str(date) + '/'
clip_path = path + 'clips/'
meta_path = path + 'meta/clips_list'

print('clip_path, meta_path')
print(clip_path, meta_path)



#loading in files --------------------------------------------------------------
meta_pickle = open(meta_path, 'rb') 
meta = pickle.load(meta_pickle)
meta_pickle.close()

curator_leaderboard_pickle = open(database_path + 'Twitch Clip Gen/curator_leaderboard', 'rb')
curator_leaderboard = pickle.load(curator_leaderboard_pickle)
curator_leaderboard_pickle.close()

broadcaster_leaderboard_pickle = open(database_path + 'Twitch Clip Gen/broadcaster_leaderboard', 'rb')
broadcaster_leaderboard = pickle.load(broadcaster_leaderboard_pickle)
broadcaster_leaderboard_pickle.close()
#---------------------------------------------------------------------------------


font = 'NotoSansCJKjp-Black.otf'

def scale_clip(clip):
	res = clip.size
	if (res == (1920, 1080)):
		return clip
	small = clip
	if (res[0] / res[1] == 1920 / 1080):
		return clip.fx(vfx.resize, height  = 1080)
	if (res[0] / res[1] < 16 / 9):
		large = clip.fx(vfx.resize, width  = 1920)
		small = clip.fx(vfx.resize, height = 1080)
		return CompositeVideoClip([large, small.set_position('center')])
	large = clip.fx(vfx.resize, width = 1920)
	small = clip.fx(vfx.resize, height= 1080)
	return CompositeVideoClip([large, small.set_position('center')])

def make_text(clip, info):
	duration = clip.duration
	title = info['node']['title']
	curator = info['node']['curator']['displayName']
	streamer = info['node']['broadcaster']['displayName']

	logo = ImageClip(img='twitchlogo.png', transparent=True)
	logo = logo.fx(vfx.resize, 0.2)
	logo = logo.set_duration(duration)
	logo = logo.set_position(lambda t: ((1/len(streamer)) * (1/0.65)*math.e**(t), 750))

	# font='Georgia'
	# fps = clip.fps
	# frame_duration = math.floor(duration * fps)
	title_text = TextClip('\"' + title + '\"', font=font, color='#96B764', size=(1000, None), fontsize=60, stroke_color='gray', stroke_width=1, method='caption', align='west')
	title_text = title_text.set_duration(duration)
	title_text = title_text.set_position(lambda t: ((1/len(title)) * (1/0.60)*math.e**t, 0))

	curator_text = TextClip('Curator: ' + curator, font=font, color='#96B764', fontsize=45, stroke_color='gray', stroke_width=0.68)
	curator_text = curator_text.set_duration(duration)
	curator_text = curator_text.set_position(lambda t: ((1/len(curator)) * (1/0.45)*math.e**t, 1000))

	streamer_text = TextClip('Streamer: ' + streamer, font=font, color='#96B764', fontsize=65, stroke_color='gray', stroke_width=1)
	streamer_text = streamer_text.set_duration(duration)
	streamer_text = streamer_text.set_position(lambda t: ((1/len(streamer)) * (1/0.65)*math.e**t, 900))

	clip_text = CompositeVideoClip([clip, title_text, curator_text, streamer_text, logo])
	return clip_text

def make_transition(clip, direction_index, directions=['top','left','bottom','right']):
	if (clip.duration < 9):
		direction = directions[direction_index % 4]
		return CompositeVideoClip([clip.fx(transfx.slide_in, 0.2, direction)])
	else:
		return clip.crossfadein(1.2)

def comma_number(integer): #takes int returns string
	string = ''
	number = str(integer)
	for index, i in enumerate(number):
		if ( ((len(number) - (index + 1)) % 3) == 0 and index != len(number) - 1):
			string += (i + ',')
		else: string += i
	return string

def make_end_screen():
	color1 = [100, 164, 183]; color2 = [150, 183, 100]
	color1Hex = '#96b764'; color2Hex = '#64a4b7'
	
	pic_index = str(random.randint(1, 7))

	pic1 = ImageClip(img='images/' + pic_index + '.png', transparent=False, duration=45)
	pic1 = pic1.set_position([1264, 357])

	pic2 = ImageClip(img='images/0.png', transparent=False, duration=45)
	pic2 = pic2.set_position([1264, 357])

	outro_song = AudioFileClip('audio/Noname.mp3')
	outro_song = outro_song.subclip(71, -1)
	outro_song = outro_song.volumex(0.15)

	try:
		preview = get_preview(40)
		preview = preview.fx(vfx.resize, height = 400)
		preview = preview.set_position([0, 700])
		# preview = preview.volumex(0.25)
		# preview = preview.audio_fadeout(11)
	except:
		preview = ColorClip(size=(10,10), color=color1)
		preview.set_position([2000, 2000])

	curator_leader_list = sorted(curator_leaderboard.items(), key=lambda item: item[1], reverse=True)

	curator_leaderb = "Curator Leaderboard: \n"
	for position in curator_leader_list:
		curator_leaderb += comma_number(position[1]) + ' - ' + position[0] + '\n'

	broadcaster_leader_list = sorted(broadcaster_leaderboard.items(), key=lambda item: item[1], reverse=True)

	broadcaster_leaderb = "Broadcaster Leaderboard: \n"
	for position in broadcaster_leader_list:
		broadcaster_leaderb += comma_number(position[1]) + ' - ' + position[0] + '\n'
	
	background1 = ColorClip(size=(1920, 1080), color=color1, ismask=False, duration=45)

	# background1.set_audio(outro_song)
	background2 = ColorClip(size=(1920, 1080), color=color2, ismask=False, duration=45)

	curator_l = TextClip(curator_leaderb, font=font, color=color1Hex, size=(1000, None), fontsize=50, method='caption', align='west')

	curator_l = curator_l.set_duration(45)
	watch = TextClip('Watch yesterday\'s video:', font=font, color=color1Hex, size=(1000, None), fontsize=50, method='caption', align='west')
	watch = watch.set_duration(45)
	watch = watch.set_position([32, 620])

	end1 = CompositeVideoClip([background1, curator_l, watch, pic1, preview.subclip(0, 45)])

	thanks = TextClip("Thanks for Watching!", font=font, color=color2Hex, fontsize=160, method='label', align='west')
	art_credits = TextClip("Profile art by @lynelmilk on Twitter.", font=font, color=color2Hex, fontsize=55, method='label', align='west')
	music_credits = TextClip("Music: Noname by @stephenstark1 on soundcloud.", font=font, color=color2Hex, fontsize=45, method='label', align='west')
	broadcaster_l = TextClip(broadcaster_leaderb, font=font, color=color2Hex, size=(1000, None), fontsize=50, method='caption', align='west')

	broadcaster_l = broadcaster_l.set_position([0, 200])
	art_credits = art_credits.set_position([0, 850])
	music_credits = music_credits.set_position([0, 1000])

	art_credits = art_credits.set_duration(45)
	broadcaster_l = broadcaster_l.set_duration(45)
	music_credits = music_credits.set_duration(45)
	thanks = thanks.set_duration(45)

	end2 = CompositeVideoClip([background2, thanks, pic2, broadcaster_l, art_credits, music_credits])
	end2 = end2.crossfadein(5)

	end = concatenate([end1, end2], padding=-10, method='compose')

	end = end.set_audio(outro_song)
	end = end.crossfadein(1.2)
	return end

def get_preview(length):
	
	preview_date = date - datetime.timedelta(days=1)

	clip_path = database_path + 'Twitch Clip Gen/' + str(preview_date) + '/clips/'
	meta_path = database_path + 'Twitch Clip Gen/' + str(preview_date) + '/meta/clips_list'

	yesterdays_meta = open(meta_path, 'rb')
	yesterdays_clips_list = pickle.load(yesterdays_meta)
	yesterdays_meta.close()

	# print(yesterdays_clips_list)
	p = edit_clips(yesterdays_clips_list, clip_path=clip_path)[0:4]

	preview_clips = concatenate(p, method='compose')
	preview_clips = preview_clips.subclip(5, 5 + length)
	return preview_clips


def edit_clips(clips_list, leaderboard=False, clip_path=clip_path): #uses clips_list meta info to stitch clips from folder
	new_clips = []
	log = []
	for info in clips_list:
		clip_file_name = info['node']['slug']
		try:
			clip = VideoFileClip(clip_path + clip_file_name)
			print('Success! Made clip object for:')
			print(info['node']['title'])
			print(info['node']['slug'])
		except:
			print('failed to make clip object for:')
			print(info['node']['title'])
			print(info['node']['slug'])
			continue

		clip = scale_clip(clip)
		clip = make_text(clip, info)
		# print(info['node']['durationSeconds'])
		clip = make_transition(clip, len(new_clips))
		print(len(new_clips))

		new_clips.append(clip)

		if (leaderboard == True):
			curator = info['node']['curator']['displayName']
			views = info['node']['viewCount']
			print(curator, views)
			if (curator in curator_leaderboard):
				curator_leaderboard[curator] += views
			else:
				curator_leaderboard[curator] = views

			caster = info['node']['broadcaster']['displayName']
			views = info['node']['viewCount']
			if (caster in broadcaster_leaderboard):
				broadcaster_leaderboard[caster] += views
			else:
				broadcaster_leaderboard[caster] = views

		log.append(info)

	with open(path + 'log', 'wb') as log_file:
		pickle.dump(log, log_file) #log of clips used in order of use

	edited_clips = concatenate(new_clips, padding=-1.2, method='compose')
	return edited_clips

# clips = edit_clips(meta, leaderboard=True)
# vid =  clips[0]
# vid = concatenate(clips, padding=-1.2, method='compose')
# vid.save_frame('frame.png', t=3)
# vid.write_videofile('vid19.mp4', fps=30)

def make_video():

	clips = edit_clips(meta, leaderboard=True)

	# del(clips)
	# print('clips.close complete')
	end = make_end_screen()
	print('make_end complete')
	# clips = VideoFileClip('temp_vid.mp4')
	clips = clips.audio_fadeout(1.2)
	vid = concatenate([clips, end], padding=-1.2, method='compose')
	print('concat complete; writing video file')
	vid.write_videofile(path + 'fin' + '.mp4', fps=3, preset='ultrafast')
	return print("Video rendered and saved to " + path)

make_video()


curator_leaderboard_pickle = open(database_path + 'Twitch Clip Gen/curator_leaderboard', 'wb')
pickle.dump(curator_leaderboard, curator_leaderboard_pickle)
curator_leaderboard_pickle.close()

broadcaster_leaderboard_pickle = open(database_path + 'Twitch Clip Gen/broadcaster_leaderboard', 'wb')
pickle.dump(broadcaster_leaderboard, broadcaster_leaderboard_pickle)
broadcaster_leaderboard_pickle.close()

log_pickle = open(database_path + 'Twitch Clip Gen/' + str(date) + '/log', 'wb')
pickle.dump(log, log_pickle)
log_pickle.close()

print("End of editVideo")

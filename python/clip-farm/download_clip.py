import shutil
import requests
import os
import json

def make_clip(clip_url):
	clipr = 'https://clipr.xyz/api/grabclip'
	params = {"clip_url":clip_url}
	response = requests.post(clipr, params=params)
	json_data = json.loads(response.text)
	return json_data['download_url']

test = make_clip('https://clips.twitch.tv/TsundereElegantWaterDeIlluminati')
# print(test);quit()

def download_file(url, filename, path): #abc.com, name, \abc\xyz\

	with requests.get(url, stream=True) as r:
		with (open(path + filename, 'wb')) as f:
			shutil.copyfileobj(r.raw, f)

	directory = os.listdir(path)
	return (filename in directory)

# download_file(r"https://static-cdn.jtvnw.net/jtv_user_pictures/c495b77e-7f47-4bc5-a216-3045d7545796-profile_image-70x70.png", 'poop', 'test\\')

# URL extension to clips page: "clips?range=24hr"

# div class name with attribute to the link
# tw-interactive tw-link tw-link--button tw-link--hover-underline-none tw-link--inherit





# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/guides/code_samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

import datetime

import config
import title_desc

title = title_desc.title
desc = title_desc.desc
tags = title_desc.tags

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

date=datetime.date.today()
date = datetime.date(month=4, year=2020, day=25)
database_path = config.database_path
path = database_path + 'Twitch Clip Gen/' + str(date) + '/fin.mp4'

def upload():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "24", #24 == entertainment
            "description": desc,
            "title": title,
            "tags": tags,
          },
          "status": {
            "privacyStatus": "public" ###change to public for 'release build'
          }
        },
        
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(path)
    )
    print('Sending upload request...')
    response = request.execute()

    print(response)
    print('Upload script finished.')
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import settings
import tweepy
import dataset
from textblob import TextBlob
from var_dump import var_dump
#from sqlalchemy.exc import ProgrammingError
import json
db = dataset.connect('sqlite:///mydatabase.db')
#db = dataset.connect(settings.CONNECTION_STRING)

class StreamListener(tweepy.StreamListener):

	def on_status(self, status):
		if status.retweeted:
			return
		if status.text[:2] == "RT":
			return
		if status.is_quote_status == True:
			return
		description = status.user.description
		loc = status.user.location
		text = status.text
		coords = status.coordinates
		geo = status.geo
		name = status.user.screen_name
		username = status.user.name
		user_created = status.user.created_at
		followers = status.user.followers_count
		id_str = status.id_str
		created = status.created_at
		retweets = status.retweet_count
		bg_color = status.user.profile_background_color
		blob = TextBlob(text)
		sent = blob.sentiment

		if geo is not None:
			geo = json.dumps(geo)

		if coords is not None:
			coords = json.dumps(coords)
		print(name)
		print(text)
		print(status.retweeted)
		
		print("----------")
		'''
		print(status)
		print("------------------------------------------------------------------------------------")'''
		table = db['tweet']
		table.insert(dict(user=name,username=username,profile=status.user.profile_image_url,text=text,created = created,id_str=id_str))
		"""
		table = db[settings.TABLE_NAME]
		try:
			table.insert(dict(
				user_description=description,
				user_location=loc,
				coordinates=coords,
				text=text,
				geo=geo,
				user_name=name,
				user_created=user_created,
				user_followers=followers,
				id_str=id_str,
				created=created,
				retweet_count=retweets,
				user_bg_color=bg_color,
				polarity=sent.polarity,
				subjectivity=sent.subjectivity,
			))
		except ProgrammingError as err:
			print(err)
		"""

	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_data disconnects the stream
			return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)
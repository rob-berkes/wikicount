from pymongo import Connection
import tweepy
conn=Connection('10.115.126.7')
api=tweepy.api
db=conn.wc

status=api.user_timeline('wikitrendsinfo',count=10)

db.twitter.remove()
for tweet in status:
	db.twitter.insert({'created_at':tweet.created_at,'screen_name':tweet.user.screen_name,'text':tweet.text})


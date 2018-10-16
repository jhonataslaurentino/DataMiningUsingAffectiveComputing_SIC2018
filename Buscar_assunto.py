import tweepy
import csv
import pandas as pd

####input your credentials here  ->> https://apps.twitter.com/
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
csvFile = open('DiadosProfessores.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
search_terms = '#DiadosProfessores'
for tweet in tweepy.Cursor(api.search,q=search_terms,count=100,
                           lang="pt",tweet_mode="extended",
                           since="2018-10-15").items():
    print (tweet.id,tweet.created_at, tweet.full_text)
    csvWriter.writerow([tweet.created_at, tweet.full_text])

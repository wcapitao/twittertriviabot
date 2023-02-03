#!/usr/bin/python3

#import subprocess
#import sys
#def install_package(package):
#    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#this is info - I will Install the tweepy package:
#install_package("openai")

from _ast import Import
#importing libraries
#tweeter api
import tweepy
#api keys from other file
import Keys
#openai
import openai
#to download images from url into my computer
import urllib.request
import requests
#import regular expression
import re
#import random
import random
#ImportingKeys
import Keys
#Importing Topics
import topics1
#importing requests
import requests
#importing json
import json





#defining API access
def api():
    auth = tweepy.OAuthHandler(Keys.apiKey, Keys.apiKeySecret)
    auth.set_access_token(Keys.accessToken, Keys.accessTokenSecret)

    return tweepy.API(auth)

api = api()

#defining 'Post Tweet'
def tweet():
    # Post the first tweet with an image
    filename = "image.jpg"
    response = api.media_upload(filename)
    media_id = response.media_id
    Post_Tweet = api.update_status(tweets[0], media_ids=[media_id])

    for tweet in tweets[1:]:
        recent_tweets = api.user_timeline()
        most_recent_tweet = recent_tweets[0]
        # Get the ID of the most recent tweet
        most_recent_tweet_id = most_recent_tweet.id
        api.update_status(tweet, in_reply_to_status_id=most_recent_tweet_id)
        # api.update_status(tweet, in_reply_to_status_id=previous_tweet_id)
        # previous_tweet_id = api.update_status(tweet).id
    print('Tweeted successfully!')


#Prompt Creation
topic = (random.choice(topics1.topics))
print(topic)
prompt = f"Act as a very interesting university teacher of {topic} trying to encourage his students. Present the most interesting fact about {topic} you know for someone with a master's degree. Start with \"did you know\". The first sentence must be strong to attract the attention of the reader and the students. Then go into more detail about the fact and finally present a conclusion. The fact must be factual. Present the last paragraph a sentence that starts with \"topic of this fact: topic\" - change the last word \"topic\" to the topic you are presenting, not considering the word \"{topic}\" and not using more than 2 words. Use no more than 150 words in total."


#accessing openAI
openai.organization = "org-NCsMrMMWlSqR7svMbRTWd81T"
openai.api_key = Keys.apiKey_OpenAI
openai.Model.list()

#Getting Response
response = openai.Completion.create(
  model="text-davinci-003",
  prompt= prompt,
    temperature=0.9,
    max_tokens=462,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6
)

#Getting final text for tweet - - - - - - - - - - - -
#getting response from openai
openai_response = response["choices"][0]["text"]
#identify hashtags - topic and specific - rsplit to split on last ":" and lstrip to remove spaces on the left side of the string and rstrip to delete "." on the right.
topic
specific = openai_response.rsplit(":", 1)[-1].lstrip().rstrip(".")
#Split sentences into different strings and ignoring numbers with ".". Now we don't need the last sentence, will delete it.
tweets_list = re.split(r'(?<!\d)\.(?!\d)', openai_response)
tweets_list.pop()
tweets_list.pop()
#This list of tweets has breaks - \n\n - and should be deleted.
for i in range(len(tweets_list)):
    tweets_list[i] = tweets_list[i].replace("\n\n", "")
#After each string, I'll add a dot "."
for i in range(len(tweets_list)):
    tweets_list[i] = tweets_list[i] + "."
#Creating a "marketing" string to invite people to follow the page and add it to our tweets list.

invite = "Trivia addicts unite! Follow @MrThingsTeller for your daily fix of fascinating facts."
tweets_list.append(invite)

#creating strings with no more than 275 characters to fit into a tweet
joined_string = ""
string_list = []

for element in tweets_list:
    if len(joined_string) + len(element) <= 275:
        joined_string += element
    else:
        string_list.append(joined_string)
        joined_string = element

string_list.append(joined_string)

#Replacing all topic expressoins by hashtag format. First, need to concatenate topic words and add"#", then replace it in all strings.

topic_hashtag = "#" + "".join(topic.split())

for i in range(len(string_list)):
    string_list[i] = re.sub(re.compile(topic, re.IGNORECASE), topic_hashtag, string_list[i])


#Replacing all Specific Hashtag expressoins by hashtag format. First, need to concatenate specific hashtag words and add"#", then replace it in all strings.

specific_hashtag = "#" + "".join(specific.split())

for i in range(len(string_list)):
    string_list[i] = re.sub(re.compile(specific, re.IGNORECASE), specific_hashtag, string_list[i])

#Sometimes, our string_list has an empty string as first element. If that happens, I'll delete it.

if string_list[0] == "":
    string_list.pop(0)

#When joining strings, sometimes there are sentences with no space after ".". So if a "." has not a space after it, should be fixed. Fixing that:

def replace_middle_dot(strings):
    new_strings = []
    for string in strings:
        new_string = ''
        for i, char in enumerate(string):
            if char == "." and i > 0 and i < len(string) - 1 and string[i-1] != " " and string[i+1] != " ":
                new_string += ". "
            else:
                new_string += char
        new_strings.append(new_string)
    return new_strings

string_list = replace_middle_dot(string_list)

print('topic: ' + topic)
print('specific: ' + specific)
print(tweets_list)
print(string_list)
print(len(tweets_list))
print(len(string_list))
print(len(tweets_list[0]))
print(string_list[0])

#Now, we have all our text done and organised. Its time to get an image to go along with our first tweet to make it more appealing. Lets use google images for that!
# API Key for Google Custom Search API
api_key = Keys.Gapikey
# Custom Search Engine ID
cx = Keys.GCSEngineID
# Query for the images
query = f'{topic}' + ' ' + f'{specific}'
# URL for the API request
url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&searchType=image"
# Make the API request
response = requests.get(url)
# Parse the JSON response
data = json.loads(response.text)
# Get the first image URL from the response
first_image_url = data["items"][0]["link"]
# Download the image
response = requests.get(first_image_url)
# Save the image to a file
with open("image.jpg", "wb") as f:
    f.write(response.content)

#       Finally we are goinf to prepare the tweet posting of a thread and include an image in the first post:
# changing "String_list" variable to "tweets" - it is more simple and makes more sense.
tweets = string_list
#        Post the first tweet with an image
#filename = "image.jpg"
#response = api.media_upload(filename)
#media_id = response.media_id
#Post_Tweet = api.update_status(tweets[0], media_ids=[media_id])

#for tweet in tweets[1:]:
#    recent_tweets = api.user_timeline()
#    most_recent_tweet = recent_tweets[0]
#    # Get the ID of the most recent tweet
#    most_recent_tweet_id = most_recent_tweet.id
#    api.update_status(tweet, in_reply_to_status_id=most_recent_tweet_id)
#    #api.update_status(tweet, in_reply_to_status_id=previous_tweet_id)
#    #previous_tweet_id = api.update_status(tweet).id





#Image Prompt Creation
#image_prompt = f' {top_trend} with a robot holding a book. make it in Rembrandts old painting style.'
#image_prompt = f'a robot in a very old library alongside with {top_trend} in the same room. make it in Rembrandts old painting style.'

#Getting DAll E image
#image_response = openai.Image.create(
#  prompt=image_prompt,
#  n=1,
#  size="1024x1024"
#)
#image_url = image_response['data'][0]['url']
#image_response = requests.get(image_url)
#open('image.jpg', 'wb').write(image_response.content)

if __name__== '__main__':
    tweet()






#user = api.get_user(screen_name='neymarjr')
#print(user.description)
#print(user.followers_count)


#CENAS PARA CORRIGIR
#HASHTAG TEM ESPACOS!!

#TRENDS _ PART _ REMOVED everything down here
#defining Trends to use in GPT prompt
#api = api()
#trends = api.get_place_trends(1)
#top_trend = (trends[0]['trends'][0]['name'])
#top_trend = top_trend.replace("#","",1)
#top_trend = top_trend.replace("_", " ")
#flag = False
#for i in range(len(top_trend)-1):
#    if top_trend[i].isupper() and top_trend[i+1].isupper():
#        flag = True
#        break
#if flag:
#    top_trend_with_spaces = top_trend
#else:
#    top_trend_with_spaces = " ".join(re.findall(r"[A-Z][a-z]*",top_trend))
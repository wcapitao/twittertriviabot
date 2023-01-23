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

#import Keys.py

#defining API access
def api():
    auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    return tweepy.API(auth)

api = api()

#defining 'Post Tweet'
def tweet(api: tweepy.API, message: str, image_path = None):
    if image_path:
        api.update_status_with_media(message, image_path)
    else:
        api.update_status(message)

    print('Tweeted successfully!')

#defining Trends to use in GPT prompt
#api = api()
trends = api.get_place_trends(1)
top_trend = (trends[0]['trends'][0]['name'])
top_trend = top_trend.replace("#","",1)
top_trend = top_trend.replace("_", " ")
top_trend_with_spaces = " ".join(re.findall(r"[A-Z][a-z]*",top_trend))

print((trends[0]['trends'][0]['name']))
print(top_trend)
print(top_trend_with_spaces)

#Prompt Creation
len = len(top_trend)
prompt = f'tell me an interesting trivia about {top_trend_with_spaces}. ' \
         f'Must start with "Did you Know".' \
         f'Must use no more than {270-len} characters.' \
         f'End the text with: #{top_trend}'

#accessing openAI
openai.organization = "org-NCsMrMMWlSqR7svMbRTWd81T"
openai.api_key = apiKey_OpenAI
openai.Model.list()

#Getting Response
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.8,
  max_tokens=70,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
)

#Getting final text for tweet
tweet_message = response["choices"][0]["text"]

#Image Prompt Creation
image_prompt = f' {top_trend} with a robot holding a book. make it in Rembrandts old painting style.'
#image_prompt = f'a robot in a very old library alongside with {top_trend} in the same room. make it in Rembrandts old painting style.'

#Getting DAll E image
image_response = openai.Image.create(
  prompt=image_prompt,
  n=1,
  size="1024x1024"
)
image_url = image_response['data'][0]['url']
image_response = requests.get(image_url)
open('image.jpg', 'wb').write(image_response.content)

#Start Tweet process
if __name__== '__main__':
    tweet(api, tweet_message, 'image.jpg')
    #user = api.get_user(screen_name='neymarjr')
    #print(user.description)
    #print(user.followers_count)


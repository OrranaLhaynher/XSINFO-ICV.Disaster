# -*- coding: utf-8 -*-
# Documentação da Lib
# http://docs.tweepy.org/en/v3.8.0/getting_started.html

import tweepy
import json

ENVS_KEYS = json.loads(
    open('ENVS.json', 'r').read()
)

# Autenticando Tokens do APP
api = tweepy.API(
    tweepy.AppAuthHandler(
        ENVS_KEYS['API_KEY'],
        ENVS_KEYS['API_SECRET']
    ),
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True
)

LAST_ID = None
RESULTS_GEO = 0
RESULT_ALL = 0
FLAG_FILTER = ''  # '-filter:retweets'

data_output = open("DATA.json", "a")

# Pega o id do último tweet.
for index in open("DATA.json", "r"):
    LAST_ID = json.loads(index)["id"]

while True:
    try:
        # q='' + FLAG_FILTER, #parâmetro opcional
        for tweet in api.search(geocode="%f,%f,%dkm" %
                                (
                                    ENVS_KEYS['LATITUDE'],
                                    ENVS_KEYS['LONGITUDE'],
                                    ENVS_KEYS['MAX_RANGE']
                                ),
                                count=100,
                                max_id=LAST_ID,
                                tweet_mode='extended'):
            if tweet.geo:

                print("\n[✅ ]- - - - - - - - - - - - - - - - - - - - - -")
                lat, long = tweet.geo['coordinates']
                print(" User: ", tweet.user.screen_name)
                print(" Data: ", tweet.created_at)
                print(" Profile: https://twitter.com/%s" %
                      tweet.user.screen_name)
                print(" Maps: https://maps.google.com/?q=%s,%s" % (lat, long))

                data_output.write(str(json.dumps(tweet._json)) + "\n")

                print(
                    " Percorridos >>  [\x1b[31m%d\x1b[0m] Tweets..." % RESULT_ALL)
                print(
                    " Validos     >>  [\x1b[31m%d\x1b[0m] Tweets..." % RESULTS_GEO)
                RESULTS_GEO += 1

            RESULT_ALL += 1
            LAST_ID = tweet.id
    except:

        print("\n 👿 Meu parceiro, deu merda, e eu não sei o que foi!")

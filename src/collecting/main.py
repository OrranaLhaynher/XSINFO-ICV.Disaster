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


def get_last_id(url_path):
    '''
    Pega o id do último tweet
    '''
    tmp = None
    for index in open(url_path, "r"):
        tmp = json.loads(index)['id']
    return tmp


while True:

    # Configurações gerais
    URL_PATH = "DATA.json"
    RESULTS_GEO = 0
    RESULT_ALL = 0
    RESULT_TWEETS = 0
    DATA_OUTPUT = open(URL_PATH, "a")
    LAST_ID = get_last_id(URL_PATH)
    FLAG_FILTER = ''  # '-filter:retweets'

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

                print("\n[✔️ ]- - - - - - - - - - - - - - - - - - - - - -")
                lat, long = tweet.geo['coordinates']
                print(" User: ", tweet.user.screen_name)
                print(" Data: ", tweet.created_at)
                print(" Profile: https://twitter.com/%s" %
                      tweet.user.screen_name)
                print(" Maps: https://maps.google.com/?q=%s,%s" % (lat, long))

                DATA_OUTPUT.write(str(json.dumps(tweet._json)) + "\n")

                print(
                    " Percorridos >>  [\x1b[31m%d\x1b[0m] Tweets..." % RESULT_ALL)
                print(
                    " Validos     >>  [\x1b[31m%d\x1b[0m] Tweets..." % RESULTS_GEO)
                RESULTS_GEO += 1

            RESULT_ALL += 1
            LAST_ID = tweet.id
    except:

        print("\n 👿 Meu parceiro, deu merda, e eu não sei o que foi!")

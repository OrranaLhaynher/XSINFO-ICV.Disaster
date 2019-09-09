import tweepy
import json
import time

# pointer file  de saida
data_output = open("DATA_TIMELINE.json", "w")
# Configurações gerais
LAST_ID = -9999
RESULTS_GEO = 0
RESULT_ALL = 0
RESULT_TWEETS = 0

# carregando arquivos de variáveis globais
ENVS_KEYS = json.loads(
    open('ENVS.json', 'r').read()
)

# Autenticando Tokens do APP MAIN
API_HIST = tweepy.API(
    tweepy.AppAuthHandler(
        ENVS_KEYS['API_KEY_HIST'],
        ENVS_KEYS['API_SECRET_HIST']
    ),
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True
)

# Autenticando APP USER TIMELINE
API_HIST_TIMELINE = tweepy.API(
    tweepy.AppAuthHandler(
        ENVS_KEYS['API_KEY_TIMELINE'],
        ENVS_KEYS['API_SECRET_TIMELINE']
    ),
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True
)

# Pega o id do último tweet.
for index in open("DATA_TIMELINE.json", "r"):
    LAST_ID = json.loads(index)["id"]

while True:
    try:
        # q='' + ' -filter:retweets' # opcional
        for tweet in API_HIST.search(geocode="%f,%f,%dkm" %
                                     (
                                             ENVS_KEYS['LATITUDE'],
                                             ENVS_KEYS['LONGITUDE'],
                                             ENVS_KEYS['MAX_RANGE']
                                     ),
                                     count=100,
                                     max_id=LAST_ID):
            RESULT_ALL += 1

            if tweet.geo:

                username = tweet.user.screen_name

                if str(tweet.id) in [x.replace('\n', '') for x in open('IDS_NOT_MINE.txt', 'r')]:
                    print("\n[❌ ]- - - - -[\x1b[46m %s \x1b[0m]- - - - -" % username)
                    continue
                else:
                    IDS_NOT_MINE = open("IDS_NOT_MINE.txt", "w")
                    IDS_NOT_MINE.write(str(tweet.id) + "\n")
                    IDS_NOT_MINE.close()

                print("\n[✅ ]- - - - -[\x1b[46m %s \x1b[0m]- - - - -" % username)

                for user_timeline in tweepy.Cursor(API_HIST_TIMELINE.user_timeline, screen_name='@'+str(username), tweet_mode="extended").items():
                    # gravando json no arquivo
                    data_output.write(
                        str(json.dumps(user_timeline._json)) + "\n"
                    )
                    # formatando data
                    tweet_date = str(str(
                        user_timeline.created_at).split(' ')[0]).replace('.', ' ')

                    # comparando para interromper coleta na timeline do user
                    if tweet_date <= ENVS_KEYS['LIMIT_DATE']:
                        break

                    RESULT_TWEETS += 1

                print(
                    "\n Percorridos     >>  [\x1b[31m%d\x1b[0m] Tweets..." % RESULT_ALL)
                print(
                    " Validos           >>  [\x1b[31m%d\x1b[0m] Tweets..." % RESULTS_GEO)
                print(
                    " Total de Tweets   >>  [\x1b[31m%d\x1b[0m] Tweets..." % RESULT_TWEETS)

                RESULTS_GEO += 1
            LAST_ID = tweet.id
    except:
        print("\n Timeout API 👿 \n")

import tweepy
import json

# Lê as Tokens de acesso à API do Twitter
ENVS_KEYS = json.loads(
    open('ENVS.json', 'r').read()
)

# Autenticando Tokens
api = tweepy.API(
    tweepy.AppAuthHandler(
        ENVS_KEYS['API_KEY'],
        ENVS_KEYS['API_SECRET']
    ),
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True
)


def get_last_id(url_path):
    ''' Pega o id do último tweet '''
    try:
        return list(reversed(
            [json.loads(x)['id'] for x in open(url_path, 'r')]
        ))[0]
    except:
        return None


if __name__ == "__main__":

    # Configurações gerais
    URL_PATH = "DATA.json"
    RESULTS_GEO = 0
    RESULT_ALL = 0
    RESULT_TWEETS = 0
    DATA_OUTPUT = open(URL_PATH, "a")
    LAST_ID = get_last_id(URL_PATH)
    GEO_PARAMS = "%f,%f,%dkm" % (
        ENVS_KEYS['LATITUDE'],
        ENVS_KEYS['LONGITUDE'],
        ENVS_KEYS['MAX_RANGE']
    )
    print('LAST', LAST_ID)
    print("-")
    while True:
        print("+")
        try:

            for tweet in api.search(geocode=GEO_PARAMS,
                                    count=100,
                                    max_id=LAST_ID,
                                    tweet_mode='extended'):
                if tweet.geo:
                    print('*')
                    DATA_OUTPUT.write(str(json.dumps(tweet._json)) + "\n")
                LAST_ID = tweet.id
        except:
            print("\n Limite da API atingido!")

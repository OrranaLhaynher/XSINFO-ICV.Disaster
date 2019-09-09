import time
import csv
import json

#  Para para o parser do datetime TWT
#  https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
#  https://stackabuse.com/how-to-format-dates-in-python/

data_output_csv = csv.writer(open("DATA_FINAL.csv", 'w'))
data_output_json = open("DATA_FINAL.json", 'w')

data_output_csv.writerow((
    'tweet_id',
    'screen_name',
    'location',
    'status_count',
    'followers_count',
    'friends_count',
    'lang',
    'text',
    'date',
    'time',
    'favourite_count',
    'hashtags',
    'source_device',
    'latitude',
    'longitude'
))

for tweet in open("DATA.json", "r"):

    item = json.loads(tweet)

    hashtags = (hash_word['text']
                for hash_word in item['entities']['hashtags']
                )

    lat, long = item['geo']['coordinates']

    # formatando date e time
    tweet_date, tweet_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
        item['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
    )).split(' ')

    data_output_csv.writerow([
        item['user']['id_str'],
        item['user']['screen_name'],
        item['user']['location'],
        item['user']['statuses_count'],
        item['user']['followers_count'],
        item['user']['friends_count'],
        item['lang'],
        item['full_text'].replace('\n', ''),
        tweet_date,
        tweet_time,
        item['favorite_count'],
        ' '.join(hashtags),
        item['source'],
        lat,
        long
    ])

    data_output_json.write(
        str(
            json.dumps({
                'tweet_id': item['user']['id_str'],
                'screen_name': item['user']['screen_name'],
                'location': item['user']['location'],
                'status_count': item['user']['statuses_count'],
                'followers_count': item['user']['followers_count'],
                'friends_count': item['user']['friends_count'],
                'lang': item['lang'],
                'text': item['full_text'].replace('\n', ''),
                'date': tweet_date,
                'time': tweet_time,
                'favourite_count': item['favorite_count'],
                'hashtags': ' '.join(hashtags),
                'source_device': item['source'],
                'latitude': lat,
                'longitude': long
            })
        ) + '\n'
    )

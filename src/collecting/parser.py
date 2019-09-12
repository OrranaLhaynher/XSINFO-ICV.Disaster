import time
import csv
import json
import sys
import pandas as pd

#  Para para o parser do datetime TWT
#  https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
#  https://stackabuse.com/how-to-format-dates-in-python/

data_output_json = open("DATA_FINAL.json", 'w')

if __name__ == "__main__":
    for tweet in open(sys.argv[1], "r"):

        item = json.loads(tweet)
        # pegando todas as hashtags sem o caractere '#'
        hashtags = (
            hash_word['text']
            for hash_word in item['entities']['hashtags']
        )
        lat, long = item['geo']['coordinates']
        # formatando date e time
        tweet_date, tweet_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
            item['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
        )).split(' ')

        data_output_json.write(
            str(json.dumps({
                'user_id': item['user']['id_str'],
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
            })) + '\n'
        )
    data_output_json.close()
    dataframe_json = pd.read_json("DATA_FINAL.json", lines=True)
    dataframe_json.to_csv("DATA_FINAL.csv", index=None)

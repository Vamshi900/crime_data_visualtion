import requests
import os
import json
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import time


def get_tweets(st, et, words, ns_tokens=[], j0=0):
    # building the tweets dataframes

    headers = {
        "Authorization": "Bearer BLAH"}
    if len(ns_tokens) > 0:
        ns_tokens = [ns_tokens]

    for j in range(j0, 500):
        tweet_lst = []
        users_lst = []
        # places_lst=[]

        for i in range(0, 100):
            # print(j,i)
            query_params = {'query': words, 'expansions': 'author_id',
                            'tweet.fields': 'id,created_at,author_id,text,public_metrics',
                            'user.fields': 'username', 'max_results': '100', 'start_time': st, 'end_time': et}

            if (i > 0) or (j > 0):
                # print(ns_tokens[-1])
                query_params = {'query': words, 'next_token': ns_tokens[-1], 'expansions': 'author_id',
                                'tweet.fields': 'id,created_at,author_id,text,public_metrics',
                                'user.fields': 'username', 'max_results': '100', 'start_time': st, 'end_time': et}
            response = requests.request(
                "GET", search_url, headers=headers, params=query_params)
            soup = BeautifulSoup(response.text, 'html.parser')
            s1 = str(soup)
            js = json.loads(s1)
            # print(js)
            try:
                js2 = js['meta']
            except:
                print(i)
                print(js)
                js2 = js['meta']

            if ('next_token' in js2.keys()):

                ns = js2['next_token']
                # print('next',ns)
                ns_tokens.append(ns)
            else:
                ns_df = pd.DataFrame(ns_tokens)
                for tweet in js['data']:
                    tweet_lst.append([tweet['created_at'], tweet['id'], tweet['author_id'], tweet['text'],
                                      tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'],
                                      tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count']])
                for users in js['includes']['users']:
                    users_lst.append([users['id'], users['username']])

                users_df = pd.DataFrame(users_lst, columns=['id', 'username'])
                # places_df=pd.DataFrame(places_lst, columns=['id','full_name','name','geo','place_type'])
                tweet_df = pd.DataFrame(tweet_lst,
                                        columns=['time', 'id', 'author_id', 'text', 'retweet', 'reply', 'like',
                                                 'quote'])

                tweet_df.to_csv(
                    'tweet_df' + words.replace(':', '') + str(j * 100) + 'to' + str((j + 1) * 100 - 1) + st[:12] + et[
                        :12] + '.csv')
                users_df.to_csv(
                    'users_df' + words.replace(':', '') + str(j * 100) + 'to' + str((j + 1) * 100 - 1) + st[:12] + et[
                        :12] + '.csv')
                # places_df.to_csv('/content/gdrive/MyDrive/twitterAPI/powerout/places_df'+str(j*100)+'to'+str((j+1)*100-1)+st+et+'.csv')
                ns_df.to_csv(
                    'ns_df' + words.replace(':', '') + str(j * 100) + 'to' + str((j + 1) * 100 - 1) + st[:12] + et[
                        :12] + '.csv')
                print('wow', i, j)

                ns_tokens = []
            for tweet in js['data']:
                tweet_lst.append([tweet['created_at'], tweet['id'], tweet['author_id'], tweet['text'],
                                  tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'],
                                  tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count']])
            for users in js['includes']['users']:
                users_lst.append([users['id'], users['username']])

            # for places in js['includes']['places']:
            #  places_lst.append([places['id'],places['full_name'],places['name'],places['geo'],places['place_type']])

            # to make sure within the rate limit, 300 requests per 15 minutes
            time.sleep(5)
        ns_df = pd.DataFrame(ns_tokens)

        users_df = pd.DataFrame(users_lst, columns=['id', 'username'])
        # places_df=pd.DataFrame(places_lst, columns=['id','full_name','name','geo','place_type'])
        tweet_df = pd.DataFrame(tweet_lst,
                                columns=['time', 'id', 'author_id', 'text', 'retweet', 'reply', 'like', 'quote'])

        tweet_df.to_csv(
            'tweet_df' + words.replace(':', '') + str(j * 100) + 'to' + str((j + 1) * 100 - 1) + st[:12] + et[
                :12] + '.csv')
        users_df.to_csv(
            'users_df' + words.replace(':', '') + str(j * 100) + 'to' + str((j + 1) * 100 - 1) + st[:12] + et[
                :12] + '.csv')
        # places_df.to_csv('/content/gdrive/MyDrive/twitterAPI/powerout/places_df'+str(j*100)+'to'+str((j+1)*100-1)+st+et+'.csv')
        ns_df.to_csv('ns_df' + words.replace(':', '') + str(j * 100) + 'to' + str((j + 1) * 100 - 1) + st[:12] + et[
            :12] + '.csv')
        ns_tokens = ns_tokens[-2:]
        print(j, len(tweet_lst))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bearer_token = os.environ.get("BEARER_TOKEN")

    search_url = "https://api.twitter.com/2/tweets/search/all"
    # if you have standard access, you can use the search url below instead, to search recent tweets from a week before
    #search_url = "https://api.twitter.com/2/tweets/search/recent"
    st = '2021-07-27T00:00:00Z'
    et = '2021-07-29T14:22:00Z'
    words = 'Simone Biles'

    get_tweets(st, et, words)

import tweepy
import pandas
import openpyxl
from datetime import datetime
import os
import zipfile


# авторизация в апи твиттера
def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    global api
    api = tweepy.API(auth)
    return api

tweets = []
users_info = []


# получение информации о юзернейме
def get_user_info(tweet):
    u = {}
    user_created_at = datetime.strptime((tweet._json.get('user').get('created_at')), '%a %b %d %X %z %Y')
    u['user'] = tweet._json.get('user').get('screen_name')
    u['name'] = tweet._json.get('user').get('name')
    u['location'] = tweet._json.get('user').get('location')
    u['friends'] = tweet._json.get('user').get('friends_count')
    u['followers'] = tweet._json.get('user').get('followers_count')
    u['creation_date'] = user_created_at.strftime('%Y-%m-%d')
    u['description'] = tweet._json.get('user').get('description')
    return users_info.append(u)


# создание архивного файла с результатом выборки
def make_file(tweets_df, user_info_df):
    name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    with pandas.ExcelWriter(name + '.xlsx') as writer:
        tweets_df.to_excel(writer, sheet_name='tweets')
        user_info_df.to_excel(writer, sheet_name='user_info')
    with zipfile.ZipFile(name + '.zip', 'w') as zip:
        zip.write(name + '.xlsx')
    os.remove(name + '.xlsx')


def query_tweets(*args):
    if len(args) == 3:
        query = args[0]
        count = args[1]
        result = args[2]

        for tweet in tweepy.Cursor(api.search, q=query, result_type=result).items(count):
            t = {}
            created_at = datetime.strptime((tweet._json.get('created_at')), '%a %b %d %X %z %Y')
            t['name'] = tweet._json.get('user').get('screen_name')
            t['creation_date'] = created_at.strftime('%Y-%m-%d')
            t['creation_time'] = created_at.strftime('%X')
            t['text'] = tweet._json.get('text')
            tweets.append(t)

            get_user_info(tweet)

        # удаление дублей твиттов
        m = list({t['text']: t for t in tweets}.values())
        tweets_df = pandas.DataFrame(m)

        # удаление дублей пользователей
        n = list({u['user']: u for u in users_info}.values())
        users_info_df = pandas.DataFrame(n)

        make_file(tweets_df, users_info_df)

    else:
        query = args[0]
        count = args[1]
        result = args[2]
        until = args[3]

        for tweet in tweepy.Cursor(api.search, q=query, result_type=result, until=until).items(count):
            t = {}
            created_at = datetime.strptime((tweet._json.get('created_at')), '%a %b %d %X %z %Y')
            t['name'] = tweet._json.get('user').get('screen_name')
            t['creation_date'] = created_at.strftime('%Y-%m-%d')
            t['creation_time'] = created_at.strftime('%X')
            t['text'] = tweet._json.get('text')
            tweets.append(t)

            get_user_info(tweet)

        # удаление дублей твиттов
        m = list({t['text']: t for t in tweets}.values())
        tweets_df = pandas.DataFrame(m)

        # удаление дублей пользователей
        n = list({u['user']: u for u in users_info}.values())
        users_info_df = pandas.DataFrame(n)

        make_file(tweets_df, users_info_df)

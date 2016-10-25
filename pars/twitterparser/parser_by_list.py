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
user_info = []


# получение информации о юзернейме
def get_user_info(username):
    u = {}
    user = api.get_user(username)._json
    user_created_at = datetime.strptime((user.get('created_at')), '%a %b %d %X %z %Y')
    u['user'] = user.get('screen_name')
    u['name'] = user.get('name')
    u['location'] = user.get('location')
    u['friends'] = user.get('friends_count')
    u['followers'] = user.get('followers_count')
    u['creation_date'] = user_created_at.strftime('%Y-%m-%d')
    u['description'] = user.get('description')
    return user_info.append(u)


# создание архивного файла с результатом выборки
def make_file(tweets_df, user_info_df):
    name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    with pandas.ExcelWriter(name + '.xlsx') as writer:
        tweets_df.to_excel(writer, sheet_name='tweets')
        user_info_df.to_excel(writer, sheet_name='user_info')
    with zipfile.ZipFile(name + '.zip', 'w') as zip:
        zip.write(name + '.xlsx')
    os.remove(name + '.xlsx')


def user_tweets(*args):
    # все твитты пользователей
    if len(args) == 1:
        username_list = args[0]

        for username in username_list:
            for tweet in tweepy.Cursor(api.user_timeline, username).items():
                t = {}
                created_at = datetime.strptime((tweet._json.get('created_at')), '%a %b %d %X %z %Y')
                t['name'] = username
                t['creation_date'] = created_at.strftime('%Y-%m-%d')
                t['creation_time'] = created_at.strftime('%X')
                t['text'] = tweet._json.get('text')
                tweets.append(t)

            get_user_info(username)

        tweets_df = pandas.DataFrame(tweets)
        user_info_df = pandas.DataFrame(user_info)

        make_file(tweets_df, user_info_df)

    # заданное количество твиттов
    else:
        username_list = args[0]
        count = args[1]

        for username in username_list:
            for tweet in tweepy.Cursor(api.user_timeline, username).items(count):
                d = {}
                created_at = datetime.strptime((tweet._json.get('created_at')), '%a %b %d %X %z %Y')
                d['name'] = username
                d['creation_date'] = created_at.strftime('%Y-%m-%d')
                d['creation_time'] = created_at.strftime('%X')
                d['text'] = tweet._json.get('text')
                tweets.append(d)

            get_user_info(username)

        tweets_df = pandas.DataFrame(tweets)
        user_info_df = pandas.DataFrame(user_info)

        make_file(tweets_df, user_info_df)

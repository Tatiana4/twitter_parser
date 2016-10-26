from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
import os
import mimetypes
import glob2
from datetime import timedelta, date
import tweepy
from .forms import ApiForm, SearchByUser, SearchByQuery


def begin(request):
    if request.POST:
        key_form = ApiForm(request.POST)
        if key_form.is_valid():
            keys = key_form.cleaned_data
            # сохраняем ключи в сессии
            request.session['apikey'] = keys['apikey']
            request.session['apisecret'] = keys['apisecret']
            request.session['token'] = keys['token']
            request.session['tokensecret'] = keys['tokensecret']
            # устанавливаем время жизни сессии 1 час
            # request.session.set_expiry(60 * 60)
            return redirect('search/')

    else:
        key_form = ApiForm()

    return render(request, 'begin.html', {'key_form': key_form})


def search(request):
    args = {}
    args.update(csrf(request))
    errors = []

    if request.POST:
        # вытаскиваем ключи из сессии
        consumer_key = request.session.get('apikey')
        consumer_secret = request.session.get('apisecret')
        access_token = request.session.get('token')
        access_token_secret = request.session.get('tokensecret')

        user_form = SearchByUser(request.POST)
        query_form = SearchByQuery(request.POST)

        # проверяем, заполнены ли поля формы поиска по пользователю
        if user_form.is_valid() and user_form.has_changed():
            from . import parser_by_list
            params = user_form.cleaned_data
            usernames = params['usernames'].split(', ')
            count = params['count']
            # авторизуем пользователя в апи твиттера и выполняем выборку
            if count is None:
                # если количество не задано, парсим все твитты
                try:
                    parser_by_list.auth(consumer_key, consumer_secret,
                                        access_token, access_token_secret)
                    parser_by_list.user_tweets(usernames)
                except tweepy.TweepError as e:
                    # на тот случай, если при вводе имени допущена ошибка
                    if int((str(e).split('= '))[-1]) == 404:
                        errors.append('Пользователь не найден')
            else:
                try:
                    parser_by_list.auth(consumer_key, consumer_secret,
                                        access_token, access_token_secret)
                    parser_by_list.user_tweets(usernames, count)
                except tweepy.TweepError as e:
                    # на тот случай, если при вводе имени допущена ошибка
                    if int((str(e).split('= '))[-1]) == 404:
                        errors.append('Пользователь не найден')

            if not errors:
                return redirect('/result/')
            else:
                return render(request, 'search.html',
                              {'user_form': user_form, 'query_form': query_form, 'errors': errors})

        # если поиск по пользователю пуст, проверяем поля формы поиска по ключевым словам
        elif query_form.is_valid() and query_form.has_changed():
            from . import parser_by_query
            params = query_form.cleaned_data
            query = params['query']
            count1 = params['count1']
            result_type = params['result_type']
            until = params['date']

            # если дата введена
            if until is not None:
                # проверяем введенную дату
                now = date.today()
                delta = now - until
                min_delta = timedelta(days=7)
                if delta < min_delta:
                    # авторизуем пользователя в апи твиттера и выполняем выборку
                    parser_by_query.auth(consumer_key, consumer_secret,
                                         access_token, access_token_secret)
                    parser_by_query.query_tweets(query, count1, result_type, until)
                else:
                    errors.append('Введенная дата старше 1 недели')

            # если дата не введена
            else:
                parser_by_query.auth(consumer_key, consumer_secret,
                                     access_token, access_token_secret)
                parser_by_query.query_tweets(query, count1, result_type)

            if not errors:
                return redirect('/result/')
            else:
                return render(request, 'search.html',
                              {'user_form': user_form, 'query_form': query_form, 'errors': errors})

    else:
        user_form = SearchByUser(request.POST)
        query_form = SearchByQuery(request.POST)

    return render(request, 'search.html', {'user_form': user_form, 'query_form': query_form})


def result(request):
    return render(request, 'result.html')


def download(request):
    # находим сформированный файл, отдаем его на скачивание и удаляем
    fname = glob2.glob('*.zip')[0]
    f = open(fname, 'rb')
    response = HttpResponse(f.read())
    f.close()
    file_type = mimetypes.guess_type(fname)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(fname).st_size)
    response['Content-Disposition'] = "attachment; filename=output.zip"
    os.remove(fname)

    return response


def how_to(request):
    return render(request, 'how_to.html')

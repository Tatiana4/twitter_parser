from django import forms


class ApiForm(forms.Form):
    apikey = forms.CharField(max_length=25, min_length=25,
                             required=True, label='Consumer Key (API Key):',
                             widget=forms.TextInput(attrs={'class': 'pure-input-1'}))
    apisecret = forms.CharField(max_length=50, min_length=50,
                                required=True, label='Consumer Secret (API Secret):',
                                widget=forms.TextInput(attrs={'class': 'pure-input-1'}))
    token = forms.CharField(max_length=50, min_length=50,
                            required=True, label='Access Token:',
                            widget=forms.TextInput(attrs={'class': 'pure-input-1'}))
    tokensecret = forms.CharField(max_length=45, min_length=45,
                                  required=True, label='Access Token Secret:',
                                  widget=forms.TextInput(attrs={'class': 'pure-input-1'}))


class SearchByUser(forms.Form):
    usernames = forms.CharField(label='имя пользователя:', required=False,
                                widget=forms.TextInput(attrs={'class': 'pure-input-2-3',
                                                              'title': 'без @. их может быть несколько - через запятую'}))
    count = forms.IntegerField(label='количество твитов:', required=False,
                               widget=forms.NumberInput(attrs={'class': 'pure-input-2-3',
                                                               'title': 'можно оставить пустым, тогда будут выбраны все'}))


class SearchByQuery(forms.Form):
    result_type_choices = (('recent', 'последние'), ('popular', 'популярные'), ('mixed', 'смешанные'))
    query = forms.CharField(label='ключевые слова:', required=False,
                            widget=forms.TextInput(attrs={'class': 'pure-input-2-3'}))
    count1 = forms.IntegerField(label='количество твитов:', required=False,
                               widget=forms.NumberInput(attrs={'class': 'pure-input-2-3'}))
    result_type = forms.ChoiceField(choices=result_type_choices, label='тип выборки:', required=False,
                               widget=forms.Select(attrs={'class': 'pure-input-2-3'}))
    date = forms.DateField(label='дата:', required=False,
                           widget=forms.DateInput(attrs={'class': 'pure-input-2-3', 'title': 'в формате YYYY-MM-DD'}))

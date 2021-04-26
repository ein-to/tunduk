from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    return render(request, 'tunduk_app/index.html')

def test_request(request):
    Header = {'Content-type': 'application/json; charset=UTF-8'}
    data = open('request.xml')
    response = requests.get('https://31.186.53.85', headers=Header, data=data, cert=('subsystemName.crt', 'subsystemName.key'))
    #response = requests.get('https://api.github.com')

    return render(request, 'tunduk_app/response.html', {'response': response.status_code})

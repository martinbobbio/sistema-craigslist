import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models

BASE_CAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return  render(request, 'base.html')

def new_search(request):

    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    url = BASE_CAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(url)

    soup = BeautifulSoup(response.text, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
    posts = []

    for post in post_listings:
        title = post.find(class_='result-title').text
        utl = post.find('a').get('href')

        if post.find(class_='result-price'):
            price = post.find(class_='result-price').text
        else:
            price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            photo_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            photo = BASE_IMAGE_URL.format(photo_id)
        else:
            photo = 'https://craigslist.org/images/peace.jpg'

        posts.append({ 'title':title, 'url':url, 'price':price, 'photo':photo })

    data = { 'search':search, 'posts': posts }

    return render(request, 'app/new_search.html', data)
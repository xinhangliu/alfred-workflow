# coding: utf-8
import urllib
import urllib2
import json
import os
import sys
import ConfigParser
import re


config = ConfigParser.ConfigParser()
config.read('conf')
max_items = config.getint('base', 'max_items') if config.has_option('base', 'max_items') else 20
auto_sort = config.getboolean('base', 'auto_sort') if config.has_option('base', 'auto_sort') else False
quick_search = config.get('base', 'quick_search') if config.has_option('base', 'quick_search') else 'movie'
apikey = config.get('base', 'apikey') if config.has_option('base', 'apikey') else ''

selection = os.getenv('selection') if os.getenv('selection') else quick_search

query = sys.argv[1]

tip = 'Go to Douban'


def get_raw(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    res = json.loads(response.read())
    return res


def gen_url(sel, q):
    base_url = 'https://api.douban.com/v2/'
    params = dict()
    params['q'] = q
    params['count'] = max_items if max_items > 0 else 20
    if re.match('\w{32}', apikey):
        params['apikey'] = apikey
    s = {
        'user': '?'
    }.get(sel, '/search?')
    url = base_url + sel + s + urllib.urlencode(params)
    return url


def movie(raw_data, sort):
    res = []
    for raw in raw_data['subjects']:
        item = dict()
        if sort:
            item['uid'] = raw['id']
        item['arg'] = raw['alt']
        item['title'] = '%s (%s)' % (raw['title'], raw['year'])
        item['quicklookurl'] = raw['images']['large']
        rating = 'Rating: ' + str(raw['rating']['average']) + ' ' if raw['rating']['average'] != 0 else ''
        genres = 'Tags: ' + ', '.join(raw['genres']) if raw['genres'] else ''
        original_title = 'Alias: ' + raw['original_title'] + ' ' if raw['original_title'] else ''
        item['subtitle'] = '%s%s%s' % (rating, original_title, genres)
        item['icon'] = dict(path='image/movie_item.png')
        res.append(item)
    return res


def book(raw_data, sort):
    res = []
    for raw in raw_data['books']:
        item = dict()
        if sort:
            item['uid'] = raw['id']
        item['arg'] = raw['alt']
        origin_title = ' (%s)' % raw['origin_title'] if raw['origin_title'] else ''
        subtitle = ' - %s' % raw['subtitle'] if raw['subtitle'] else ''
        item['title'] = raw['title'] + origin_title + subtitle
        item['quicklookurl'] = raw['images']['large']
        rating = 'Rating: ' + str(raw['rating']['average']) + ' ' if raw['rating']['average'] != 0 else ''
        author = 'Author: ' + ', '.join(raw['author']) + ' ' if raw['author'] else ''
        translator = 'Translator: ' + ', '.join(raw['translator']) + ' ' if raw['translator'] else ''
        publisher = raw['publisher'] if raw['publisher'] else ''
        pubdate = raw['pubdate'] if raw['pubdate'] else ''
        pub = 'Pub: ' + publisher + ', ' + pubdate + ''
        item['subtitle'] = '%s%s%s%s' % (rating, author, translator, pub)
        item['icon'] = dict(path='image/book_item.png')
        res.append(item)
    return res


def music(raw_data, sort):
    res = []
    for raw in raw_data['musics']:
        item = dict()
        if sort:
            item['uid'] = raw['id']
        item['arg'] = raw['alt']
        item['title'] = raw['title']
        item['quicklookurl'] = raw['image'].replace('spic', 'lpic')
        rating = 'Rating: ' + str(raw['rating']['average']) + ' | ' if raw['rating']['average'] != 0 else ''
        author = raw.get('author', '')
        author = author[0]['name'] + ' | ' if author else ''
        pubdate = raw['attrs'].get('pubdate', '')
        pubdate = pubdate[0] if pubdate else ''
        version = raw['attrs'].get('version', '')
        version = version[0] + ' | ' if version else ''
        item['subtitle'] = '%s%s%s%s' % (rating, author, version, pubdate)
        item['icon'] = dict(path='image/music_item.png')
        res.append(item)
    return res


def user(raw_data, sort):
    res = []
    for raw in raw_data['users']:
        item = dict()
        if sort:
            item['uid'] = raw['uid']
        item['arg'] = raw['alt']
        signature = ' - ' + raw['signature'] if raw['signature'] else ''
        item['title'] = '%s' % raw['name'] + signature
        item['quicklookurl'] = raw['large_avatar']
        loc_name = raw.get('loc_name', '')
        desc = raw.get('desc', '')
        sep = ' | ' if loc_name and desc else ''
        item['subtitle'] = '%s%s%s' % (loc_name, sep, desc)
        item['icon'] = dict(path='image/user_item.png')
        res.append(item)
    return res


def gen_first_item(sel):
    cat = {
        'book': 1001,
        'movie': 1002,
        'music': 1003,
        'user': 1005
    }.get(sel, '')
    base_url = 'https://www.douban.com/search'
    params = dict(q=query, cat=cat) if cat else dict(q=query)
    url = base_url + '?' + urllib.urlencode(params)
    item0 = dict()
    item0['uid'] = sel
    item0['title'] = tip
    item0['subtitle'] = 'Go to Douban search directly'
    item0['arg'] = url
    item0['icon'] = dict(path='image/douban_item.png')
    return item0


def main():
    global tip
    items = [gen_first_item(selection)]
    try:
        raw = get_raw(gen_url(selection, query))
    except urllib2.URLError or urllib2.HTTPError as e:
        if e.reason == 'Bad Request':
            tip = 'Error: %s You may exceed the limit. Try again later' % e.reason
        else:
            tip = 'Error: %s' % e.reason
        raw = None
    if raw:
        if raw.get('code', None):
            tip = 'Sorry, Douban limit. Try again later'
        else:
            items += eval(selection)(raw, auto_sort)
            if len(items) == 1:
                tip = 'Nothing Found'
    elif query == '':
        tip = 'Go to Douban'
    items[0]['title'] = tip
    j = json.dumps({'items': items})
    print(j)

if __name__ == '__main__':
    main()

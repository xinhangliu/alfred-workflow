# coding: utf-8
import sys
import json
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('conf')
selections = config.get('base', 'selections').split()

query = sys.argv[1]


def gen_item(name):
    name = name.lower()
    item = dict()
    item['title'] = 'Search Douban for \'%s\'' % query if name == 'douban' else name.capitalize()
    item['icon'] = {
        'path': 'image/' + name + '.png'
    }
    item['arg'] = query
    item['variables'] = {
        'selection': name
    }
    return item

items = []
for n in selections:
    items.append(gen_item(n))

res = json.dumps({'items': items})
print(res)

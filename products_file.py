import json

products = []
products_persist = []

with open('products.json') as data:
    products = json.load(data)

with open('products_init.json') as data:
    products_persist = json.load(data)    
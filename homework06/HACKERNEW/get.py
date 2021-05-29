import requests
from bs4 import BeautifulSoup

r = requests.get("https://news.ycombinator.com/newest")
print(r.ok)
print(r.status_code)
print(r.text[:100])
# r = requests.get("https://news.ycombinator.com/abrakadabra")
# print(r.ok, r.status_code)


from bs4 import BeautifulSoup
import requests

r = requests.get("https://news.ycombinator.com/newest")
page = BeautifulSoup(r.text, 'html.parser')
# print(page)
print(page.head.title.get_text())
print(page.head.title.text[-5:])
print(page.table.table)
tb1_list = page.table.find_all('a')
print(len(tb1_list))


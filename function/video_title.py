import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=pitbull")

content = request.content

soup = BeautifulSoup(content, 'html.parser')

for element in soup.find_all('a', {"rel": "spf-prefetch"}):
    titles = element.get("title")
    print(titles)

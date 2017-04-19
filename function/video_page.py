import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=pitbull")

content = request.content

soup = BeautifulSoup(content, 'html.parser')

pageDic = {}
for page in soup.find_all("a", {"class": True, "data-sessionlink": True, "data-visibility-tracking": True,
                                "aria-label": True}):
    # print(page.text)
    # print(page.get("href"))
    pageDic[page.text] = page.get("href")
print(pageDic)

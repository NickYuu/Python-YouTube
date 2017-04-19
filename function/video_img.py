import re
import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=pitbull")

content = request.content

soup = BeautifulSoup(content, 'html.parser')

for element in soup.find_all('a', {"rel": "spf-prefetch"}):
    imgName = element.get("href").split("=")[1]
    all_image = soup.find_all("img", {"width": True, "alt": True, "height": True, "data-ytimg": True, "onload": True})
    img = re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(imgName), str(all_image))[0].strip("\"")
    img = img.replace("&amp;", "&")

    print(img)

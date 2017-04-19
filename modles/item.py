import re
import requests
from bs4 import BeautifulSoup
import youtube_dl


def find_search_content(name):
    request = requests.get("https://www.youtube.com/results?search_query={}".format(name))
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def find_page_content(search):
    request = requests.get("https://www.youtube.com/results?{}".format(search))
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup



def find_all_video(soup: BeautifulSoup) -> list:
    all_item = list()
    for element in soup.find_all('a', {"rel": "spf-prefetch"}):
        title = element.get("title")
        link = element.get("href")
        img_name = element.get("href").split("=")[1]
        all_image = soup.find_all("img",
                                  {"width": True,
                                   "alt": True,
                                   "height": True,
                                   "data-ytimg": True,
                                   "onload": True})
        img = re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(img_name), str(all_image))
        img = img[0].strip("\"")
        img = img.replace("&amp;", "&")

        all_item.append({"title": title,
                         "link": "https://www.youtube.com{}".format(link),
                         "img": img})
    for index, time in enumerate(soup.find_all("span", {"class": "video-time"})):
        all_item[index]["time"] = str(time.text)

    return all_item


def page_bar(soup: BeautifulSoup) -> dict:
    page_dic = {}
    for page in soup.find_all("a", {"class": True,
                                    "data-sessionlink": True,
                                    "data-visibility-tracking": True,
                                    "aria-label": True}):
        page_dic[page.text] = page.get("href")
    return page_dic


def download_mp3(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        "outtmpl": "music/%(title)s.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_mp4(url: str):
    ydl_opts = {'format': 'best', "outtmpl": "video/%(title)s.%(ext)s"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

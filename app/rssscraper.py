'''

Small Application to download files from a podcasts rss feed

'''

import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def scrape_rss(feed_url:str) -> None:
    try:
        r = requests.get(url)
        print("Scraping successful: ", r.status_code)
        soup = BeautifulSoup(r.content, features="xml")
        url_list = get_urls(soup)
        download_files(url_list)

    except Exception as e:
        print("There was an error:")
        print(e)

def get_urls(soup: BeautifulSoup) -> list:
    lst = [*soup.findAll("enclosure")]
    return [*map(lambda a: a.get('url'), lst)]

def download_files(url_list: list) -> None:
    for url in url_list:
        file_name = get_file_name(url)
        home_dir = Path.home()
        file_location = f"{home_dir}/Downloads/{file_name}"
        print("Downloading: " + file_name)

        r = requests.get(url)
        output = open(file_location, "wb")
        output.write(r.content)
        output.close()


def get_file_name(url: str) -> str:
    parts = url.split("/")
    if (len(parts) == 6):
        return parts[4] + ".mp3"
    else:
        return parts[8] + ".mp3"


if __name__ == "__main__":
    url = sys.argv[1] or "example.com"
    scrape_rss(url)
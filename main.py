import wikipediaapi as wiki_api

from bs4 import BeautifulSoup
from urllib.request import urlopen

if __name__ == '__main__':

    # Used for easily navigating and accessing Wikipedia
    wiki = wiki_api.Wikipedia(
        language='en',
    )

    page = wiki.page('Python_(programming_language)')

    # print(page)

    page_html = urlopen(page.fullurl).read().decode('utf-8')

    # print(page_html)

    soup = BeautifulSoup(page_html, 'html.parser')

    refs = soup.find("ol", {"class": "references"}).findAll("li")
    print(len(refs))

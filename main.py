import wikipediaapi as wiki_api
import argparse

from bs4 import BeautifulSoup
from urllib.request import urlopen


def number_of_refs(url):
    """
    Computes the number of list items in the <ol class="references"> HTML object for the given URL.
    :param url: URL of the page to be inspected.
    :return: integer representing the number of references.
    """

    page_html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(page_html, 'html.parser')

    refs = soup.find("ol", {"class": "references"}).findAll("li")

    return len(refs)


if __name__ == '__main__':

    # Parser setup
    parser = argparse.ArgumentParser(description="Counts the number of references on a wikipedia page and the "
                                                 "references on the linked articles.")
    parser.add_argument('url', type=str, help="URL of a wikipedia article (example: "
                                              "https://en.wikipedia.org/wiki/Artificial_intelligence).")
    args = parser.parse_args()

    # Used for easily navigating and accessing Wikipedia
    wiki = wiki_api.Wikipedia(
        language='en',
    )

    # Retrieve and verify article
    page = wiki.page(args.url.split("/wiki/", 1)[1])
    if not page.exists():
        raise ValueError("Invalid Wikipedia article URL, please verify your input.")

    print(number_of_refs(page.fullurl))

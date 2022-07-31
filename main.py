import urllib.error

import argparse

from bs4 import BeautifulSoup
from urllib.request import urlopen


def number_of_refs(url):
    """
    Computes the number of list items in the <ol class="references"> HTML object for the given URL.
    :param url: URL of the page to be inspected.
    :return: integer representing the number of references.
    """

    # Print url for
    print("Inspecting : " + url)

    page_html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(page_html, 'html.parser')

    refs = soup.find("ol", {"class": "references"})
    if not refs:
        return 0

    return len(refs.findAll("li"))


if __name__ == '__main__':

    # Parser setup
    parser = argparse.ArgumentParser(description="Counts the number of references on a wikipedia page and the "
                                                 "references on the linked articles.")
    parser.add_argument('url', type=str, help="URL of a wikipedia article (example: "
                                              "https://en.wikipedia.org/wiki/Artificial_intelligence).")
    args = parser.parse_args()

    # Retrieve and verify page
    try:
        page = urlopen(args.url).read().decode('utf-8')

    # HTTP specific errors
    except urllib.error.HTTPError:
        raise ValueError("Invalid Wikipedia article URL, please verify your input.")

    # Parse page
    soup = BeautifulSoup(page, 'html.parser')

    # Find all links within the article's content
    urls = soup.find("div", {"id": "content"}).findAll("a", href=True)

    # Limit links to other wikipedia pages
    urls = ["https://en.wikipedia.org" + url['href'] for url in urls if url['href'].startswith("/wiki/")]

    # Prepend the initial page
    urls = [args.url] + urls

    # Remove duplicates
    urls = list(set(urls))

    # Remove file links
    urls = [url for url in urls if "/File:" not in url]

    # Sort links
    urls = sorted(urls)
    print(len(urls))

    ref_counts = [(url, number_of_refs(url)) for url in urls]
    print(ref_counts)


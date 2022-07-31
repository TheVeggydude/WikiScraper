import urllib.error
import argparse
import multiprocessing

from bs4 import BeautifulSoup
from urllib.request import urlopen


def number_of_refs(url):
    """
    Computes the number of list items in the <ol class="references"> HTML object for the given URL.
    :param url: URL of the page to be inspected.
    :return: Tuple containing URL string and an Integer representing the number of references.
    """

    page_html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(page_html, 'html.parser')

    refs = soup.find("ol", {"class": "references"})
    if not refs:
        return url, 0

    return url, len(refs.findAll("li"))


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
    print("Total number of pages found", len(urls))

    # Map list using parallel processing library.
    pool = multiprocessing.Pool()

    try:
        ref_counts = pool.map(number_of_refs, urls)

    finally:
        # Close parallel poop when computation is done.
        pool.close()

    print(ref_counts)

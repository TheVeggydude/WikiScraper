# WikiScraper

This scraper scrapes a given wikipedia page (e.g. 'https://en.wikipedia.org/wiki/Python_(programming_language)') for 
references used a returns the total. Moreover, it will scan for wikipedia articles used in the given page and also check
for references on all those pages.

This scraper is built using Python3.

## Usage

First, install the required libraries from the `requirements.txt` file.

Next, run the code using:

```commandline
python main.py 'https://en.wikipedia.org/wiki/Python_(programming_language)'
```

### Docker
If Docker is available, this code can be run in a Docker container. The Docker image first needs to be built, then it can simply be ran whilst providing a Wikipedia link.
```commandline
docker build -t scraper .
docker run scraper 'https://en.wikipedia.org/wiki/Python_(programming_language)'
```
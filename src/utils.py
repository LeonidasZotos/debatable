import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from config import settings


def getSource(url):
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    req = Request(url,
                  headers={'User-Agent':
                           custom_user_agent})  # mask to avoid HTTP 403 error
    try:
        webpage = urlopen(req, timeout=5).read()
        if settings['debug'] == True:
            print("Successfully opened url: " + url)
    except:
        print("Could not access source of URL: " + url)
    return soup(webpage, 'html.parser')


def getTitleFromSource(htmlSourceSoup):
    title = htmlSourceSoup.find("title").get_text()
    return title


def getTextFromSource(htmlSourceSoup):

    # kill all script and style elements
    for script in htmlSourceSoup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = htmlSourceSoup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # remove new lines from string
    text = text.replace('\n', ' ')
    return (text)


def getTextFromURL(url, listToAppendTo = None):
    source = getSource(url)
    if listToAppendTo is not None:
        listToAppendTo.append(getTextFromSource(source))
    return getTextFromSource(source)


def getTitleFromURL(url):
    source = getSource(url)
    return getTitleFromSource(source)


#function that picks x random items from list
def pickRandomItems(list, x):
    return random.sample(list, x)

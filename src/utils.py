from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup


def getSource(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) # mask to avoid HTTP 403 error
    webpage = urlopen(req).read()
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


def getTextFromURL(url):
    source = getSource(url)
    return getTextFromSource(source)

def getTitleFromURL(url):
    source = getSource(url)
    return getTitleFromSource(source)
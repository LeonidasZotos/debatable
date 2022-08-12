from urllib.request import urlopen
from bs4 import BeautifulSoup


def extractKeyTerms(url):
    all_text = extractAllText(url)
    return all_text


def extractAllText(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # remove new lines from string
    text = text.replace('\n', ' ')
    return(text)

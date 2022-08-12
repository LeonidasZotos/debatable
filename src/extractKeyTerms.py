import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from textblob import TextBlob
from collections import Counter


def extractKeyTerms(url):
    all_text = extractAllText(url)
    nouns = extractNouns(all_text)
    mostCommonNouns = getMostCommonWords(nouns)
    return mostCommonNouns


def extractNouns(text):
    # get all nouns in text
    blob = TextBlob(text)
    nouns = blob.noun_phrases
    return nouns


def getMostCommonWords(text, numberOfWords=5):
    #get most frequent words in string
    counter = Counter(text)
    mostCommonWords = counter.most_common(numberOfWords)
    justWords = [i[0] for i in mostCommonWords]
    return justWords


def extractAllText(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

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
    return (text)

keyTerms = extractKeyTerms(sys.argv[1])
print(keyTerms)
sys.exit(0)

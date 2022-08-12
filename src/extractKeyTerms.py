import sys
from textblob import TextBlob
from collections import Counter
from utils import *


def extractKeyTerms(url, method='common'):
    if method == 'common':
        all_text = getTextFromURL(url)
        nouns = extractNouns(all_text)
        keyTerms = getMostCommonWords(nouns)
    elif method == 'title':
        title = getTitleFromURL(url)
        keyTerms = extractNouns(title)
    return keyTerms


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

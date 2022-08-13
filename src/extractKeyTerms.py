import sys
from textblob import TextBlob
from collections import Counter
from utils import *
from config import settings

def extractKeyTerms(url):
    try:   
        if settings['keyTermsMethod'] == 'common':
            all_text = getTextFromURL(url)
            nouns = extractNouns(all_text)
            keyTerms = getMostCommonWords(nouns)
        elif settings['keyTermsMethod'] == 'title':
            title = getTitleFromURL(url)
            keyTerms = extractNouns(title)
    except:
        print("Key terms could not be retrieved, check that the link works.")
        sys.exit(0)
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

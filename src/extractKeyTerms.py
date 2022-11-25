import sys
from textblob import TextBlob
from collections import Counter
from newspaper import Article

from config import settings


def extractKeyTerms(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        if settings['keyTermsMethod'] == 'common':
            allText = article.text
            nouns = extractNouns(allText)
            keyTerms = getMostCommonWords(nouns)
        elif settings['keyTermsMethod'] == 'title':
            title = article.title
            keyTerms = extractNouns(title)
    except Exception as e:
        print("Key terms could not be retrieved, returning None.", e)
        return None
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

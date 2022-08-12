import numpy as np

from utils import *
from textblob import TextBlob


#Extracts text from the list of urls
def extractTextFromUrls(listOfUrls):
    allTexts = []

    for url in listOfUrls:
        try:
            text = getTextFromURL(url)
            allTexts.append(text)
            print("success!")
        except:
            print('Could not get text from url: ' + url)
            pass

    return allTexts


#calculate sentiment polarity of text, based on adjectives and adverbs
def calculateSentiment(text):
    blob = TextBlob(text)
    blob = blob.tags
    blob = [word for word, pos in blob if pos in ['JJ', 'RB']]
    blob = ' '.join(blob)
    blob = TextBlob(blob)

    return blob.sentiment.polarity


def calculatePolarityScores(allTexts):
    allPolarityScores = []
    for text in allTexts:
        allPolarityScores.append(calculateSentiment(text))
    return allPolarityScores


#normalise values around the mean
def normaliseValues(polarities):
    mean = np.mean(polarities)
    for i in range(len(polarities)):
        polarities[i] = polarities[i] - mean
    return polarities


def normaliseAndScaleValues(polarities):
    #normalise values to between 0 and 1
    minValue = min(polarities)
    maxValue = max(polarities)
    for i in range(len(polarities)):
        polarities[i] = (polarities[i] - minValue) / (maxValue - minValue)

    return polarities


def calculateVariationScore(polarities):
    #return standard deviation of the polarity scores
    return np.std(polarities)


def calcSentimentVariation(relatedArticlesURLs, numberOfArticles=5):
    allTexts = extractTextFromUrls(relatedArticlesURLs)
    if (len(allTexts) > numberOfArticles):
        #if there are more articles than we want to look at, pick random ones
        allTexts = pickRandomItems(allTexts, numberOfArticles)
    polarities = calculatePolarityScores(allTexts)
    normPolarities = normaliseValues(polarities)
    return calculateVariationScore(normPolarities)
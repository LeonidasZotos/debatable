import os
import multiprocessing as mp
import numpy as np
from tqdm import tqdm
from textblob import TextBlob
from newspaper import Article

from config import settings
from utils import pickRandomItems

## Sentiment Variation. Not used by default, but could be useful in the future. 


def getTextFromURL(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print("Error while trying to access url: " + url)
        print("Full exception: ", e)
        return None

# Extracts text from the list of urls
def extractTextFromUrls(listOfUrls):
    if settings['multiProcessing'] == 'L2':
        with mp.Pool(os.cpu_count()) as pool:
            result = list(
                tqdm(pool.imap(getTextFromURL, listOfUrls),
                     total=len(listOfUrls),
                     disable=settings['disableLoadingBars']))
    else:
        result = list(
            map(getTextFromURL,
                tqdm(listOfUrls, disable=settings['disableLoadingBars'])))

    #remove None values from result (sites that could not be accessed)
    result = [i for i in result if i != None]
    return result


# Calculate sentiment polarity of text, based on adjectives and adverbs
def calculateSentiment(text):
    blob = TextBlob(text)
    if settings['scoreType'] == "subjectivity":
        return blob.sentiment.subjectivity
    elif settings['scoreType'] == "polarity":
        return blob.sentiment.polarity
    else:
        print("Score type not recognised.")
        return None


#calculate polarity scores for all texts
def calculateScores(allTexts):
    allPolarityScores = []
    for text in tqdm(allTexts, desc="Calculating scores", disable=settings['disableLoadingBars']):
        allPolarityScores.append(calculateSentiment(text))
    return allPolarityScores


#normalise values around the mean
def normaliseValues(polarities):
    mean = np.mean(polarities)
    for i in range(len(polarities)):
        polarities[i] = polarities[i] - mean
    return polarities


def calculateVariationScore(polarities):
    print("Calculating variation score.")
    #return standard deviation of the polarity scores
    return np.std(polarities)


def calcSentimentVariation(relatedArticlesURLs):
    allTexts = extractTextFromUrls(relatedArticlesURLs)
    if (len(allTexts) > settings['numberOfArticles']):
        #if there are more articles than we want to look at, pick random ones
        allTexts = pickRandomItems(allTexts, settings['numberOfArticles'])
    polarities = calculateScores(allTexts)
    normPolarities = normaliseValues(polarities)
    return calculateVariationScore(normPolarities)
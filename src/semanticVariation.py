from newspaper import Article
from textblob import TextBlob
from wordfreq import zipf_frequency
import string
import re
from utils import calcJaccardSimilarity, calcIntersection
from config import settings

def calcSemanticVariationBetweenTwo(rareWordsMainArticle, url2):    
    # Given the rare words of the main article and a URL to another article, calculate the similarity score between them.
    # If the overlap is large, the score will be high (i.e. high similarity).
    
    # First, extract the rare words from the second article
    rareWordsSecondArticle = extractRareWords(url2)
    # Then, calculate the Jacard similarity between the two sets of rare words
    similarityScore = 2 * calcJaccardSimilarity(rareWordsMainArticle, rareWordsSecondArticle) # Multiplied by 2 so that it's in the range 0-1.
    if settings['debug'] == True:
        print("There are " + str(len(rareWordsMainArticle)) + " rare words in the main article.")
        print("There are " + str(len(rareWordsSecondArticle)) + " rare words in the article with url: " + url2)
        print("The overlap is: " + str(len(calcIntersection(rareWordsMainArticle, rareWordsSecondArticle))) + " words.")
        print("The Jaccard Similarity is:" + str(similarityScore))
    return similarityScore


def extractRareWords(articleContent, zipfFrequency = 6):
    articleText = articleContent.text
    blob = TextBlob(articleText)
    articleNounPhrases = blob.noun_phrases
    articleNounPhrases = list(set(articleNounPhrases)) # remove duplicate noun phrases

    rareWords = []
    charactersToGetRidOf = string.punctuation + "’" + "‘" + "“" + "”" + "–" + "—" + "…"
    for word in articleNounPhrases:
        word = word.lemmatize()
        # clean word/remove punctuation
        for char in charactersToGetRidOf:
            word = word.replace(char, "")
        # remove "s " that sometimes remains
        word = word.replace("s ", "") 
        # remove starting and training whitespace
        word = word.strip()        
        # check if word is rare and more than two characters in length and has no numbers
        if (zipf_frequency(word, 'en') < zipfFrequency) and len(word) > 2 and not bool(re.search(r'[0-9]', word)): 
            rareWords.append(word)
    
    return rareWords

def calcSemanticVariation(mainArticleContent, relatedArticlesContent):
    # For each related article, calculate the similarity score to the main article.
    
    # Find the rare words in the main article here, so we only have to find them once
    rareWordsMainArticle = extractRareWords(mainArticleContent)
    
    relatedArticlesAndSimilarityScores = []
    for relatedArticle in relatedArticlesContent:
        similarityScore = calcSemanticVariationBetweenTwo(rareWordsMainArticle, relatedArticle)
        relatedArticlesAndSimilarityScores.append([relatedArticle.url, similarityScore])
    
    # sort the list by decreasing similarity score
    relatedArticlesAndSimilarityScores.sort(key=lambda x: x[1], reverse=False)
    
    return relatedArticlesAndSimilarityScores
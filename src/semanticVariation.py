from newspaper import Article
from textblob import TextBlob
from wordfreq import zipf_frequency
from utils import calcJaccardSimilarity, calcIntersection
from config import settings

def calcSemanticVariationBetweenTwo(rareWordsMainArticle, url2):    
    # Given the rare words of the main article and a URL to another article, calculate the similarity score between them.
    # If the overlap is large, the score will be high (i.e. high similarity).
    
    # First, extract the rare words from the second article
    rareWordsSecondArticle = extractRareWords(url2)
    #Then, calculate the Jacard similarity between the two sets of rare words
    similarityScore = calcJaccardSimilarity(rareWordsMainArticle, rareWordsSecondArticle)
    print("There are " + str(len(rareWordsMainArticle)) + " rare words in the main article.")
    print("There are " + str(len(rareWordsSecondArticle)) + " rare words in the article with url: " + url2)
    print("The overlap is: " + str(len(calcIntersection(rareWordsMainArticle, rareWordsSecondArticle))) + " words.")
    print("The Jaccard Similarity is:" + str(similarityScore))
    return similarityScore


def extractRareWords(articleURL, zipfFrequency = 6): # zipfRareness needs tuning
    # Given a URL, extracts the words that are rare in the English language, using the zipf distribution.
    try:
        articleText = Article(articleURL)
        articleText.download()
        articleText.parse()
    except Exception as e:
        if settings['debug'] == True:
            print("Exception while downloading article: " + str(e))
        return []
    
    articleText = articleText.text
    blob = TextBlob(articleText)
    articleNounPhrases = blob.noun_phrases
    print("There are " + str(len(articleNounPhrases)) + " noun phrases in the article.")
    articleNounPhrases = list(set(articleNounPhrases))
    print("After removing duplicates, there are " + str(len(articleNounPhrases)) + " noun phrases in the article.")

    rareWords = []
    for word in articleNounPhrases:
        if zipf_frequency(word, 'en') < zipfFrequency:
            rareWords.append(word)

    print("The shape of rareWords is: " + rareWords.shape())
    print("---------START OF RARE WORDS---------")
    print("The rare words are: " + str(rareWords))
    print("---------END OF RARE WORDS---------")
    return rareWords

def calcSemanticVariation(mainArticle, relatedArticles):
    # For each related article, calculate the similarity score to the main article.
    
    # Find the rare words in the main article here, so we only have to download it once
    rareWordsMainArticle = extractRareWords(mainArticle)
    
    relatedArticlesAndSimilarityScores = []
    for relatedArticle in relatedArticles:
        similarityScore = calcSemanticVariationBetweenTwo(rareWordsMainArticle, relatedArticle)
        relatedArticlesAndSimilarityScores.append([relatedArticle, similarityScore])

    # sort the list by similarity score
    relatedArticlesAndSimilarityScores.sort(key=lambda x: x[1], reverse=True)
    
    return relatedArticlesAndSimilarityScores
import sys
from extractKeyTerms import extractKeyTerms
from findArticles import findArticles
from sentimentVariation import calcSentimentVariation
from config import settings
from argumentParser import getArguments

if __name__ == "__main__":
    if settings['debug'] == True:
        print("Debug mode is on.")
        
    args = getArguments() # Get command line arguments

    url = args.link
    keyTerms = extractKeyTerms(url)
    query = ' '.join(keyTerms)
    print("Key terms have been extracted from the article.")
    relatedArticles = findArticles(query)
    print("Related articles have been found.")
    variationScore = calcSentimentVariation(relatedArticles)
    print("The variation score is: " + str(variationScore))

    sys.exit(0)

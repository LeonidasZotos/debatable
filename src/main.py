import sys
from extractKeyTerms import extractKeyTerms
from findArticles import findArticles
from sentimentVariation import calcSentimentVariation
from config import settings

if __name__ == "__main__":
    if settings['debug'] == True:
        print("Debug mode is on.")
    # check if the user has provided a link to analyze
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    keyTerms = extractKeyTerms(url)
    query = ' '.join(keyTerms)
    print("Key terms have been extracted from the article.")
    relatedArticles = findArticles(query)
    print("Related articles have been found.")
    variationScore = calcSentimentVariation(relatedArticles)
    print("The variation score is: " + str(variationScore))


    sys.exit(0)

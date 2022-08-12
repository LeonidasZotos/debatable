import sys
from extractKeyTerms import extractKeyTerms
from findArticles import findArticles
from sentimentVariation import calcSentimentVariation # CHANGE THIS!!!

if __name__ == "__main__":
    # check if the user has provided a link to analyze
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    keyTerms = extractKeyTerms(url)
    query = ' '.join(keyTerms)
    print("The key terms are:" + str(keyTerms))
    relatedArticles = findArticles(query)
    print("The articles found are:")
    for article in relatedArticles:
        print(article)
        print("")
    
    variationScore = calcSentimentVariation(relatedArticles)
    print("The variation score is: " + str(variationScore))


    sys.exit(0)

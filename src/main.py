import sys
import os
from tqdm import tqdm
import multiprocessing as mp
from extractKeyTerms import extractKeyTerms
from findArticles import findArticles
from semanticVariation import calcSemanticVariation
from config import settings
from argumentParser import getArguments


def inputSetup(args):
    listOfLinksToCheck = []
    url = args.link
    path = args.path
    if path != None:
        # Extract urls from file
        with open(path, 'r') as f:
            listOfLinksToCheck = f.readlines()
    if url != None:
        listOfLinksToCheck.append(url)
    if len(listOfLinksToCheck) == 0:
        print("No links have been provided. Exiting.")
    return listOfLinksToCheck


def checkURL(url):
    keyTerms = extractKeyTerms(url)
    if keyTerms == None:
        return None
    query = ' '.join(keyTerms)
    relatedArticles = findArticles(query)
    # Here, relatedArticles is a list of urls of related articles.
    relatedArticlesAndSimilarityScores = calcSemanticVariation(url, relatedArticles)
   
    return [url, relatedArticlesAndSimilarityScores]


def runner(listOfUrls):
    allResults = []  # List of results
    if settings['multiProcessing'] == 'L1':
        with mp.Pool(os.cpu_count()) as pool:
            allResults = list(
                tqdm(pool.imap(checkURL, listOfUrls),
                     total=len(listOfUrls),
                     disable=settings['disableLoadingBars']))
    else:
        allResults = list(
            map(checkURL,
                tqdm(listOfUrls, disable=settings['disableLoadingBars'])))

    # Remove none results from list (e.g. because one of the sources is down)
    filteredResults = list(filter(None, allResults))
    
    return filteredResults

def printResults(results):
    print("Results:")
    for queryNum, query in enumerate(results): # here, "query" refers to each article that was analysed, in case multiple were provided
        print("Given URL:", results[queryNum][0])
        print("The recomendations for articles to read are (in order of dissimilarity):")

        for index, result in enumerate(query[1]):
            # Print recommendations and their similarity score. 
            print(str(index + 1) + ") "+ str(result[0]) + " (content similarity = " + str(round(result[1], 2)) + ")")
            
        print("---------------------------------------------------")
        
    return None
        

if __name__ == "__main__":
    input = inputSetup(getArguments())
    if input == None:
        sys.exit(0)
    
    results = runner(input)

    printResults(results)
    
    # Export results if desired.
    if settings['exportOutput']:
        filename = settings['outputFile'] + '.txt'
        standardOuput = sys.stdout
        with open(filename, 'w') as f:
            sys.stdout = f
            printResults(results)
            sys.stdout = standardOuput
        print("Results have been written to " + filename)

    sys.exit(0)
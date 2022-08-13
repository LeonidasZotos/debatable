import sys
import os
from tqdm import tqdm
import multiprocessing as mp
from extractKeyTerms import extractKeyTerms
from findArticles import findArticles
from sentimentVariation import calcSentimentVariation
from config import settings
from argumentParser import getArguments


def inputSetup(args):
    listOfLinksToCheck = []
    url = args.link
    path = args.path
    if path != None:
        #extract data from file
        with open(path, 'r') as f:
            listOfLinksToCheck = f.readlines()
    if url != None:
        listOfLinksToCheck.append(url)
    if len(listOfLinksToCheck) == 0:
        print("No links have been provided. Exiting.")
    return listOfLinksToCheck


def checkURL(url):
    keyTerms = extractKeyTerms(url)
    query = ' '.join(keyTerms)
    if settings['debug'] == True:
        print("Key terms have been extracted from the article.")
    relatedArticles = findArticles(query)
    if settings['debug'] == True:
        print("Related articles have been found.")
    variationScore = calcSentimentVariation(relatedArticles)
    if settings['debug'] == True:
        print("The variation score is: " + str(variationScore))
    return [url, str(variationScore)]


def runner(listOfUrls):
    allResults = []  # List of results
    if settings['multiProcessing'] == 'L1':
        with mp.Pool(os.cpu_count()) as pool:
            allResults = list(tqdm(pool.imap(checkURL, listOfUrls), total=len(listOfUrls), disable=settings['loadingBars']))

    else:
        allResults = list(map(checkURL, tqdm(listOfUrls, disable=settings['loadingBars'])))

    return allResults


if __name__ == "__main__":
    input = inputSetup(getArguments())
    if input != None:
        results = runner(input)
        #write results to file
        with open(settings['outputFile'], 'w') as f:
            for result in results:
                f.write(result[0] + '           ' + result[1] + '\n')
        print("Results have been written to " + settings['outputFile'])
        
    # keyTerms = extractKeyTerms(url)
    # query = ' '.join(keyTerms)
    # print("Key terms have been extracted from the article.")
    # relatedArticles = findArticles(query)
    # print("Related articles have been found.")
    # variationScore = calcSentimentVariation(relatedArticles)
    # print("The variation score is: " + str(variationScore))

    sys.exit(0)
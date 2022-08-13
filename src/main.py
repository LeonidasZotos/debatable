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
    if keyTerms == None:
        return None
    query = ' '.join(keyTerms)
    if settings['debug'] == True:
        print("Key terms have been extracted from the article.")
    relatedArticles = findArticles(query)
    if settings['debug'] == True:
        print("Related articles have been found.")
    variationScore = calcSentimentVariation(relatedArticles)
    if settings['debug'] == True:
        print("The variation score is: " + str(variationScore))
    
    #Write to the ongoing file in case there is a crash later on
    with open(settings['ongoingOutputFile'], 'a') as f:
        f.write(str([str(keyTerms), str(variationScore)]) + '\n')
    return [str(keyTerms), str(variationScore)]


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


if __name__ == "__main__":
    input = inputSetup(getArguments())
    if input == None:
        sys.exit(0)
    
    results = runner(input)
    #write results to file
    print(results)
    with open(settings['finalOutputFile'], 'w') as f:
        for result in results:
            f.write(result[0] + '           ' + result[1] + '\n')
    print("Results have been written to " + settings['finalOutputFile'])

    sys.exit(0)
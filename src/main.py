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
        #extract urls from file
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
    recommendations = []
    relatedArticlesAndSimilarityScores = calcSemanticVariation(url, relatedArticles)
    recommendations = relatedArticlesAndSimilarityScores
   
    return [str(url), str(recommendations)]


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
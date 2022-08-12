from utils import *

def extractTextFromUrls(listOfUrls):
    allTexts = []

    for url in listOfUrls:
        allTexts.append(getTextFromURL(url))
    return allTexts




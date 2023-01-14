from urllib.request import Request, urlopen
from collections import Counter
from textblob import TextBlob
from bs4 import BeautifulSoup as soup
from newspaper import Article
from nltk.corpus import stopwords
from config import settings


def gethtmlSource(url):
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    req = Request(url,
                  headers={'User-Agent':
                           custom_user_agent})  # mask to avoid HTTP 403 error
    try:
        webpage = urlopen(req,
                          timeout=settings['webpageLoadingTimeout']).read()
    except Exception as e:
        if settings['debug'] == True:
            print("Could not access source of URL: " + url)
            print("Full exception: ", e)
        return None

    return soup(webpage, 'html.parser')


def extractContent(url):
    # Extracts the content of the article from the URL
    try:
        articleContent = Article(url)
        articleContent.download()
        articleContent.parse()
    except Exception as e:
        if settings['debug'] == True:
            print(
                "Could not access related article for url:" + url +
                ", returning None.", e)
        return None
    return articleContent


def extractKeyTerms(url):
    # Also returns the article's content, so that we don't need to download it again if we use it elsewhere
    try:
        article = extractContent(url)
        if settings['keyTermsMethod'] == 'common':
            allText = article.text
            nouns = extractNouns(allText)
            keyTerms = getMostCommonWords(nouns)
        elif settings['keyTermsMethod'] == 'title':
            title = article.title
            keyTerms = extractNouns(title)
    except Exception as e:
        print("Key terms could not be retrieved, returning None.", e)
        return None
    return keyTerms, article


def extractNouns(text):
    # get all nouns in text
    blob = TextBlob(text)
    nouns = blob.noun_phrases
    return nouns


def getMostCommonWords(text, numberOfWords=5):
    # remove stopwords from text
    enStopwords = stopwords.words('english')
    text = [word for word in text if word not in enStopwords]
    #get most frequent words in string
    counter = Counter(text)
    mostCommonWords = counter.most_common(numberOfWords)
    justWords = [i[0] for i in mostCommonWords]
    print("Most common words: ", justWords)
    return justWords
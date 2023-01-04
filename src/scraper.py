from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from newspaper import Article
from config import settings

def gethtmlSource(url):
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    req = Request(url,
                  headers={'User-Agent':
                           custom_user_agent})  # mask to avoid HTTP 403 error
    try:
        webpage = urlopen(req, timeout=settings['webpageLoadingTimeout']).read()
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
        print("Could not access related article for url:" + url + ", returning None.", e)
        return None
    return articleContent
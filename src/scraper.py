from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
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
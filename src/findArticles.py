import urllib
from scraper import gethtmlSource
from utils import *
# from scraper import getSource
from config import settings


def scrapeGoogle(query):
    query = urllib.parse.quote_plus(query)
    url = "https://www.google.com/search?q=" + query + "&num=" + str(settings['numOfSourcesToLoad'])
    response = gethtmlSource(url)
    links = []
    for link in response.findAll('a'):
        links.append(link.get('href'))

    googleDomains = ('https://www.google.', 'https://google.',
                     'https://webcache.googleusercontent.',
                     'http://webcache.googleusercontent.',
                     'https://policies.google.', 'https://support.google.',
                     'https://maps.google.', 'https://accounts.google.',
                     'youtube.com')

    #If any googleDomain is in the link, remove it
    for link in links[:]:
        if any(domain in link for domain in googleDomains):
            links.remove(link)

    return links


def scrapeGoogleNews(query):
    query = urllib.parse.quote_plus(query)
    url = "https://www.google.com/search?q=" + query + "&tbm=nws&lr=lang_en&hl=en&sort=date&num=" + str(settings['numOfSourcesToLoad'])
    response = gethtmlSource(url)
    links = []
    for link in response.findAll('a'):
        links.append(link.get('href'))

    googleDomains = ('https://www.google.', 'https://google.',
                     'https://webcache.googleusercontent.',
                     'http://webcache.googleusercontent.',
                     'https://policies.google.', 'https://support.google.',
                     'https://maps.google.', 'https://accounts.google.',
                     'youtube.com')

    #If any googleDomain is in the link, remove it
    for link in links[:]:
        if any(domain in link for domain in googleDomains):
            links.remove(link)

    return links


#filters out strings that are not links, and converts them to proper links starting with http or https
def keepOnlyHttpLinks(links):
    http_domains = ('http://', 'https://')
    for link in links[:]:
        if not any(domain in link for domain in http_domains):
            links.remove(link)
    return links


#function that removes things before the 'http' and after the &dev
def keepMainLink(links):
    for i in range(len(links)):
        links[i] = 'http' + links[i].split('http', 1)[1]
        links[i] = links[i].split('&ved')[0]
    return links


def getLinks(query):
    googleLinks = scrapeGoogle(query)
    googleNewslinks = scrapeGoogleNews(query)

    links = googleLinks + googleNewslinks

    links = keepOnlyHttpLinks(links)
    links = keepMainLink(links)
    links = list(set(links))  #remove duplicates
    return links


def findArticles(query):
    links = getLinks(query)
    return links
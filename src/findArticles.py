from curses import meta
import sys
import os
import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from utils import *


def scrapeGoogle(query):
    query = urllib.parse.quote_plus(query)
    url = "https://www.google.com/search?q=" + query
    response = getSource(url)
    links = []
    for link in response.findAll('a'):
        links.append(link.get('href'))

    googleDomains = ('https://www.google.', 'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://policies.google.', 'https://support.google.',
                      'https://maps.google.', 'https://accounts.google.')

    for link in links[:]:
        if link.startswith(googleDomains):
            links.remove(link)

    return links


def scrapeBing(query):
    links = []
    return links


def scrapeDuck(query):
    links = []
    return links

#filters out strings that are not links, and converts them to proper links starting with http or https
def keepOnlyHttpLinks(links):
    http_domains = ('http://', 'https://')
    for link in links[:]:
        if not any(domain in link for domain in http_domains):
            links.remove(link)
    return links


#function that removes text from string until 'http' is encountered
def removeUntilHttp(links):
    for i in range(len(links)):
        links[i] = 'http' + links[i].split('http', 1)[1]


def getLinks(query):
    # update once more engines can be scraped
    googleLinks = scrapeGoogle(query)
    # duckLinks = scrapeDuck(query)
    # bingLinks = scrapeBing(query)

    links = googleLinks
    

    links = keepOnlyHttpLinks(links)
    removeUntilHttp(links)
    return links


def findArticles(query):
    links = getLinks(query)
    return links

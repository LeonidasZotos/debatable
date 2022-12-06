import os
import multiprocessing as mp
import numpy as np
from tqdm import tqdm
from textblob import TextBlob
from newspaper import Article

from config import settings
from utils import pickRandomItems

def calcSemanticVariationBetweenTwo(url1, url2):
    similarityScore = 0
    similarityScore = np.random.randint(0, 10)
    
    return similarityScore


def calcSemanticVariation(mainArticle, relatedArticles):
    
    # for each related article, calculate the similarity score
    relatedArticlesAndSimilarityScores = []
    for relatedArticle in relatedArticles:
        similarityScore = calcSemanticVariationBetweenTwo(mainArticle, relatedArticle)
        relatedArticlesAndSimilarityScores.append([relatedArticle, similarityScore])

    # sort the list by similarity score
    relatedArticlesAndSimilarityScores.sort(key=lambda x: x[1], reverse=True)
    
    return relatedArticlesAndSimilarityScores
    
    

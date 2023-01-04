from sentence_transformers import SentenceTransformer, util
from config import settings


def filterArticles(mainArticleContent, relatedArticlesContent, model):
    
    
    print("Currently just return the articles without any filtering. Needs to be implemented")
    return relatedArticlesContent
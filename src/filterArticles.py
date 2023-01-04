from sentence_transformers import util
from config import settings


def constructEmbeddings(mainArticleTitle, relatedArticlesContent, model):
    # Constructs embeddings of the main article and the related articles (latter in a dictionary with the url as key)

    # First, calculate embedding of main article
    mainArticleEmbedding = model.encode(mainArticleTitle)

    # Then, calculate embedding of related articles, and store in dictionary
    relatedArticlesEmbeddingsDict = {}
    for relatedArticleContent in relatedArticlesContent:
        relatedArticlesEmbeddingsDict[relatedArticleContent] = model.encode(
            relatedArticleContent.title)
    return mainArticleEmbedding, relatedArticlesEmbeddingsDict


def filterArticles(mainArticleContent, relatedArticlesContent, model):
    # Filters the related articles based on similarity with main article's title (very dissimilar articles are filtered out)
    mainArticleTitle = mainArticleContent.title

    #Calculate embeddings
    mainTitleEmbedding, relatedArticlesEmbeddings = constructEmbeddings(
        mainArticleTitle, relatedArticlesContent, model)

    relatedArticlesSimilarity = relatedArticlesEmbeddings
    for content, embedding in relatedArticlesEmbeddings.items():
        similarity = util.cos_sim(mainTitleEmbedding, embedding).item()
        if similarity < settings['titleSimilarityThreshold']:
            relatedArticlesContent.remove(content)
        else:
            relatedArticlesSimilarity[content] = similarity

    return relatedArticlesContent
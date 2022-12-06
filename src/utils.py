import random

# Function that picks x random items from list
def pickRandomItems(list, x):
    return random.sample(list, x)

# Function that returns the intersection of two lists
def calcIntersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# Function that returns the jaccard similarity of two sets
def calcJaccardSimilarity(lst1, lst2):
    nominator = calcIntersection(lst1, lst2)
    denominator = lst1 + lst2 # union of the two lists
    jaccardSimilarity = len(nominator)/len(denominator)
    
    return round(jaccardSimilarity, 3)
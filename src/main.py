import sys
import os
from extractKeyTerms import *
from tkinter import *
import tkinter.scrolledtext as tkst

if __name__ == "__main__":
    # check if the user has provided a link to analyze
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    keyTerms = extractKeyTerms(url)

    print(keyTerms)
    
    sys.exit(0)

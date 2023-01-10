# Debatable
Given a news story, it is inevitable that different news outlets cover the story from different viewpoints, potentially omitting parts of it (either intentionally or unintentionally). However, it is important for a reader to be well-informed and aware of all parts of the story. Unfortunately, this takes time and effort as the reader has to manually find and read different sources that cover the same topic. Admittedly, this is cumbersome and is something not many people do.

The objective of this project is to develop a tool that, given a (link to a) news article, it can recommend other news articles on the same topic. An important aspect of this tool is that these recommendations are not based on the popularity or credibility of the news source, but rather on the content of the article. That is, articles on the same topic that contain different content are more strongly recommended compared to articles that contain similar content. Consequently, the reader can obtain a more complete picture by reading articles on the same topic but with different content.

# How to run

## Environment
- To run the program using Conda, the condaEnvironment.yml file can be used to create a Conda environment with the necessary packages. 
- In case some NLTK corpora are not already present, they can be downloaded by using `nltk.download()` within a Python environment

## Fine-Tuned model
- A fine-tuned model must be present in `src/models`. An example model can be found [here](https://drive.google.com/drive/folders/1cx52wIAuNu-VwIhKk5A40WsOgUOOGQuL?usp=sharing).
- To fine-tune a different model/on a different dataset, the `trainModel.py` script can be used (name of the pre-trained model is placed in line 13). The script also evaluates the model on the given dataset. The entire folder of the newly trained model should be placed in `src/models`

## Running the Recommendation System, using the GUI
- From within the `src` folder, run `python UI.py`

## Running the Recommendation System, using the command line
- From within the `src` folder, run `python main.py --link [URL_TO_ARTICLE]` or `python main.py --path [PATH_TO_INPUTS]`.
- In the latter case, the path to a text file should be given, in which URLs are separated by new lines. The system will analyse all links in the file. 

## Customisation
- The behaviour of the system can be changed through the `settings.yaml` file. 

# Sentiment Analysis

➢ Goal: Develop a model to predict the star rating of a
review based on the text within the review.


➢ Results: A model with 90% accuracy on a dataset of 1000 one and five star reviews

➢ To test our final model, run *model_test_script.py*.

➢ Files:

  - *data/* contains training data
  - *extension/* contains files to an uncompleted chrome extension
  - *models/SM_LSTM_90* contains an LSTM model which can be loaded by a StringModel. It was trained on data/26064_yelp_reviews.json. It has 90% accracy on a testing set of 1000 reviews set apart from the training data. 
  - *creating_model.py* is the script used to build SM_LSTM_90 .
  - *ebay_selective_scrape.py* is a script to scrape Ebay listings for reviews.
  - *embeddding.py* contains functions for embedding strings.
  - *glove.6b.50d_shortened.txt* has all of the word/punctuation embeddings. Downloaded from https://nlp.stanford.edu/projects/glove/. It is an abbrieviated version because GitHub has a file size limmit.
  - *model_test_script.py* is a script to test *SM_LSTM_90*.
  - *models.py* has the Keras model wrapper class StringModel. It auto embeds strings to numerical arrays.
  - *yelp.py* has functions for scraping Yelp reviews.
  
  
  
  

---------Technologies---------

➢ Python and some libraries/modules:

  - “Requests” for data collection.
  - “Tensorflow” for machine learning.


# Multi-Label IMDb Movie Genre Classifier

The goal of this project was to build a classifier that would classify movies by genre using the synopses’ of the movies from IMDb. This project was completed as a part of the University of Victoria's Data Mining class (SENG 474). 

Team Members: 

- Christopher Norton
- Louie Kedziora
- Kian Gorgichuk

## Project Overview

- The web scaper uses multi-threading to reduce overall processing time.
- Overall, 4964 movie synopses were scraped from IMDb.
- The pre-processing of data included removing stop words, punctuation, capitalization, and movies which lacked synopses. 
- The movie synopses data set was split into training and test data with 4,274 and 667 movie synopses respectively.
- The multi-label classifier was then built using the one vs. all approach where for each genre a multinomial Naive Bayes classifier was trained. This allows for the multi-label classifier to return multiple genres for a single movie synopses, which is unlike how a normal Naive Bayes classifier work.
- The multi-label classifier was tested with the test data set and achieved an accuracy of 88.51% with a hamming loss ratio of 0.1149.

## Code Overview: 

This repo is split into four separate modules:

1. Aquisition: 
    - Crawl IMDb website and save data to the data/raw folder.

2. Data: 
    - Contains the data scraped from the IMDb website and the 
       preproccessed data.
    - Statistics on both the raw and pre-processed data.

3. Processing:
    - Pre-process and separate the data acquired from IMDb into a test 
       and training data set. Store this data in the data module. 

4. Mining:
    - Train and test our multi-label classifier.

Each module has its' own README.md detailing on to run the code in that module. 

## Requirements:

To run this project the following packages must be install:

- Python 3 (all modules)
- beautifulsoup4 (acquisition module)
- numpy (data module)
- matplotlib (data module)
- nltk (processing  module)
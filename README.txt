SENG 474 Project: Multi-Label IMDB Movie Genre Classifier    

Members: 

- Christopher Norton (V00852920)
- Louie Kedziora (V00820695)
- Kian Gorgichuk (V00855771)

Overview: 

This repo is split into four seperate modules:

1. Aquisition: 
    - Crawl IMDB website and save data to the data/raw folder

2. Data: 
    - Containts the data scraped from the IMDB website and the 
       preproccessed data.
    - Statistics on both the raw and preprocessed data

3. Processing:
    - Preprocess and seperate the data acquired from IMDB into a test 
       and training data set. Store this data in the data module. 

4. Mining:
    - Train and test the our multi-label classifier.

Each module has its' own README.txt detailing on to run the code in that module. 

Requirements:

To run this project the following packages must be install:

- Python 3 (all modules)
- beautifulsoup4 (acquisition module)
- numpy (data module)
- matplotlib (data module)
- nltk (processsing module)
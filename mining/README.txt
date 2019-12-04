Mining Module

This module is separated into four files:

    - movie_synopsis.py: A class that represents a movie synopses.

    - train.py: The python scripts used to train the multi-label classifier 
                using the training data set. Saves the model to a model.json file.

    - test.py: The python script used to test the multi-label classifier. The script loads
                the model stored in the model.json file. 

    - model.json: The saved model created from the test data set. 

To train the multi-label classifier on the training data set (data/train_movies.txt)
navigate to the mining folder and run "python3 train.py". 

To test the multi-label classifier using the model.json file with the
test data set (data/test_movies.txt) navigate to the mining folder and run 
"python3 test.py".
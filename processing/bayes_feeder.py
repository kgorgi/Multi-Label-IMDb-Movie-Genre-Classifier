import bayes_text as bt
import pandas as pd
from math import log2
import datetime

# All of this is just copied from Thomos bayes_text implementation,
#   so I have no idea how it works what I have done here is just
#   turned his old main() into a function that takes a training set
#   and testing set.
def feed_data(train_data_filename, train_labels_filename, test_data_filename, test_labels_filename):
    print("Feed #1")
    print(datetime.datetime.now())

    fd = bt.readDataLines(train_data_filename)
    fl = bt.readLabelLines(train_labels_filename)
    doc_set = list(zip(fd, fl))
    classes_set = [0, 1]
    print("Feed #2")
    print(datetime.datetime.now())

    vocab, prior, condprob = bt.trainMultinomialNB(classes_set ,doc_set)
    print("Feed #3")
    print(datetime.datetime.now())

    doc = bt.readDataLines(train_data_filename)
    comparer = []
    for line in doc:
        comparer.append(bt.applyMultinomialNB(classes_set, vocab, prior, condprob, line))
    print("Feed #4")
    print(datetime.datetime.now())
    
    fl = bt.readLabelLines(train_labels_filename)
    indexer = 0
    correct_count = 0
    print("Feed #5")
    print(datetime.datetime.now())

    for element in comparer:
        if element == fl[indexer]:
            correct_count += 1
        indexer += 1
    fraction_train = "Amount Correctly Predicted = " + str(correct_count) + " / " + str(len(comparer)) + "\n"
    percent_train = "Percentage Correctly Predicted = " + str(correct_count/len(comparer)) + "\n\n"
    print("Feed #6")
    print(datetime.datetime.now())

    fd2 = bt.readDataLines(test_data_filename)
    fl2 = bt.readLabelLines(test_labels_filename)
    comparer2 = []
    print("Feed #7")
    print(datetime.datetime.now())

    for line in fd2:
        comparer2.append(bt.applyMultinomialNB(classes_set, vocab, prior, condprob, line))
    print("Feed #8")
    print(datetime.datetime.now())
    indexer = 0
    correct_count = 0
    for element in comparer2:
        if element == fl2[indexer]:
            correct_count += 1
        indexer += 1
    print("Feed #9")
    fraction_train2 = "Amount Correctly Predicted = " + str(correct_count) + " / " + str(len(comparer2)) + "\n"
    percent_train2 = "Percentage Correctly Predicted = " + str(correct_count/len(comparer2)) + "\n\n"
    print("Results " + train_data_filename + ":\n" + fraction_train + percent_train + "Results  " + test_data_filename + ":\n" + fraction_train2 + percent_train2)
    print(datetime.datetime.now())

def main():
    # Sanity check to see if the copy pasta worked
    # feed_data("traindata.txt", "trainlabels.txt", "testdata.txt", "testlabels.txt")

    # Testing seems to be 100 percent for train data, but we assume that is 
    print("TESTING: action-100.txt")
    print("So this includes the first 100 synopsis and whether or not they are action movies")
    print()
    feed_data("../data/train_synopsis.txt", "../genres/action_1-100.txt", "../data/test_synopsis_101-200.txt", "../genres/action_101-200.txt")

if __name__ == "__main__":
    main()

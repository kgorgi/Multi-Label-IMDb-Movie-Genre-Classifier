import math
import datetime
import pickle


def ClassifyTrainingData(data_lines, labels):
    data_in_classifications = dict()
    for index, val in enumerate(data_lines):
        classification = int(labels[index])
        if not classification in data_in_classifications:
            data_in_classifications[classification] = list()
        data_in_classifications[int(labels[index])].append(val)
    return data_in_classifications

def GetWords(data_lines, unique = False):
    words = list()
    for line in data_lines:
        for word in line.split(" "):
            if unique:
                if not word in words:
                    words.append(word)
            else:
                words.append(word)
    return words

def ReadData(data, labels):
    with open(data) as data, open(labels) as labels:
        return data.read().splitlines(), labels.read().splitlines()

# Count unique occurunces within classification
def CountUniqueWords(categorized_data, classification):
    unique_terms_within_classification = dict()
    for line in categorized_data[classification]:
        for term in line.split(" "):
            if term in unique_terms_within_classification:
                unique_terms_within_classification[term] += 1
            else:
                unique_terms_within_classification[term] = 1
    return unique_terms_within_classification

def CalculateScore(test_data_split, prior, result):
    score = list()
    # Initialize score with log(prior)
    for classification in range(0, 2):
        #Set initial score to ratio between documents in classification and all documents
        score.append(math.log(prior[classification]))
        #Go through each term in data we want to classify
        for term in test_data_split:
            # Term may not have been classified yet!
            if term in result[2] and classification in result[2][term]:
                score[classification] += math.log(result[2][term][classification])
    return score

def CalculateMaxScore(score):
    current_max = score[0]
    index_of_max = 0
    for current_index, current_score in enumerate(score):
        if current_score > current_max:
            current_max = current_score
            index_of_max = current_index
    return index_of_max

def TrainModel(data_lines, labels):
    condprob = dict()
    prior = list()

    data_seperated_into_classifications = ClassifyTrainingData(data_lines, labels)
    unique_words = GetWords(data_lines, unique = True)
    classification_count = len(data_seperated_into_classifications.keys())

    for classification in range(0, classification_count):
        # Append the ratio between documents in classification and all documents
        prior.append(len(data_seperated_into_classifications[classification])/len(data_lines))
        unique_terms_within_classification = CountUniqueWords(data_seperated_into_classifications, classification)
        unique_classification_count = len(GetWords(data_seperated_into_classifications[classification]))

        for term in unique_words:
            # If not within classification assign an initial probability of 0
            if term in unique_terms_within_classification:
                probability_of_term = unique_terms_within_classification[term]
            else:
                probability_of_term = 0    
            probability = (probability_of_term + 1) / (len(unique_words) + unique_classification_count)
            # If no probability already recorded, add dict to list
            if not term in condprob:
                condprob[term] = dict()
            condprob[term][classification] = probability
    return unique_words, prior, condprob

def ApplyModel(result, test_sample, classification):
    prior = result[1]
    test_data_split = test_sample.split(" ")
    score = CalculateScore(test_data_split, prior, result)
    return CalculateMaxScore(score)

def CalculateAccuracy(test_results, test_labels):
    correct_result = 0

    for index, result in enumerate(test_results):
        # print(result, test_labels[index])
        if int(result) == int(test_labels[index]):
            correct_result += 1
    return correct_result / len(test_results)

def main():
    start_time = datetime.datetime.now()
    train_data = '../data/train_synopsis.txt'
    train_labels = '../genres/action.txt'
    test_data = '../data/test_synopsis_101-200.txt'
    test_labels = '../genres/action_101-200.txt'

    training_data, training_labels = ReadData(train_data, train_labels)

    training_results = TrainModel(training_data, training_labels)

    # Use this to write the training model to the memory
    with open('../data/training_memory.txt', "wb") as outfile:
        pickle.dump(training_results, outfile)

    # Use this to read the training model from memory
    with open('../data/training_memory.txt', "rb") as infile:
        training_results = pickle.load(infile)

    
    
    testing_data, testing_labels = ReadData(train_data, train_labels)
    testing_data, testing_labels = ReadData(test_data, test_labels)
    test_results = list()

    for ind, test_sample in enumerate(testing_data):
        test_results.append(ApplyModel(training_results, test_sample, testing_labels[ind]))
    
    test_accuracy = CalculateAccuracy(test_results, testing_labels)
    
    with open('result.txt', 'w') as results:
        results.write('File was trained with the data file: %s and labels: %s. It was tested with the data in: %s and labels in %s\n\n' % (train_data, train_labels, test_data, test_labels))
        results.write('Accuracy: %s%%' % (test_accuracy*100))
        results.write('\nComputation time was:\n')
        dt = datetime.datetime.now() - start_time
        dt = divmod(dt.days * 86400 + dt.seconds, 60)
        results.write("Runtime took " + str(dt[0]) + " minutes, and " + str(dt[1]) + " seconds.")
        
if __name__ =="__main__":
    main()
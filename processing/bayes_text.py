import pandas as pd
from math import log2

# def main():
#     fd = readDataLines("traindata.txt")
#     fl = readLabelLines("trainlabels.txt")
#     doc_set = list(zip(fd, fl))
#     classes_set = [0, 1]

#     vocab, prior, condprob = trainMultinomialNB(classes_set ,doc_set)

#     doc = readDataLines("traindata.txt")
#     comparer = []
#     for line in doc:
#         comparer.append(applyMultinomialNB(classes_set, vocab, prior, condprob, line))
    
#     fl = readLabelLines("trainlabels.txt")
#     indexer = 0
#     correct_count = 0
#     for element in comparer:
#         if element == fl[indexer]:
#             correct_count += 1
#         indexer += 1
#     fraction_train = "Amount Correctly Predicted = " + str(correct_count) + " / " + str(len(comparer)) + "\n"
#     percent_train = "Percentage Correctly Predicted = " + str(correct_count/len(comparer)) + "\n\n"

#     fd2 = readDataLines("testdata.txt")
#     fl2 = readLabelLines("testlabels.txt")
#     comparer2 = []
#     for line in fd2:
#         comparer2.append(applyMultinomialNB(classes_set, vocab, prior, condprob, line))

#     indexer = 0
#     correct_count = 0
#     for element in comparer2:
#         if element == fl2[indexer]:
#             correct_count += 1
#         indexer += 1
#     fraction_train2 = "Amount Correctly Predicted = " + str(correct_count) + " / " + str(len(comparer2)) + "\n"
#     percent_train2 = "Percentage Correctly Predicted = " + str(correct_count/len(comparer2)) + "\n\n"
#     print("Results traindata.txt:\n" + fraction_train + percent_train + "Results testdata.txt:\n" + fraction_train2 + percent_train2)



def trainMultinomialNB(classes_set, doc_set):
    vocab = extractVocabulary(doc_set)
    num_docs = countDocs(doc_set)
    prior = [0, 0]
    cols = len(vocab)
    rows = 2
    # condprob = [[0 for i in range(cols)] for j in range(rows)]
    condprob = [dict() for x in range(rows)]
    for class_c in classes_set:
        prior[class_c] = countClassDocs(class_c, doc_set) / num_docs
        class_docs_concat = concatTextAllClassDocs(doc_set, class_c)
        num_unique_words = countClassUnique(class_docs_concat)
        indexer = 0
        for word in vocab:
            T_ct = countNumOccurences(class_docs_concat, word)
            condprob[class_c][word] = (T_ct + 1) / ( len(class_docs_concat.split(" ")) + num_unique_words - T_ct - 1)
            indexer += 1
    return vocab, prior, condprob

def applyMultinomialNB(Classes_Set, vocab, prior, condprob, line):
    w = extractDocTokens(vocab, line)
    score = [0, 0]
    for class_c in Classes_Set:
        score[class_c] = log2(prior[class_c])
        for word in w:
            score[class_c] += log2(condprob[class_c][word])

    return  score.index(max(score))

def extractDocTokens(vocab, line):
    same_vocab = []
    for word in line.split(" "):    
        if word in vocab:
           same_vocab.append(word)
    return same_vocab


def countClassUnique(class_docs_concat):
    word_list = []
    for word in class_docs_concat.split(" "):
        if word not in word_list:
            word_list.append(word)
    return len(word_list)

def countClassDocs(class_c, doc_set):
    count = 0
    for line, cur_class in doc_set:
        if class_c == cur_class:
            count += 1
    return count

def countNumOccurences(class_docs_concat, word):
    occurences = 0
    for cur_word in class_docs_concat.split(" "):
        if cur_word == word:
            occurences += 1
    return occurences

def concatTextAllClassDocs(doc_set, class_c):
    class_docs_concat = ""
    for word, cur_class in doc_set:
        if cur_class == class_c:
            class_docs_concat = class_docs_concat + " " + word

    return class_docs_concat

def countDocs(doc_set):
    return len(doc_set)

def extractVocabulary(doc_set):
    vocab = []
    for line, cur_class in doc_set:
        words = line.split()
        for word in words:
            if word not in vocab:
                vocab.append(word)
    return vocab

def readDataLines (filename):
    fd = open(filename, "r")
    fd_read = fd.readlines()
    return list(map( lambda d : d.strip(), fd_read))

def readLabelLines (filename):
    fl = open(filename, "r")
    fl_read = fl.readlines()
    return list(map( lambda d : int(d.strip()), fl_read))

if __name__ == "__main__":
    main()

# def TrainMultinomialNB(Classes_Set, Doc_Set):
#
#     vocab = extractVocab(Doc_Set) # vocab == V
#     num_of_docs = countDocs(Doc_Set) # num_of_docs == N
#     prior
#     condprob
#
#     for each class in Classes_Set
#         do num_class_docs = CountDocsInClass(Doc_Set, class)
#         prior[class] = num_class_docs / num_of_docs
#         text_c = ConcatTextOfAllDocsInClass(Doc_Set, class)
#         
#
#         for word in vocab
#           do T_ct = CountTokensOfTerm(Text_c, t)
#         for word in vocab
#           condprob[word][class] = (T_ct + 1)/(Sum{t'}(T_ct' + 1))
#
#     return V, prior, condprob
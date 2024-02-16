import math
import string
from stemming.porter2 import stem
from collections import defaultdict


def readFromFileTabSeparated(path):
    """
    Reads the data from a file with the given path, the data is tab separated.
    Different file types are read differently:
    - .idf files are read as a dictionary with the words as keys and the IDF as value
    - .tf files are read as a dictionary with the document index as key and as value a dictionary with the words as keys
     and the TF as value
    :param path: path to the file
    :type path: str
    :return: data from the file
    :rtype: dict
    """
    # check if path ends with .idf
    if path.endswith(".idf"):
        with open(path, "r") as f:
            idf_dict = defaultdict(float)
            for line in f:
                key, value = line.split("\t")
                value = value.replace("\n", "")
                idf_dict[key] = float(value)
            return idf_dict
    # check if path ends with .tf
    elif path.endswith(".tf"):
        with open(path, "r") as f:
            tf = dict()
            for line in f:
                index, key, value = line.split("\t")
                value = value.replace("\n", "")
                if index not in tf:
                    tf[index] = defaultdict(float)
                tf[index][key] = float(value)
            return tf


def sort_lists(list1, list2):
    """
    Sorts two lists based on the values of the first list. This is called pairwise sorting.
    :param list1: first list
    :type list1: list
    :param list2: second List
    :type list2: list
    """
    combined_lists = list(zip(list1, list2))

    # Sort based on the values of the first list (list1)
    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[0])

    # Extract the sorted lists
    sorted_list1 = [pair[0] for pair in sorted_combined_lists]
    sorted_list2 = [pair[1] for pair in sorted_combined_lists]

    return sorted_list1, sorted_list2


def binaryJoining(l: list):
    """
    Joins a list of strings by splitting the list in half and joining the two halves recursively
    :param l: list of strings
    :type l: list
    :return: joined string
    :rtype: str
    """
    if len(l) == 1:
        return l[0]
    elif len(l) == 2:
        return l[0] + " " + l[1]
    else:
        return binaryJoining(l[:len(l) // 2]) + " " + binaryJoining(l[len(l) // 2:])


def preprocess(data):
    """
    Preprocess the input data, this includes:
        - all words to lowercase
        - remove punctuation
        - split on whitespace
        - create a word2stem dict to store the stemmed words (This allows for faster stemming of words because we only need to stem unseen words)
        - create a vocab_dict to store the number of documents a stemmed word appears in
    :param data: list of documents containing lists of sentences
    :type data: list[list[str]]
    :return: the modified data list now containing for every document a defaultdict with the stemmed words as keys and
     their number of occurrences in this document, a vocab_dict containing the number of documents a word appears in
    :rtype: (list[defaultdict], defaultdict)
    """
    # all words to lowercase, remove punctuation, split on whitespace
    # create a defaultdict for vocabulary with key being the word and value beeing the stemmed word
    # This is faster than stemming every unique words in every document
    word2stem_dict = defaultdict(str)
    # vocab_dict contains as keys the stemmed words and as values the number of documents the word appears in
    # vocab_dicts = []
    vocab_dict = defaultdict(int)
    for i in range(len(data)):
        data[i] = binaryJoining(data[i]).split()
        # remove all characters that are in string.punctuation
        # Remove punctuation and empty entries
        words = [''.join(char for char in word if char not in string.punctuation) for word in data[i]]
        # create a defaultdict to count the number of times a word appears in a document, don't add empty strings
        word_count = defaultdict(int)
        for word in words:
            if word != "":
                word_count[word] += 1
        # create a defaultdict to count the number of times a stemmed word appears in a document
        stemmed_word_count_dict = defaultdict(int)
        # this _temp_vocab_dict is used to check if a word has already been added to the vocab_dict
        _temp_vocab_dict = defaultdict(bool)
        for key, value in word_count.items():
            # check for empty string
            if key == "":
                continue
            # check if word was already stemmed, if not stem it and save it in the word2stem_dict
            if key not in word2stem_dict:
                word2stem_dict[key] = stem(key)
            # get the stemmed word from the word2stem_dict
            stemmed_word = word2stem_dict[key]
            # increment the value of the stemmed word in the stemmed_word_count_dict
            stemmed_word_count_dict[stemmed_word] += value
            # set the value of the stemmed word in the _temp_vocab_dict to True which means the word occurs in the
            # document
            _temp_vocab_dict[stemmed_word] = True
        # add the stemmed_word_count_dict to the data list replacing the list of sentences in the document
        data[i] = stemmed_word_count_dict
        # increment the vocab_dict for every word that occurred in the document
        for key in _temp_vocab_dict.keys():
            vocab_dict[key] += 1
    return data, vocab_dict


def calculateIDF(vocab_dict, num_docs):
    """
    Calculates the IDF for every word in the vocabulary
    :param vocab_dict: dictionary with the vocabulary every word as key and the number of documents the word appears in as value
    :type vocab_dict: defaultdict
    :param num_docs: number of documents in the collection
    :type num_docs: int
    :return: dictionary with the vocabulary every word as key and the IDF as value, sorted by key
    :rtype: defaultdict
    """
    idf_dict = defaultdict(float)
    for key, value in vocab_dict.items():
        idf_dict[key] = math.log(num_docs / value)
    # sort by key
    return defaultdict(float, (sorted(idf_dict.items(), key=lambda x: x[0])))


def calculateTF(index, document_list):
    """
    Calculates the TF for every document in the collection
    :param index: list of document indices
    :type index: list[str]
    :param document_list: list of documents containing defaultdicts with the words as keys and their number of
     occurrences as value
    :type document_list: list[defaultdict]
    :return tf dict with document index as key and as value a dict with the words as keys and the TF as value
    :rtype: dict[str, dict[str, float]]
    """
    tf = dict()
    for ind, document_dict in zip(index, document_list):
        tf[ind] = calculateDocumentTF(document_dict)
    return tf


def calculateDocumentTF(document_dict):
    """
    Calculates the TF for every word in the provided document
    :param document_dict: dictionary with the words as keys and the number of times the word appears in the document as value
    :type document_dict: defaultdict
    :return: dictionary with the words as keys and the TF as value
    :rtype: defaultdict[str, float]
    """
    tf_dict = defaultdict(float)
    max_value = max(document_dict.values())
    for key, value in document_dict.items():
        tf_dict[key] = value / max_value
    # sort by key
    return defaultdict(float, sorted(tf_dict.items(), key=lambda x: x[0]))


def writeToFileTabSeparated(path, data):
    """
    Writes the data to a file with the given path, the data is tab separated. Different handling for .idf and .tf files
    :param path: path to the file
    :type path: str
    :param data: data to be written to the file
    :type data: dict[str, float] or dict[str, dict[str, float]]
    :raises NotImplementedError: if the file ending is not .idf or .tf
    :return: None
    :rtype: None
    """
    # check file ending
    if path.endswith(".idf"):
        with open(path, "w") as f:
            for key, value in data.items():
                f.write(key + "\t" + str(value) + "\n")
    elif path.endswith(".tf"):
        with open(path, "w") as f:
            for index, item_dict in data.items():
                for key, value in item_dict.items():
                    f.write(str(index) + "\t" + key + "\t" + str(value) + "\n")
    else:
        raise NotImplementedError

import math
import os
import xml.parsers.expat
import string
from stemming.porter2 import stem
from collections import defaultdict
import cProfile


class Index:
    def __init__(self, collectionName: str, create: bool):
        # holds the idf values for every word in the vocabulary
        self.idf = None
        # is a list holding the tf values for every document
        self.tf = None
        if create:
            self.createIndex(collectionName)
        else:
            self.readIndex(collectionName)

    def createIndex(self, collectionName):
        path_to_files = os.path.join(os.getcwd(), collectionName)
        self.index, data = parse_xml(path_to_files + ".xml")
        data, vocab = preprocess(data)
        self.tf = calculateTF(data)
        self.idf = calculateIDF(vocab, len(self.tf))
        writeToFileTabSeparated(path_to_files + ".idf", self.idf)
        writeToFileTabSeparated(path_to_files + ".tf", self.tf)

    def readIndex(self, collectionName):
        path_to_files = os.path.join(os.getcwd(), collectionName)
        self.idf = readFromFileTabSeparated(path_to_files + ".idf")
        self.tf = readFromFileTabSeparated(path_to_files + ".tf")


class XMLParser:
    def __init__(self):
        self.data = []
        self.index = []
        self.count = 0
        self.write = False

    def start_element(self, name, attrs):
        if name == "DOC":
            self.index.append(attrs["id"])
        if name == "HEADLINE":
            if len(self.data) <= self.count:
                self.data.append([])
            self.write = True
        if name == "DATELINE":
            self.write = False
        if name == "TEXT":
            if len(self.data) <= self.count:
                self.data.append([])
            self.write = True

    def end_element(self, name):
        if name == "DOC":
            self.count += 1

    def character_data(self, data):
        if self.write and data != "\n":
            self.data[self.count].append(data.lower())


def parse_xml(file_path):
    parser = xml.parsers.expat.ParserCreate()
    xml_parser = XMLParser()

    parser.StartElementHandler = xml_parser.start_element
    parser.EndElementHandler = xml_parser.end_element
    parser.CharacterDataHandler = xml_parser.character_data

    with open(file_path, "rb") as f:
        parser.ParseFile(f)

    # Sort the lists based on the values of the first list (index) before returning them
    return sort_lists(xml_parser.index, xml_parser.data)


def readFromFileTabSeparated(path):
    """
    Reads the data from a file with the given path, the data is tab separated
    """
    # check if path ends with .idf
    if path.endswith(".idf"):
        with open(path, "r") as f:
            idf_dict = defaultdict(float)
            for line in f:
                key, value = line.split("\t")
                idf_dict[key] = float(value)
            return idf_dict
    # check if path ends with .tf
    elif path.endswith(".tf"):
        with open(path, "r") as f:
            tf = dict()
            for line in f:
                index, key, value = line.split("\t")
                if index not in tf:
                    tf[index] = defaultdict(float)
                tf[index][key] = float(value)
            return tf


def sort_lists(list1, list2):
    """
    Sorts two lists based on the values of the first list
    :param list1: first list
    :type list1: list
    :param list2: second list
    :type list2: list
    :return: sorted lists
    :rtype: tuple[list, list]
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


def cosineSimilarity(vector1, vector2):
    """
    Calculates the cosine similarity between two vectors
    :param vector1: first vector
    :type vector1: defaultdict
    :param vector2: second vector
    :type vector2: defaultdict
    :return: cosine similarity
    :rtype: float
    """
    raise NotImplementedError


def preprocess(data):
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
        # create a new dict for the stemmed words, this is more efficient than stemming every word in the document and counting it
        stemmed_word_count_dict = defaultdict(int)
        # this _temp_vocab_dict is used check if a word has already been added to the vocab_dict
        _temp_vocab_dict = defaultdict(bool)
        for key, value in word_count.items():
            if key == "":
                continue
            if key not in word2stem_dict:
                word2stem_dict[key] = stem(key)
            stemmed_word = word2stem_dict[key]
            stemmed_word_count_dict[stemmed_word] += value
            _temp_vocab_dict[stemmed_word] = True
        data[i] = stemmed_word_count_dict
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
    :return: dictionary with the vocabulary every word as key and the IDF as value
    :rtype: defaultdict
    """
    idf_dict = defaultdict(float)
    for key, value in vocab_dict.items():
        idf_dict[key] = math.log(num_docs / value)
    # sort by key
    return dict(sorted(idf_dict.items(), key=lambda x: x[0]))


def calculateTF(document_list):
    """
    Calculates the TF for every document in the collection
    """
    tf = dict()
    for document_dict in document_list:
        tf[document_dict] = calculateDocumentTF(document_dict)
    return tf


def calculateDocumentTF(document_dict):
    """
    Calculates the TF for every word in the provided document
    :param document_dict: dictionary with the words as keys and the number of times the word appears in the document as value
    :type document_dict: defaultdict
    :return: dictionary with the words as keys and the TF as value
    :rtype: defaultdict
    """
    tf_dict = defaultdict(float)
    max_value = max(document_dict.values())
    for key, value in document_dict.items():
        tf_dict[key] = value / max_value
    # sort by key
    return dict(sorted(tf_dict.items(), key=lambda x: x[0]))


def writeToFileTabSeparated(path, data):
    """
    Writes the data to a file with the given path, the data is tab separated
    :param path: path to the file
    :type path: str
    :param data: data to be written to the file
    :type data:
    """
    # check if data is dict
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


def profile():
    pass


def main():
    # profile the profile() function
    cProfile.run('profile()', sort='cumtime')


main()

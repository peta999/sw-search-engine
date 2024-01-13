import os
import xml.parsers.expat
import string
from stemming.porter2 import stem
from collections import defaultdict
import cProfile

class Index:
    def __init__(self):
        pass

    def createIndex(self, collectionName):
        pass

    def readIndex(self, collectionName):
        pass


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

    return xml_parser.index, xml_parser.data



def binaryJoining(l: list):
    if len(l) == 1:
        return l[0]
    elif len(l) == 2:
        return l[0] + " " + l[1]
    else:
        return binaryJoining(l[:len(l)//2]) + " " + binaryJoining(l[len(l)//2:])
def preprocess(data):
    # all words to lowercase, remove punctuation, split on whitespace
    # create a defaultdict for vocabulary with key being the word and value beeing the stemmed word
    # This is faster than stemming every unique words in every document
    word2stem_dict = defaultdict(str)
    # vocab_dict contains as keys the stemmed words and as values the number of documents the word appears in
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
        for key, value in word_count.items():
            if key not in word2stem_dict and key != "":
                word2stem_dict[key] = stem(key)
            stemmed_word = word2stem_dict[key]
            stemmed_word_count_dict[stemmed_word] += value
            vocab_dict[word2stem_dict[key]] += 1
        data[i] = stemmed_word_count_dict

    return data, vocab_dict

def calculateIDF(vocab_dict):
    pass

def profile():
    pth = r'C:\Users\hoppe\Documents\GitHub\sw-search-engine\data\nytsmall.xml'
    index, data = parse_xml(pth)
    data, vocab = preprocess(data)
    print("")

def main():
    # profile the profile() function
    cProfile.run('profile()', sort='cumtime')

main()









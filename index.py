import os

from searchEngineUtil import preprocess, readFromFileTabSeparated, writeToFileTabSeparated, calculateTF, calculateIDF
from xmlParser import parse_xml


class Index:
    """
    Class that represents the index object of a collection of documents
    """
    def __init__(self, collectionName, create):
        """
        Initialize the index object, if create is True, the index is created and written to files, if create is False,
        the index is read from files
        :param collectionName: string that holds the name of the collection file
        :type collectionName: str
        :param create: boolean that indicates if the index should be created or read from files
        :type create: bool
        :return: None
        :rtype: None
        """
        # a dict that holds the idf values for every word in the vocabulary
        self.idf = None
        # a nested dict that holds the tf values for every document
        self.tf = None
        if create:
            self.createIndex(collectionName)
        else:
            self.readIndex(collectionName)

    def createIndex(self, collectionName):
        """
        Create the index for the collection and write it to files
        :param collectionName: string that holds the name of the collection file
        :type collectionName: str
        :return: None
        :rtype: None
        """
        path_to_files = os.path.join(os.getcwd(), collectionName)
        self.index, data = parse_xml(path_to_files + ".xml")
        data, vocab = preprocess(data)
        self.tf = calculateTF(self.index, data)
        self.idf = calculateIDF(vocab, len(self.tf))
        writeToFileTabSeparated(path_to_files + ".idf", self.idf)
        writeToFileTabSeparated(path_to_files + ".tf", self.tf)

    def readIndex(self, collectionName):
        """
        Read the index from files
        :param collectionName: string that holds the name of the collection file
        :type collectionName: str
        :return: None
        :rtype: None
        """
        path_to_files = os.path.join(os.getcwd(), collectionName)
        self.idf = readFromFileTabSeparated(path_to_files + ".idf")
        self.tf = readFromFileTabSeparated(path_to_files + ".tf")

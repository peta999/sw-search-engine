import xml.parsers.expat

from searchEngineUtil import sort_lists


class XMLParser:
    """
    Class that parses provided XML files
    """
    def __init__(self):
        """
        Initialize the XMLParser
        :return: None
        :rtype: None
        """
        # List of Lists that holds the data of the XML file
        self.data = []
        # List that holds the id of the documents
        self.index = []
        # Counter that holds the current index of the data list
        self.count = 0
        # Flag that indicates if the data should be written to the data list
        self.write = False

    def startElement(self, name, attrs):
        """
        Start element handler for the XMLParser, if the start element is HEADLINE or TEXT, the write flag is set to True.
        If the start element is DOC, the id of the document is appended to the index list.
        If the start element is DATELINE, the write flag is set to False.
        :param name: start element name
        :type name: str
        :param attrs: attributes of the start element
        :type attrs: dict
        :return: None
        :rtype: None
        """
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

    def endElement(self, name):
        """
        End element handler for the XMLParser, if the end element is DOC, the count is incremented.
        :param name: name of the end element
        :type name: str
        :return: None
        :rtype: None
        """
        if name == "DOC":
            self.count += 1

    def characterData(self, data):
        """
        Handles all data between tags, writes the data to the data list if the write flag is True.
        :param data: data between tags
        :type data: str
        :return: None
        :rtype: None
        """
        if self.write and data != "\n":
            self.data[self.count].append(data.lower())


def parse_xml(file_path):
    """
    Parses the provided XML file and returns the data and the index
    :param file_path: path to the XML file
    :type file_path: str
    :return: list of lists with the data of the XML file, list with the id of the documents sorted by index list
    :rtype: (list[str], list[list[str]])
    """
    parser = xml.parsers.expat.ParserCreate()
    xml_parser = XMLParser()

    parser.StartElementHandler = xml_parser.startElement
    parser.EndElementHandler = xml_parser.endElement
    parser.CharacterDataHandler = xml_parser.characterData

    with open(file_path, "rb") as f:
        parser.ParseFile(f)

    # Sort the lists based on the values of the first list (index) before returning them
    return sort_lists(xml_parser.index, xml_parser.data)

'''
Introduction to Python Programming / Programmierkurs I
Software Assignment WS 2014/2015
SEARCH ENGINE

'''
from searchEngineUtil import Index
from searchEngineUtil import Vector


class SearchEngine:
    
    def __init__(self, collectionName, create):
        '''
        Initialize the search engine, i.e. create or read in index.
        If create=True, the search index should be created and written
        to files. If create=False, the search index should be read from
        the files. The collectionName points to the filename of the
        document collection (without the .xml at the end). Hence, you
        can read the documents from <collectionName>.xml, and should
        write / read the idf index to / from <collectionName>.idf, and
        the tf index to / from <collectionName>.tf respectively.
        All of these files must reside in the same folder as THIS file.
        If your program does not adhere to this "interface specification",
        we will subtract some points as it will be impossible for us
        to test your program automatically!
        '''
        self.index = Index(collectionName, create)
        self.VectorList = []
        # create VectorList using self.index.tf
        for doc in self.index.tf:
            vector = Vector(doc, self.index.tf[doc], self.index.idf)
            self.VectorList.append(vector)


    def executeQuery(self, queryTerms):
        '''
        Input to this function: list of query terms
        Returns a sorted list of tuples: [('NYT_ENG_19950101.0001', 0.07237004260325626),
        ('NYT_ENG_19950101.0022', 0.013039249597972629)]
        ==> Top 10 documents, sorted by their tf.idf-sum score (highest score,
            = most relevant document comes first).
            (May be less than 10 documents if there aren't as many documents that contain
            the terms.)
        '''
        pass

    def executeQueryConsole(self):
        '''
        When calling this, the interactive console should be started, ask for queries
        and display the search results, until the user simply hits enter.
        '''
        pass
        
        

if __name__ == '__main__':
    '''
    write your code here:
    * load index / start search engine
    * start the loop asking for query terms
    * program should quit if users enters no term and simply hits enter
    '''
    # Example for how we might test your program:
    # Should also work with nyt199501 !
    searchEngine = SearchEngine("nytsmall", create=False)
    print(searchEngine.executeQuery(['hurricane', 'philadelphia']))

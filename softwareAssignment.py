'''
Introduction to Python Programming / Programmierkurs I
Software Assignment WS 2014/2015
SEARCH ENGINE

'''
from index import Index
from vector import Vector


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
        if create:
            print("Creating index")
        else:
            print("Reading index")
        self.index = Index(collectionName, create)
        print("Done")
        self.VectorList = []
        # create VectorList using self.index.tf
        for doc in self.index.tf:
            vector = Vector(index_name=doc, tf=self.index.tf[doc], idf=self.index.idf)
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
        # create query vector
        queryVector = Vector(idf=self.index.idf, world_list=[queryTerms])
        result = []
        # iterate over all document vectors and calculate similarity
        for vector in self.VectorList:
            result.append((vector.index_name, queryVector.similarity(vector)))
        result.sort(key=lambda x: x[1], reverse=True)
        # return max top ten results, results with score 0 are not returned
        r_result = [x for x in result if x[1] != 0][:10]
        if len(r_result) == 0:
            print("No results found")
        return r_result

    def executeQueryConsole(self):
        '''
        When calling this, the interactive console should be started, ask for queries
        and display the search results, until the user simply hits enter.
        '''
        while True:
            query = input("Please enter query, terms separated by whitespace: ")
            if query == "":
                break
            else:
                # print(self.executeQuery(query.split()))
                # for testing format result to have each doc with score in one line
                for result in self.executeQuery(query.split()):
                    print(result[0], result[1])
        
        

if __name__ == '__main__':
    '''
    write your code here:
    * load index / start search engine
    * start the loop asking for query terms
    * program should quit if users enters no term and simply hits enter
    '''
    # the following line loads the search engine
    searchEngine = SearchEngine("nytsmall", create=True)
    # the following line executes a query and prints the results
    # print(searchEngine.executeQuery(['hurricane', 'philadelphia']))
    # the following line starts the interactive console
    searchEngine.executeQueryConsole()

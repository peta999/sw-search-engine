import math
from collections import defaultdict

from searchEngineUtil import preprocess, calculateDocumentTF


class Vector:
    """
    Class that represents a vector for a document or a query
    """
    def __init__(self, index_name=None, tf=None, idf=None, world_list=None):
        """
        Initialize the vector, this can either be a query vector or a document vector.
        If it is a document vector, index_name, tf and idf must be provided.
        If it is a query vector, world_list and idf must be provided.
        If not exactly one of the two options is provided, a ValueError is raised.
        :param index_name:
        :param tf:
        :param idf:
        :param world_list:
        :raises ValueError: Either tf and idf and index_name or world_list and idf must be provided
        :return: None
        :rtype: None
        """
        if (not idf and ((not tf and not index_name) or not world_list)) or (index_name and idf and tf and world_list):
            raise ValueError("Either tf and idf and index_name or world_list and idf must be provided")
        self.index_name = index_name
        self.tf = tf
        self.idf = idf
        self.world_list = world_list
        self.tf_idf = None
        self.norm = None

        # create tf.idf vector and calculate norm
        self.createVector()
        self.calculateNorm()

    def createVector(self):
        """
        Create the tf.idf vector based on the provided tf and idf or world_list and idf in the constructor
        :raises ValueError: Either tf, idf and index_name or world_list and idf must be provided
        :return: None
        :rtype: None
        """
        if self.tf and self.idf and self.index_name:
            pass

        elif self.world_list and self.idf:
            # treat word_list as own document, preprocess it and calculate tf
            data, vocab = preprocess(self.world_list)
            self.tf = calculateDocumentTF(data[0])
        else:
            raise ValueError("Either tf, idf and index_name or world_list and idf must be provided")
        # calculate tf.idf
        self.tf_idf = defaultdict(float)
        for key, value in self.tf.items():
            # keys that don't appear in the idf dict return 0 and result in a tf.idf of 0
            self.tf_idf[key] = value * self.idf[key]

    def calculateNorm(self):
        """
        Precalculate the norm of the vector, this allows for faster similarity calculations because the norm calculation
        doesn't have to be done every time the similarity is calculated, but upon vector creation.
        :return: None
        :rtype: None
        """
        self.norm = math.sqrt(sum([value ** 2 for value in self.tf_idf.values()]))

    def similarity(self, vector2):
        """
        Calculate the cosine similarity between this vector and vector2
        :param vector2: the vector to calculate the similarity with
        :type vector2: Vector
        :return: the cosine similarity between this vector and vector2
        :rtype: float
        """
        assert isinstance(vector2, Vector)
        # calculate cosine similarity
        # calculate the dot product of the two vectors
        dot_product = 0
        # we can take the intersection of the two sets of keys for dot product, because the tf.idf of every word that
        # doesn't appear in both vectors is 0
        dict_set = set(self.tf_idf.keys()).intersection(set(vector2.tf_idf.keys()))
        for key in dict_set:
            dot_product += self.tf_idf[key] * vector2.tf_idf[key]
        # calculate and return the cosine similarity
        return dot_product / (self.norm * vector2.norm) if self.norm * vector2.norm != 0 else 0

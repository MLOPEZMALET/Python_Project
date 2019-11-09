#!/usr/bin/python
# coding: utf-8

"""clustering_viz : Performs clustering on textfile

Usage:
  clustering_viz.py <infile> <nbclusters> [options]

Options:
    --stopwords      Use stopwords in preprocess (list from nltk, french only).
    --tfidf          Use tfidf for preprocess.
    --stemming       Use stemming for preprocess.
    --distance=DIST  Algorithm for computing distances, choices : euclidean','manhattan', 'cosine' [default: cosine]
    --algo=ALGO      Clustering algorithm to use, choices : 'spectral','kmeans', 'dbscan', 'meanshift' [default: dbscan]
    --all            all categories
    --fake           only fake news
    --trusted        only trusted
    --noheader       no header in csv file
    -h --help        Display help and exits
"""

from __future__ import unicode_literals, print_function

from copy import deepcopy
import numpy as np
import csv

from sklearn.cluster import SpectralClustering, KMeans, MeanShift, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances, cosine_distances, manhattan_distances
from nltk.stem.snowball import SnowballStemmer

import stopwords


class Clustering():
    def __init__(self,
                 stopwords=False,
                 tfidf=False,
                 stemming=False,
                 dist="cosine",
                 algo="dbscan",
                 nbclusters=5):
        self.stopwords = stopwords
        self.stemming = stemming
        self.tfidf = tfidf
        if dist not in ["euclidean", "cosine", "manhattan"]:
            raise NotImplementedError("distance type must be cosine, euclidean or manhattan")
        else:
            self.dist = dist
        if algo not in ["spectral", "kmeans", "dbscan", "meanshift"]:
            raise NotImplementedError('clustering algorithm {} not handled'.format(algo))
        else:
            self.algo = algo
        self.nbclusters = nbclusters

    def preprocess(self, sentences):
        """Creates document-term matrix from input documents

        Args:
            sentences (list): input data
            stopwords (list): vocabulary no to consider in matrix
            tfidf (bool): if True use tfidf weight mesure in matrix
                          else just token frequencies
            stemming (bool): if True stems vocabulary in matrix
                             else use original tokens
                             /!\ French only

        Returns:
            dtm (np.array): document-term matrix (shape n_documents, n_vocabulary)
            vocab (np.array): vocabulary used to buid the matrix
        """
        lstopwords = stopwords.STOPWORDS

        if self.stemming:
            data = self._stemming(sentences)
        else:
            data = deepcopy(sentences)

        # TF IDF
        if self.tfidf:
            vectorizer = TfidfVectorizer(stop_words=lstopwords)
        # Term Frequency
        else:
            vectorizer = CountVectorizer(stop_words=lstopwords)

        dtm = vectorizer.fit_transform(data)
        # vocabulary : terms
        vocab = vectorizer.get_feature_names()

        dtm = dtm.toarray()
        vocab = np.array(vocab)
        return dtm, vocab

    def _stemming(self, documents):
        """Stems tokens in documents.

        Args:
            documents (list): list of documents to process

        Returns:
            list : documents with stemmed tokens
        """
        stemmer = SnowballStemmer("french")
        newsents = []
        for sent in documents:
            newsent = [stemmer.stem(word) for word in sent.split()] 
            newsents.append(" ".join(newsent))
        return newsents

    def compute_distances(self, dtm):
        """Creates distance matrix from document-term matrix

        Args:
            dtm (np.array): document-term matrix of shape (n_doc, n_features)

        Returns:
            np.array: distance matrix of shape (n_doc, n_doc)
        """
        if self.dist == "euclidean":
            distance_matrix = euclidean_distances(dtm)
            # on arrondit à la première décimale
            np.round(distance_matrix, 1)

        elif self.dist == "cosine":
            distance_matrix = 1 - cosine_distances(dtm)
            # on arrondit à la deuxième décimale
            np.round(distance_matrix, 2)

        elif self.dist == "manhattan":
            distance_matrix = manhattan_distances(dtm)
            np.round(distance_matrix, 2)

        return distance_matrix

    def cluster(self, distance_matrix):
        """Clustering function

        Args:
            distance_matrix (np.array): data to process (distance matrix)

        Returns:
            y_pred (np.array): results of clustering
                1-d array, for each index, value is the id of cluster
                which document is assigned to.
        """

        X = StandardScaler(with_mean=False).fit_transform(distance_matrix)

        if self.algo == "spectral":
            algorithm = SpectralClustering(n_clusters=self.nbclusters,
                                           eigen_solver='arpack',
                                           affinity="nearest_neighbors",
                                           assign_labels="discretize")

        elif self.algo == "kmeans":
            algorithm = KMeans(n_clusters=self.nbclusters,
                               precompute_distances=False)

        elif self.algo == "dbscan":
            algorithm = DBSCAN(min_samples=self.nbclusters,
                               eps=0.1,
                               metric="precomputed")

        elif self.algo == "meanshift":
            algorithm = MeanShift(cluster_all=False)

        algorithm.fit_predict(X)
        y_pred = algorithm.labels_.astype(np.int)
        final_clusters = len(set(algorithm.labels_))

        return y_pred, final_clusters

    def analyse(self, sentences):
        dtm, vocab = self.preprocess(sentences)
        distance_matrix = self.compute_distances(dtm)
        y_pred, final_clusters = self.cluster(distance_matrix)
        return y_pred, final_clusters


def main(args):
    print(args)
    analyser = Clustering(stopwords=args["--stopwords"],
                          tfidf=args["--tfidf"],
                          stemming=args["--stemming"],
                          dist=args["--distance"],
                          algo=args["--algo"],
                          nbclusters=int(args["<nbclusters>"]))
#    if args["--noheader"]:
#        sentences = open(args["<infile>"]).readlines()
#    else:
#        f = open(args["<infile>"])
#        sentences = csv.DictReader(f, delimiter='\t', quotechar='"')
#
#    sentences = {line["id"]: line["text"] for line in sentences}
    print ("clustering sentences ")
    print(sentences)

#    if args["--all"]:
#        sentences = {line["id"]: line["text"] for line in sentences}
#    elif args["--fake"]:
#        sentences = {line.split('\t')[0]: line.split('\t')[-3] for line in sentences if line["type"] == "fakeNews"}
#    elif args["--trusted"]:
#        sentences = {line.split('\t')[0]: line.split('\t')[-3] for line in sentences if line["type"] == "trusted"}

    y_pred, final_clusters = analyser.analyse(sentences)
    print(y_pred, final_clusters)

if __name__ == '__main__':
    from docopt import docopt

    args = docopt(__doc__)
    print (args)
    main(args)

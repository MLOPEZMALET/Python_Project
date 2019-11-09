#!/usr/bin/python3
# coding: utf-8

"""plotting.py cluster and plot for hackatal2018

Usage:
  plotting.py <infile> <out> [options]

Options:
    --false          only fake news
    --true           only trusted
    -h --help        Display help and exits
"""


import clustering
import clustervisualizer
import csv
import docopt
import json


def main(args):
    if args["--true"]:
        data = csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"')
        sentences = [row["text"] for row in data if row["type"] == "trusted"]
        data = csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"')
        index = {i: row["id"] for i, row in enumerate(data) if row["type"] == "trusted"}
    elif args["--false"]:
        data = csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"')
        sentences = [row["text"] for row in data if row["type"] == "fakeNews"]
        data = csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"')
        index = {i: row["id"] for i, row in enumerate(data) if row["type"] == "fakeNews"}

    else:
        data = csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"')
        print(data)
        sentences = ["\n".join([row["text"], row["title"], row["uri"]]) for row in data]
        data = csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"')
        index = {i: row["id"] for i, row in enumerate(data)}

    analyzer = clustering.Clustering(stopwords=True, tfidf=True, stemming=True, nbclusters=2, algo="spectral", dist="manhattan")
    dtm, vocab = analyzer.preprocess(sentences)
    dm = analyzer.compute_distances(dtm)
    y_pred, nb = analyzer.cluster(dm)
    visu = clustervisualizer.ClusterVisualizer(nb)
    visu.make_plot(dm, sentences, y_pred, index, output=args["<out>"])
    data = list(csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"'))
    results = {}
    for docid, val in enumerate(y_pred):
        results[str(val)] = results.get(str(val), []) + [data[docid]]
    with open(args["<out>"]+".json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)

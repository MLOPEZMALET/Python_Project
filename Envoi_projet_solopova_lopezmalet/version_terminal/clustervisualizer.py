#!/usr/bin/python
# coding: utf-8

"""Visualizer : used to visualize clustering results
"""

from __future__ import unicode_literals, print_function

import random
import os
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
plt.switch_backend('agg')


class ClusterVisualizer():
    def __init__(self, nbclusters):
        self.nbclusters = nbclusters

    def _gen_color(self):
        """Randomly generates hexadecimal color code

        Returns:
            str: hexadecimal color code
        """
        color = ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
        return "#"+color

    def make_plot(self, distance_matrix, sentences, y_pred, index, output=None):
        """Creates plot to visualize clusters

        Args:
            distance_matrix (np.array): distance matrix
            sentences (list): documents
            y_pred (np.array): results of clustering
            output (str): if None: shows plot
                          else: basename for output files

        Returns:
            None.
        """
        # Multi dimensionnal scaling for visualization
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(distance_matrix)  # shape (n_components, n_samples)
        # x and y axes
        xs, ys = pos[:, 0], pos[:, 1]

        # labels : index of documents in list
        names = [index[i] for i, sent in enumerate(sentences)]

        fig, ax = plt.subplots(figsize=(20, 10))

        colors = []
        for _ in range(self.nbclusters):
            colors.append(self._gen_color())

        for i, color in enumerate(colors):
            x = [z for j, z in enumerate(xs) if y_pred[j] == i]
            y = [z for j, z in enumerate(ys) if y_pred[j] == i]
            ax.scatter(x, y, c=color, label=str(i))

        for x, y, name in zip(xs, ys, names):
            ax.annotate(name, xy=(x, y))
        ax.legend(title="Clusters")

        if output is None:
            plt.tight_layout()
            plt.show()
        else:
            fig.suptitle(os.path.basename(output)[:-4], fontsize=20)
            plt.savefig(output+".png")


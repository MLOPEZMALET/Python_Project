from sklearn import svm
from sklearn.svm import SVC
from sklearn import preprocessing
import numpy as np
from sknn.mlp import Classifier, Layer 
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
import joblib
from sklearn.preprocessing import label_binarize
from sklearn.utils.multiclass import unique_labels
import sys, os

print("on entre TESTSVM ")
if (len(sys.argv) > 2) :
	fic_test = open(sys.argv[1], 'r')
	nom_model = sys.argv[2]
	fic_res = open(sys.argv[3], 'w')

	# Récupération des données annotées
	listeVecteursSegments = []
	ligne = fic_test.readline()
	print("on entre dans la boucle while")
	while (ligne != '') :
		if (ligne != '\n') :
			vecteurSegment = []
			elmLigne = ligne.replace('\n','').split('\t')
			elmVecteur = elmLigne[1].split(' ')
			for i in range(0, len(elmVecteur)-1) :
				vecteurSegment.append(float(elmVecteur[i]))
			# On a alors : les données du segment (id, seg, tokens...) + le vecteur + l'étiquette réelle
			listeVecteursSegments.append([elmLigne[0], vecteurSegment, elmLigne[2]])
		ligne = fic_test.readline()
	print("on sorte des boucles")
	print("on load model avec joblib")
	# Chargement du modèle
	model = joblib.load(nom_model)
	# Test du modèle et écriture du résultats dans le fic_res
	for vect in listeVecteursSegments :
		etiq_reelle=vect[2]
		x=vect[1]
		#xn=np.asarray(x)
		#min_max_scaler = preprocessing.MinMaxScaler()
		#x = min_max_scaler.fit_transform([x])
		#scaler = preprocessing.StandardScaler().fit([x])
		#x =scaler.transform([x]) 
		etiq_predite=model.predict([x])[0]
		#slack = abs(t-clf.decision_function([x]))
		#print(slack)
		#fic_res.write(vect[0]+' ')
		#for i in range(0, len(vect[1])):
			#if (i==0) :
				#fic_res.write(str(vect[1][i]))
			#else:
				#fic_res.write(' '+str(vect[1][i]))
		fic_res.write(str(etiq_reelle) + '\t' + str(etiq_predite) + '\n')
	# Fermeture des flux
	print ("on a écrit le fichier")
	fic_test.close()
	fic_res.close()
from time import time, ctime
t = time()
print(ctime(t))

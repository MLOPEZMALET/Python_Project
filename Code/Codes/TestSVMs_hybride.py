from sklearn import svm
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import sys, os


if (len(sys.argv) > 2) :
	fic_test = open(sys.argv[1], 'r')
	nom_model = sys.argv[2]
	fic_res = open(sys.argv[3], 'w')

	# Récupération des données annotées
	listeVecteursSegments = []
	ligne = fic_test.readline()
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

	# Chargement du modèle
	model = joblib.load(nom_model)

	# Test du modèle et écriture du résultats dans le fic_res
	for vect in listeVecteursSegments :
		etiq_reelle=vect[2]
		#if (etiq_reelle != 'Neutre') :
		etiq_predite=model.predict([vect[1]])[0]
		fic_res.write(vect[0])
		for i in range(0, len(vect[1])):
			if (i==0) :
				fic_res.write(str(vect[1][i]))
			else:
				fic_res.write(' '+str(vect[1][i]))
		fic_res.write('\t' + etiq_reelle + '\t' + etiq_predite + '\n')
		#else :
		#	fic_res.write('\t' + etiq_reelle + '\t' + etiq_reelle + '\n')

	# Fermeture des flux
	fic_test.close()
	fic_res.close()

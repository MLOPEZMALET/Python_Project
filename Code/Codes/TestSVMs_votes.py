from sklearn import svm
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import sys, os


if (len(sys.argv) > 6) :
	fic_test = open(sys.argv[1], 'r')
	nom_model_rbf = sys.argv[2]
	#p_rbf = sys.argv[3]
	nom_model_linear = sys.argv[3]
	#p_linear = sys.argv[5]
	nom_model_poly = sys.argv[4]
	#p_poly = sys.argv[7]
	nom_model_sigmoid = sys.argv[5]
	#p_sigmoid = sys.argv[9]
	fic_res = open(sys.argv[6], 'w')

	fic_p = open(sys.argv[7], 'r')
	# Récupération des données précision par étiquettes par modele
	#EXEMPLE :
	#rbf	TresPositif-45.5|Positif-43.86|Neutre-25|Negatif-31.67|TresNegatif-45.67
	#linear	TresPositif-33.9|Positif-41.88|Neutre-0|Negatif-39.8|TresNegatif-47.47
	#poly	TresPositif-30.5|Positif-37.77|Neutre-18.33|Negatif-32.77|TresNegatif-45.59
	#sigmoid	TresPositif-0|Positif-28.45|Neutre-9.83|Negatif-17.79|TresNegatif-18.99
	dico_etiq_p={}
	ligne=fic_p.readline()
	while(ligne!='') :
		ligne=ligne.replace('\n', '')
		dico_etiq_p[ligne.split('\t')[0]] = {}
		for elm in ligne.split('\t')[1].split('|') :
			dico_etiq_p[ligne.split('\t')[0]][elm.split('-')[0]] = float(elm.split('-')[1])
		ligne=fic_p.readline()

	#type_vote = sys.argv[11]

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
	model_rbf = joblib.load(nom_model_rbf)
	model_linear = joblib.load(nom_model_linear)
	model_poly = joblib.load(nom_model_poly)
	model_sigmoid = joblib.load(nom_model_sigmoid)

	# Test du modèle et écriture du résultats dans le fic_res
	for vect in listeVecteursSegments :
		etiq_reelle=vect[2]
		etiq_predite_rbf=model_rbf.predict([vect[1]])[0]
		etiq_predite_linear=model_linear.predict([vect[1]])[0]
		etiq_predite_poly=model_poly.predict([vect[1]])[0]
		etiq_predite_sigmoid=model_sigmoid.predict([vect[1]])[0]
		fic_res.write(vect[0])
		for i in range(0, len(vect[1])):
			if (i==0) :
				fic_res.write(str(vect[1][i]))
			else:
				fic_res.write(' '+str(vect[1][i]))
		
		etiq_predite='NOT_SURE'

		dico_etiq={}
		'''
		# Vote majoritaire
		if(type_vote == 'maj') :
			for etiq in [etiq_predite_rbf, etiq_predite_linear, etiq_predite_poly, etiq_predite_sigmoid] :
				if (etiq not in dico_etiq.keys()) :
					dico_etiq[etiq] = 1
				else :
					dico_etiq[etiq] += 1
			dico_etiq=sorted(dico_etiq.items(), key=lambda t:t[1], reverse=True)
			if(len(dico_etiq)>1) :
				if(dico_etiq[0][1] != dico_etiq[1][1]) :
					etiq_predite=dico_etiq[0][0]
		# Vote pondéré par la précision du modèle
		elif (type_vote == 'pond') :
			if (etiq_predite_rbf not in dico_etiq.keys()) :
				dico_etiq[etiq_predite_rbf]=float(p_rbf)
			else:
				dico_etiq[etiq_predite_rbf]+=float(p_rbf)
			if (etiq_predite_linear not in dico_etiq.keys()) :
				dico_etiq[etiq_predite_linear]=float(p_linear)
			else:
				dico_etiq[etiq_predite_linear]+=float(p_linear)
			if (etiq_predite_poly not in dico_etiq.keys()) :
				dico_etiq[etiq_predite_poly]=float(p_poly)
			else:
				dico_etiq[etiq_predite_poly]+=float(p_poly)
			if (etiq_predite_sigmoid not in dico_etiq.keys()) :
				dico_etiq[etiq_predite_sigmoid]=float(p_sigmoid)
			else:
				dico_etiq[etiq_predite_sigmoid]+=float(p_sigmoid)
			
			dico_etiq=sorted(dico_etiq.items(), key=lambda t:t[1], reverse=True)
			if(len(dico_etiq)>1) :
				if(dico_etiq[0][1] != dico_etiq[1][1]) :
					etiq_predite=dico_etiq[0][0]'''

		# Vote pondéré par le précision des étiquettes
		"""
		if (etiq_predite_rbf not in dico_etiq.keys()) :
			dico_etiq[etiq_predite_rbf]=dico_etiq_p['rbf'][etiq_predite_rbf]
		else:
			dico_etiq[etiq_predite_rbf]+=dico_etiq_p['rbf'][etiq_predite_rbf]
		if (etiq_predite_linear not in dico_etiq.keys()) :
			dico_etiq[etiq_predite_linear]=dico_etiq_p['linear'][etiq_predite_linear]
		else:
			dico_etiq[etiq_predite_linear]+=dico_etiq_p['linear'][etiq_predite_linear]
		if (etiq_predite_poly not in dico_etiq.keys()) :
			dico_etiq[etiq_predite_poly]=dico_etiq_p['poly'][etiq_predite_poly]
		else:
			dico_etiq[etiq_predite_poly]+=dico_etiq_p['poly'][etiq_predite_poly]
		if (etiq_predite_sigmoid not in dico_etiq.keys()) :
			dico_etiq[etiq_predite_sigmoid]=dico_etiq_p['sigmoid'][etiq_predite_sigmoid]
		else:
			dico_etiq[etiq_predite_sigmoid]+=dico_etiq_p['sigmoid'][etiq_predite_sigmoid]

		dico_etiq=sorted(dico_etiq.items(), key=lambda t:t[1], reverse=True)
		if(len(dico_etiq)>1) :
			if(dico_etiq[0][1] != dico_etiq[1][1]) :
				etiq_predite=dico_etiq[0][0]"""


		# Vote par la précision la plus importe
		p_max = 0
		etiq_max = ''
		if (dico_etiq_p['rbf'][etiq_predite_rbf] > p_max) :
			etiq_max=etiq_predite_rbf
			p_max=dico_etiq_p['rbf'][etiq_predite_rbf]
		if (dico_etiq_p['linear'][etiq_predite_linear] > p_max) :
			etiq_max=etiq_predite_linear
			p_max=dico_etiq_p['linear'][etiq_predite_linear]
		if (dico_etiq_p['poly'][etiq_predite_poly] > p_max) :
			etiq_max=etiq_predite_poly
			p_max=dico_etiq_p['poly'][etiq_predite_poly]
		if (dico_etiq_p['sigmoid'][etiq_predite_sigmoid] > p_max) :
			etiq_max=etiq_predite_sigmoid
			p_max=dico_etiq_p['sigmoid'][etiq_predite_sigmoid]
		etiq_predite=etiq_max
		

		fic_res.write('\t' + etiq_reelle + '\t' + etiq_predite + '\n')

	# Fermeture des flux
	fic_test.close()
	fic_res.close()

from sklearn import svm
from sklearn import preprocessing
import numpy as np
from sknn.mlp import Classifier, Layer 
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVC,LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import label_binarize
from sklearn.utils.multiclass import unique_labels
import joblib
import sys, os
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import QuantileTransformer
print('debut apprentissage svm')
print(sys.argv[1])
if (len(sys.argv) > 1) :
	fic=open(sys.argv[1], 'r',)
	#nomModel=sys.argv[2]
	fic_test = open(sys.argv[2], 'r')
	nom_model = sys.argv[3]
	fic_res = open(sys.argv[4], 'w')
	#Récupération des données annotées
	#Quand on voudra dépasser ovo et ovr, il faudra transformer les étiquettes (genre MaClasse et PasMaClasse)
	#Ainsi, on entrainera des modèles spécifiques...
	listeVecteursSegments=[]
	ligne=fic.readline()
	print("on entre la boule while")
	while(ligne!=''):
		if(ligne!='\n'):
			vecteurSegment=[]
			elmLigne=ligne.replace('\n','').split('\t')
			#elmLigne[0] : les segments, elmLigne[1] : les dimensions, elmLigne[2] : la polarité annotée manuellement
			elmVecteur=elmLigne[1].split(' ')
			#print(str(len(elmVecteur))
			for i in range(0, len(elmVecteur)-1):
				vecteurSegment.append(float(elmVecteur[i]))
			#Ex : entrainement SVM pour détecter Positif uniquement
			#if (elmVecteur[len(elmVecteur)-1] == 'Positif'):
			listeVecteursSegments.append([vecteurSegment, elmLigne[2]])
			#else:
			#	listeVecteursSegments.append([vecteurSegment, 'PasPositif'])
		ligne=fic.readline()
	print("on sorte de la boucle")

	#Entrainement
	# PARTIE 1 : Un contre tous
	classif=svm.SVC(decision_function_shape='ovr', kernel='rbf',C=100,gamma=0.01,coef0=1)
	#classif=svm.SVC(decision_function_shape='ovr', kernel='linear')
	#classif=svm.SVC(decision_function_shape='ovr', kernel='poly')
	#classif=svm.SVC(decision_function_shape='ovr', kernel='sigmoid')
	#-> model=classif.fit([vect[0] for vect in listeVecteursSegments], [vect[1] for vect in listeVecteursSegments])

	# PARTIE 2 : Un contre un
	#classif=svm.SVC(decision_function_shape='ovo', kernel='rbf',C=10.0,gamma=1, coef0=1)
	#classif=svm.SVC(decision_function_shape='ovo', kernel='linear')
	#classif=svm.SVC(decision_function_shape='ovo', kernel='poly')
	#classif=svm.SVC(decision_function_shape='ovo', kernel='sigmoid')
	#-> model=classif.fit([vect[0] for vect in listeVecteursSegments], [vect[1] for vect in listeVecteursSegments])

	# PARTIE 3 : Hybride
	# a) SVM un-contre-tous entre Positif, Negatif et Neutre
	# b) SVM un-contre-un pour savoir si c'est intense (Positif Fort versus Positif Pas Fort, idem pour Négatif)
	#classif=svm.SVC(decision_function_shape='ovo', kernel='poly', degree=4)#, class_weight='balanced') #rbf, linear, poly(+), sigmoid
	#vso
	#clf_SVM = OneVsRestClassifier(LinearSVC())
	#ficout=open("xy.txt", 'w')
	x=[vect[0] for vect in listeVecteursSegments]
	y=[vect[1] for vect in listeVecteursSegments]
	#scaler = RobustScaler()
	#x=scaler.fit_transform(x)

	print("Neutre","\t",y.count("Neutre"))
	print("Positif","\t",y.count("Positif"))
	print("Negatif","\t",y.count("Negatif"))
	print("TresPositif","\t",y.count("TresPositif"))
	print("TresNegatif","\t",y.count("TresNegatif"))

	#un=unique_labels(y)
	#print(un)
	#classif= Classifier(layers=[Layer("Sigmoid")],learning_rate=0.001,n_iter=25)
	#x = np.asarray(x)
	#enc = OneHotEncoder(handle_unknown='ignore')
	#enc.fit(x)
	#y = label_binarize(y, classes=un)
	#y = np.asarray(y)
	#un=unique_labels(y)
	#print(un)
	#print (x[:30])
	#print(y[:30])
	#print(x[1:3],y[1:3])
	print("on fait l'apprentissage")
	#classif = LinearRegression()
	#classif = MLPClassifier(solver='sgd',activation='relu', alpha=1e-5,hidden_layer_sizes=(100,100), max_iter=600,verbose=10, random_state=21,tol=0.000000001)
	#classif=MultinomialNB(alpha=1.0e-10)
	model=classif.fit(x,y)
	#print("on fait dump avec joblib")
	#Sauvegarde du modèle
	#joblib.dump(model, nomModel) 
	print('Fin apprentissage Partition')
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
	#model = joblib.load(nom_model)
	# Test du modèle et écriture du résultats dans le fic_res
	for vect in listeVecteursSegments :
		etiq_reelle=vect[2]
		X=vect[1]
		#X = scaler.transform([X])
		etiq_predite=model.predict([X])[0]
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
#classif=MultinomialNB()
#classif = OneVsRestClassifier(estimator=SVC(random_state=0))
#----------> http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
#classif=svm.LinearSVC()
#classif=svm.SVC(decision_function_shape='ovr')
#classif=svm.SVC(decision_function_shape='ovo')

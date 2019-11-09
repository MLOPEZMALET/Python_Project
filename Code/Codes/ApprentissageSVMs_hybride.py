from sklearn import svm
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import sys, os


if (len(sys.argv) > 2) :
	fic=open(sys.argv[1], 'r')
	nomModel=sys.argv[2]
	noyau=sys.argv[3]

	#Récupération des données annotées
	#Quand on voudra dépasser ovo et ovr, il faudra transformer les étiquettes (genre MaClasse et PasMaClasse)
	#Ainsi, on entrainera des modèles spécifiques...
	listeVecteursSegments=[]
	ligne=fic.readline()
	while(ligne!=''):
		if(ligne!='\n'):
			vecteurSegment=[]
			elmLigne=ligne.replace('\n','').split('\t')
			elmVecteur=elmLigne[1].split(' ')
			for i in range(0, len(elmVecteur)-1):
				vecteurSegment.append(float(elmVecteur[i]))
			#Ex : entrainement SVM pour détecter Positif uniquement
			#if (elmVecteur[len(elmVecteur)-1] == 'Positif'):
			if (elmLigne[2] != 'Neutre'):
				listeVecteursSegments.append([vecteurSegment, elmLigne[2]])
			#else:
			#	listeVecteursSegments.append([vecteurSegment, 'PasPositif'])
		ligne=fic.readline()

	#Entrainement
	# PARTIE 1 : Un contre tous
	classif=svm.SVC(decision_function_shape=noyau, kernel='rbf')
	#classif=svm.SVC(decision_function_shape='ovr', kernel='linear')
	#classif=svm.SVC(decision_function_shape='ovr', kernel='poly')
	#classif=svm.SVC(decision_function_shape='ovr', kernel='sigmoid')
	#-> model=classif.fit([vect[0] for vect in listeVecteursSegments], [vect[1] for vect in listeVecteursSegments])

	# PARTIE 2 : Un contre un
	#classif=svm.SVC(decision_function_shape='ovo', kernel='rbf')
	#classif=svm.SVC(decision_function_shape='ovo', kernel='linear')
	#classif=svm.SVC(decision_function_shape='ovo', kernel='poly')
	#classif=svm.SVC(decision_function_shape='ovo', kernel='sigmoid')
	#-> model=classif.fit([vect[0] for vect in listeVecteursSegments], [vect[1] for vect in listeVecteursSegments])

	# PARTIE 3 : Hybride
	# a) SVM un-contre-tous entre Positif, Negatif et Neutre
	# b) SVM un-contre-un pour savoir si c'est intense (Positif Fort versus Positif Pas Fort, idem pour Négatif)

	#classif=svm.SVC(decision_function_shape='ovo', kernel='poly', degree=4)#, class_weight='balanced') #rbf, linear, poly(+), sigmoid

	
	model=classif.fit([vect[0] for vect in listeVecteursSegments], [vect[1] for vect in listeVecteursSegments])

	#Sauvegarde du modèle
	joblib.dump(model, nomModel) 

	'''
	classif=MultinomialNB()
	classif = OneVsRestClassifier(estimator=SVC(random_state=0))
	----------> http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
	classif=svm.LinearSVC()
	classif=svm.SVC(decision_function_shape='ovr')
	classif=svm.SVC(decision_function_shape='ovo')
	'''
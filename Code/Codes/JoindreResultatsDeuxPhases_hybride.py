import sys, os, re, csv

'''
Ce programme permet de joindre les deux étiquettes preduites par deux SVM :
	- la polarité simple
	- l'intensité de la polarité
Les deux premiers fichiers fournis en parametre sont identiques sauf dans 
leur dernière colonne. 
'''

# Cette fonction permet de construire les étiquettes TresPositif, Positif,
# Neutre, Negatif et TresNegatif à partir des deux ensembles d'étiquettes :
# 	- Polarité large : Positif, Neutre et Négatif
# 	- Intensité : Intense et Faible
def DeterminerEtiquette(etiq1, etiq2) :
	if (etiq1 == 'Positif') :
		if (etiq2 == 'Intense') :
			return 'TresPositif'
		else :
			return 'Positif'
	elif (etiq1 == 'Negatif') :
		if (etiq2 == 'Intense') :
			return 'TresNegatif'
		else :
			return 'Negatif'
	else :
		return 'Neutre'

if (len(sys.argv) > 1) :
	# Ouverture des flux de lecture
	fichier1 = open(sys.argv[1], 'r')
	fichier2 = open(sys.argv[2], 'r')

	# Ouverture du flux d'écriture
	fic = open(sys.argv[3], 'w')

	# Lecture de la première ligne des deux fichiers
	ligne1 = fichier1.readline()
	ligne2 = fichier2.readline()

	while (ligne1 != '' and ligne2 != '') :
		# On coupe la ligne selon les tabulations.
		# On a alors : 
		# 	- partie 1 : les informations sur le segment + le vecteur (identitique pour les deux fichiers lus)
		# 	- partie 2 : l'étiquette réelle
		# 	- partie 3 : l'étiquette prédite par le modèle
		elmLigne1 = ligne1.replace('\n', '').split('\t')
		elmLigne2 = ligne2.replace('\n', '').split('\t')

		# Ecriture de la première partie : informations segment + vecteur segment
		fic.write(elmLigne1[0])
		# Ecriture de l'étiquette réelle
		fic.write('\t' + DeterminerEtiquette(elmLigne1[1], elmLigne2[1]))
		# Ecriture de l'étiquette prédite
		fic.write('\t' + DeterminerEtiquette(elmLigne1[2], elmLigne2[2]))
		# Ecriture du retour chariot
		fic.write('\n')


		# Lecture des lignes suivantes
		ligne1 = fichier1.readline()
		ligne2 = fichier2.readline()
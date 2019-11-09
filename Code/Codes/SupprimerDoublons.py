import sys, os

if (len(sys.argv) > 0) :
	# Ouverture du flux de lecture
	fichier=open(sys.argv[1], 'r')
	# Ouverture du flux d'écriture
	fichier_net=open(sys.argv[1].replace('.txt', '_net.txt'), 'w')
	
	# Lecture de la première ligne du fichier
	ligne=fichier.readline()

	ancien_segment='' # Initialisation de la variable

	# Tant qu'on n'est pas arrivé à la fin du fichier
	while(ligne!='') :
		elmLigne=ligne.split('\t') # Décomposition de la ligne selon les tabulations
		if (len(elmLigne) > 10) : # On vérifie que la ligne est remplie (peut-être sans polarité)
			ID=elmLigne[0]
			segment=elmLigne[1]
			theme=elmLigne[2]
			tokens=elmLigne[3]
			lemmes=elmLigne[4]
			POS=elmLigne[5]
			fct=elmLigne[6]
			chuncks=elmLigne[7]
			EN=elmLigne[8]
			nbTokens=elmLigne[9]
			entropy=elmLigne[10].replace('\n', '') # On prend le soit de supprimer le retour chariot s'il est présent
			if (len(elmLigne)>11) : # S'il y a une polarité associée au segment
				pola=elmLigne[11].replace('\n', '')
			
			# Ecriture des exemples
			# On vérifie qu'on n'a pas affaire à un doublon
			if (segment != ancien_segment) :
				fichier_net.write(ID+'\t'+segment+'\t'+theme+'\t'+tokens+'\t'+lemmes+'\t'+POS+'\t'+fct+'\t'+chuncks+'\t'+EN+'\t'+nbTokens+'\t'+entropy)
				if (len(elmLigne)>11) : # S'il y a une polarité
					fichier_net.write('\t' + pola)
				fichier_net.write('\n')
			else:
				print(ID)
			ancien_segment=segment
			segment=''
		# Lecture de la ligne suivante
		ligne=fichier.readline()

	# Fermeture du flux de lecture
	fichier.close()

	# Fermeture du fluc d'écriture 
	fichier_net.close()

	# Suppression de l'ancien fichier
	os.remove(sys.argv[1])
	os.rename(sys.argv[1].replace('.txt', '_net.txt'), sys.argv[1])
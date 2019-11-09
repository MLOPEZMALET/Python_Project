import sys, os

'''
Ce code permet, lorsqu'on lui fournit en paramètre un fichier contenant les sorties
de la fonction dump de Wapiti associé à une étiquette donnée, d'en extraire les
lemmes ayant un poids positif et de construire un lexique (associée à l'étiquette
de la fonction dump, évidemment).
Le second paramètre est une liste de mots qui ne doivent apparaître dans aucun
lexique (comme les mots vides par exemple).
'''

# Cette fonction ouvre un lexique et retourne les éléments du fichier sous forme
# de liste.
def RetournerListe(nomFichier) :
	# Initialisation de la liste contenant les most à ne pas integrer
	liste = []
	# Ouverture du flux de lecture
	fichier = open(nomFichier, 'r')

	ligne = fichier.readline().replace('\n', '') # Lecture de la première ligne
	while (ligne != '') :
		liste.append(ligne)
		ligne = fichier.readline().replace('\n', '') # Lecture de la ligne suivante

	# Fermeture du flux de lecture
	fichier.close()
	# Retour de la liste
	return liste

if (len(sys.argv) > 2) :
	# Ouverture du flux de lecture du fichier à traiter
	fichier = open(sys.argv[1], 'r')
	# Ouverture du flux d'écriture, fichier qui contiendra tous les lemmes à poids positif
	lexique = open('lexique_' + sys.argv[1], 'w')

	# Récupération des mots à ne pas intégrer au lexique
	# Mots vides
	mots_a_ne_pas_integrer = RetournerListe(sys.argv[2])

	# Lecture de la première ligne du fichier
	ligne = fichier.readline()
	while(ligne != '') : # Tant qu'on n'est pas arrivé à la fin du fichier
		elm_ligne = ligne.split(' ') # Toutes les informations d'une fct caractéristique sont séparées par une espace
		if (len(elm_ligne) >= 3) : # Ainsi on ne prend que les lignes qui nous intéressent
			poids = elm_ligne[0] # Le poids de la fct caractéristique est le premier élément de la ligne
			lemme = ''
			info_lemme = elm_ligne[2] # Le nom du patron et sa réalisation sont en troisième position
			if (':' in info_lemme) : # On vérifie qu'il y a bien une réalisation du patron
				lemme = info_lemme.split(':')[1].replace('\n', '') # On découpe la chaine d'info, on prend le second elm, on supprime le retour chariot
			if (lemme != '' and lemme not in mots_a_ne_pas_integrer) : # Si on a bien un lemme, et que le poids est positif et que le lemmes n'est pas dans la liste à ne pas intégrer, on l'écrit
				lexique.write(poids + '\t' +lemme + '\n')
				lemme = '' # On vide la chaine pour les tests du prochain tour de boucle
		ligne = fichier.readline() # Lecture de la ligne suivante

	# Fermeture du flux de lecture
	fichier.close()
	# Fermeture du flux d'écriture
	lexique.close()

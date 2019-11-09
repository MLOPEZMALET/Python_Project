import sys, os, re

from CompterNegations import NbNegations

def NbPresencesElmsDansFichier(ficEcriture, cheminFicLecture, elms):
	ficLect=open(cheminFicLecture, 'r')
	
	ligne=ficLect.readline()
	while(ligne!=''):
		if(ligne.replace('\n','') in elms):
			ficEcriture.write(' ' +str(elms.count(ligne.replace('\n',''))))
		else:
			ficEcriture.write(' 0')
		ligne=ficLect.readline()
	ficLect.close()

def TransformeEnListe(chaine):
	nvChaine=''
	for char in chaine :
		if(char!='[' and char!=']'):
			nvChaine+=char
	return nvChaine.split('|')

if (len(sys.argv) > 9) :
	fic=open(sys.argv[1], 'r') #fichier qui a les segments et a cote toutes les informations necessaires
	fic_vect=open(sys.argv[1].replace('.txt', '_vect.txt'), 'w')

	#On récupère tous les mots positifs
	elmPos=[]
	lex_pos=open(sys.argv[2], 'r')
	ligne=lex_pos.readline()
	while(ligne!=''):
		elmPos.append(ligne.replace('\n', '').lower())
		ligne=lex_pos.readline()

	# On récupère tous les mots négatifs
	elmNeg=[]
	lex_neg=open(sys.argv[3], 'r')
	ligne=lex_neg.readline()
	while(ligne!=''):
		elmNeg.append(ligne.replace('\n', '').lower())
		ligne=lex_neg.readline()

	# On récupère tous les mots d'opinion
	elmOpi=[]
	lex_opi=open(sys.argv[4], 'r')
	ligne=lex_opi.readline()
	while(ligne!=''):
		elmOpi.append(ligne.replace('\n', '').lower())
		ligne=lex_opi.readline()

	# On récupère tous les mots vides
	elmVide=[]
	lex_vide=open(sys.argv[5], 'r')
	ligne=lex_vide.readline()
	while(ligne!=''):
		elmVide.append(ligne.replace('\n', '').lower())
		ligne=lex_vide.readline()

	ligne=fic.readline()
	while(ligne!=''):
		if(ligne!='\n'):
			elmLigne=ligne.split('\t')
			ID=elmLigne[0]
			segment=elmLigne[1]
			theme=elmLigne[2]
			tokens=TransformeEnListe(elmLigne[3])
			lemmes=TransformeEnListe(elmLigne[4])
			POS=TransformeEnListe(elmLigne[5])
			FctSyn=TransformeEnListe(elmLigne[6])
			Chunck=TransformeEnListe(elmLigne[7])
			EN=TransformeEnListe(elmLigne[8])
			nbTokens=elmLigne[9]
			entropy=elmLigne[10].replace('\n', '')
			if(len(elmLigne)>11): #Si le fichier a été annoté en polarité...
				pola=elmLigne[11].replace('\n', '')

			# 0) ON RECOPIE TOUTES LES INFORMATIONS DU SEGMENT AVANT SA REPRÉSENTATION EN VECTEUR
			fic_vect.write(elmLigne[0]+' '+elmLigne[1]+' '+elmLigne[2]+' '+elmLigne[3]+' '+elmLigne[4]+' '+elmLigne[5]+' '+elmLigne[6]+' '+elmLigne[7]+' '+elmLigne[8]+' '+elmLigne[9]+' '+elmLigne[10])

			# 1) MORPHOSYNTAXE
			# -> Article détection opinions journaux politiques arabes
			tot_adv=POS.count('ADV')
			tot_adj=POS.count('ADJ')
			tot_ver=0
			for p in POS :
				if ('VER' in p) :
					tot_ver += 1
			
			tot_adv_adj_ver=tot_adv+tot_adj+tot_ver if (tot_adv+tot_adj+tot_ver>0) else 1
			# tot(adv)
			fic_vect.write('\t'+str(tot_adv))
			# moy(adv)
			fic_vect.write(' ' +str(tot_adv/tot_adv_adj_ver))
			# tot(adj)
			fic_vect.write(' '+str(tot_adj))
			# moy(adj)
			fic_vect.write(' ' +str(tot_adj/tot_adv_adj_ver))
			# tot(ver)
			fic_vect.write(' '+str(tot_ver))
			# moy(ver)
			fic_vect.write(' ' +str(tot_ver/tot_adv_adj_ver))
			# "émotivité"
			#if(tot_ver>0):
			#	fic_vect.write(' ' +str((tot_adv + tot_adj)/tot_ver))
			#else:
			#	fic_vect.write(' 1')
			# -> Autres possibilités
			# Représentation des POS-tags -> Pas bénéfique
			NbPresencesElmsDansFichier(fic_vect, sys.argv[6], POS)
			# Représentation des fonctions syntaxiques -> Pas bénéfique
			#NbPresencesElmsDansFichier(fic_vect, sys.argv[7], FctSyn) -> Pas bénéfique
			# Représentation des chuncks (le lexique ne contient que les B-Chuncks : Si B- alors un chunck et c'est info suffisante)
			#NbPresencesElmsDansFichier(fic_vect, sys.argv[8], Chunck)
			# Représentation des entités nommées
			#NbPresencesElmsDansFichier(fic_vect, sys.argv[9], EN)
			
			# Presence de 'très' dans les lemmes :
			cpt_tres = 0
			for l in lemmes :
				if (l == 'très') :
					cpt_tres+=1
			fic_vect.write(' ' +str(cpt_tres))

			# -> Mots vides
			# tot(motsVides)
			nbMotsVides = 0
			for l in lemmes:
				if (l in elmVide) :
					nbMotsVides += 1
			#fic_vect.write(' ' +str(nbMotsVides))
			# prop(motsVides)
			fic_vect.write(' ' +str(nbMotsVides / int(nbTokens)))
			
			# 2) LEXIQUES
			# Nb lemmes positifs
			nbPos = 0
			for l in lemmes:
				if (l in elmPos) :
					nbPos += 1
			fic_vect.write(' '+str(nbPos))
			# Nb lemmes négatifs
			nbNeg = 0
			for l in lemmes:
				if (l in elmNeg) :
					nbNeg += 1
			fic_vect.write(' '+str(nbNeg))
			# Nb lemmes opinion (on associe d'une manière ou d'une autre opinion à neutre (s'il n'y en a pas... neutre...))
			#nbOpi = 0
			#for l in lemmes:
			#	if (l in elmOpi) :
			#		nbOpi += 1
			#fic_vect.write(' '+str(nbOpi))

			
			# 3) POLARITES
			# Somme des polarités
			#sommePola = nbPos + nbNeg + nbOpi
			#sommePola = nbPos + nbNeg
			#fic_vect.write(' ' +str(sommePola)) -> inutile
			#sommePola = nbPos + nbNeg + nbOpi if (nbPos + nbNeg + nbOpi > 0) else 1 # Pour ne pas diviser par 0
			#sommePola = nbPos + nbNeg if (nbPos + nbNeg > 0) else 1
			# Proportion de positif
			#fic_vect.write(' ' + str(nbPos/sommePola))
			# Proportion de négatif
			#fic_vect.write(' ' + str(nbNeg/sommePola))
			# Proportion d'opinion
			#fic_vect.write(' ' + str(nbOpi/sommePola))
			########## FIN AJOUT

			# 4) NEGATION
			# Nb négations dans segment
			nbNegationsSeg = NbNegations(segment)
			fic_vect.write(' '+str(nbNegationsSeg))
			# Proportion de négation dans le segment
			#fic_vect.write(' '+str(nbNegationsSeg/int(nbTokens)))
			# Proportion positif selon négation
			#if(nbPos>0):
			#	fic_vect.write(' ' + str(nbNegationsSeg/nbPos))
			#else:
			#	if (nbNegationsSeg == 0) :
			#		fic_vect.write(' 0')
			#	else:
			#		fic_vect.write(' 1')
			# Proportion négatif selon négation
			#if(nbNeg>0):
			#	fic_vect.write(' ' + str(nbNegationsSeg/nbNeg))
			#else:
			#	if (nbNegationsSeg == 0) : 
			#		fic_vect.write(' 0')
			#	else:
			#		fic_vect.write(' 1')

			# 5) CARACTERISTIQUES DE SURFACES
			# NbTokens
			#fic_vect.write(' '+nbTokens)
			# Entropy
			#fic_vect.write(' ' + entropy)
			# Nb ponctuations expressives (une répétition d'au moins deux ? ou ! ou .)
			# Points d'exclamation
			fic_vect.write(' ' + str(len(re.findall("!+",segment)))) 
			# Points d'interrogation
			fic_vect.write(' ' + str(len(re.findall("\?+",segment)))) 
			# Points
			fic_vect.write(' ' + str(len(re.findall("\.{2,}",segment)))) 

			# Nb émoticônes
			if('EEMMOOTTIICCOONNEE' in lemmes):
				fic_vect.write(' ' + str(lemmes.count('EEMMOOTTIICCOONNEE')))
			else:
				fic_vect.write(' 0')
			# Nb tokens en majuscules
			cpt=0
			for t in tokens:
				if(t.isupper()):
					cpt+=1
			fic_vect.write(' '+str(cpt))
			# Proportion de tokens en majuscules
			cpt=0
			for t in tokens:
				if(t.isupper()):
					cpt+=1
			fic_vect.write(' ' + str(cpt/len(tokens)))

			# 6) POLARITE (si vectorisation pour apprentissage)
			if(len(elmLigne)>11):
				fic_vect.write('\t'+pola+'\n')
			else:
				fic_vect.write('\n')

		ligne=fic.readline()
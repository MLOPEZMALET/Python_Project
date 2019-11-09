import sys, os, entropy

def EcrireElmListe(fichier_seg, liste):
	fichier_seg.write('[')
	for i in range(0,len(liste)-1):
		if(liste[i]!='_'):
			if (i!=0):
				fichier_seg.write('|')
			fichier_seg.write(liste[i])
	if(liste[len(liste)-1]!='_'):
		fichier_seg.write('|'+liste[len(liste)-1])
	fichier_seg.write(']\t')

def EcrireElmSegment(fichier_seg, liste):
	for i in range(0,len(liste)):
		seg = liste[i]
		if (i!=len(liste)-1):
			seg += ' '
		fichier_seg.write(seg)
	fichier_seg.write('\t')


if (len(sys.argv) > 0) :
	fichier_conll=open(sys.argv[1], 'r')
	fichier_seg=open(sys.argv[1].replace('.conll','_regroupementInfo.txt'), 'w')

	segment=''
	listeTokens=[]
	listeLemmes=[]
	listePOS=[]
	listeChuncks=[]

	meme_segment=True
	ligne=fichier_conll.readline()
	ligne=ligne.replace('\n', '')

	old_theme = 'Init'
	cpt=0
	while(ligne!=''):
		cpt+=1
		if (cpt ==912 or cpt ==913 or cpt ==914):
			print ('Impeccable '+ str(cpt))
			print (ligne)

		if(ligne!='\n'):
			theme=ligne.split('\t')[19]
			theme=theme.replace('\n', '') 

			if (cpt ==912 or cpt ==913 or cpt ==914):
				print('new '+theme+' old '+old_theme)

			#Continuité de segment ou nouveau segment
			if (old_theme == 'Init'):
				meme_segment = True
			elif (old_theme =='Vide' and theme == 'Vide'):
				meme_segment = True
			elif (old_theme =='Vide' and theme !='Vide'):
				meme_segment = False
			elif ('B#' in old_theme and 'B#' in theme):
				meme_segment = False
			elif ('B#' in old_theme and 'I#' in theme):
				meme_segment = True
			elif ('B#' in old_theme and theme=='Vide'):
				meme_segment = False
			elif ('I#' in old_theme and 'I#' in theme):
				meme_segment = True
			elif ('I#' in old_theme and 'B#' in theme):
				meme_segment = False
			elif ('I#' in old_theme and theme=='Vide'):
				meme_segment = False

			if (cpt ==912 or cpt ==913 or cpt ==914):
				print ('meme_segment '+ str(meme_segment)+ ' theme ' +theme + ' old theme ' +old_theme)

			if (meme_segment== False and theme!='Vide'):
			#	print('token '+ligne.split('\t')[0])
			#	listeTokens.append(ligne.split('\t')[0])
			#	listeLemmes.append(ligne.split('\t')[1])
			#	listePOS.append(ligne.split('\t')[2])
			#	listeChuncks.append(ligne.split('\t')[7])
			#	old_theme=theme
			#else:		
				if (cpt ==912 or cpt ==913 or cpt ==914):
					print('Ecrire token ')
					print(listeTokens)
				#Changement de segment, écrire le segment et ces infos dans le fichier
				EcrireElmSegment(fichier_seg, listeTokens) #écriture du segment brut sans crochet
				if ('#' in theme):
					fichier_seg.write(theme.split('#')[1]+'\t') #suppression BIO
				else: 
					fichier_seg.write('Vide'+'\t') #theme = Vide
			
				EcrireElmListe(fichier_seg, listeTokens)
				EcrireElmListe(fichier_seg, listeLemmes)
				EcrireElmListe(fichier_seg, listePOS)
				EcrireElmListe(fichier_seg, listeChuncks)
				fichier_seg.write(str(len(listeTokens))+'\n') #nombre de mots dans le segment

				old_theme='Vide'
				#Annuler toutes les variables
				segment=''
				listeTokens=[]
				listeLemmes=[]
				listePOS=[]
				listeChuncks=[]
			
			if (cpt ==912 or cpt ==913 or cpt ==914):
				print ('theme ' +theme + ' old theme ' +old_theme)

			if (theme != 'Vide'):

				if (cpt ==912 or cpt ==913 or cpt ==914):
					print('append ligne '+ligne)
				listeTokens.append(ligne.split('\t')[0])
				listeLemmes.append(ligne.split('\t')[1])
				listePOS.append(ligne.split('\t')[2])
				listeChuncks.append(ligne.split('\t')[7])
				old_theme=theme
		
		else:
			old_theme ='Vide'
			
		ligne=fichier_conll.readline()

	if (theme == 'Vide' and old_theme!='Vide'):
		EcrireElmSegment(fichier_seg, listeTokens) #écriture du segment brut sans crochet
		if ('#' in old_theme):
			fichier_seg.write(old_theme.split('#')[1]+'\t') #suppression BIO
		else: 
			fichier_seg.write(old_theme+'\t') #theme = Vide

		EcrireElmListe(fichier_seg, listeTokens)
		EcrireElmListe(fichier_seg, listeLemmes)
		EcrireElmListe(fichier_seg, listePOS)
		EcrireElmListe(fichier_seg, listeChuncks)
		fichier_seg.write(str(len(listeTokens))+'\n') #nombre de mots dans le segment
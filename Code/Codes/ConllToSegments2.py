import sys, os, entropy

def EcrireElmListe(fichier_seg, liste):
	txt='['
	for i in range(0,len(liste)-1):
		if(liste[i]!='_'):
			if (txt!='['):
				txt+='|'
			txt+=liste[i]
	if(liste[len(liste)-1]!='_'):
		if (txt!='['):
			txt+='|'
		txt+=liste[len(liste)-1]
	fichier_seg.write(txt+']\t')

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
		if (6700 < cpt < 6710):
			print (str(cpt)+' ')
			print('>'+ligne+'<\n')

		if(ligne!='\n'):
			theme=ligne.split('\t')[19]
			theme=theme.replace('\n', '') 

			if (6700 < cpt < 6710):
				print('new '+theme+' old '+old_theme+'\n')

			#Continuité de segment ou nouveau segment
			if (old_theme == 'Init'):
				meme_segment = True
			elif (old_theme =='Vide' and theme == 'Vide'):
				meme_segment = False
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

			if (6700 < cpt < 6710):
				print ('meme_segment '+ str(meme_segment)+ ' theme ' +theme + ' old theme ' +old_theme)
		
		else:
			if (6700 < cpt < 6710):
				print('RC meme_segment '+ str(meme_segment)+ ' theme ' +theme)
				print(listeTokens)
			meme_segment= False 
			theme ='Vide'
		
#######
		if (meme_segment== False and len(listeTokens)!=0):
#		if (meme_segment== False and len(listeTokens)!=0 and old_theme!='Vide' and '#' not in theme):
			#	print('token '+ligne.split('\t')[0])
			#	listeTokens.append(ligne.split('\t')[0])
			#	listeLemmes.append(ligne.split('\t')[1])
			#	listePOS.append(ligne.split('\t')[2])
			#	listeChuncks.append(ligne.split('\t')[7])
			#	old_theme=theme
			#else:		
			if (82 < cpt < 6710):
				print('Ecrire token theme')
				print(listeTokens)
				print(theme)
				#Changement de segment, écrire le segment et ces infos dans le fichier
			EcrireElmSegment(fichier_seg, listeTokens) #écriture du segment brut sans crochet
			if ('#' in old_theme):
				fichier_seg.write(old_theme.split('#')[1]+'\t') #suppression BIO
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
#########

		if (theme != 'Vide' or meme_segment == True):

				if (6700 < cpt < 6710):
					print('append ligne token'+ligne.split('\t')[0]+'\n')

				listeTokens.append(ligne.split('\t')[0])
				listeLemmes.append(ligne.split('\t')[1])
				listePOS.append(ligne.split('\t')[2])
				listeChuncks.append(ligne.split('\t')[7])
				old_theme=theme
				meme_segment= True

				if (6700 < cpt < 6710):
					print (listeTokens)

		#################

			
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
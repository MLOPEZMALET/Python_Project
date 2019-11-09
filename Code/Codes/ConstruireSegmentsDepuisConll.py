import sys, os, entropy

def EcrireElmListe(fichier_seg, liste):
	fichier_seg.write('[')
	for i in range(0,len(liste)-1):
		if(liste[i]!='_'):
			fichier_seg.write(liste[i]+'|')
	if(liste[len(liste)-1]!='_'):
		fichier_seg.write(liste[len(liste)-1])
	fichier_seg.write(']\t')

if (len(sys.argv) > 0) :
	fichier_conll=open(sys.argv[1], 'r')
	fichier_seg=open(sys.argv[1].replace('.conll','_regroupementInfo.txt'), 'w')

	ID=''
	segment=''
	listeTokens=[]
	listeLemmes=[]
	listePOS=[]
	listeFctSyntax=[]
	listeChuncks=[]
	listeEntitesNommees=[]

	cpt=0
	ligne=fichier_conll.readline()
	while(ligne!=''):
		if(ligne!='\n'):
			if(cpt==0): #C'est la première ligne d'un segment donc on a l'identifiant et le segment, pas le conll
#				nv_ID=ligne.split('\t')[0]
#				if (nv_ID == ID) :
#					print(nv_ID)
#					continue
#				else :
#					ID = nv_ID
#				segment=ligne.split('\t')[1]
#				theme=ligne.split('\t')[2]
				nv_ID='ID BIDON'
				segment="SEGMENT BIDON"
				theme='THEME BIDON'
			else:
				listeTokens.append(ligne.split('\t')[0])
				listeLemmes.append(ligne.split('\t')[1])
				listePOS.append(ligne.split('\t')[9])
				listeFctSyntax.append(ligne.split('\t')[5])
				listeChuncks.append(ligne.split('\t')[7])
				listeEntitesNommees.append(ligne.split('\t')[8])
			
			cpt+=1
		else:
			#Ecrire le segments et les infos dans le fichier
			fichier_seg.write(ID+'\t'+segment.replace('\n', '')+'\t'+theme.replace('\n', '')+'\t')
			EcrireElmListe(fichier_seg, listeTokens)
			EcrireElmListe(fichier_seg, listeLemmes)
			EcrireElmListe(fichier_seg, listePOS)
			EcrireElmListe(fichier_seg, listeFctSyntax)
			EcrireElmListe(fichier_seg, listeChuncks)
			EcrireElmListe(fichier_seg, listeEntitesNommees)
			fichier_seg.write(str(len(listeTokens))+'\t') #nombre de mots dans le segment
			fichier_seg.write(str(entropy.shannon_entropy(segment))+'\n')
			cpt=0
			#Annuler toutes les variables
			ID=''
			segment=''
			listeTokens=[]
			listeLemmes=[]
			listePOS=[]
			listeFctSyntax=[]
			listeChuncks=[]
			listeEntitesNommees=[]
			
		ligne=fichier_conll.readline()

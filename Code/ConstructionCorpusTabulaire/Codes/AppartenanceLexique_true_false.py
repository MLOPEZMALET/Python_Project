#coding: utf-8

import sys, csv, os, re

def AppartientLexique(chaine, cheminfic):
	f=open(cheminfic, 'r')
	res=False
	l=f.readline()
	while(l!=''):
		elm=SupprimerRetourChariot(l)
		if(chaine==elm):
			res=True
		l=f.readline()
	f.close()
	return res

def SupprimerRetourChariot(chaine):
	nvChaine=''
	for char in chaine :
		if(char!='\n'):
			nvChaine+=char
	return nvChaine

def Troncature(chaine):
	nvChaine=''
	for i in range(4,len(chaine)-4):
		nvChaine+=chaine[i]
	return nvChaine

if (len(sys.argv) > 1) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)
	nomFichier_lex='lex_'+nomFichier
	fichier_lex=open(nomFichier_lex, 'w')

	listeFichier=[]
	for ligne in reader :
		listeFichier.append(ligne)

	for cpt in range(0,len(listeFichier)):
		if (len(listeFichier[cpt])>1) :
			i=0
			while(i<len(listeFichier[cpt])):
				fichier_lex.write(listeFichier[cpt][i]+'\t')
				i+=1
			listeValBool=[]
			for fic in os.listdir('./Lexiques'):
				if(bool(re.match('.*\.txt', fic))):
					cheminFichier='./Lexiques/'+fic
					if(AppartientLexique(listeFichier[cpt][2], cheminFichier)):
						listeValBool.append('true')
					else:
						listeValBool.append('false')

			j=0
			while(j<len(listeValBool)-1):
				fichier_lex.write(listeValBool[j]+'\t')
				j+=1
			fichier_lex.write(listeValBool[len(listeValBool)-1]+'\n')
		else:
			fichier_lex.write('\n')
	fichier.close()
	fichier_lex.close()
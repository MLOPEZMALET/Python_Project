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
	nomFichier_lex='head_'+nomFichier
	fichier_head=open(nomFichier_lex, 'w')

	listeFichier=[]
	for ligne in reader :
		listeFichier.append(ligne)

	for cpt in range(0,len(listeFichier)):
		if (len(listeFichier[cpt])>1) :
			indiceRelTeteSyntax=int(listeFichier[cpt][5])
			Head_Lemme=listeFichier[cpt+indiceRelTeteSyntax][2]
			Head_POSTalismane=listeFichier[cpt+indiceRelTeteSyntax][3]
			Head_FctSyntaxique=listeFichier[cpt+indiceRelTeteSyntax][6]
			Head_POSSEM=listeFichier[cpt+indiceRelTeteSyntax][7]
			Head_ChunkSEM=listeFichier[cpt+indiceRelTeteSyntax][8]
			Head_ENSEM=listeFichier[cpt+indiceRelTeteSyntax][9]
			Head_POSTTe=listeFichier[cpt+indiceRelTeteSyntax][10]
			Head_POSTTo=listeFichier[cpt+indiceRelTeteSyntax][11]

			'''
			lexique='_'
			for fic in os.listdir('./Lexiques'):
				if(bool(re.match('^\w.*\.txt$', fic))):
					cheminFichier='./Lexiques/'+fic
					if(AppartientLexique(Head_Lemme, cheminFichier)):
						lexique=fic
						lexique=Troncature(lexique)
			'''
			j=0

			while(j<len(listeFichier[cpt])):
				fichier_head.write(listeFichier[cpt][j]+'\t')
				j+=1
			#fichier_head.write(Head_Lemme+'\t'+Head_POSTalismane+'\t'+Head_FctSyntaxique+'\t'+Head_POSSEM+'\t'+Head_ChunkSEM+'\t'+Head_ENSEM+'\t'+Head_POSTTe+'\t'+Head_POSTTo+'\t'+lexique+'\n')
			fichier_head.write(Head_Lemme+'\t'+Head_POSTalismane+'\t'+Head_FctSyntaxique+'\t'+Head_POSSEM+'\t'+Head_ChunkSEM+'\t'+Head_ENSEM+'\t'+Head_POSTTe+'\t'+Head_POSTTo+'\n')
		else:
			fichier_head.write('\n')
	fichier.close()
	fichier_head.close()

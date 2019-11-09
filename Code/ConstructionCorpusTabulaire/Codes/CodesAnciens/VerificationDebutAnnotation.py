#coding: utf-8

import csv

fichier=open('corpusEntrainement_test.conll', 'r')
reader=csv.reader(fichier, delimiter='\t')

def ModifierDebutAnnotation(annotation):
	nv='B'
	for i in range(1, len(annotation)):
		nv+=annotation[i]
	return nv

with open('net_corpusEntrainement_test.conll','w') as fic:
	etaitLigneVide=False
	lignePrece=[]
	for ligne in reader :
		if(len(ligne)>1):
			for i in range(0, len(ligne)-1) :
				fic.write(ligne[i]+'\t')
			annotation=ligne[len(ligne)-1]
			if(etaitLigneVide):
				if(annotation!='Vide' and annotation[0]=='B'):
					fic.write(ModifierDebutAnnotation(annotation)+'\n')
				else:
					fic.write(annotation+'\n')
			else:
				fic.write(annotation+'\n')
		else:
			fic.write('\n')
			etaitLigneVide=True
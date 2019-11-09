#coding: utf-8

import sys, csv, os, re, codecs

def AppartientLexique(chaine, cheminfic):
	#print("-------------->"+cheminfic)
	#f=codecs.open(cheminfic, 'r', encoding='utf-8')
	f=open(cheminfic, 'r')
	res=''
	l=f.readline()
	#for l in f:
		#print(l)
	while(l!=''):
		elm=SupprimerRetourChariot(l).split('\t')
		if(chaine==elm[1]):
			if (float(elm[0]) < -1) :
				res = 'TresNeg'
			elif (float(elm[0]) < 0) :
				res = 'Neg'
			elif (float(elm[0]) > 1) :
				res = 'TresPos'
			elif (float(elm[0]) < 1) :
				res = 'Pos'
			else :
				res = 'Rien'
		l=f.readline()
	f.close()
	if (res == '') :
		res = 'Rien'
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
				if(bool(re.match('^\w.*\.txt$', fic))):
					cheminFichier='./Lexiques/'+fic
					listeValBool.append(AppartientLexique(listeFichier[cpt][2], cheminFichier))


			j=0
			while(j<len(listeValBool)-1):
				fichier_lex.write(listeValBool[j]+'\t')
				j+=1
			fichier_lex.write(listeValBool[len(listeValBool)-1]+'\n')
		else:
			fichier_lex.write('\n')
	fichier.close()
	fichier_lex.close()

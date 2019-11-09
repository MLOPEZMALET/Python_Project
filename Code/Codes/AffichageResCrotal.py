import sys, os, re, csv

def TransformeChaine(chaine) :
	return chaine.replace('.', ',').replace('%', '').replace(':','').replace(';', '')

if (len(sys.argv) > 0) :
	nom=sys.argv[1]
	fic=open(nom, 'r')
	reader=csv.reader(fic, delimiter=' ')
	dicoLigne={}
	for ligne in reader :
		listeElmLigne=[]
		clef=''
		for elm in ligne:
			if (elm!=''):
				if(clef==''):
					clef=elm
				else:
					if('%' in elm or '/' in elm):
						listeElmLigne.append(elm)
					else:
						if('.' in elm):
							print(elm)
		if(clef!='' and listeElmLigne!=[]):
			dicoLigne[clef]=listeElmLigne
			#listeFichier.append(dicoLigne)
	
	for clef in dicoLigne :
		print(TransformeChaine(str(clef))+'\t', end='')
		for i in range(0,len(dicoLigne[clef])-1) :
			print(TransformeChaine(dicoLigne[clef][i])+'\t', end='')
		print(TransformeChaine(dicoLigne[clef][len(dicoLigne[clef])-1])+'\n', end='')

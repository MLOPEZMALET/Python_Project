import sys, os, re
from time import time, ctime
from CompterNegations import NbNegations
t = time()
print(ctime(t))
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

print('vectorisation segment debut')
if (len(sys.argv) > 1) :
	fic=open(sys.argv[1], 'r') #fichier qui a les segments et a cote toutes les informations necessaires
	fic_vect=open(sys.argv[1].replace('.txt', '_tfidf.txt'), 'w')

	#On récupère tous les mots positifs
	

	ligne=fic.readline()
	while(ligne!=''):
		if(ligne!='\n'):
			elmLigne=ligne.split('\t')
			segment=elmLigne[0]
			tfidf=elmLigne[1]
			pola=elmLigne[2].replace('\n', '')
		
			# 0) ON RECOPIE TOUTES LES INFORMATIONS DU SEGMENT AVANT SA REPRÉSENTATION EN VECTEUR
			fic_vect.write(segment+'\t'+tfidf+'\t'+pola+'\n')

		ligne=fic.readline()
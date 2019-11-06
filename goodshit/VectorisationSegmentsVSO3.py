import sys, os, re
from time import time, ctime
import csv
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
	elmneut=[]
	lex_opi=open(sys.argv[4], 'r')
	ligne=lex_opi.readline()
	while(ligne!=''):
		elmneut.append(ligne.replace('\n', '').lower())
		ligne=lex_opi.readline()

	# On récupère tous les mots vides
	elmVide=[]
	lex_vide=open(sys.argv[5], 'r')
	ligne=lex_vide.readline()
	while(ligne!=''):
		elmVide.append(ligne.replace('\n', '').lower())
		ligne=lex_vide.readline()

	
	with open('dictionary.txt', 'r',encoding='utf-8',newline='') as dic:
		#tout=dic.read()
		#tout=tout.replace('\n','').replace('\r','\t').split('\t')
		#print('on calcule lexique')
		#liste=[[x] for x in tout]
		#f = lambda tout, n=6: [tout[i:i+n] for i in range(0, len(tout), n)]
		#liste=f(tout)

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
				Chunck=TransformeEnListe(elmLigne[6])
				nbTokens=elmLigne[7]
				tfidf=elmLigne[8]
				pola=elmLigne[9].replace('\n', '')
				# 0) ON RECOPIE TOUTES LES INFORMATIONS DU SEGMENT AVANT SA REPRÉSENTATION EN VECTEUR

				#fic_vect.write(segment+'\t'+nbTokens)
				fic_vect.write(segment+'\t')
				###################### Représentation en vecteur (une tabulation comme séparateur)
				# 1) MORPHOSYNTAXE
				# -> Article détection opinions journaux politiques arabes

				mais=lemmes.count('mais')
				et=lemmes.count('et')
				npp=POS.count("NPP")
				pon=POS.count("PONCT")
				conj=POS.count("CC")
				subj=POS.count("VS")
				tot_adv=POS.count('ADV')
				tot_adj=POS.count('ADJ')
				tot_ver=0
				nc=0
				etrang=0
				for p in POS :
					if ('V' in p) :
						tot_ver += 1
				for n in POS :
					if ('NC' in n) :
						nc += 1
				for s in POS :
					if (n=="ET") :
						etrang += 1
				tot_pos=len(POS)
				# tot(adv)
				#fic_vect.write('\t'+str(tot_adv))
				# moy(adv)
				#fic_vect.write(' ' +str(tot_adv/tot_pos))
				# tot(adj)
				#fic_vect.write('\t'+str(tot_adj))
				# moy(adj)
				#fic_vect.write(' ' +str(tot_adj/tot_pos))
				# tot(ver)
				#fic_vect.write(' '+str(tot_ver))
				# tot(ver)
				#fic_vect.write(' '+str(subj))
				# moy(ver)
				#fic_vect.write(' ' +str(tot_ver/tot_pos))
				#total nom
				#fic_vect.write(' ' +str(npp+nc))
				#total ponct
				#fic_vect.write(' ' +str(pon))
				#total mais
				#fic_vect.write('\t' +str(mais))
				#total et
				#fic_vect.write(' ' +str(et))
				# "émotivité"
				#if(tot_ver>0):
				#	fic_vect.write(' ' +str((tot_adv + tot_adj)/tot_ver))
				#else:
				#	fic_vect.write(' 1')
				# -> Autres possibilités
				# Représentation des POS-tags -> Pas bénéfique
				#NbPresencesElmsDansFichier(fic_vect, sys.argv[6], POS)
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
				#fic_vect.write(str(cpt_tres))
				if cpt_tres>0:
					fic_vect.write(str(1))
				else:
					fic_vect.write(str(0))


				cpt_n = 0
				for l in tokens :
					if (l == "n'") :
						cpt_n+=1
				#if cpt_n>0:
					#fic_vect.write(' ' +str(1))
				#else:
					#fic_vect.write(' ' +str(0))

				cpt_peu = 0
				for l in tokens :
					if (l == "un_peu") :
						cpt_peu+=1
				#if cpt_peu>0:
					#fic_vect.write(' ' +str(1))
				#else:
					#fic_vect.write(' ' +str(0))

				cpt_et = 0
				for et in lemmes :
					if (et == 'et') :
						cpt_et+=1
				#fic_vect.write(' ' +str(cpt_et))
				#bémol (pour négatifs)
				cpt_b = 0
				for b in lemmes :
					if (b == 'bémol') :
						cpt_b+=1
				#fic_vect.write(' ' +str(cpt_b))
				#dommage (pour très neg)
				cpt_d = 0
				for d in lemmes :
					if (d == 'dommage') :
						cpt_d+=1
				#fic_vect.write(' ' +str(cpt_d))
				#excellent (très positif)
				cpt_ex = 0
				for ex in lemmes :
					if (ex == 'excellent') :
						cpt_ex+=1
				#emoticons (pour très positifs)
				#fic_vect.write(' ' +str(cpt_ex))
				cpt_em = 0
				for em in tokens :
					if (em == 'EEMMOOTTIICCOONNEE') :
						cpt_em+=1
				#fic_vect.write(' ' +str(cpt_em))

				#cpt_neg=0
				#for neg in lemmes:
					#if neg=='non' or neg=='pas' or neg =='ne' or neg=='ni':
						#cpt_neg+=1
				#fic_vect.write(' ' +str(cpt_neg))

				# -> Mots vides
				# tot(motsVides)
				nbMotsVides = 0
				for l in lemmes:
					if (l in elmVide) :
						nbMotsVides += 1
				#fic_vect.write('\t' +str(nbMotsVides))
				#prop(motsVides)
				#fic_vect.write(' ' +str(nbMotsVides / int(nbTokens)))
				
				# 2) LEXIQUES
				#notresentinet
				#liste3=[]
				#for mot in tokens:
					#for e in liste:
						#if mot in e:
							#liste3.append(e)
				pos=[]
				neg=[]
				n=[]
				tp=[]
				tn=[]
				#for e in liste3:
					#n.append(float(e[1]))
					#pos.append(int(e[2]))
					#neg.append(int(e[3]))
					#pos.append(int(e[4]))
					#neg.append(int(e[5]))
					#tp.append(int(e[4]))
					#tn.append(int(e[5]))
				#n=sum(n)
				#pos=sum(pos)
				#neg=sum(neg)
				#tp=sum(tp)
				#tn=sum(tn)
				#fic_vect.write(' '+str(n))
				# Nb lemmes positifs
				nbPos = 0
				for l in lemmes:
					if (l in elmPos) :
						nbPos += 1
				#fic_vect.write(' '+str(n)+' '+str(neg)+' '+str(pos)+' '+str(tp)+' '+str(tn))
				#fic_vect.write(' '+str(n)+' '+str(neg))
				#fic_vect.write(' '+str(nbPos))
				#proportion de lemmes positifs en segment
				fic_vect.write(' '+str(nbPos/int(nbTokens)))

				# Nb lemmes négatifs
				nbNeg = 0
				for l in tokens:
					if (l in elmNeg) :
						nbNeg += 1
				#fic_vect.write(' '+str(nbNeg))
				fic_vect.write(' '+str(nbNeg/int(nbTokens)))
				#proportion de lemmes negqtifs en segment
				#fic_vect.write(' '+str(nbNeg/int(nbTokens)))
				#proportion de lemmes positifs to négatifs
				#if nbNeg != 0:
					#fic_vect.write(' '+str((nbPos/nbNeg)))
				#else:
					#fic_vect.write(' '+str(0))
				# Nb lemmes d'opinion
				nbneut = 0
				for l in tokens:
					if (l in elmneut) :
						nbneut += 1
				#fic_vect.write(' '+str(nbneut))
				fic_vect.write(' '+str(nbneut/int(nbTokens)))
				#if len(tokens)==nbneut:
					#fic_vect.write(' '+str(1))
				#else:
					#fic_vect.write(' '+str(0))

				#adv article Noémi Boubel
				cpt=0
				for i in range(len(lemmes)):
					if lemmes[i]=="jamais" or lemmes[i]=="pas":
						if lemmes[-1]!=lemmes[i]:
							if POS[i+1]=="ADJ" or POS[i+1] =="VPP":
								cpt+=1
				fic_vect.write(' ' +str(cpt))
				#cpt_plus=0
				#for i in range(len(lemmes)):
					#if lemmes[i]=="profondement" or lemmes[i]=="absolument":
						#if lemmes[-1]!=lemmes[i]:
							#if POS[i+1]=="ADJ" or POS[i+1] =="VPP":
								#if tokens[i+1] in elmPos:
									#cpt_plus+=1
				#fic_vect.write(' ' +str(cpt_plus))
				#cpt_moins=0
				#for i in range(len(lemmes)):
					#if lemmes[i]=="bien" or lemmes[i]=="franchement" or lemmes[i]=="souvent" or lemmes[i]=="totalement" or tokens[i]=="complètement" or tokens[i]=="proprement" or tokens[i]=="lourdement" or tokens[i]=="faussement":
						#if lemmes[-1]!=lemmes[i]:
							#if POS[i+1]=="ADJ" or POS[i+1] =="VPP":
								#if tokens[i+1] in elmNeg:
									#cpt_moins+=1
				#fic_vect.write(' ' +str(cpt_moins))
				# 4) NEGATION
				# Nb négations dans segment
				nbNegationsSeg = NbNegations(segment)
				fic_vect.write(' '+str(nbNegationsSeg))
				# 5) CARACTERISTIQUES DE SURFACES
				# Points d'exclamation
				fic_vect.write(' ' + str(len(re.findall("!+",segment)))) 
				# Points d'interrogation
				fic_vect.write(' ' + str(len(re.findall("\?+",segment)))) 
				# Points
				fic_vect.write(' ' + str(len(re.findall("\.{2,}",segment)))) 

				# Nb émoticônes
				#if('EEMMOOTTIICCOONNEE' in tokens):
					#fic_vect.write(' ' + str(tokens.count('EEMMOOTTIICCOONNEE')))
				#else:
					#fic_vect.write(' 0')
				# Nb tokens en majuscules
				cpt=0
				for t in tokens:
					if(t.isupper()):
						cpt+=1
				#fic_vect.write(' '+str(cpt))
				# Proportion de tokens en majuscules
				cpt=0
				for t in tokens:
					if(t.isupper()):
						cpt+=1
				#fic_vect.write(' ' + str(cpt/len(tokens)))

				# 6) tfidf
				fic_vect.write(' '+tfidf)

				# 7) POLARITE (si vectorisation pour apprentissage)
				fic_vect.write('\t'+pola)

				fic_vect.write('\n')

			ligne=fic.readline()
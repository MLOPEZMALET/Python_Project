import re, sys

def Nettoyer(phrase):
	nvPhrase=""
	for char in phrase:
		if char not in ",?;.:/=+£%*€*_)°!(\"[{]}":
			nvPhrase+=char
	return nvPhrase.lower().replace('\n', '')


def NbNegations(phrase) :
	phrase=Nettoyer(phrase)

	cpt=0
	# REGLE 1 : ne ... pas/point/plus/rien/jamais/rien/guère/aucun
	while(bool(re.match(r"(^(n\'|ne)|^.*? (n\'|ne )).*? (pas|point|plus|rien|guère|aucun)( .*?)?$", phrase))):
		phrase=re.sub(r"(^(n\'|ne)|^(.*?) (n\'|ne ))(.*? )(pas|point|plus|rien|guère|aucun)( .*?)?$", r"\3 \5\7", phrase)
		cpt+=1

	# REGLE 2 : ne ... ni ... ni
	while(bool(re.match(r"(^(n\'|ne)|^.*? (n\'|ne )).*? ni .*? ni( .*?)?$", phrase))):
		phrase=re.sub(r"(^(n\'|ne)|^(.*?) (n\'|ne ))(.*? )(ni) (.*?) (ni)( .*?)?$", r"\3\5 \7\9", phrase)
		cpt+=1

	# REGLE 4 : ni ... ni
	while(bool(re.match(r"(^ni|.*? ni) .*? ni .*?$", phrase))):
		phrase=re.sub(r"(^ni|(.*? )ni)( .*? )ni( .*?)$", r"\2\3\4", phrase)
		cpt+=1

	# REGLE 5 : sans ... ni
	while(bool(re.match(r"(^sans|.*? sans) .*? ni .*?$", phrase))):
		phrase=re.sub(r"(^sans|(.*? )sans)( .*? )ni( .*?)$", r"\2\3\4", phrase)
		cpt+=1

	# REGLE 6 : ne ... nulle part/jamais
	while(bool(re.match(r"(^(n\'|ne)|^.*? (n\'|ne )).*? (nulle part|jamais)( .*?)?$", phrase))):
		phrase=re.sub(r"(^(n\'|ne)|^(.*?) (n\'|ne ))(.*? )(nulle part|jamais)( .*?)?$", r"\3 \5\7", phrase)
		cpt+=1

	# REGLE 7 : ne ... que
	while(bool(re.match(r"(^(n\'|ne)|^.*? (n\'|ne )).*? (qu\'|que )(.*?)?$", phrase))):
		phrase=re.sub(r"(^(n\'|ne)|^(.*?) (n\'|ne ))(.*? )(qu\'|que )(.*?)?$", r"\3 \5\7", phrase)
		cpt+=1

	# REGLE 8 : jamais/personne/nul ... ne ...
	while(bool(re.match(r"(^(jamais|personne|nul)|^.*? (jamais|personne|nul)).*? (n\'|ne ).*?$", phrase))):
		phrase=re.sub(r"(^(jamais|personne|nul)|^(.*?) (jamais|personne|nul))(.*? )(n\'|ne )(.*?)$", r"\3 \5\7", phrase)
		cpt+=1

	# REGLE 9 : ... non pas ... mais ...
	while(bool(re.match(r"(^non pas|.*? non pas) .*? mais .*?$", phrase))):
		phrase=re.sub(r"(^non pas|(.*? )non pas)( .*? )mais( .*?)$", r"\2\3\4", phrase)
		cpt+=1

	# REGLE 10 : ... non seulement ... mais/encore/en plus ...
	while(bool(re.match(r"(^non seulement|.*? non seulement) .*? (mais|encore|en plus) .*?$", phrase))):
		phrase=re.sub(r"(^non seulement|(.*? )non seulement)( .*? )(mais|encore|en plus)( .*?)$", r"\2\3\5", phrase)
		cpt+=1

	# REGLE 11 : non plus -> seul en fin de traitement
	while(bool(re.match(r"(^(non plus)|^.*? (non plus))(( |-).*?$|$)", phrase))):
		phrase=re.sub(r"(^(non plus)|^(.*? )(non plus))((( |-)(.*?))$|$)", r"\3\8", phrase)
		cpt+=1

	# REGLE 12 : pas/ne/non/plus/ni -> seul en fin de traitement
	# REGLE 12 : pas/ne/non/plus/ni -> seul en fin de traitement
	while(bool(re.match(r"(^(pas|ne|non|plus|ni|rien|sans|aucun(e)?)|^.*? (pas|ne|non|plus|ni|rien|sans|aucun(e)?))(( |-).*?$|$)", phrase))):
		phrase=re.sub(r"(^(pas|ne|non|plus|ni|rien|sans|aucun(e)?)|^(.*? )(pas|ne|non|plus|ni|rien|sans|aucun(e)?))((( |-)(.*?))$|$)", r"\4\8", phrase)
		cpt+=1

	return cpt
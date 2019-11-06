# objectif : fusionner deux fichier tsv en gardant que certaines colonnes
# méthode 1 : le module csv



import csv
import itertools
import time
start = time.time()

# ouvrir en mode lecture les deux fichiers "basics" et "ratings" que nous voulons fusionner.
# attribuer un nom de variable à chaque fichier "basics_file" pour 'title.basics.tsv' et "ratings_file" pour 'title.ratings.tsv'
with open('title.basics.tsv','r') as basics_file, open('title.ratings.tsv', 'r') as ratings_file, open('new.tsv','w') as new_file :
    basics = csv.DictReader(basics_file, delimiter='\t')
    headers_basics = basics.fieldnames
    ratings = csv.DictReader(ratings_file, delimiter='\t')
    headers_ratings = ratings.fieldnames
    
    headers = headers_ratings+[headers_basics[-1]]
    writer = csv.DictWriter(new_file,delimiter='\t',fieldnames=headers)
    writer.writeheader()
    
    # lire le contenu de chaque fichier ouvert avec la classe csv.DictReader
    # Au lieu de mettre chaque ligne dans une liste (comme reader), DictReader crée avec chaque ligne un OrderedDict (sousclasse de Dict qui garde en mémoire l'ordre dans lequel les éléments ont été insérés) où la clé est le nom de la colonne et la valeur est le contenu de la cellule.
    # Exemple pour la première ligne :
    # OrderedDict([('tconst', 'tt0000001'), ('titleType', 'short'), ('primaryTitle', 'Carmencita'), ('originalTitle', 'Carmencita'), ('isAdult', '0'), ('startYear', '1894'), ('endYear', '\\N'), ('runtimeMinutes', '1'), ('genres', 'Documentary,Short')])
    
    
    liste_ratings = list(ratings)
    liste_basics = list(basics)
    
    # Fonction qui fusionne deux listes de dictionnaires sur la base d'une clé et stocke le résultat dans un nouveau dictionnaire
    def merge_lists(l1, l2, key):
        merged = {}
        for item in l1+l2:
            if item[key] in merged:
                merged[item[key]].update(item) #update l'élément si "tconst" existe déjà dans le nouveau dictionnaire, expliquer pourquoi cet update
            else:
                merged[item[key]] = item #ajouter l'élément si "tconst" n'existe pas dans le nouveau dictionnaire
            
        return merged

    '''
        Comment fonctionne le bloc "for item in l1+L2" dans notre fonction :
        >>> liste1 = [1,2,3,4]
        >>> liste2 = [5,6,7,7]
        >>> for m in liste1+liste2 :
        ...     print(m)
        ...
        1
        2
        3
        4
        5
        6
        7
        7
    '''
    new = merge_lists(liste_ratings,liste_basics,"tconst")

    # ce contient new :
    # {'tt0000001': OrderedDict([('tconst', 'tt0000001'), ('averageRating', '5.8'), ('numVotes', '1473'), ('titleType', 'short'), ('primaryTitle', 'Carmencita'), ('originalTitle', 'Carmencita'), ('isAdult', '0'), ('startYear', '1894'), ('endYear', '\\N'), ('runtimeMinutes', '1'), ('genres', 'Documentary,Short')]),...}
   
    counter = 0
    for k, v in new.items():
        if "averageRating" in v :
            writer.writerow({"tconst":v["tconst"],"averageRating":v["averageRating"],"numVotes":v["numVotes"],"genres":v["genres"]})
            counter +=1

                       
                
    print(counter)
    #915171
    end = time.time()
    processing = end-start
    print(processing)
    #151.14127397537231


# Inconvénient de cette méthode : lenteur
# Alternative : pandas




import pandas as pd
import time
start = time.time()


basics = pd.read_csv('title.basics.tsv',sep='\t')
ratings = pd.read_csv('title.ratings.tsv',sep='\t')
#ou
#basics = pd.read_table('title.basics.tsv')
#ratings = pd.read_table('title.ratings.tsv')

merged = pd.merge(basics, ratings, on='tconst',how='inner') # 1) on fusionne les deux documents sur la base de la colonne "tconst", c'est à dire qu'on ne garde que les lignes où la valeur de "tconst" est la même dans les deux documents

df = merged[['tconst','averageRating','numVotes','genres']] # 2) on créer un dataframe et on détermine les headers

#ou on peut effectuer les deux opérations en une seule ligne
#df = pd.merge(ratings[['tconst','averageRating','numVotes']],basics[['tconst','genres']],on='tconst',how='inner')

df.to_csv("new_pandas.tsv",sep='\t',header=True,index=False)
end = time.time()
processing = end-start
print(processing)
#27.96478509902954

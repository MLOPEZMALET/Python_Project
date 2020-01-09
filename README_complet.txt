<<<<<<< HEAD
PROJET LANGAGES DE SCRIPT M2 - Veronika Solopova, Mélanie Lopez Malet

ANALYSEUR DE TEXTE: pour une première analyse de corpus


CONTENU DU PROJET

Notre projet consiste en un système d'analyse de corpus de texte proposés par un usager avec des critères lexicométriques et statistiques. Pour cela, deux modalités:

	-Le programme sur terminal "script.py", qui fonctionne par ligne de commande et permet à l'utilisateur de sauvegarder directement en local des informations sur le texte concerné. Il propose des 		fonctionnalités plus techniques, telles que le calcul du TFIDF ou de la spécificité des termes. 

	-Le programme avec une interface graphique "app.py" qui permet une meilleure expérience utilisateur avec un fonctionnement plus intuitif ("drag and drop"). Il est plus simple d'utilisation, et 		permet à l'utilisateur de sélectionner uniquement les fonctionnalités dont il a besoin dans l'onglet "configuration".


FONCTIONNEMENT

	- programme sans interface graphique: lancez le programme "script.py" en ligne de commande suivi du fichier que vous voulez traiter et suivez les instructions
	- programme avec interface graphique: lancez le programme "app.py" en ligne de commande et cliquez sur le lien proposé: l'application devrait s'ouvrir dans votre explorateur.


STACK TECHNIQUE

modules nécessaires à installer avant:
dash
pandas
spacy
spacy "fr_core_news_sm"
psutil
matplotlib
chart-studio
wordcloud
plotly



alias python='python3'

# Récupération du nom du corpus
corpus=$1
# Récupération du nombre de partitions déjà créées par l'utilisateur 
nombrePartitions=$2
# Récupération du nom de la série de modèles qu'on veut tester avec le vote
serieModels=$3

# Création des partitions
cd ./../CORPUS/
python ./Codes/CrossValidation_CreationPartition.py $corpus $nombrePartitions
cd ./../Codes


echo '--------------------------------------------'
echo 'RÉSULTATS DES APPRENTISSAGES POUR LA SÉRIE '$serieModels
echo '--------------------------------------------\n'

for i in `seq 1 $nombrePartitions`;
	do
		echo '--> PARTITION '$i
		# Récupération des noms des corpus d'entrainement et de test
		corpus_train='./../CORPUS/TRAIN/'$i'_train.txt'
		corpus_test='./../CORPUS/TEST/'$i'_test.txt'

		# Vectorisation des corpus
		python VectorisationSegments.py $corpus_train ./../Lexiques/Positif.txt ./../Lexiques/Negatif.txt ./../Lexiques/Opinion.txt ./../Lexiques/MotsVides.txt ./../Lexiques/LabelTreeTagger.txt ./../Lexiques/LabelFctSyntaxTalismane.txt ./../Lexiques/LabelChuncksSEM.txt ./../Lexiques/LabelENSEM.txt
		python VectorisationSegments.py $corpus_test ./../Lexiques/Positif.txt ./../Lexiques/Negatif.txt ./../Lexiques/Opinion.txt ./../Lexiques/MotsVides.txt ./../Lexiques/LabelTreeTagger.txt ./../Lexiques/LabelFctSyntaxTalismane.txt ./../Lexiques/LabelChuncksSEM.txt ./../Lexiques/LabelENSEM.txt

		# Récupération des noms de fichiers vectorisés
		corpus_train_vect='./../CORPUS/TRAIN/'$i'_train_vect.txt'
		corpus_test_vect='./../CORPUS/TEST/'$i'_test_vect.txt'

		# Apprentissage du SVM avec le corpus d'entrainement
		#python ApprentissageSVMs.py $corpus_train_vect './../MODELS/'$i'_model_'$serieModels'.pkl'

		# Test du modèle appris sur les données tests
		#python TestSVMs_votes.py $corpus_test_vect './../MODELS/'$i'_model_'$serieModels'_rbf.pkl' '38.94' './../MODELS/'$i'_model_'$serieModels'_linear.pkl' '36.6' './../MODELS/'$i'_model_'$serieModels'_poly.pkl' '34.71' './../MODELS/'$i'_model_'$serieModels'_sigmoid.pkl' '13.1' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt' 'pond'
		python TestSVMs_votes.py $corpus_test_vect './../MODELS/'$i'_model_'$serieModels'_rbf.pkl' './../MODELS/'$i'_model_'$serieModels'_linear.pkl' './../MODELS/'$i'_model_'$serieModels'_poly.pkl' './../MODELS/'$i'_model_'$serieModels'_sigmoid.pkl' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt' './../serieA_precisions.txt'

		# Appel de CROTAL pour visualiser les résultats
		# Suppression du fichier s'il existe déjà
		if [ -f './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal' ]; then
			rm './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		fi
		~/../../Applications/CROTAL/crotal eval './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt' >> './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		python AffichageResCrotal.py './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		python AffichageMicroMoyenneParEtiquettes.py './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt'
		echo '\n'
	done;

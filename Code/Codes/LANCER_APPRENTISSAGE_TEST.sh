
alias python='python3'

# Récupération du nom du corpus
corpus=$1
# Récupération du nombre de partitions déjà créées par l'utilisateur 
nombrePartitions=$2
# Récupération du nom de la série de modèle à créer
serieModels=$3

# Création des partitions
cd ./../CORPUS/
echo 'avant cross-validation'
python ./Codes/CrossValidation_CreationPartition2.py $corpus $nombrePartitions
echo 'apres cross-validation'
cd ./../Codes


echo '--------------------------------------------'
echo 'RÉSULTATS DES APPRENTISSAGES POUR LA SÉRIE '$serieModels
echo '--------------------------------------------\n'

for i in `seq 1 $nombrePartitions`;
	do
		echo '--> PARTITION '$i
		# Récupération des noms des corpus d'entrainement et de test
		corpus_train='./../CORPUS/TRAIN/'$i'_train2.txt'
		corpus_test='./../CORPUS/TEST/'$i'_test2.txt'

		# Vectorisation des corpus
		python VectorisationSegmentsVSO3.py $corpus_train ./../Lexiques/pos.txt ./../Lexiques/negat.txt ./../Lexiques/neut.txt ./../Lexiques/MotsVides.txt		
		echo 'train fait'
		python VectorisationSegmentsVSO3.py $corpus_test ./../Lexiques/pos.txt ./../Lexiques/negat.txt ./../Lexiques/neut.txt ./../Lexiques/MotsVides.txt		
		echo 'test fait'
#		python VectorisationSegments.py $corpus_test ./../Lexiques/Positif.txt ./../Lexiques/Negatif.txt ./../Lexiques/Opinion.txt ./../Lexiques/MotsVides.txt ./../Lexiques/LabelTreeTagger.txt ./../Lexiques/LabelFctSyntaxTalismane.txt ./../Lexiques/LabelChuncksSEM.txt ./../Lexiques/LabelENSEM.txt

		# Récupération des noms de fichiers vectorisés
		corpus_train_vect='./../CORPUS/TRAIN/'$i'_train2_tfidf.txt' 
		corpus_test_vect='./../CORPUS/TEST/'$i'_test2_tfidf.txt'

		# Apprentissage du SVM avec le corpus d'entrainement
		python Apprentissage.py $corpus_train_vect $corpus_test_vect './../MODELS/'$i'_model_'$serieModels'.pkl' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt'
		#'./../MODELS/'$i'_model_'$serieModels'.pkl'
		# Test du modèle appris sur les données tests
		#python TestSVMs.py $corpus_test_vect './../MODELS/'$i'_model_'$serieModels'.pkl' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt'

		# Appel de CROTAL pour visualiser les résultats
		# Suppression du fichier s'il existe déjà
		if [ -f './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal' ]; then
			rm './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		fi
		./../../../outils/CROTAL/crotal eval './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt' >> './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		python AffichageResCrotal.py './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		python AffichageMicroMoyenneParEtiquettes.py './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt'
		echo '\n'
	done;

#!/usr/bin/python
# coding: utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import io

with io.open('out.txt','w', encoding='utf8') as csvfile1:
	filewriter = csv.writer(csvfile1, delimiter=' ')

	with io.open('Corpus.txt','r', encoding='utf8') as csvfile:
		corpus = csv.reader(csvfile, delimiter='\t')
		list1=list(corpus)
	for row in list1:
		b=row[0]
		r=b.split()
		filewriter.writerow(r)

	csvfile.close()
csvfile1.close()
 

with io.open('out2.txt', 'w',encoding='utf8') as f2:
	filewriter = csv.writer(f2, delimiter=' ')

	with io.open('out.txt', 'r',encoding='utf8') as f:
		corpus=f.reader(csvfile, delimiter=' ')
            
		#ici on peut ajouter liste de stop words
		vectorizer = TfidfVectorizer()
		vectorizer.fit(corpus)
		vector = vectorizer.transform(corpus)
		filewriter.writerow(vectorizer.idf_)
		print(vectorizer.idf_)

#print(vector.shape),
features = vectorizer.fit_transform(corpus)
print(features)
f.close()
f2.close()
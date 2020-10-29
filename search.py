# from min_hash import jaccard
import pandas as pd
import lsh
import os
from main import create_shingles_matrix, create_hash_matrix, create_signature_matrix

df = pd.read_csv('DNA/human_data.txt', sep='\t')

def find_similar_docs(bucket, doc_id):
	doc_result = []

	for band in bucket :
		for hash_val, docs in bucket[band].items():
			if doc_id in docs:
				doc_result += docs

	doc_result.sort()
	return list(set(doc_result))


def process_query(query, signature_matrix):

	search_result = lsh.locality_sensitive_hashing(signature_matrix)
	'''
	query
	rows -> sequences
	find the index of first row which contains query
	'''
	sample_doc_index = -1
	seq = df['sequence']
	for idx, s in enumerate(seq):
		if query in str(s):
			sample_doc_index = idx
			break

	similar_docs = find_similar_docs(search_result, sample_doc_index)
	print ("Similar docs are : ")
	for doc_id in similar_docs: 
		print(doc_id)
	print()


print('Starting Processing ....')
npmatrix = create_shingles_matrix()
hash_matrix = create_hash_matrix()
signature_matrix = create_signature_matrix(npmatrix, hash_matrix)

while True:
	query = input("Enter query :  ")
	process_query(query, signature_matrix)

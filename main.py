import numpy as np
import pandas as pd

# Key - Shingle, Value - List of docs containing that shingle
main_dict = {}
# Contains all shingles
shingle_list = []
# Contains all unique shingles
main_shingle_list = []
# Number of hash functions
num_of_hash_func = 100

df = pd.read_csv('DNA/human_data.txt', sep='\t')

def create_shingles_matrix():
	seq = df['sequence']

	for docid, sequence in enumerate(seq):
		sequence = str(sequence)
		shingle_list = [sequence[x:x+4] for x in range(0, len(sequence)-3)]

		for shingle in shingle_list:
			if 'N' in shingle:
				continue
			if shingle in main_dict:
				if docid not in main_dict[shingle]:
					main_dict[shingle].append(docid)
			else:
				main_dict[shingle] = []
				main_shingle_list.append(shingle)
				main_dict[shingle].append(docid)

	npmatrix = np.zeros((len(main_dict), len(seq)), dtype='int32')
	for i in range(len(main_shingle_list)):
		for j in main_dict[main_shingle_list[i]]:
			npmatrix[i][j] = 1

	print(len(main_shingle_list))

	return npmatrix

def create_hash_matrix():
	hash_matrix = np.zeros((len(main_dict), num_of_hash_func), dtype='int32')
	for hash in range(num_of_hash_func):
		for i in range(len(main_shingle_list)):
			hash_matrix[i][hash] = ((2*(i+1))+1+((5*(i+1)+1)*(hash+1))) % 256

	return hash_matrix


def create_signature_matrix(npmatrix, hash_matrix):
	signature_matrix = np.empty((num_of_hash_func, len(df)), dtype='int32')
	signature_matrix.fill(100000)

	for hash in range(0, num_of_hash_func):
		for row in range(0, len(main_shingle_list)):
			for docid in range(0, len(df)):
				if(npmatrix[row][docid] == 1):
					signature_matrix[hash][docid] = min(hash_matrix[row][hash], signature_matrix[hash][docid])

	return signature_matrix

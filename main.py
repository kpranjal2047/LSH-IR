import zlib

import pandas as pd
import numpy as np
import re
import random
import os

# Import data
df = pd.read_csv('data.csv', sep=',')
# print(df)


# Creates Boolean Shingle Matrix with number of rows = unique_shingles and columns = number of documents

shingle_dict = {}
unique_shingles = []

shingle_length = int(input("Enter length of shingles to be generated: "))

def create_shingles():
    '''
    Creates Shingle Matrix of dimension (No of unique shingles * No of Docs) 
    Returns: Shingle Matrix 
    '''
    print('[INFO] Creating Shingles Matrix ...')
    desc = df['description']
    for doc_id, desc in enumerate(desc):
        # store all shingles of length k
        desc = str(desc)
        desc = re.sub(r"<.*>", "", desc)
        desc = re.sub(r"[^a-z0-9\s]", "", desc.lower())
        # print(desc)
        shingle_list = [desc[x:x + shingle_length] for x in range(0, len(desc) - (shingle_length-1))]

        for shingle in shingle_list:
            if shingle in shingle_dict:
                if doc_id not in shingle_dict[shingle]:
                    shingle_dict[shingle].append(doc_id)
            else:
                shingle_dict[shingle] = []
                # store the unique shingles
                unique_shingles.append(shingle)
                shingle_dict[shingle].append(doc_id)

    # create a boolean matrix for all shingles
    shingle_matrix = np.zeros((len(unique_shingles), len(df)), dtype='int32')
    for i in range(len(unique_shingles)):
        for j in shingle_dict[unique_shingles[i]]:
            shingle_matrix[i][j] = 1

    print('[SUCCESS] Shingle Matrix Created.')
    # print(shingle_matrix.shape)
    # print(shingle_matrix)
    # print(shingle_dict)
    # print(len(unique_shingles))

    return shingle_matrix


# num of hash functions is 100
def get_min_hash_functions():
    '''
    Generates 100 random hash functions of size ax + b  
    Returns: List of hash functions
    '''
    result = []
    for x in range(100):
        vector = []
        for y in range(2):
            vector.append(random.randint(1, 200))
        result.append(vector)

    return result


def find_signature_matrix(shingle_matrix):
    '''
    Generates signature matrix for the given shingle matrix of the same dimension
    Input: Shingle Matrix  
    Returns: Signature Matrix
    '''
    print('[CHECK] Checking for Signature Matrix')
    if os.path.exists('Saved/signature_matrix_{}.npy'.format(shingle_length)):
        print('[SUCCESS] Signature Matrix Found!')
        signature_matrix = np.load('Saved/signature_matrix_{}.npy'.format(shingle_length))
        #print("Shingle Matrix\n",shingle_matrix)
        #print(shingle_matrix.shape)
        #print("Signature Matrix\n",signature_matrix)
        #print(signature_matrix.shape)
        return signature_matrix

    print('[INFO] Creating Signature Matrix')
    # We assume min hash functions to be of the form a*x + b
    print('[INFO] Generating 100 Random Hash Functions ...')
    min_hash_functions = get_min_hash_functions()

    # Initialize signature matrix elements to infinity
    signature_matrix = []
    for x in range(100):
        vector = []
        for y in range(len(shingle_matrix[0])):
            vector.append(1000000)
        signature_matrix.append(vector)

    print('Creating Signature Matrix using Hash Functions')
    # Update the similarity matrix for each hash function
    for x in range(len(shingle_matrix)):
        print(f'{x}/{len(unique_shingles)}')
        for y in range(100):
            hash_value = ((min_hash_functions[y][0] * x) + min_hash_functions[y][1]) % len(shingle_matrix)
            for z in range(len(shingle_matrix[0])):
                if shingle_matrix[x][z] == 1:
                    if hash_value < signature_matrix[y][z]:
                        signature_matrix[y][z] = hash_value

    print(signature_matrix)

    if not os.path.exists('Saved'):
        os.mkdir('Saved')
    np.save('Saved/signature_matrix_{}.npy'.format(shingle_length), signature_matrix)

    return signature_matrix

def create_buckets(signature_matrix):
    '''
    Finds documents similar to input Query DocId and displays the results in rank order fashion.
    Creates a dictionary of buckets using the signature matrix and hashes documents with
    similar signature in the same bucket
    Input: Signature Matrix
    Prints: List of similar documents in descending order of similarity
    '''
    query_docid = int(input("Enter DocId to be checked for similarity (0-499): "))
    bands = 25
    rows_per_band = 4
    threshold = float(input("Enter threshold of Jaccard similarity: "))
    print('[CHECK] Checking for similar documents')
    bucket = 0
    answer = {}
    for band in range(0, bands):
        band_dict = {}
        for docid in range(0, 500):
            sum = 0
            for row in range(band * rows_per_band, (band * rows_per_band) + rows_per_band):
                sum += ((row+1-(band * rows_per_band)) * signature_matrix[row][docid])

            if sum not in band_dict:
                band_dict[sum] = []
            band_dict[sum].append(docid)
            if(docid == query_docid):
                bucket = sum
        for i in band_dict[bucket]:
            if i not in answer:
                answer[i] = calc_jaccard_sim(query_docid, i,signature_matrix)
        band_dict.clear()
    print('[SUCCESS] Printing similar documents (most relevant first)')
    for i in sorted(answer, key = answer.get, reverse = True):
        if (answer[i]>threshold):
            print(i,answer[i])

def calc_jaccard_sim(query_docid, docid,relevant_matrix):
    '''
    Calculates Jaccard Similarity between two documents
    Input: Documents to be compared and signature/shingle matrix
    Returns: Jaccard Similarity 
    '''
    a = relevant_matrix[:,query_docid]
    b = relevant_matrix[:,docid]
    return np.double(np.bitwise_and(a, b).sum()) / np.double(np.bitwise_or(a, b).sum())


shingle_matrix = create_shingles()
signature_matrix = find_signature_matrix(shingle_matrix)
create_buckets(signature_matrix)

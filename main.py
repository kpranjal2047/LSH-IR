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
    result = []
    for x in range(100):
        vector = []
        for y in range(2):
            vector.append(random.randint(1, 200))
        result.append(vector)

    return result


def find_signature_matrix(shingle_matrix):

    print('[CHECK] Checking for Signature Matrix')
    if os.path.exists('Saved/signature_matrix_{0}.npy'.format(shingle_length)):
        print('[SUCCESS] Signature Matrix Found!')
        signature_matrix = np.load('Saved/signature_matrix_{0}.npy'.format(shingle_length))
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

    np.save('Saved/signature_matrix_{0}.npy'.format(shingle_length), signature_matrix)

    return signature_matrix





shingle_matrix = create_shingles()
signature_matrix = find_signature_matrix(shingle_matrix)

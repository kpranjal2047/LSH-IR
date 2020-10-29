""" Text-based information retrieval system using Locality Sensitive Hashing"""

import numpy as np


def building_shingle_doc_dictionary():
    """ main_dict is a dictionary which stores shingles of size 8 as keys and the 
    docNames as a list of values corresponding to that key"""

    """main_shingle_list stores the list of all the shingles"""

    """
    The file is read in dataset and shingles of length 8 are taken from it 
    and then further stored in shingle_list. main_dict is also filled accordingly.
    """


main_dict = {}
s = 0
main_shingle_list = []
for j in range(1, 101):
    file = open("corpus/"+str(j)+".txt", 'r', encoding="utf8")
    docid = j
    dataset = file.read()
    dataset = dataset.lower()
    length_of_doc = len(dataset)

    shingle_list = [dataset[x:x+8] for x in range(0, length_of_doc-8, 1)]
    s += len(shingle_list)
    for i in range(0, len(shingle_list)):
        shingle = shingle_list[i]
        if shingle in main_dict:
            if docid not in main_dict[shingle]:
                main_dict[shingle].append(docid)  # docid
        else:
            main_dict[shingle] = []
            main_shingle_list.append(shingle)
            main_dict[shingle].append(docid)


def making_shingle_doc_matrix():
    """
    npmatrix is the original matrix with rows as shingles and columns as docIds
    storing 0 if a shingle present in document else 1
    """


npmatrix = np.zeros((len(main_dict), 101), dtype='int32')
for i in range(0, len(main_shingle_list)):
    for j in main_dict[main_shingle_list[i]]:
        npmatrix[i][j] = 1


def building_hash_matrix():
    """ The num_of_hash_func is taken as 96 and the hash matrix has shingles as rows
    and hash functions as columns. This matrix stores the hash values according to 
    the hash function declared below.
    """


num_of_hash_func = 96
hash_matrix = np.zeros((len(main_dict), num_of_hash_func), dtype='int32')
for hash in range(0, num_of_hash_func):
    for i in range(0, len(main_shingle_list)):
        hash_matrix[i][hash] = ((2*(i+1))+1+((5*(i+1)+1)*(hash+1))) % 53808


def building_signature_matrix():
    """
    sign_matrix has rows as number of hash functions and columns as the docs.
    This matrix is initialised with infinity values. Now the npmatrix is mapped
    to the sign_matrix. So, if the npmatrix contains 1 , then the sign_matrix will
    have the corresponding hash values for a particular hash function
    Similarly, different rows of the sign_matrix will be filled with different
    hash functions values 
    """


sign_matrix = np.empty((num_of_hash_func, 101), dtype='int32')
sign_matrix.fill(100000)

for hash in range(0, num_of_hash_func):
    for row in range(0, len(main_shingle_list)):

        for docid in range(1, 101):
            if(npmatrix[row][docid] == 1):
                sign_matrix[hash][docid] = min(
                    hash_matrix[row][hash], sign_matrix[hash][docid])


def building_buckets_and_finding_plagiarised_docs():
    """         
    Here, rows are clubbed into 24 bands with each band having 4 rows.
    The dictionary band_dict stores the documents present in every band.

    To hash a document into bands, 
    multiply the sign_matrix values of that document with the indexes 
    corresponding to a band and then take a summation over those values.
    If the sum is an index of the band_dict , then append the document to that bucket(i.e, sum),
    otherwise make a new bucket and then append that document to that bucket.

    Finally, print all the documents present in the same bucket as the input document.
    This will be the final set of plagiarised documents.
 """


query_docid = eval(input("Enter query docid:  "))  # Give query here


bands = 24
rows = 4
bucket = 0
answer = set()
for band in range(0, bands):
    band_dict = {}
    for docid in range(1, 101):
        sum = 0
        prod = 1
        for row in range(band*rows, (band*rows)+rows):
            sum += ((row+1-(band*rows))*sign_matrix[row][docid])

        if sum not in band_dict:
            band_dict[sum] = []
        band_dict[sum].append(docid)
        if(docid == query_docid):
            bucket = sum
    for i in band_dict[bucket]:
        answer.add(i)
    band_dict.clear()
print(answer)

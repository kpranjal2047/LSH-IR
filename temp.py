
import numpy as np
import pandas as pd

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

npmatrix = np.zeros((len(main_dict), 101), dtype='int32')
for i in range(0, len(main_shingle_list)):
    for j in main_dict[main_shingle_list[i]]:
        npmatrix[i][j] = 1

# ------------------
num_of_hash_func = 96
hash_matrix = np.zeros((len(main_dict), num_of_hash_func), dtype='int32')
for hash in range(0, num_of_hash_func):
    # x=np.random.randint(53808)
    # y=np.random.randint(53808)
    for i in range(0, len(main_shingle_list)):
        # hash_matrix[i][hash]=((((hash+2)*i)+1)%53808)
        hash_matrix[i][hash] = ((2*(i+1))+1+((5*(i+1)+1)*(hash+1))) % 53808
        # hash_matrix[i][hash]=((x*(i+1))+1+((y*(i+1)+1)*(hash+1)))%53808

#sign_matrix=[[12 for i in range(101)] for j in range(8)]
sign_matrix = np.empty((num_of_hash_func, 101), dtype='int32')
sign_matrix.fill(100000)

for hash in range(0, num_of_hash_func):
    for row in range(0, len(main_shingle_list)):

        for docid in range(1, 101):
            if(npmatrix[row][docid] == 1):
                sign_matrix[hash][docid] = min(
                    hash_matrix[row][hash], sign_matrix[hash][docid])


# Query-----------------------

query_docid = eval(input("Enter query docid:  "))
# query_docid=97

bucket = 0
answer = set()
bands = 24
rows = 4
for band in range(0, bands):
    band_dict = {}
    # for i in range(0,100):
    # band_dict[i]=[]
    for docid in range(1, 101):
        sum = 0
        prod = 1
        for row in range(band*rows, (band*rows)+rows):
            sum += ((row+1-(band*rows))*sign_matrix[row][docid])
            # prod*=sign_matrix[row][docid]
        # sum+=prod
        # sum=sum%100
        if sum not in band_dict:
            band_dict[sum] = []
        band_dict[sum].append(docid)
        if(docid == query_docid):
            bucket = sum
    for i in band_dict[bucket]:
        answer.add(i)
    band_dict.clear()
print(answer)

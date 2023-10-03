import os
import shutil
import numpy as np
import SPTAG

vector_number = 1000000
vector_dimension = 128

# Randomly generate the database vectors. Currently SPTAG only support int8, int16 and float32 data type.
x = np.random.rand(vector_number, vector_dimension).astype(np.float32) 

# Prepare metadata for each vectors, separate them by '\n'. Currently SPTAG python wrapper only support '\n' as the separator
m = ''
for i in range(vector_number):
    m += str(i) + '\n'

index = SPTAG.AnnIndex('BKT', 'Float', vector_dimension)

# Set the thread number to speed up the build procedure in parallel 
index.SetBuildParam("NumberOfThreads", '4', "Index")

# Set the distance type. Currently SPTAG only support Cosine and L2 distances. Here Cosine distance is not the Cosine similarity. The smaller Cosine distance it is, the better.
index.SetBuildParam("DistCalcMethod", 'L2', "Index") 

if (os.path.exists("sptag_index")):
    shutil.rmtree("sptag_index")
if index.BuildWithMetaData(x, m, vector_number, False, False):
    index.Save("sptag_index") # Save the index to the disk

os.listdir('sptag_index')

# Local index test on the vector search
index = SPTAG.AnnIndex.Load('sptag_index')

# prepare query vector
q = np.random.rand(vector_dimension).astype(np.float32)

result = index.SearchWithMetaData(q, 10) # Search k=3 nearest vectors for query vector q
print (result[0]) # nearest k vector ids
print (result[1]) # nearest k vector distances
print (result[2]) # nearest k vector metadatas
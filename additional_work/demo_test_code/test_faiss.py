import faiss
import numpy as np

# Create a random dataset of 10 vectors, each with 5 dimensions
d = 5  # dimension
nb = 10  # number of database vectors
np.random.seed(1234)  # make reproducible
xb = np.random.random((nb, d)).astype('float32')

# Create a FAISS index
index = faiss.IndexFlatL2(d)  # L2 distance index
print(f"Is the index trained? {index.is_trained}")

# Add vectors to the index
index.add(xb)
print(f"Number of vectors in the index: {index.ntotal}")

# Search for the 2 nearest neighbors of the first vector
k = 2  # number of nearest neighbors
D, I = index.search(xb[:1], k)
print("Distances:", D)
print("Indices:", I)

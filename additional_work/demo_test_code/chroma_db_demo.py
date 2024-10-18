# python can also run in-memory with no server running: chromadb.PersistentClient()

import chromadb
client = chromadb.PersistentClient(path="/vector_db")

client.heartbeat() # returns a nanosecond heartbeat. Useful for making sure the client remains connected.
# client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
# I can also use inner product for normalized data (same distance measure as cosine sim in that case)
collection = client.get_or_create_collection(
    name="my_collection",
    metadata={"hnsw:space": "cosine"} # l2 is the default
)

# collection = client.create_collection(name="my_collection", embedding_function=emb_fn)
# collection = client.get_collection(name="my_collection", embedding_function=emb_fn)

# # Add docs to the collection. Can also update and delete. Row-based API coming soon!
collection.add(
    documents=["This is document1", "This is document2"], # we embed for you, or bring your own
    metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on arbitrary metadata!
    ids=["doc1", "doc2"], # must be unique for each doc 
)

results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)  
print(results)

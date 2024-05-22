from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import time
from dotenv import dotenv_values
import pickle
import re
import os
from MTBLoadDataset import MTBLoadDataset

# load the metadata set
loadData = MTBLoadDataset()
metadata_set = loadData.load_dataset()

# connect to the pine cone api
config = dotenv_values(".env")
env_key = config["PINE_CONE_ENV_KEY"]
api_key = config["PINE_CONE_API_KEY"]
embed_model_id = config["EMBED_MODEL_ID"]
print(f"env_key = {env_key}")
print(f"api_key = {api_key}")
print("\n")

# TODO: This needs to be renamed to MTBDatasetLoad, then create
# the actual PineConeUpload class for upserting the new_dataset

# initialize pinecone, create the index
pc = Pinecone(
    api_key=api_key
)

# create pinecone index for searching trailz ai
#pinecone.create_index(name="trailz-ai", metric="cosine", dimension=768)
#index = pinecone.Index("trailz-ai")
index = pc.Index("trailz-ai")
print("Index:")
print(index)
print("\n")

# create the embedder for the query
# mini model - sentence-transformers/all-MiniLM-L12-v2
search_query = "Flowy and steep rocky trails, including blue and black rated trails"
#search_query = "Trails in Illinois"
model = SentenceTransformer(embed_model_id)
query = model.encode(search_query)

# run the query for the trail
start = time.time()
results = index.query(vector=[query.tolist()], top_k=5)
end = time.time()
total = end - start

# load the query squad dataset
print("Results from top 5 regular query:")
loadData.show_results(results, metadata_set)
print("\n")

# filter using conditions for metadata
conditions = {
    "areaNames": {"$in": ["Albuquerque"]},
    "difficulty": {"$in": ["Intermediate", "Difficult"]},
    "average_rating": {"$gte": 3.5} 
}
meta_results = index.query(vector=[query.tolist()], top_k=10, filter=conditions)
print("Results from top 5 conditional metadata query:")
print(f"Type meta res = {type(meta_results)}")
loadData.show_results(meta_results, metadata_set)
print("\n")

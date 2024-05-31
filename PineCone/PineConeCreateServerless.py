from pinecone import Pinecone, ServerlessSpec
from tqdm.auto import tqdm
import os
import pickle
from dotenv import dotenv_values
import re

# connect to the pine cone api
config = dotenv_values("../.env")
env_key = config["PINE_CONE_ENV_KEY"]
api_key = config["PINE_CONE_API_KEY"]
print(f"env_key = {env_key}")
print(f"api_key = {api_key}")
print("\n")

# initialize pinecone, create the index
#    environment=env_key
pc = Pinecone(api_key=api_key)

"""
pinecone.init(
    api_key=api_key
)
"""

# create pinecone index for searching trailz ai
pc.create_index(name="trailz-ai-v2",
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-west-2"
    )
)
print("PC:")
print(pc)


import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Load datasets
india_df = pd.read_csv("data/drugs_india.csv")
usa_df = pd.read_csv("data/drugs_usa_fda.csv")

# Combine text
texts = list(india_df['brand_name']) + list(usa_df['generic_name'])

# Model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings
vectors = model.encode(texts)

# Save index
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))

faiss.write_index(index, "model/drug_index.faiss")

# Save mapping
with open("model/drug_mapping.pkl", "wb") as f:
    pickle.dump(texts, f)

print("Embedding complete! 🚀")

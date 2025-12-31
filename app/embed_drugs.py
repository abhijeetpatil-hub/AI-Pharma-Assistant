import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

DATA_PATH = "data/drugs_full_500.csv"
EMB_PATH = "data/drug_embeddings.faiss"
MAP_PATH = "data/drug_mapping.csv"

print("📌 Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("🧠 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("🔍 Generating embeddings...")
sentences = df["generic_name"].fillna("") + " " + df["brand_name"].fillna("")
embeddings = model.encode(sentences.tolist(), show_progress_bar=True)

print("🗂 Converting to FAISS index...")
embeddings = np.array(embeddings).astype("float32")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

print("💾 Saving FAISS & mapping...")
faiss.write_index(index, EMB_PATH)
df.to_csv(MAP_PATH, index=False)

print("🎯 Completed: Embeddings saved successfully!")
print(f"➡ {EMB_PATH}")
print(f"➡ {MAP_PATH}")

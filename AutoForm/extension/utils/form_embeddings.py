import requests
from sentence_transformers.util import semantic_search
import pandas as pd
import torch
import os
import json

from .embedding_source import EMBEDDING_SOURCE, model_id

with open(os.path.join(os.path.dirname(__file__), 'hf_token.json')) as f:
    hf_token = json.load(f)['hf_token_embeddings']

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

def embed_categories(embedding_source=EMBEDDING_SOURCE):

    response = requests.post(api_url, headers=headers, json={"inputs": embedding_source, "options":{"wait_for_model":True}})
    embeddings = response.json()

    embeddings = torch.tensor(embeddings)

    df = pd.DataFrame(embeddings)
    df.to_csv('embeddings.csv', index=False)

    return embeddings

def load_embeddings(path='embeddings.csv'):
    df = pd.read_csv(path)
    embeddings = df.to_numpy()
    embeddings = embeddings.tolist()
    embeddings = torch.tensor(embeddings)

    return embeddings

def query_embedding(query, headers=headers):
    query = requests.post(api_url, headers=headers, json={"inputs": query, "options":{"wait_for_model":True}})
    query_embeddings = query.json()

    query_embeddings_tensor = torch.tensor(query_embeddings)

    return query_embeddings_tensor


def similarity_search(query):

    if os.path.exists('embeddings.csv'):
        embeddings = load_embeddings('embeddings.csv')
    else:
        embeddings = embed_categories()

    query_embeddings_tensor = query_embedding(query, headers)

    hits = semantic_search(query_embeddings_tensor, embeddings, top_k=1)
    if hits[0][0]['score'] < 0.1:
        most_similar = 'No se encontró campo similar'
    else:
        most_similar = EMBEDDING_SOURCE[hits[0][0]['corpus_id']]
    return most_similar
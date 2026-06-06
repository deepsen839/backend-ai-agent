import json
from pathlib import Path

import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

CATALOG_PATH = (
    Path(__file__).parent.parent
    / "catalog"
    / "catalog.json"
)

model = None
index = None
documents = None


def initialize_catalog_search():
    global model
    global index
    global documents

    if index is not None:
        return

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    with open(
        CATALOG_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        catalog = json.load(f)

    documents = []

    for plan in catalog["plans"]:

        doc = f"""
        Plan: {plan['name']}
        Price: {plan['price']}
        Features:
        {', '.join(plan['features'])}
        """

        documents.append(doc)

    embeddings = model.encode(
        documents
    )

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(
        embeddings
    )


def search_catalog(
    query: str,
    top_k: int = 3
):
    global index

    if index is None:
        initialize_catalog_search()

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    distances, indices = (
        index.search(
            query_embedding,
            top_k
        )
    )

    results = []

    for idx in indices[0]:

        if idx < len(documents):

            results.append(
                documents[idx]
            )

    return results
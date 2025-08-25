import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def main():
    with open('data/articles.json') as f:
        articles_json = json.load(f)

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    for articles in articles_json:
        sentences = [articles['text'] for articles in articles_json]
        embeddings = model.encode(sentences)

        embeddings = np.array(embeddings).astype('float32')
        print(embeddings)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        faiss.write_index(index, 'data/vector.index')
        print("Number of vectors :", index.ntotal)


if __name__ == "__main__":
    main()

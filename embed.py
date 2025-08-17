import json

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def main():
    # sentences = ["This is an example sentence", "Each sentence is converted"]
    # model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    #
    # embeddings = model.encode(sentences)
    #
    # embeddings = np.array(embeddings).astype('float32')
    # index = faiss.IndexFlatL2(embeddings.shape[1])
    # index.add(embeddings)
    # print(index)
    # faiss.write_index(index, 'data/vector.index')
    # print("Number of vectors :", index.ntotal)
    #
    # k = 2  # Number of nearest neighbors to search for
    # D, I = index.search(embeddings, k)  # Search for the embeddings themselves
    # print("Distances:\n", D)
    # print("Indices:\n", I)
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

    metadata_dict = {}
    for idx, article in enumerate(articles_json):
        metadata_dict[idx] = {
            "title": article['title'],
            "date": article['date'],
            "url": article['url'],
            "publisher": article['publisher']
        }
    with open('data/metadata.json', 'w') as m_file:
        json.dump(metadata_dict, m_file, indent=2)
    print("dumped meta data")


if __name__ == "__main__":
    main()

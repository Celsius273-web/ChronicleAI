import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os



def chunkandvect():
    try:
        with open('data/articles.json') as f:
            articles_json = json.load(f)
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,  # ~800 characters max per chunk
            chunk_overlap=100,  # overlap so context carries over
            separators=["\n\n", "\n", " ",]
        )

        metadata_path = "data/metadata.json"
        if os.path.exists(metadata_path):
            with open(metadata_path) as f:
                try:
                    metadata = json.load(f)
                except:
                    metadata = {}
        else:
            metadata = {}
        c_id = len(metadata)
        index_path = "data/vector.index"
        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
        else:
            index = None
        chunklist = []
        for url, article in articles_json:
            if url in articles_json[url]:
                continue
            raw_text = article["text"]
            chunks = splitter.split_text(raw_text)

            for chunk in chunks:
                meta = {
                    "text": chunk,  # Replace with actual text for the article
                    "info": article["publisher"] + " " + article["date"] + " " + article["title"]
                }
                metadata[c_id] = meta
                c_id += 1
                chunklist.append(chunk)

            embeddings = model.encode(chunklist)
            embeddings = np.array(embeddings).astype('float32')
            if index is None:
                index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)
            chunklist.clear()


        faiss.write_index(index, 'data/vector.index')
        print("Number of vectors:", index.ntotal)
        print("Num of chunks", len(metadata))
        output_file_path = 'data/metadata.json'
        with open(output_file_path, 'w') as fd:
            json.dump(metadata, fd, indent=2)
        print(f"Data written to JSON file successfully at {output_file_path}.")

    except Exception as e:
        print(f"Error writing to JSON file: {e}")


def main():
    chunkandvect()

if __name__ == "__main__":
    main()
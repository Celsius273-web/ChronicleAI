import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def askuser():
    print("Please share a prompt")
    prompt = input("Enter a prompt for the NEWSBOT: ")
    return prompt

def vectorizeandsearch(userprompt):
    with open('data/metadata.json') as f:
        metadata = json.load(f) #metadata is dict

    #setup and vectoring the prompt
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    vectorprompt = model.encode(userprompt)
    faiss_index = faiss.read_index('data/vector.index')
    query_vector = np.array([vectorprompt]).astype("float32")

    #  Search the index
    k = 9
    distances, indicies = faiss_index.search(query_vector, k)
    print("Distances:", distances, " indicies", indicies)
    retrieved_chunks = []
    print(np.shape(indicies), " shape of indicies")
    for idx in indicies:
        for i in idx:
            retrieved_chunks.append(metadata[str(i)])
    print(retrieved_chunks)

    #turn the vectors into chunks
    #make a list of chunks
    #input LLM: chunks & meta + prompt + reminder 4 LLM


def main():
    #ask user
    question = askuser()
    vectorizeandsearch(question)

if __name__ == "__main__":
    main()
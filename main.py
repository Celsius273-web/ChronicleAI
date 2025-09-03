import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline
from google import genai
from google.genai import types
import ingest
import process
import os
from dotenv import load_dotenv, dotenv_values
import warnings
def loadandorganize():
    ingest.main()
    process.main()
    print("ingested and processed")

def askuser():
    print("Please share a prompt")
    prompt = input("Enter a prompt for the NEWSBOT: ")
    return prompt

def newsBot():
    load_dotenv()
    with warnings.catch_warnings():
        api_k = os.environ.get("MY_KEY")
    with open('data/metadata.json') as f:
        metadata = json.load(f) #metadata is dict
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    userprompt = askuser()
    #setup and vectoring the prompt

    vectorprompt = model.encode(userprompt)
    faiss_index = faiss.read_index('data/vector.index')
    query_vector = np.array([vectorprompt]).astype("float32")

    #  Search the index
    k = 5
    distances, indicies = faiss_index.search(query_vector, k)
    result_string = " "


    summarizer = pipeline("summarization", model='t5-small')
    for idx in indicies:
        for i in idx:
            chunk_text = metadata[str(i)]['text'] + " " + metadata[str(i)]['info']   # Extract the text directly
            warnings.simplefilter("ignore", UserWarning)
            chunk_summary = summarizer(chunk_text, max_new_tokens=120, do_sample=False, truncation=True)
            result_string += chunk_summary[0]['summary_text'] + " "    #summary of the chunks reduce work for API

    #API CALL
    text = (userprompt + "\nHere are chunk summaries from multiple sources:\n" + result_string +
    "\nPlease synthesize a detailed, balanced answer. Use as much information as possible from the chunks. " +
       " Do not hallucinate; rely only on the given content and your own verified knowledge." +
    "Ensure the responses have depth and you can include dates." )

    client = genai.Client(api_key=api_k)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= text,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    print(response.text)

    new_memory = userprompt + response.text
    vector_mem = model.encode(new_memory)
    vector_mem = np.array(vector_mem).astype('float32')
    vector_mem = vector_mem.reshape(1, -1)  # 1 row, vector_dim columns
    faiss_index.add(vector_mem)
    id = len(metadata) + 1
    metadata[str(id)] = new_memory
    faiss.write_index(faiss_index, 'data/vector.index')
    output_file_path = 'data/metadata.json'
    with open(output_file_path, 'w') as fd:
        json.dump(metadata, fd, indent=2)
    print(f"Data written to JSON file successfully at {output_file_path}.")


def run():

    while True:
        answer = input("Options: p for new prompt, n for new sources, other chars to quit: ").lower()
        if answer == 'p':
            newsBot()
        elif answer == 'n':
            loadandorganize()
        else:
            break

if __name__ == '__main__':
    run()


import json
from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunker():
    try:
        with open('data/articles.json') as f:
            articles_json = json.load(f)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,  # ~800 characters max per chunk
            chunk_overlap=100,  # overlap so context carries over
            separators=["\n\n", "\n", ".", " ", ""]
        )

        structured_chunks = []
        for article in articles_json:
            raw_text = article["text"]

            chunks = splitter.split_text(raw_text)

            for i, chunk in enumerate(chunks):
                structured_chunks.append({
                    "chunk_id": f"{article['title'][:30]}_{i}",  # unique id
                    "text": chunk,
                    "publisher": article["publisher"],
                    "date": article["date"],
                    "url": article["url"],
                    "title": article["title"]
                })

        output_file_path = 'data/chunkedArticles.json'
        with open(output_file_path, 'w') as fd:
            json.dump({"chunked": structured_chunks}, fd, indent=4)
        print(f"Data written to JSON file successfully at {output_file_path}.")

    except Exception as e:
        print(f"Error writing to JSON file: {e}")


def main():
    chunker()

if __name__ == "__main__":
    main()
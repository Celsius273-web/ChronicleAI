import yaml
import os
import feedparser
import json
from playwright.sync_api import sync_playwright

def openyaml(fpath):
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"The file {fpath} does not exist.")
    with open(fpath, "r") as file:
        data = yaml.safe_load(file)
        newsList = []
        for item in data:
            newsList.append([item['name'], item['url']])
    return newsList

def fetchtext(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=50000)  # Set a timeout for page loading
            content = page.query_selector('article')  # Example selector for the main article
            if content:
                text = content.inner_text()  # Get the text content
            else:
                text = "No content found."
        except Exception as e:
            print(f"Error fetching text from {url}: {e}")
            text = "Error fetching content."
        finally:
            browser.close()
        return text.strip()

def parselinks(links):
    organizedjson = []
    for item in links:
        source = item[1]
        print(f"Parsing feed: {source}")  # Log the feed being parsed
        f = feedparser.parse(source)
        if not f.entries:
            print(f"No articles found in feed: {source}")  # Log if no articles are found
            continue  # Skip to the next feed if no entries

        for article in f.entries:
            if article.link:
                details = fetchtext(article.link)
                if details and "Error fetching content." not in details and "No content found." not in details:
                    organizedjson.append({
                        "title": article.title if 'title' in article else 'No title available',
                        "date": article.get('published', 'No date provided'),
                        "publisher": item[0],
                        "summary": article.get('summary', 'No summary available'),
                        "url": article.link if 'link' in article else 'No URL available',
                        "text": details
                    })
                else:
                    print(f"Skipping article due to lack of content: {article.title if 'title' in article else 'No title available'}")

    print(f"Total articles collected: {len(organizedjson)}")
    try:
        output_file_path = 'data/articles.json'
        with open(output_file_path, 'w') as fd:
            json.dump(organizedjson, fd, indent=4)
        print(f"Data written to JSON file successfully at {output_file_path}.")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

def main():
    try:
        info = openyaml("/Users/school/Desktop/newsBOT/data/config.yaml")
        parselinks(info)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

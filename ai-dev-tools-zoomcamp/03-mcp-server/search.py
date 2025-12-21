import os
import requests
import zipfile
import minsearch
import io

URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_NAME = "fastmcp-main.zip"

def download_data():
    if os.path.exists(ZIP_NAME):
        print(f"{ZIP_NAME} already exists.")
        return

    print(f"Downloading {URL}...")
    response = requests.get(URL)
    response.raise_for_status()
    
    with open(ZIP_NAME, "wb") as f:
        f.write(response.content)
    print("Download complete.")

def load_documents():
    print("Loading documents from zip...")
    documents = []
    
    with zipfile.ZipFile(ZIP_NAME, 'r') as z:
        for file_info in z.infolist():
            if file_info.is_dir():
                continue
            
            if not (file_info.filename.endswith('.md') or file_info.filename.endswith('.mdx')):
                continue
                
            # Remove first part of the path
            parts = file_info.filename.split('/', 1)
            if len(parts) > 1:
                clean_filename = parts[1]
            else:
                clean_filename = file_info.filename
                
            with z.open(file_info) as f:
                content = f.read().decode('utf-8')
                
            documents.append({
                'content': content,
                'filename': clean_filename
            })
            
    print(f"Loaded {len(documents)} documents.")
    return documents

def index_documents(documents):
    print("Indexing documents...")
    index = minsearch.Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    index.fit(documents)
    print("Indexing complete.")
    return index

def search(index, query):
    print(f"Searching for: {query}")
    results = index.search(query, num_results=5)
    return results

def initialize_index():
    download_data()
    documents = load_documents()
    index = index_documents(documents)
    return index

def main():
    index = initialize_index()
    
    query = "demo"
    results = search(index, query)
    
    print("\nSearch Results:")
    for result in results:
        print(f"File: {result['filename']}")
        # print(f"Preview: {result['content'][:100]}...") # Optional preview
        print("-" * 20)

if __name__ == "__main__":
    main()

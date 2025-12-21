# server.py
from fastmcp import FastMCP
import search

import requests

mcp = FastMCP("Demo 🚀")

# Initialize search index
index = search.initialize_index()

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def _get_page_content(url: str) -> str:
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    return response.text

@mcp.tool
def get_page_content(url: str) -> str:
    """Get the content of a web page in markdown using r.jina.ai"""
    return _get_page_content(url)

@mcp.tool
def search_fastmcp(query: str) -> str:
    """Search FastMCP documentation"""
    results = search.search(index, query)
    output = []
    for result in results:
        output.append(f"File: {result['filename']}\nContent: {result['content'][:500]}...\n---")
    return "\n".join(output)

if __name__ == "__main__":
    mcp.run()
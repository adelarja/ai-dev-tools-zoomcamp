# server.py
from fastmcp import FastMCP

import requests

mcp = FastMCP("Demo 🚀")

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

if __name__ == "__main__":
    mcp.run()
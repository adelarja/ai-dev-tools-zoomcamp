# 03-mcp-server

This is a demo MCP server with a web scraper tool powered by `r.jina.ai`.

## Tools

- `add(a: int, b: int) -> int`: Add two numbers.
- `get_page_content(url: str) -> str`: Get the content of a web page in markdown.

## Integration

To use this server with an MCP client (like Claude Desktop or an IDE extension), add the following configuration to your MCP settings file (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "demo-server": {
      "command": "uv",
      "args": [
        "run",
        "main.py"
      ],
      "cwd": "<PATH>/03-mcp-server"
    }
  }
}
```

Make sure to reload your client after updating the configuration.

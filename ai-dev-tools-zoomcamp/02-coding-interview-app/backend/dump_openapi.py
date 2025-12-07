import json
import sys
import os

# Add the backend directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.main import app

def dump_openapi():
    openapi_data = app.openapi()
    with open("openapi.json", "w") as f:
        json.dump(openapi_data, f, indent=2)
    print("OpenAPI spec saved to openapi.json")

if __name__ == "__main__":
    dump_openapi()

# Question 1

## First iteration

Let's implement a coding interview app using the next requisites:

The app should be able to do the following:

- Create a link and share it with candidates
- Allow everyone who connects to edit code in the code panel
- Show real-time updates to all connected users
- Support syntax highlighting for multiple languages
- Execute code safely in the browser

Use fastAPI for the backend and React + Vite for the frontend. In addition, we need postgres for db. Generate the OpenAPI Spect.

Follow the directives in AGENT.md. FYI, I already have the project into a git repo, so you don't need to create a new repo.

## Second iteration
the frontend is quite awful. could you please improve it? Furthermore It only allows to use one language (python) and the components are not well placed in the screen.

## Third iteration
I found two errors:

1. There is a comment in python: # Write your code here. The comment should change when changing the language (you don't do comments with # in javascript).

2. The output doesn't actually run the code. it only prints the same code that you write!

Could you please fix them?

# Question 2

## First iteration

OK that's good. now I need to add:
- Unit tests for the backend
- Unit tests for the frontend
- Integration tests

Create a README.md explaining how to run it.

## Second Iteration

tests/test_api.py::test_get_session
  sys:1: SAWarning: transaction already deassociated from connection

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_api.py::test_get_session - RuntimeError: Task <Task pending name='Task-8' coro=<test_get_session() run...
=================== 1 failed, 3 passed, 2 warnings in 0.95s ====================

## Third iteration

how about the integration tests?

## Fourth iteration

how about integration tests?

don't forget to follow AGENT.md directives

# Question 4

I have verified the syntax highlighting implementation.

The application is using @monaco-editor/react, which provides built-in syntax highlighting.

I confirmed that frontend/src/pages/Interview.jsx correctly maps the language IDs:

Python: python
JavaScript: javascript
C++: cpp (This is the correct ID for Monaco Editor)
No code changes were needed as the implementation was already correct. You should see proper syntax highlighting for all supported languages when running the app.

# Question 5

I used the following approaches:

Python: I used Pyodide.
How it works: Pyodide is a port of CPython to WebAssembly (WASM). It downloads a compiled WASM binary of the Python interpreter to your browser, allowing it to execute Python code locally.
Why: It is the industry standard for running Python in the browser, supporting many scientific packages (NumPy, Pandas) out of the box.
JavaScript: I did not compile JavaScript to WASM.
How it works: I executed it natively using the browser's built-in JavaScript engine (like V8 in Chrome).
Why: Browsers already run JavaScript natively and highly optimized. Compiling JS to WASM to run in the browser (which then runs WASM) would be redundant and slower. I simply used new Function(code)() to execute the user's code string safely within the existing environment.
C++: I used JSCPP.
How it works: It is a C++ interpreter written in JavaScript.
Why: A full C++ WASM compiler (like Clang) is very heavy (~100MB+). JSCPP is lightweight and sufficient for basic algorithmic interview problems.
Java: I included CheerpJ.
How it works: It is a full JVM replacement in WebAssembly.
Limitation: It runs bytecode (.class files). Running raw source code (.java) requires a compiler (javac) in the browser, which is a more complex setup not fully implemented in this demo.

# Question 6

I used a multi-stage build with two base images:

Stage 1 (Frontend Build): node:20-slim
Used to install dependencies and build the React application.
slim variant keeps the build environment lightweight.
Stage 2 (Final Runtime): python:3.11-slim
This is the final image that runs the application.
It contains the Python runtime for FastAPI and the built static files from Stage 1.
It also copies the uv binary from ghcr.io/astral-sh/uv:latest for fast package management.





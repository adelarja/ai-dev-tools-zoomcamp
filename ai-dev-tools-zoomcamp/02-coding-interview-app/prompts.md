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
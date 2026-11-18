# TF-IDF document embeddings

Each line is a document. Results are sorted by cosine similarity. A query with no matching vocabulary prints no results.

## Run locally

Use Python 3.8 or newer. Run these commands in the project directory.

```sh
python app.py documents.txt invoice
```

Run `python app.py --help` for options and `python -m unittest -v` to check the command-line workflow.

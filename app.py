import argparse
import math
import re
from collections import Counter
from pathlib import Path


def tokens(text):
    return re.findall(r"\w+", text.casefold())


def rank(documents, query):
    frequency = Counter(term for doc in documents for term in set(tokens(doc)))
    idf = {term: 1 + math.log((1+len(documents))/(1+count)) for term, count in frequency.items()}

    def vector(text):
        weights = {t: n*idf[t] for t, n in Counter(tokens(text)).items() if t in idf}
        norm = math.sqrt(sum(w*w for w in weights.values()))
        return {t: w/norm for t, w in weights.items()}

    q = vector(query)
    results = []
    for doc in documents:
        score = sum(q.get(t, 0)*w for t, w in vector(doc).items())
        if score > 0:
            results.append((score, doc))
    return sorted(results, key=lambda row: -row[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find text using TF-IDF and cosine similarity.")
    parser.add_argument("documents", type=Path)
    parser.add_argument("query")
    args = parser.parse_args()
    try:
        docs = args.documents.read_text(encoding="utf-8").splitlines()
    except (ValueError, OSError) as error:
        parser.error(str(error))
    for score, doc in rank(docs, args.query):
        print(f"{score:.4f}\t{doc}")

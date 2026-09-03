# test_threshold.py — run once, delete after
from rag import db

test_questions = [
    "What courses do you offer?",       # currently failing — should be relevant
    "what is python course fee",         # currently working — should be relevant
    "What is the capital of France?",    # should be irrelevant
]


for q in test_questions:
    print(f"\nQ: {q}")
    for doc, score in db.similarity_search_with_score(q, k=3):
        print(f"  score={score:.3f} | {doc.page_content[:60]}...")
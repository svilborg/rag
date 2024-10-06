import argparse
import pprint
from transformers import pipeline
from qdrant import Qdrant

def search_question(question):
    
    result = Qdrant().query(
        collection_name="products",
        query_text=question,
        limit=1
    )

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search a collection based on a question")
    parser.add_argument("question", type=str, help="The question to search for")

    args = parser.parse_args()
    
    question = args.question
    collections = search_question(question)

    docs = [doc.document for doc in collections] 

    context='products '.join(docs)
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    summary = summarizer(context, max_length=130, min_length=30, do_sample=False)

    print('\n')
    print(summary[0]['summary_text'])


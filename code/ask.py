import argparse
import pprint
import torch
from transformers import pipeline
from qdrant import Qdrant

def get_context(question):
    
    result = Qdrant().query(
        collection_name="products",
        query_text=question
    )

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search a collection based on a question")
    parser.add_argument("question", type=str, help="The question to search for")

    args = parser.parse_args()
    
    
    question = args.question
    collections = get_context(question)

    docs = [doc.document for doc in collections] 

    context='\n- product ' + '\n- product '.join(docs)
    
    # pprint.pp(context)

    pipe = pipeline(
        "text-generation", 
        model="TinyLlama/TinyLlama-1.1B-Chat-v0.6", 
        torch_dtype=torch.bfloat16, 
        device_map="auto",
        return_full_text=False,
        )

    messages = [
        {
            "role": "user",
            "content": """Using this list of products, give a comprehensive answer to the question.:
    ---
    {context}
    ---

    Question: {question}""",
        },
    ]

    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    final_prompt = prompt.format(question=question, context=context)

    outputs = pipe(final_prompt, max_new_tokens=256, do_sample=True, temperature=1, top_k=50, top_p=0.95)

    print(outputs[0]["generated_text"])



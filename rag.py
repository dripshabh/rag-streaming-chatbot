import anthropic
import chromadb
import os
from dotenv import load_dotenv
from utils import embedding_function

load_dotenv()

"""
This function generates a response using the Claude API
"""
Claude_API_Key = os.getenv("CLAUDE_API_KEY")

def rag_chain_of_thought_response(query, chroma_client, client):
    context = get_rag_context(query, chroma_client)
    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=20000,
        thinking={"type": "enabled", "budget_tokens": 16000},
        messages=[{"role": "user", "content": f"query: {query}. context: {context}"}]
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                if event.delta.type == "thinking_delta":
                    yield event.delta.thinking
                elif event.delta.type == "text_delta":
                    yield event.delta.text


def get_rag_context(query, chroma_client, num_docs=3):
    collection = chroma_client.get_collection(name="policy_db", embedding_function=embedding_function)
    results = collection.query(
        query_texts=[query],
        n_results=num_docs
    )
    documents = results['documents'][0] if results['documents'] else []
    return "\n\n".join(documents)

def main():
    chroma_client = chromadb.PersistentClient(path="chroma_db")

    query = "What are the reasons to get a total knee arthroplasty?"
    rag_chain_of_thought_response(query, chroma_client)

if __name__ == "__main__":
    main()
"""
This file is used to create a vector database for the chatbot.
"""

import chromadb
import anthropic
import PyPDF2
import os
from utils import embedding_function
from dotenv import load_dotenv

load_dotenv()

Claude_API_Key = os.getenv("CLAUDE_API_KEY")

client = anthropic.Anthropic(api_key=Claude_API_Key)

def main():
    policy_names = ["Knee-Arthroplasty-Adults.pdf"]
    collection = chromadb.PersistentClient(path="chroma_db").get_or_create_collection("policy_db", embedding_function=embedding_function)
    for policy_name in policy_names:
        policy_text = extract_pdf_text("policies/" + policy_name)
        chunks = chunk_policy(policy_text, 1000)
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"policy_name": policy_name}],
                ids=[str(i)]
            )
        print(f"Added {len(chunks)} chunks for {policy_name}")
    print("Database updated successfully")

def load_policy(policy_name):
    with open(policy_name, 'r') as file:
        policy_text = file.read()
    return policy_text

def chunk_policy(policy_text, chunk_size):
    chunks = [ policy_text[i:i+chunk_size] for i in range(0, len(policy_text), chunk_size) ]
    return chunks

def extract_pdf_text(policy_name):
    with open(policy_name, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
    return text

if __name__ == "__main__":
    main()
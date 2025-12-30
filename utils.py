from chromadb.utils import embedding_functions

def get_embedding_function():
    # Use default embedding function - works out of the box, no installation needed
    return embedding_functions.DefaultEmbeddingFunction()

# Export embedding_function for use in update_database.py
embedding_function = get_embedding_function()

def embed_text(text):
    response = anthropic
    return response
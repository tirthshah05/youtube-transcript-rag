import faiss
from embedding import encode_text


def build_index(embeddings):
    """
    Builds a FAISS index from the embeddings.

    Args:
        embeddings (numpy.ndarray): Shape (num_chunks, embedding_dimension)

    Returns:
        faiss.IndexFlatL2: FAISS index containing all embeddings.
    """
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def retrieve(index, question, chunks, k=3):
    """
    Retrieves the top-k most relevant chunks for a user question.

    Args:
        index (faiss.IndexFlatL2): FAISS index.
        question (str): User's question.
        chunks (list[str]): Original transcript chunks.
        k (int): Number of relevant chunks to retrieve.

    Returns:
        list[str]: Top-k relevant transcript chunks.
    """

    # Convert question into embedding
    question_embedding = encode_text(question)

    # FAISS expects a 2D array (1, embedding_dimension)
    question_embedding = question_embedding.reshape(1, -1)

    # Search the FAISS index
    distances, indices = index.search(question_embedding, k)

    # Retrieve corresponding chunks
    retrieved_chunks = []

    for i in indices[0]:
        retrieved_chunks.append(chunks[i])

    return retrieved_chunks
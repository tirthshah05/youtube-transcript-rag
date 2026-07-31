def create_chunks(transcript):
    words = transcript.split()

    chunks = []

    chunk_size = 200
    overlap = 50
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        current_chunk = words[i:i + chunk_size]
        chunk = " ".join(current_chunk)
        chunks.append(chunk)

    return chunks
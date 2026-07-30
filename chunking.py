def create_chunks(transcript):
    chunks = []

    chunk_size = 20
    overlap = 5
    step = chunk_size - overlap

    for i in range(0, len(transcript), step):

        current_chunk = transcript[i:i + chunk_size]

        text = []

        for snippet in current_chunk:
            text.append(snippet.text)

        chunk = "\n".join(text)

        chunks.append(chunk)

    return chunks
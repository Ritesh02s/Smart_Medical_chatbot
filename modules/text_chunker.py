def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    i = 0

    while i < len(text):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

        i += chunk_size - overlap

    return chunks
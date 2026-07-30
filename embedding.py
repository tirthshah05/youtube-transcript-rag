import streamlit as st


@st.cache_resource(show_spinner=False)
def load_embedding_model():

    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )


def encode_text(text):

    model = load_embedding_model()

    embeddings = model.encode(
        text,
        convert_to_numpy=True
    )

    return embeddings
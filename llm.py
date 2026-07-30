import os
import streamlit as st

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


@st.cache_resource(show_spinner=False)
def get_client():
    return genai.Client(api_key=api_key)


client = get_client()


def generate_answer(question, retrieved_chunks, chat_history):

    context = "\n\n".join(retrieved_chunks)

    history = ""

    for message in chat_history:
        history += f"{message['role'].capitalize()}: {message['content']}\n"

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided transcript context.

Reply in the same language as the user's latest question.

Use the previous conversation ONLY to understand follow-up questions.

Do not invent information that is not present in the transcript context.

If the answer cannot be found in the transcript context, reply:

"I couldn't find the answer in the provided transcript."

-------------------------

Previous Conversation:

{history}

-------------------------

Transcript Context:

{context}

-------------------------

Current Question:

{question}
"""

    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

    return response.text
import requests
import streamlit as st


@st.cache_data(show_spinner=False, ttl=3600)
def get_video_meta(video_id: str) -> dict:
    """
    Fetches title/author/thumbnail for a video using YouTube's public
    oEmbed endpoint (no API key required). Falls back to a generic
    thumbnail URL if the request fails.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    try:
        response = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": url, "format": "json"},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        return {
            "title": data.get("title", "Untitled video"),
            "author": data.get("author_name", ""),
            "thumbnail": data.get("thumbnail_url", thumbnail),
        }

    except Exception:
        return {
            "title": "Untitled video",
            "author": "",
            "thumbnail": thumbnail,
        }

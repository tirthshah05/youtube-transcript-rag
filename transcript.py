import os

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from youtube_transcript_api.proxies import WebshareProxyConfig
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):

    parsed_url = urlparse(url)

    if parsed_url.netloc == "www.youtube.com":

        query = parse_qs(parsed_url.query)

        return query["v"][0]

    elif parsed_url.netloc == "youtu.be":

        return parsed_url.path.strip("/")

    else:

        raise ValueError("Invalid YouTube URL")


def _get_api_client():
    """
    Builds the YouTubeTranscriptApi client. On a cloud host (Streamlit
    Community Cloud, AWS, GCP, etc.) YouTube blocks the datacenter IP, so
    we route requests through a Webshare rotating-residential proxy if
    credentials are configured. Locally, without those env vars set, it
    just falls back to a direct (unproxied) client.
    """
    proxy_username = os.getenv("WEBSHARE_PROXY_USERNAME")
    proxy_password = os.getenv("WEBSHARE_PROXY_PASSWORD")

    if proxy_username and proxy_password:
        return YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=proxy_username,
                proxy_password=proxy_password,
            )
        )

    return YouTubeTranscriptApi()


def get_transcript(video_id):
    ytt_api = _get_api_client()

    try:
        # Try English first
        return ytt_api.fetch(video_id, languages=["en"])

    except NoTranscriptFound:
        # If English isn't available, fetch any available transcript
        transcript_list = ytt_api.list(video_id)

        transcript = next(iter(transcript_list))

        return transcript.fetch()




















# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api._errors import NoTranscriptFound
# from urllib.parse import urlparse, parse_qs


# def extract_video_id(url):

#     parsed_url = urlparse(url)

#     if parsed_url.netloc == "www.youtube.com":

#         query = parse_qs(parsed_url.query)

#         return query["v"][0]

#     elif parsed_url.netloc == "youtu.be":

#         return parsed_url.path.strip("/")

#     else:

#         raise ValueError("Invalid YouTube URL")
    

# def get_transcript(video_id):
#     ytt_api = YouTubeTranscriptApi()

#     try:
#         # Try English first
#         return ytt_api.fetch(video_id, languages=["en"])

#     except NoTranscriptFound:
#         # If English isn't available, fetch any available transcript
#         transcript_list = ytt_api.list(video_id)

#         transcript = next(iter(transcript_list))

#         return transcript.fetch()
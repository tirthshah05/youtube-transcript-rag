import os
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv
from supadata import Supadata

load_dotenv()

client = Supadata(api_key=os.getenv("SUPADATA_API_KEY"))


def extract_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.netloc == "www.youtube.com":
        query = parse_qs(parsed_url.query)
        return query["v"][0]

    elif parsed_url.netloc == "youtu.be":
        return parsed_url.path.strip("/")

    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    response = client.transcript(
        url=video_url,
        text=True,
        mode="auto"
    )

    return response.content



















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
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
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
    

def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()

    try:
        # Try English first
        return ytt_api.fetch(video_id, languages=["en"])

    except NoTranscriptFound:
        # If English isn't available, fetch any available transcript
        transcript_list = ytt_api.list(video_id)

        transcript = next(iter(transcript_list))

        return transcript.fetch()
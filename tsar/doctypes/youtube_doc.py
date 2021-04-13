from bs4 import BeautifulSoup
from datetime import datetime
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptAvailable,
    NoTranscriptFound,
    TranscriptsDisabled,
)
from tsar.doctypes.doctype import DocType, update_dict, BASE_SCHEMA, BASE_MAPPING
from tsar.lib import parse_lib


class YoutubeDoc(DocType):
    """Doc type for youtube videos."""

    schema = {
        "publish_date": float,
    }
    schema = update_dict(schema, BASE_SCHEMA)

    index_mapping = {
        "mappings": {
            "properties": {
                "publish_date": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_second",
                },
            }
        }
    }
    index_mapping = update_dict(index_mapping, BASE_MAPPING)

    @staticmethod
    def gen_record(document_id, primary_doc, gen_links):
        """Generate record from youtube url.

        # example document_id: https://www.youtube.com/watch?v=3LtQWxhqjqI
        """
        video_id = document_id.split("v=")[-1]
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([d["text"] for d in transcript_data])
        except (NoTranscriptAvailable, NoTranscriptFound, TranscriptsDisabled) as err:
            text = "(no transcript available)"

        # get title:
        res = requests.get(document_id)
        soup = BeautifulSoup(markup=res.text, features="html.parser")
        title = soup.find("title").text
        links = []
        record = {
            "document_id": document_id,
            "document_name": title,
            "primary_doc": primary_doc,
            "document_type": YoutubeDoc,
            "content": text,
            "links": links,
        }
        return record

    @staticmethod
    def gen_search_index(record, link_content=None):
        """Generate a search index from a record."""
        document_id = record["document_id"]
        record_index = {
            "document_name": record["document_name"],
            "document_type": record["document_type"].__name__,
            "content": record["content"],
        }
        return (document_id, record_index)

    @staticmethod
    def gen_links(text):
        """Return citations found in text."""
        return []

    @staticmethod
    def gen_from_source(source_id, *source_args, **source_kwargs):
        """Return document ids from a document source (e.g. folder or query)."""
        pass

    @staticmethod
    def resolve_id(document_id):
        return document_id

    @staticmethod
    def resolve_source_id(source_id):
        return source_id

    @staticmethod
    def is_valid(document_id):
        url = requests.urllib3.util.parse_url(document_id)
        cond = bool(url.host == "www.youtube.com")
        if cond:
            return True
        else:
            return False

    @staticmethod
    def preview(record):

        preview = (
            f"{record['document_name']}\n"
            f"Preview: {record['content'][0:1200]}"
        )
        return preview

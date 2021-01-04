from tsar import doctypes
from tsar.doctypes.markdown_doc import MarkdownDoc
from tsar.doctypes.arxiv_doc import ArxivDoc
from tsar.doctypes.youtube_doc import YoutubeDoc

# list of recognized doc types
DOCTYPES = {
    ArxivDoc.__name__: ArxivDoc,
    MarkdownDoc.__name__: MarkdownDoc,
    YoutubeDoc.__name__: YoutubeDoc,
}

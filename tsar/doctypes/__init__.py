from tsar import doctypes
from tsar.doctypes.markdown_doc import MarkdownDoc
from tsar.doctypes.arxiv_doc import ArxivDoc
from tsar.doctypes.youtube_doc import YoutubeDoc
from tsar.doctypes.webpage import WebpageDoc

# list of recognized doc types.  Order as most to least specific (e.g WebpageDoc occurs after YoutubeDoc, at least for now)
DOCTYPES = {
    ArxivDoc.__name__: ArxivDoc,
    MarkdownDoc.__name__: MarkdownDoc,
    YoutubeDoc.__name__: YoutubeDoc,
    WebpageDoc.__name__: WebpageDoc,
}

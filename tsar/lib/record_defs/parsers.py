"""
Parsers and higher-level parsing functionality.

Parsers map source document to a dict for BASE_SCHEMA, e.g.:

    {"title": doc_title, "body": doc_text} = parser(document)  

- multiple parsers may exist for a given file type
- RecordDefs are used to convert documents into `records` of fixed schema; this additional layer of flexibility permits
generating record types of uniform schema for different docs even if the parser keys are not identical. 

An example:
`{"title": "file1.md", "body": "file1_text", "keywords": ['key1', 'key2'] } = text_parser(file1.md)`
`{"title": "file1.md", "body": "file1_text", "classes": ["c1", "c2"], funcs: ["f1"]} = python_parser(file1.py)`
`record_schema: ["title": str, "body": str, "keywords": set]`

`MyRecordDef` pseudocode: 
if doc_type is text:
    record = text_parser("record_id")
if doc_type is python:
    record = python_parser("record_id")
    record["keywords"] = set(record["classes"]) + set(record["funcs"])
    del record["classes"]
    dle record["funcs"]
"""
import os
import arxiv
import tldextract
import urllib
from tsar.lib.record_defs import parse_lib

# documents that can be inferred and parsed:
PARSABLE_DOC_TYPES = {
    "text",
    "python",
    "markdown",
    "arxiv",
}

# extension -> type map for text files
TEXTFILE_DOCTYPE_MAP = {
    ".txt": "text",
    ".py": "python",
    ".md": "markdown",
}

# domain -> type map for urls when possible:
URL_DOCTYPE_MAP = {
    "arxiv": "arxiv",
}


def infer_type(document_id):
    """Infer the document type based on the document_id (filepath, url, etc).
    
    used to parse files when type is not indicated, e.g. markdown files.
    """
    extension = os.path.splitext(document_id)[-1]
    extract = tldextract.TLDExtract()
    domain = extract(document_id).domain 
    
    if extension in TEXTFILE_DOCTYPE_MAP.keys():
        doc_type = TEXTFILE_DOCTYPE_MAP[extension]
    elif document_id.startswith("http") and domain in URL_DOCTYPE_MAP.keys(): 
        doc_type = URL_DOCTYPE_MAP[domain]
    else:
        doc_type = "unknown_type"
    return doc_type

def parse_textfile(path, source_path=None):
    """Generic parser for text file on host.
    Relative paths resolved to same dir as source_path
    """
    file_path = parse_lib.resolve_path(path, source_path=source_path)

    content = parse_lib.return_file_contents(file_path)    
    file_info = parse_lib.file_meta_data(file_path)
    document_dict = {
        "record_id": file_path,
        "content": content,
    }
    document_dict = {**document_dict, **file_info}
    document_dict["links"] = parse_lib.return_links(content)
    return document_dict


def parse_arxiv_url(arxiv_url):
    """Generate content for arxiv paper.

    # example doc_id: https://arxiv.org/abs/1810.04805
    ref: https://arxiv.org/help/api/user-manual#_calling_the_api
    # api url = 'http://export.arxiv.org/api/query?id_list=1311.5600'
    """
    # see https://arxiv.org/help/arxiv_identifier
    paper_id = arxiv_url.split("abs/")[-1]
    record_dict = arxiv.query(id_list=[paper_id])[-1]
    return record_dict

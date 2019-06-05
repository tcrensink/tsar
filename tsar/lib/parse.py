"""
Elasticsearch ingests json representation of a document. Each parser defines a mapping from a (human) document to json.

Glorious future:
write function factory for creating custom parsers.
"""
import os
import json

def wiki_page(path):
    """parse a wiki page (.md) into elasticsearch ingestible json
    """
    with open(path) as fp:
        text = fp.read()
    json_doc = json.dumps({'body': text})
    return json_doc


def gen_docs(path, parser, extension):
    """find all files with extension, return as
    docs of doc_type
    """
    docs = []
    for root, subdirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(extension):
                file_path = os.path.join(root, file)
                doc = parser(file_path)
                docs.append((file_path, doc))
    return docs


# example: https://github.com/elastic/elasticsearch-py/blob/master/example/load.py

# def parse_commits(head, name):
#     """
#     Go through the git repository log and generate a document per commit
#     containing all the metadata.
#     """
#     for commit in head.traverse():
#         yield {
#             "_id": commit.hexsha,
#             "repository": name,
#             "committed_date": datetime.fromtimestamp(commit.committed_date),
#             "committer": {
#                 "name": commit.committer.name,
#                 "email": commit.committer.email,
#             },
#             "authored_date": datetime.fromtimestamp(commit.authored_date),
#             "author": {"name": commit.author.name, "email": commit.author.email},
#             "description": commit.message,
#             "parent_shas": [p.hexsha for p in commit.parents],
#             # we only care about the filenames, not the per-file stats
#             "files": list(commit.stats.files),
#             "stats": commit.stats.total,
#         }

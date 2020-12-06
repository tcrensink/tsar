from tsar.doctypes.markdown_doc import MarkdownDoc

SOURCE1_MARKDOWN_DOC_RECORD = {
    "document_id": "/Users/trensink/git/mbp16_backup/git/my_repos/tsar/tests/fixtures/source_path1/source1_doc.md",
    "document_name": "/Users/trensink/git/mbp16_backup/git/my_repos/tsar/tests/fixtures/source_path1/source1_doc.md",
    "primary_doc": True,
    "document_type": MarkdownDoc,
    "content": "This is the 'source1' markdown file with some content for parsing/testing.\n\n# links\nbare links\n- ../source_path2/source2_doc.md\n- https://arxiv.org/abs/1906.03926\n\nmarkdown-style links\n\n- [rel link to source2](../source_path2/source2_doc.md)\n- [external link](https://arxiv.org/abs/1906.03926)\n\n# Formatting\n\nlist:\n- get milk\n- *dont* get soda\n- get eggs\n\n**bold item**\n*italic item*\n\n## subheading\nsubheading text\n### subsubheading\nsubsubheading text\n",
    "links": [
        "/Users/trensink/git/mbp16_backup/git/my_repos/tsar/tests/fixtures/source_path2/source2_doc.md",
        "https://arxiv.org/abs/1906.03926",
    ],
}

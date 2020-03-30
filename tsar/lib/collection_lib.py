"""This module contains collection-level functions, e.g. tf/idf keyword generation and document similarity measures."""
import spacy
import pandas as pd
from itertools import combinations
from cachetools import cached

SPACY_MODELS = ["en_core_web_sm", "en_core_web_lg"]


@cached(cache={})
def return_spacy_model(model="en_core_web_lg"):
    nlp = spacy.load(model)
    return nlp


def similarity_doc2vec(doc1, doc2, spacy_model):
    """Calculate (cosine) similarity of doc1, doc2."""
    doc1 = spacy_model(doc1)
    doc2 = spacy_model(doc2)
    score = doc1.similarity(doc2)
    return score


def df_doc_pairs(df_records, text_col):
    """Create df record_id pairs."""
    df_records.index.name = "record_id"
    df_records = df_records[["record_id", text_col]].reset_index(drop=True)
    record_pairs = combinations(df_records.index.values, 2)
    df_pairs = pd.DataFrame(record_pairs, columns=["row_id1", "row_id2"])

    df_doc1 = df_records.loc[df_pairs.row_id1].reset_index(drop=True)
    df_doc1 = df_doc1.rename(
        columns={"record_id": "record_id_1", text_col: f"{text_col}_1"}
    )
    df_doc2 = df_records.loc[df_pairs.row_id2].reset_index(drop=True)
    df_doc2 = df_doc2.rename(
        columns={"record_id": "record_id_2", text_col: f"{text_col}_2"}
    )
    df_docs = pd.concat([df_doc1, df_doc2], axis=1)
    return df_docs


def run_spacy_pipeline(docs, spacy_model, disable=("parser", "ner")):
    """Run spacy pipeline on list of docs.
    Excludes expensive bits not needed for cosine similarity.
    """

    results = [doc for doc in spacy_model.pipe(docs, disable=disable)]
    return results


if __name__ == "__main__":
    """standalone example for calculating the similarity of arxiv papers."""
    from tsar.lib.collection import Collection

    coll = Collection("arxiv")
    df = coll.df

    print("loading spacy word2vec model")
    spacy_model = return_spacy_model()
    df["spacy_docs"] = run_spacy_pipeline(
        df.record_summary.values, spacy_model=spacy_model
    )

    df_pairs_original = df_doc_pairs(df_records=df, text_col="spacy_docs")
    df_pairs = df_pairs_original.sample(n=100000)

    df_pairs["similarity"] = df_pairs.apply(
        lambda x: x.spacy_docs_1.similarity(x.spacy_docs_2), axis=1
    )

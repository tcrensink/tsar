"""Test classes in tsar.lib.collection.

Included tests:
- Data creation, deletion, record addition/removal
- Index creation, deletion, record addition/removal
- Collection creation, deletion, record addition/removal

Todo:
- use pytest fixtures for tmp folders, files, artifacts, and exection order:
https://docs.pytest.org/en/latest/tmpdir.html#the-tmpdir-factory-fixture
"""
import os
from pathlib import Path
import pandas as pd
from tsar.lib.collection import Data, Collection
from tsar.lib.record_defs.wiki_record import WikiRecord
from tsar.lib.search import Client, Server
from tsar import HOST_TESTS_FOLDER

TEST_COLLECTIONS_FOLDER = "/tmp/test_Collections/"
TEST_DATA_FOLDER = "/tmp/test_Data/"
TEST_COLLECTION_NAME = "test_collection"
TEST_DB_META_PATH = TEST_COLLECTIONS_FOLDER + "meta_db.pkl"
FIXTURES_FOLDER = os.path.join(HOST_TESTS_FOLDER, "fixtures")
WIKI_RECORD_ID = os.path.join(FIXTURES_FOLDER, "wiki_doc.md")
TEST_INDEX = "test_index"
Server().start()


def test_data_new():
    """test creation of Data object."""
    data = Data.new(
        collection_name=TEST_COLLECTION_NAME,
        RecordDef=WikiRecord,
        folder=TEST_DATA_FOLDER,
    )
    df_saved = pd.read_pickle(
        os.path.join(TEST_DATA_FOLDER, TEST_COLLECTION_NAME, "records.pkl")
    )
    assert df_saved.equals(data.df)


def test_data_add_record():
    """Add a data record, assert that:

    - the record_id is in the index
    - the record keys and df columns are identical
    """
    data = Data(collection=TEST_COLLECTION_NAME, folder=TEST_DATA_FOLDER)
    record = WikiRecord.gen_record(path=WIKI_RECORD_ID)
    data.update_record(record)
    data.write_db()

    path = str(Path(WIKI_RECORD_ID).resolve())
    assert path in data.df.index
    assert set(record.keys()) == set(data.df.columns)


def test_data_rm_record():
    """Verify remove added record."""
    data = Data(collection=TEST_COLLECTION_NAME, folder=TEST_DATA_FOLDER)
    init_num_records = data.df.shape[0]
    data.rm_record(WIKI_RECORD_ID)
    num_records = data.df.shape[0]
    assert init_num_records - 1 == num_records


def test_data_drop():
    """test deletion of Data objects"""
    Data.drop(collection_name=TEST_COLLECTION_NAME, folder=TEST_DATA_FOLDER)
    db_path = os.path.join(TEST_DATA_FOLDER, TEST_COLLECTION_NAME, "records.pkl")
    assert not os.path.exists(db_path)


def test_client_index_new():
    """Test search index creation"""
    client = Client()
    res = client.new_index(collection_name=TEST_INDEX, mapping=WikiRecord.index_mapping)
    res.raise_for_status()
    assert res.status_code == 200


def test_client_index_record():
    """Test search index creation."""

    record = WikiRecord.gen_record(WIKI_RECORD_ID)
    (record_id, record_index) = WikiRecord.gen_record_index(record)

    client = Client()
    res = client.index_record(
        record_id=record_id, record_index=record_index, collection_name=TEST_INDEX,
    )
    res.raise_for_status()
    assert res.status_code == 201


def test_client_rm_record():
    """Test search index creation."""

    client = Client()
    res = client.delete_record(record_id=WIKI_RECORD_ID, collection_name=TEST_INDEX)
    res.raise_for_status()
    assert res.status_code == 200


def test_client_index_drop():
    """Test search index creation."""
    client = Client()
    res = client.drop_index(collection_name=TEST_INDEX,)
    res.raise_for_status()
    assert res.status_code == 200


def test_collection_new():
    """test collection creation."""
    Collection.db_path = TEST_DB_META_PATH
    Collection.create_db_meta()
    # Collection.db_meta = pd.read_pickle(TEST_DB_META_PATH)
    coll = Collection.new(
        collection_name=TEST_COLLECTION_NAME,
        RecordDef=WikiRecord,
        folder=TEST_COLLECTIONS_FOLDER,
    )
    coll_db = pd.read_pickle(TEST_DB_META_PATH)
    assert coll_db.equals(coll.db_meta())


def test_collection_init():
    """test adding document to collection."""
    Collection.db_path = TEST_DB_META_PATH
    coll = Collection(
        collection_name=TEST_COLLECTION_NAME, folder=TEST_COLLECTIONS_FOLDER,
    )
    assert isinstance(coll, Collection)


def test_collection_add_document():
    """test adding document to collection."""
    coll = Collection(
        collection_name=TEST_COLLECTION_NAME, folder=TEST_COLLECTIONS_FOLDER,
    )
    num_records_init = coll.df.shape[0]
    coll.add_document(WIKI_RECORD_ID)
    num_records_final = coll.df.shape[0]
    assert num_records_init + 1 == num_records_final


def test_collection_remove_record():
    """test adding document to collection."""
    coll = Collection(
        collection_name=TEST_COLLECTION_NAME, folder=TEST_COLLECTIONS_FOLDER,
    )
    num_records_init = coll.df.shape[0]
    coll.remove_record(WIKI_RECORD_ID)
    num_records_final = coll.df.shape[0]
    assert num_records_init - 1 == num_records_final


def test_collection_drop():
    """Test deleting a collection."""
    Collection.drop(
        collection_name=TEST_COLLECTION_NAME, folder=TEST_COLLECTIONS_FOLDER,
    )
    db_meta = pd.read_pickle(TEST_DB_META_PATH)
    assert TEST_COLLECTION_NAME not in db_meta.index

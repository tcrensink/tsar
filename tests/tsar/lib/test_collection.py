import os
import pandas as pd
import pathlib
from pathlib import Path
import pytest
import tsar
from tsar.lib.collection import Data, Register, REGISTER_PATH
from tsar.lib.collection import Collection as ProdCollection
from tsar import TESTS_FOLDER, COLLECTIONS_FOLDER
from tsar.doctypes import DOCTYPES


@pytest.fixture
def COLLECTIONS_FOLDER_TEST(tmpdir):
    # create path COLLECTION_FOLDER within tmpdir.
    coll_path = pathlib.Path(COLLECTIONS_FOLDER)
    test_coll_folder = os.path.join(tmpdir, *coll_path.parts[1:])
    return test_coll_folder


@pytest.fixture
def register_path(tmp_path):
    register_path = REGISTER_PATH.lstrip("/")
    tmp_path = str(tmp_path)
    tmp_register_path = os.path.join(tmp_path, register_path)
    os.makedirs(os.path.dirname(tmp_register_path), exist_ok=True)
    return tmp_register_path


@pytest.fixture
def register(register_path):
    register = Register(path=register_path)
    return register


@pytest.fixture
def arxiv_record1():
    arxiv_record1 = {
        "authors": ["auth1", "auth2"],
        "publish_date": 1539219001,
        "document_id": "http://arxiv.org/abs/2222.2222v2",
        "document_name": "Title of some paper",
        "document_type": tsar.doctypes.arxiv_doc.ArxivDoc,
        "content": "document content goes here.",
        "links": [],
    }
    return arxiv_record1


@pytest.fixture
def arxiv_record2():
    arxiv_record2 = {
        "authors": ["auth3"],
        "publish_date": 1539219051,
        "document_id": "http://arxiv.org/abs/3333.3333v3",
        "document_name": "Title of next paper",
        "document_type": tsar.doctypes.arxiv_doc.ArxivDoc,
        "content": "other content.",
        "links": ["http://arxiv.org/abs/2222.2222v2"],
    }
    return arxiv_record2


@pytest.fixture
def records_db_fixture(arxiv_record1):
    df = pd.DataFrame([arxiv_record1])
    df = df.set_index("document_id", drop=True)
    return df


@pytest.fixture
def data(arxiv_record1):
    df = pd.DataFrame([arxiv_record1])
    df = df.set_index("document_id", drop=True)
    data = Data(df)
    return data


@pytest.fixture
def Collection(register):
    # Collection class with test register attribute
    Collection = ProdCollection
    Collection._register = register
    return Collection


def test_data_init(records_db_fixture):
    data = Data(records_db_fixture)
    assert data.df.equals(records_db_fixture)


def test_data_new(arxiv_record1):
    # assert 0
    # import IPython; IPython.embed()
    schema = pd.DataFrame(data=[arxiv_record1]).dtypes
    data = Data.new(schema)
    df = pd.DataFrame(columns=schema.keys()).set_index("document_id", drop=True)
    assert df.equals(data.df)


def test_data_read_write(tmpdir, data):
    path = str(tmpdir.join("test_db.pkl"))
    data.write(path)
    data2 = Data.read(path)
    assert data.df.equals(data2.df)


def test_data_drop(tmpdir, data):
    path = str(tmpdir.join("test_db2.pkl"))
    data.write(path)
    assert os.path.exists(path)
    Data.drop(path)
    assert not os.path.exists(path)


def test_data_update_record(arxiv_record1, arxiv_record2):
    df = pd.DataFrame(data=[arxiv_record1]).set_index("document_id", drop=True)
    data = Data(df)
    data.update_record(arxiv_record2)
    assert arxiv_record2["document_id"] in data.df.index


def test_data_return_record(arxiv_record1, data):
    doc_id = arxiv_record1.pop("document_id")
    record = data.return_record(doc_id)
    assert arxiv_record1 == record


def test_data_rm_record(data):
    doc_id = data.df.index[0]
    n_docs_init = data.df.shape[0]
    data.rm_record(doc_id)
    n_docs_after_rm = data.df.shape[0]
    assert n_docs_after_rm + 1 == n_docs_init


def test_register_init(register_path):
    # test that register file didn't exist, is created, and object has schema
    assert not os.path.exists(register_path)
    register = Register(path=register_path)
    schema = {
        "records_db_path": object,
        "config_path": object,
        "search_indices": object,
    }
    assert os.path.exists(register_path)
    assert register.schema == schema


def test_register_read_df(register):
    df = register.read_df()
    df2 = pd.read_pickle(register.path)
    assert df.equals(df2)


def test_register_add_exists(register, tmpdir):
    # add collection, verify it exists

    tmpdir = str(tmpdir)
    records_db_path = os.path.join(tmpdir, "records.pkl")
    config_path = os.path.join(tmpdir, "config.json")

    collection_record = {
        "collection_id": "test_collection",
        "records_db_path": records_db_path,
        "config_path": config_path,
        "search_indices": ["non_search_index"],
    }
    register.add(collection_record)
    assert register.exists("test_collection")


def test_drop(register, tmpdir):
    # add collection and remove it; verify it no longer exists.
    tmpdir = str(tmpdir)
    records_db_path = os.path.join(tmpdir, "records.pkl")
    config_path = os.path.join(tmpdir, "config.json")

    collection_record = {
        "collection_id": "test_collection",
        "records_db_path": records_db_path,
        "config_path": config_path,
        "search_indices": ["non_search_index"],
    }
    register.add(collection_record)
    assert register.exists("test_collection")
    register.drop("test_collection")
    assert not (register.exists("test_collection"))


def test_return_record(register, tmpdir):
    # add collection and remove it; verify it no longer exists.
    tmpdir = str(tmpdir)
    records_db_path = os.path.join(tmpdir, "records.pkl")
    config_path = os.path.join(tmpdir, "config.json")

    collection_record = {
        "collection_id": "test_collection",
        "records_db_path": records_db_path,
        "config_path": config_path,
        "search_indices": ["non_search_index"],
    }
    register.add(collection_record)
    assert register.exists("test_collection")
    record = register.return_record("test_collection")
    assert record == collection_record


def test_collection_new(Collection, COLLECTIONS_FOLDER_TEST):
    # test new collection, and second collection by same name overwites first if unregistered (dropped)
    coll = Collection.new("test", doc_types=list(DOCTYPES.values()))
    coll = Collection.new("test", doc_types=list(DOCTYPES.values()))


def test_collection_register(Collection, register, COLLECTIONS_FOLDER_TEST):
    # test unregistered collection can't be written
    coll = Collection.new("test", doc_types=list(DOCTYPES.values()))
    with pytest.raises(KeyError):
        coll.write()

    # register collection
    records_db_path = os.path.join(
        COLLECTIONS_FOLDER_TEST, coll.collection_id, "records.pkl"
    )
    config_path = os.path.join(
        COLLECTIONS_FOLDER_TEST, coll.collection_id, "config.json"
    )
    coll.register(records_db_path=records_db_path, config_path=config_path)

    # create another collection same name, but "in-memory"
    coll = Collection.new("test", doc_types=list(DOCTYPES.values()))

    # test unable to register collection of same name
    with pytest.raises(KeyError):
        coll.register(records_db_path=records_db_path, config_path=config_path)


def test_collection_write_load_drop(
    Collection, register, arxiv_record1, COLLECTIONS_FOLDER_TEST
):
    """Test register, write, load, drop operations."""
    # add doc, register, and write to disk
    coll = Collection.new("test", doc_types=list(DOCTYPES.values()))
    coll.add_document("https://arxiv.org/abs/1810.04805")
    records_db_path = os.path.join(
        COLLECTIONS_FOLDER_TEST, coll.collection_id, "records.pkl"
    )
    config_path = os.path.join(
        COLLECTIONS_FOLDER_TEST, coll.collection_id, "config.json"
    )
    coll.register(records_db_path=records_db_path, config_path=config_path)
    coll.write()

    # test assets are created
    assert os.path.exists(records_db_path)
    assert os.path.exists(config_path)
    for index_name in coll.search_indices:
        assert Collection.client.index_exists(index_name)

    # test assets loaded from disk are identical
    coll_load = Collection.load("test")
    assert coll.records_db.df.equals(coll_load.records_db.df)
    assert coll.configd == coll_load.configd

    # test that assets are removed when collection is dropped
    Collection.drop("test")
    assert not os.path.exists(records_db_path)
    assert not os.path.exists(config_path)
    for index_name in coll.search_indices:
        assert not Collection.client.index_exists(index_name)


def test_add_document_remove_record(Collection, register, arxiv_record1, arxiv_record2):

    doc_id = "https://arxiv.org/abs/1810.04805"
    coll = Collection.new("test", doc_types=list(DOCTYPES.values()))
    resolved_id = coll.doctype_resolver.resolve_id(doc_id)

    coll.add_document(resolved_id)
    assert resolved_id in coll.records_db.df.index

    coll.remove_record(resolved_id)
    assert coll.records_db.df.shape[0] == 0
    assert coll.query_records("*") == {}

import os
import time
import pytest
from tsar.lib.services import TaskManager
from tsar import tasks
from tsar.tasks import DEFAULT_SECONDS
from tsar.lib.collection import Collection, DOCTYPES
from tsar import TEST_FIXTURES_FOLDER


@pytest.fixture
def coll():
    col = Collection.new(collection_id="test", doc_types=list(DOCTYPES.values()))
    return col


@pytest.fixture
def task_manager(coll):
    task_man = TaskManager(collection=coll)
    return task_man


@pytest.fixture
def config_path(tmp_path):
    tmp_path = str(tmp_path)
    tmp_config_path = os.path.join(tmp_path, "config.json")
    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
    return tmp_config_path


def dummy_task(collection, tmp_path):
    tmp_path = os.path.join(str(tmp_path), "output.txt")
    with open(tmp_path, "a") as fp:
        fp.write(str(collection.client.summary))
    return collection.client.summary


def test_export_config(task_manager, config_path):

    task_manager.add_task(dummy_task, sched_kwargs=DEFAULT_SECONDS)
    # task_manager.start()
    init_task_dict = task_manager.tasks
    task_manager.export_config(config_path)
    # wipe tasks dict, verify same dict is recovered
    task_manager.tasks = {}
    task_manager.load_config(config_path)

    # tuple != list, so equality fails. Modified equality comparison:
    assert len(task_manager.tasks) == len(init_task_dict)
    assert init_task_dict.keys() == task_manager.tasks.keys()


def test_export_load_config(task_manager, config_path):

    task_manager.add_task(dummy_task, sched_kwargs=DEFAULT_SECONDS)
    init_task_dict = task_manager.tasks
    task_manager.export_config(config_path)
    # wipe tasks dict, verify same dict is recovered
    task_manager.tasks = {}
    task_manager.load_config(config_path)
    # tuple != list, so equality fails. Modified equality comparison:
    assert len(task_manager.tasks) == len(init_task_dict)
    assert init_task_dict.keys() == task_manager.tasks.keys()


def test_add_task(task_manager):
    # add a task to the collection
    df = task_manager.collection.records_db.df
    # no records to start with
    assert df.shape[0] == 0
    task_manager.add_task(
        tasks.add_source,
        sched_kwargs={"misfire_grace_time": 4},
        doc_type="MarkdownDoc",
        source_id=TEST_FIXTURES_FOLDER,
    )
    task_manager.start()
    time.sleep(4)
    # verify records were added
    assert df.shape[0] > 0


def test_task_job_sync(task_manager, tmp_path):
    # verify tasks/jobs remain the same on various operations
    tmp_config_path = os.path.join(str(tmp_path), "config2.json")

    return_jobs = lambda x: set([job.id for job in x.scheduler.get_jobs()])
    return_tasks = lambda x: set(x.tasks.keys())

    # empty, and adding tasks
    assert return_jobs(task_manager) == return_tasks(task_manager)
    task_manager.add_task(dummy_task, sched_kwargs=DEFAULT_SECONDS)
    task_manager.add_task(dummy_task, sched_kwargs=DEFAULT_SECONDS)
    assert return_jobs(task_manager) == return_tasks(task_manager)

    # verify tasks/jobs are all removed
    task_manager.remove_all_tasks()
    assert return_jobs(task_manager) == return_tasks(task_manager)

    # after adding tasks, saving to config, loading from config
    task_manager.add_task(dummy_task, sched_kwargs=DEFAULT_SECONDS)
    task_manager.add_task(dummy_task, sched_kwargs=DEFAULT_SECONDS)
    task_manager.start()
    task_manager.pause()
    task_manager.export_config(tmp_config_path)
    task_manager.load_config(tmp_config_path)
    task_manager.resume()
    assert return_jobs(task_manager) == return_tasks(task_manager)
    new_manager = TaskManager(task_manager.collection)
    assert return_jobs(new_manager) == return_tasks(new_manager)

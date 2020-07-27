"""Module for monitoring services, such as:
- watch folders for changed files to add to collections
- scheduled tasks, such as api queries
- collection consistency: records <-> search index
- retrain/update browse model
"""
import os
import sys
import time
from apscheduler.schedulers.background import BackgroundScheduler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import apscheduler
from datetime import datetime
import time
import os

def expensive_time():
    time.sleep(2)
    print('Current time: {}'.format(datetime.now()))


class ScheduledEvent(object):
    """Class to run scheduled events for a collection."""
    def __init__(collection):

    def source_changed(self):
        """Determine if a source has changed, or scheduled task can be skipped."""
    
    def return_modified_docs(self):
        """Determine which documents need to be updated for the scheduled event."""


def scan_folder(RecordDef):
    """Scan folder and return updated records if changed."""

class FolderWatchHandler(FileSystemEventHandler):
    """Watch folders for changes to source."""
    # def on_any_event(self, event):
    #     print("just some event...")
    def on_created(self, event):
        print("created source path:", event.src_path)
    def on_deleted(self, event):
        print("deleted source path:", event.src_path)
    def on_file_modified(self, event1, event2):
        print("modified source path:", event1.src_path)
    def on_moved(self, event):
        print(type(event))
        print(event)
        print('test moved')


if __name__ == "__main__":
    
    coll_handler = CollectionHandler()
    observer = Observer()
    observer.schedule(coll_handler, path='./', recursive=True)
    observer.start()

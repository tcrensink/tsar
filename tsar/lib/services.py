"""Module for scheduled background services."""
import sys
import time
import logging
from logging.handlers import SysLogHandler
import apscheduler
from subprocess import call
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from datetime import datetime

"""
Scheduled tasks:

* watch folder associated with collection, add records based on pattern (every 3 sec?)
- clean/update index (low priority for scheduled task)
- pull records from a Catelogue (e.g., scheduled query/api calls, backfill)
- scan records for retraining association model
-

Time intervals: S seconds, M minutes, D days

Other Requirements:
- start in background as daemon; record pids in tmp file
- allow stop by new process
- monitoring to know if it's running
- reconnect?  later...


# define how to create apscheduled tasks; write class if needed (remember it's already a class?)
-> use BackgroundScheduler (or asynciosscheduler).  This will run in daemon, so shouldn't interfere with main proc
-> daemon is at app level (expose single daemon), but schedulers are at collection level.  Add scheduled services to daemon.

ideal:
- scheduled task is assigned/defined by collection
- daemon (single, easier to manage) can add scheduled tasks via daemon.add_task() or something
- daemon lives/dies at app level, scheduled tasks are appended from each collection when app is instantiated
- how does teardown work?  Maybe save pids to file, remove them if needed.  This is a "nice to have"

ok this is the usage pattern:
- daemon is instantiated with app.  At run time, it binds all scheduled jobs from all collections to run method
- apscheduled jobs are bound to collections.  Scheduled jobs may be associated with RecordDefs which are added to scheduled jobs of collections (?)

# write needed code
# test functionality
# profit $$$
"""


def test_func():
    path = os.path.abspath("./daemon_test")
    print("Printing to :", path)
    call(
        "echo 'scheduler called at: {}' >> {}".format(datetime.now(), path),
        # "echo running.. >> {}".format(path),
        shell=True,
    )
    print("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))


if __name__ == "__main__":

    scheduler = BackgroundScheduler()
    # scheduler.add_job(tick, "interval", seconds=3)
    scheduler.add_job(test_func, "interval", seconds=1)

    scheduler.start()
    time.sleep(10)
    scheduler.pause()

    # time.sleep(10)
    # daemon.stop()
    # time.sleep(10)

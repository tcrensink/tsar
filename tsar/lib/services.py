"""Module for monitoring services, such as:
- watch folders for changed files to add to collections
- scheduled tasks, such as api queries
- collection consistency: records <-> search index
- retrain/update browse model
"""
from functools import partial
import inspect
import json
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import os
import importlib
from tsar import tasks
from tsar.tasks import bind_func


class TaskManager(object):
    def __init__(self, collection, scheduler=None):
        if scheduler is None:
            scheduler = BackgroundScheduler()
        self.scheduler = scheduler
        self.collection = collection

        # bind self.tasks to collection.configd["tasks"]
        if "tasks" not in self.collection.configd:
            self.collection.configd["tasks"] = {}

        self.tasks = self.collection.configd["tasks"]
        self.schedule_tasks()

    @property
    def state(self):
        return self.scheduler.state

    def scheduled_tasks(self):
        return self.scheduler.get_jobs()

    def pause(self):
        self.scheduler.pause()

    def start(self):
        self.scheduler.start()

    def resume(self):
        self.scheduler.resume()

    def load_config(self, config_file):
        """Load config from json file."""
        if self.scheduler.state == 1:
            raise RuntimeError("Scheduler can't be running when loading a new config")
        self.remove_all_tasks()
        with open(config_file) as fp:
            self.tasks = json.load(fp)
        self.schedule_tasks()

    def export_config(self, file_path):
        """Export config to file_path as json."""
        with open(file_path, mode="w") as fp:
            json.dump(self.tasks, fp)

    def schedule_task(self, task_id):
        """Add task to scheduler."""
        task = self.tasks[task_id]
        module = importlib.import_module(task["module"])
        func = getattr(module, task["func"])
        task_func = bind_func(
            self.collection, func, *task["func_args"], **task["func_kwargs"]
        )
        self.scheduler.add_job(
            id=task_id,
            name=func.__name__,
            func=task_func,
            args=task["func_args"],
            kwargs=task["func_kwargs"],
            *task["sched_args"],
            **task["sched_kwargs"],
        )

    def schedule_tasks(self):
        """Schedule all tasks from config."""
        for task_id in self.tasks.keys():
            self.schedule_task(task_id)

    def add_task(
        self, func, sched_args=(), sched_kwargs={}, *func_args, **func_kwargs,
    ):
        """Add task to task config dict.  All arguments must be serializable."""
        # record is constructed from passed arguments.
        task_func = bind_func(self.collection, func, *func_args, **func_kwargs)
        job = self.scheduler.add_job(
            name=func.__name__,
            func=task_func,
            *sched_args,
            **sched_kwargs,
            args=func_args,
            kwargs=func_kwargs,
        )
        self.tasks[job.id] = {
            "module": inspect.getmodule(func).__name__,
            "func": func.__name__,
            "sched_args": sched_args,
            "sched_kwargs": sched_kwargs,
            "func_args": func_args,
            "func_kwargs": func_kwargs,
        }

    def remove_task(self, task_id):
        self.scheduler.remove_job(job_id=task_id)
        del self.tasks[task_id]

    def remove_all_tasks(self):
        """Modify in place so it stays bound with collection config."""
        self.scheduler.remove_all_jobs()
        self.tasks.clear()

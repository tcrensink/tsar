"""
Module of "task" functions that operate on a collection.

Requirements:
- first arg is `collection` object
- args, kwargs are json serializable
"""
from functools import partial
import json
from tsar.doctypes import DOCTYPES
from tsar.lib.collection import Collection

# some default kwargs
DEFAULT_SECONDS = {"trigger": "interval", "seconds": 5}
DEFAULT_MINUTE = {"trigger": "interval", "seconds": 60}
DEFAULT_HOUR = {"trigger": "interval", "seconds": 60 * 60}


def bind_func(collection, func, *func_args, **func_kwargs):
    """Return partial function bound to collection."""
    func = partial(func, collection=collection, *func_args, **func_kwargs)
    return func


def add_source(collection, doc_type, source_id, *source_args, **source_kwargs):
    """adds source to collection_config."""
    source_id = DOCTYPES[doc_type].resolve_source_id(source_id)
    Collection.add_from_source(
        collection,
        doc_type=doc_type,
        source_id=source_id,
        *source_args,
        **source_kwargs,
    )

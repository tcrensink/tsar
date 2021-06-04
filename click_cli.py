#!/usr/bin/env python3
"""
host-side terminal client for handling tsar requests.

(outdated)
CLI summary:
- tsar ls                         # prints collection, record_type summaries, current collection

- tsar new --name --record_type   # create a new collection with record type
- tsar record_types               # print available record types
- tsar <coll>                     # open app search interface for that collection
- tsar <coll> info                # prints summary info of collection
- tsar <coll> drop                # drops the collection
- tsar <coll> add <record_id>     # add record_id to collection
- tsar <coll> rm <record_id>      # rm record_id from collection
- tsar kill                       # kill tsar
- tsar restart                    # restart tsar
"""
import requests
import click
import os

PORT = 8137
BASE_URL = f"http://0.0.0.0:{PORT}"

RUN_PATH = os.path.realpath(__file__)
RUN_DIR = os.path.dirname(RUN_PATH)


# this group allows for sub-commands
@click.group()
def cli():
    pass


@cli.command(help="Verify connection to app")
def test():
    res = requests.get(url=f"http://0.0.0.0:{PORT}")
    click.echo(res.text)


@cli.command(help="Summary of existing collections")
@click.argument("collection_id", default="")
def ls(collection_id):

    if collection_id:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/collection_info/{collection_id}")
    else:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/collection_info")
    click.echo(res.json())
    click.echo()


@cli.command(help="List of recognized document types")
@click.argument("collection_id", default="")
def doctypes(collection_id):

    if collection_id:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/doctypes/{collection_id}")
    else:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/doctypes")
    click.echo(res.json())
    click.echo()


@cli.command(help="Add a new document to a collection")
@click.argument("collection_id")
@click.argument("document_id")
def add(collection_id, document_id):
    res = requests.post(
        url=f"http://0.0.0.0:8137/add_doc/{collection_id}",
        json={"document_id": document_id},
    )
    click.echo(res.json())
    click.echo()


@cli.command(help="Remove a document from a collection")
@click.argument("collection_id")
@click.argument("document_id")
def rm(collection_id, document_id):
    res = requests.post(
        url=f"http://0.0.0.0:{PORT}/rm_doc/{collection_id}",
        json={"document_id": document_id},
    )
    click.echo(res.json())
    click.echo()


@cli.command(help="Create new collection")
@click.argument("collection_id")
@click.option("--doctypes", "-d", help="comma separated list (no spaces)")
def new(collection_id, doctypes):

    if not doctypes:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/doctypes")
        doctype_list = res.json()
    else:
        doctype_list = doctypes.split(",")

    res = requests.post(
        url=f"http://0.0.0.0:{PORT}/new/{collection_id}",
        json={"collection_id": collection_id, "doctypes": doctype_list},
    )
    click.echo(res.json())
    click.echo()


@cli.command(help="Permanently drop a collection")
@click.argument("collection_id")
def drop(collection_id):

    res = requests.post(
        url="http://0.0.0.0:{PORT}/drop", json={"collection_id": collection_id}
    )
    click.echo(res.json())
    click.echo()


if __name__ == "__main__":
    cli()

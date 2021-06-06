#!/usr/bin/env python3
"""
host-side terminal client for handling tsar requests.

# TODO
- attach to running shell (debugging)

"""
import requests
import click
import os
from subprocess import run

PORT = 8137
RUN_PATH = os.path.realpath(__file__)
RUN_DIR = os.path.dirname(RUN_PATH)


@click.group()
def cli():
    # this group allows for sub-commands
    pass


@cli.command(help="Verify connection to app")
def ping():
    res = requests.get(url=f"http://0.0.0.0:{PORT}")
    click.echo(res.text)


@cli.command(help="Summary of existing collections")
@click.argument("collection_id", default="")
def ls(collection_id):

    if collection_id:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/collection_info/{collection_id}")
    else:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/collection_info")

    for info in res.json():
        title, body = info.split("\n", 1)
        click.secho(title, bold=True, fg="red")
        click.secho(body)


@cli.command(help="List of recognized document types")
@click.argument("collection_id", default="")
def doctypes(collection_id):

    if collection_id:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/doctypes/{collection_id}")
    else:
        res = requests.get(url=f"http://0.0.0.0:{PORT}/doctypes")
    click.echo(res.json())
    click.echo()


@cli.command(help="Add document to a collection")
@click.argument("collection_id")
@click.argument("document_id")
def add(collection_id, document_id):
    res = requests.post(
        url=f"http://0.0.0.0:8137/add_doc/{collection_id}",
        json={"document_id": document_id},
    )
    click.echo(res.json())
    click.echo()


@cli.command(help="Add a documents to a collection from a source")
@click.argument("collection_id")
@click.argument("doctype")
@click.argument("source_id")
def add_source(collection_id, doctype, source_id):
    res = requests.post(
        url=f"http://0.0.0.0:8137/add_source/{collection_id}",
        json={"doctype": doctype, "source_id": source_id},
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
        url=f"http://0.0.0.0:{PORT}/new",
        json={"collection_id": collection_id, "doctypes": doctype_list},
    )
    click.echo(res.json())
    click.echo()


# https://click.palletsprojects.com/en/8.0.x/options/#yes-parameters
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@cli.command(help="Permanently drop a collection")
@click.argument("collection_id")
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Permanently delete collection?",
)
def drop(collection_id):
    res = requests.post(
        url=f"http://0.0.0.0:{PORT}/drop", json={"collection_id": collection_id}
    )
    click.echo(res.json())
    click.echo()


@cli.command(help="Shut down all processes")
def shutdown():
    click.echo("shutting down...")
    res = run(f"cd {RUN_DIR} && docker compose down -v", shell=True)


@cli.command(help="Restart all processes")
def restart():
    click.echo("restarting...")
    res = run(
        f"cd {RUN_DIR} && docker compose down -v && docker compose up -d app",
        shell=True,
    )


if __name__ == "__main__":
    cli()

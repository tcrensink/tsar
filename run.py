#!/usr/bin/env python3
"""
Host CLI for sending commands to running TSAR instance in docker app.

CLI summary:
- tsar                            # open app
- tsar ls                         # prints collection, record_type summaries
- tsar new --name --record_type   # create a new collection with record type
- tsar record_types               # print available record types
- tsar <coll>                     # open app search interface for that collection
- tsar <coll> info                # prints summary info of collection
- tsar <coll> drop                # drops the collection
- tsar <coll> add <record_id>     # add record_id to collection
- tsar <coll> rm <record_id>      # rm record_id from collection
- tsar kill                       # kill tsar
- tsar restart                    # restart tsar

Syntax:
`tsar <command> <sub_command> ... <argument>`

each (sub) command is implemented in argparse as a sub_parser.
"""
import os
import time
import subprocess
import argparse
import requests

# returns container name if currently running:
NAME = "tsar"
ATTACH_CMD = f'docker attach {NAME} --detach-keys="ctrl-q"'
KILL_CMD = f"docker kill {NAME}"
CLEAR_SCREEN_CMD = 'echo -e "\033[H\033[J"'
STARTUP_TIMEOUT = 30

PORT = 8137
HOST = "0.0.0.0"
BASE_URL = f"http://{HOST}:{PORT}"

RUN_PATH = os.path.realpath(__file__)
RUN_DIR = os.path.dirname(RUN_PATH)

def container_running():
    """Return whether app container is running or not."""
    proc = subprocess.run(
        f"""docker ps -f "name={NAME}" --format '{{{{.Names}}}}'""", 
        shell=True,
        capture_output=True,
    )    
    if proc.stdout.decode().strip() == NAME:
        return True
    return False

def run_container(timeout=STARTUP_TIMEOUT):
    """Start the app docker container."""
    proc = subprocess.run(
        f'cd {RUN_DIR} && make run', 
        shell=True,
        capture_output=True,
    )  
    err_msg = proc.stderr.decode()  
    if err_msg:
        raise ValueError(err_msg)
    time.sleep(timeout)

def kill_container():
    """kill the docker container."""
    proc = subprocess.run(
        KILL_CMD, 
        shell=True,
        capture_output=True,
    )

def restart_container():
    """Restart the docker container."""
    kill_container()
    run_container()    

def attach_to_app_container():
    """Attach to a running container."""
    subprocess.run(ATTACH_CMD, shell=True)
    subprocess.run(CLEAR_SCREEN_CMD, shell=True)


def gen_collection_parser(
    collection_name,
    sub_parsers,
):
    """generate (sub) parser for a collection."""

    collection_parser = sub_parsers.add_parser(collection_name)
    coll_cmd_parser = collection_parser.add_subparsers(
        title="collection commands", 
        dest="sub_command",
    )

    rm_parser = coll_cmd_parser.add_parser("rm", help="remove record from collection")
    rm_parser.add_argument("record_id")
    add_parser = coll_cmd_parser.add_parser("add", help="add record to collection")
    add_parser.add_argument("record_id")


if __name__ == '__main__':

    # start container if it's not running
    if not container_running():
        print("starting tsar...")
        run_container(timeout=STARTUP_TIMEOUT)

    # base parser is not used directly; sub_parsers define first <command> args
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(title="commands", dest="command")

    # non-collection parsers
    sub_parsers.add_parser("", help="(No arguments) attach to running app.")
    sub_parsers.add_parser("ls", help="list collections information")
    sub_parsers.add_parser("kill", help="kill the app")
    sub_parsers.add_parser("restart", help="restart the app")

    # new collection parser
    new_collection_parser = sub_parsers.add_parser("new", help="Create a new collection.")
    new_collection_parser.add_argument("--name", help="Name of new collection", required=True)
    new_collection_parser.add_argument("--record_def", help="Record type for collection", required=True)

    # drop collection parser
    drop_collection_parser = sub_parsers.add_parser("drop", help="Drop (delete) a collection permanently.")
    drop_collection_parser.add_argument("collection_name", help="Name of collection to drop")

    # add (sub) parsers for collections
    collections = requests.get(f"{BASE_URL}/Collections").json()
    for collection in collections:
        gen_collection_parser(
            collection_name=collection,
            sub_parsers=sub_parsers,
        )

    # parse args
    args = parser.parse_args()

    # read args, execute commands
    if not args.command:
        # attach to running container
        attach_to_app_container()
    elif args.command == "ls":
        # show basic collections info
        res = requests.get(f"{BASE_URL}/Collections")
        print(res.json())
    elif args.command == "kill":
        # kill the running container
        kill_container()
    elif args.command == "restart":
        # restart the container
        restart_container()
    elif args.command == "new":
        # create a new collection
        res = requests.post(
            f"{BASE_URL}/Collections", 
            json={"collection_name": args.name, "RecordDef": args.record_def},
        )
        print("created new collection.")
    elif args.command == "drop":
        # drop a collection
        usr_input = input(f"drop collection {args.collection_name} [y/N]?")
        if usr_input.lower() == "y":
            res = requests.delete(
                f"{BASE_URL}/Collections", 
                json={"collection_name": args.collection_name},
            )
            print(f"dropped collection: {args.collection_name}")
    elif args.command in collections and args.sub_command == "add":
        # add record to a collection
        res = requests.post(
            f"{BASE_URL}/Collections/{args.command}", 
            json={"record_id": args.record_id},
        )
        print(f"added {args.record_id} to Collection: {args.command}")
    elif args.command in collections and args.sub_command == "rm":
        # rm record from a collection
        res = requests.delete(
            f"{BASE_URL}/Collections/arxiv", 
            json={"record_id": args.record_id}
        )
        print(f"Removed {args.record_id} from Collection:{args.command}.")

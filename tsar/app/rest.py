"""
RESTful server (for terminal commands from client).

The server is run in a thread in the main app process (in app.py).  The CLI
is exposed on the host machine which makes http requests.
"""
from tsar.lib.collection import Collection, DOCTYPES
from flask import Flask, jsonify, request
from flask_restful import (
    abort,
    Api,
    Resource,
)

DEBUG = False
FLASK_KWARGS = {
    "port": 8137,
    "host": "0.0.0.0",
    "debug": DEBUG,
}

# used for creating new collection; (would be better to have a collection manager)
RECORD_DEF_DICT = DOCTYPES


def return_active_screen_name(tsar_app):
    for k, v in tsar_app.screens.items():
        if v == tsar_app.state["active_screen"]:
            return k


def return_flask_app(tsar_app):
    """Return flask cli app with rest API.

    Wrapped in a function for resources to access to (in-memory) tsar_app.
    """
    app = Flask(__name__)
    @app.route('/')
    def ping():
        return 'successful tsar cli client ping.'

    api = Api(app)
    class CollectionsInfo(Resource):
        def get(self):
            """Return summary info of collections.

            example:
            res = requests.get(
                "http://0.0.0.0:8137/info",
            )
            """
            tsar_app.state["collections"]
            df["creation_date"] = df["creation_date"].dt.normalize()
            return df.to_string()

    api.add_resource(CollectionsInfo, "/info")

    class RestCollections(Resource):
        """Resource that handles Collection(s) related requests."""

        def get(self):
            """Return list of collections.

            example:
            res = requests.get(
                "http://0.0.0.0:8137/Collections",
            )
            """
            df = tsar_app.state["Collection"]
            return list(df.index)

        def post(self):
            """Create a new collection.

            example:
            res = requests.post(
                "http://0.0.0.0:8137/Collections",
                json={"collection_name": "test", "RecordDef": "ArxivRecord"},
            )
            """
            request.json["RecordDef"] = RECORD_DEF_DICT[request.json["RecordDef"]]
            coll = Collection.new(**request.json)
            active_screen_name = return_active_screen_name(tsar_app)
            tsar_app.update_state(active_screen_name)

        def delete(self):
            """Drop a collection.

            example:
            res = requests.delete(
                "http://0.0.0.0:8137/Collections",
                json={"collection_name": "test"},
            )
            """
            coll = Collection.drop(**request.json)
            active_screen_name = return_active_screen_name(tsar_app)
            tsar_app.update_state(active_screen_name)

    api.add_resource(RestCollections, "/Collections")

    class RestCollection(Resource):
        """Resource that handles Collection records."""

        def get(self, collection_name):
            """Return collection summary.

            example:
            res = requests.get("http://0.0.0.0:8137/Collections/test")
            """
            coll = Collection(collection_name=collection_name)
            return coll.summary

        def post(self, collection_name):
            """Add a record to the collection.

            example:
            res = requests.post(
                "http://0.0.0.0:8137/Collections/test",
                json={"record_id": "https://arxiv.org/abs/2008.07320"},
            )
            """
            coll = Collection(collection_name=collection_name)
            coll.add_document(request.json["record_id"])
            active_screen_name = return_active_screen_name(tsar_app)
            tsar_app.update_state(active_screen_name)

        def delete(self, collection_name):
            """Remove a record from the collection.

            example:
            res = requests.delete(
                "http://0.0.0.0:8137/Collections/test",
                json={"record_id": "https://arxiv.org/abs/2008.07320"}
            )
            """
            # request.json includes `record_id`
            coll = Collection(collection_name=collection_name)
            coll.remove_record(request.json["record_id"])
            active_screen_name = return_active_screen_name(tsar_app)
            tsar_app.update_state(active_screen_name)

    api.add_resource(RestCollection, "/Collections/<collection_name>")

    return app


if __name__ == "__main__":

    # used for debugging, but will not have access to main app objects.
    app = return_flask_app(tsar_app=None)
    app.run(**FLASK_KWARGS)

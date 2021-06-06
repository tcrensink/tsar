"""
RESTful server (for terminal commands from client).

The server is run in a thread in the main app process (in app.py).  The CLI
is exposed on the host machine which makes http requests.

Debug flow:
- start shell in docker image
- run app from cmd line: python tsar/tsar/app/app.py
- check browser/make requests from host, http://0.0.0.0:8137/
"""
from tsar.lib.collection import Collection, Register, DOCTYPES
from flask import Flask, jsonify, request

FLASK_KWARGS = {
    "port": 8137,
    "host": "0.0.0.0",
    "debug": False,
}


def return_flask_app(tsar_app):
    """Return flask cli app with rest API.

    Wrapped in a function for resources to access to (in-memory) tsar_app.
    """
    app = Flask(__name__)

    @app.route("/")
    def ping():
        return "successful connection to tsar cli server."

    @app.route("/collection_info")
    def infos():
        """Get summary information for all collections.
        ex:
        res = requests.get(url="http://0.0.0.0:8137/collection_info")
        """
        coll_info = []
        for name, coll in tsar_app.state["collections"].items():
            coll_info.append(coll.preview())
        response = jsonify(coll_info)
        return response

    @app.route("/collection_info/<collection>")
    def info(collection):
        """Get summary information for one collection.
        res = requests.get(url="http://0.0.0.0:8137/collection_info/test_collection")
        """
        coll_info = tsar_app.state["collections"][collection].preview()
        response = jsonify(coll_info)
        return response

    @app.route("/doctypes", defaults={"collection": None})
    @app.route("/doctypes/<collection>")
    def get_doctypes(collection):
        """Return record types (optionally for a specific collection)."""

        if collection is None:
            doctypes = list(DOCTYPES)
        else:
            doctype_values = tsar_app.state["collections"][collection].doc_types
            doctypes = [k for k, v in DOCTYPES.items() if v in doctype_values]
        return jsonify(doctypes)

    @app.route("/add_doc/<collection>", methods=["POST"])
    def add_doc(collection):
        """Add docuemnt to collection.

        ex:
        requests.post(
            url="http://0.0.0.0:8137/add_doc/pkb",
            json={"document_id":"https://www.youtube.com/watch?v=3UAqhSwEZxU"}
        )
        """
        data = request.json
        document_id = data["document_id"]
        collection = tsar_app.state["collections"][collection]
        try:
            collection.add_document(document_id)
            response = f"document {document_id} added to collection"
        except Exception as e:
            response = "error adding document to collection"
        return jsonify(response)

    @app.route("/rm_doc/<collection>", methods=["POST"])
    def rm_doc(collection):
        """Remove document from collection.

        ex:
        requests.post(
            url="http://0.0.0.0:8137/rm_doc/pkb",
            json={"document_id":"https://www.youtube.com/watch?v=3UAqhSwEZxU"}
        )
        """
        data = request.json
        document_id = data["document_id"]
        collection = tsar_app.state["collections"][collection]
        try:
            collection.remove_record(document_id)
            response = f"removed document: {document_id} from {collection}"
        except Exception as e:
            response = "error removing document from collection"
        return jsonify(response)

    @app.route("/new", methods=["POST"])
    def new_collection():
        """Create a new collection and register it.
        ex:
        requests.post(
            url="http://0.0.0.0:8137/new",
            json={
                "collection_id": "test_collection",
                "doctypes": ['ArxivDoc', 'MarkdownDoc', 'YoutubeDoc', 'WebpageDoc']}
        )
        """
        data = request.json
        collection_id = data["collection_id"]
        doctypes = data["doctypes"]

        try:
            coll = Collection.new(
                collection_id=collection_id, doc_types=[DOCTYPES[dt] for dt in doctypes]
            )
            coll.register()
        except:
            response = "error creating new collection."
        else:
            tsar_app.state["collections"][collection_id] = coll
            response = f"created new collection: {collection_id}"
        return jsonify(response)

    @app.route("/drop", methods=["POST"])
    def drop_collection():
        """Drop an existing collection.
        ex:
        requests.post(url="http://0.0.0.0:8137/drop", json={"collection_id": "test_collection"})
        """
        data = request.json
        collection_id = data["collection_id"]
        register = Register()

        try:
            register.drop(collection_id)
        except:
            response = "error dropping collection."
        else:
            response = f"collection was permanently dropped: {collection_id}"
        return jsonify(response)

    return app


if __name__ == "__main__":

    # used for debugging, but will not have access to main app objects.
    app = return_flask_app(tsar_app=None)

    FLASK_KWARGS["debug"] = True
    app.run(**FLASK_KWARGS)

from typing import Dict
from flask import Blueprint, request, abort
from flask.wrappers import Response
import json


kv_store_app = Blueprint("v1", "kv_store")

KV_STORE = None  # this variable will be shared across threads


def get_kv_store():

    global KV_STORE

    if KV_STORE is None:
        from storage.simple import DictionaryStorage
        from storage.facade import KvStore

        KV_STORE = KvStore([DictionaryStorage().capability])

    return KV_STORE


@kv_store_app.route("/<key>", methods=["GET"])
def get(key: str):
    store = get_kv_store()

    try:
        value = store.get(key)
        return Response(
            response=json.dumps({"value": value}),
            status=200,
            mimetype="application/json",
        )
    except KeyError:
        abort(404)


@kv_store_app.route("/", methods=["POST"])
def insert():
    data: Dict = request.json
    key, value = data["key"], data["value"]

    store = get_kv_store()

    if store.exists(key):
        return Response(
            response=json.dumps({"error": "duplicate key"}),
            status=409,
            mimetype="application/json",
        )

    store.set(key, value)

    return Response(status=200)


@kv_store_app.route("/<key>", methods=["PUT"])
def set(key: str):
    store = get_kv_store()
    data: Dict = request.json

    value = data["value"]

    store.set(key, value)

    return Response(status=200)


@kv_store_app.route("/<key>", methods=["DELETE"])
def delete(key: str):
    store = get_kv_store()
    status = store.delete(key)

    if not status:
        abort(404)

    return Response(status=200)

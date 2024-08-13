#!/usr/bin/env python3
"""
lists all doucment in a collection
"""


def list_all(mongo_collection):
    """
    list all documents in a collection
    """
    return [docs for docs in mongo_collection.find()]

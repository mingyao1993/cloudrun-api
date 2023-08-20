"""Fetch from Google Cloud datastore"""
import hashlib

from google.cloud import datastore

from config.env import app_config


class DataStoreUtils:
    """DataStore for Google cloud"""

    def __init__(self):
        self.client = datastore.Client(
            project=app_config.project_id, namespace=app_config.datastore_namespace
        )

    @staticmethod
    def _generate_hash(value: str) -> str:
        value = str(value)
        hex_value = hashlib.md5(value.encode("utf-8")).hexdigest()
        return f"{hex_value}_{value}"

    def _generate_key(self, key_id: str, kind: str) -> datastore.key.Key:
        incomplete_key = self._generate_hash(key_id)
        return self.client.key(kind, incomplete_key)

    def get_entity(self, key_id: str, kind: str) -> dict:
        key = self._generate_key(key_id=key_id, kind=kind)
        return self.client.get(key=key)

    def upsert_entity(self, key_id: str, properties: dict, kind: str) -> None:
        key = self._generate_key(key_id=key_id, kind=kind)
        entity = datastore.Entity(key=key)
        entity.update(properties)
        self.client.put(entity)

    def delete_all_entities_in_kind(self, kind: str):
        query = self.client.query(kind=kind)
        all_entities = list(query.fetch())
        for entity in all_entities:
            self.client.delete(entity.key)

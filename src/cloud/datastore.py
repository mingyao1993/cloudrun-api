import hashlib
import logging

from google.cloud import datastore

from config.env import app_config

logger = logging.getLogger(__name__)


class Datastore:
    def __init__(self):
        self.client = datastore.Client(project=app_config.project_id, namespace=app_config.datastore_namespace)

    @staticmethod
    def _generate_hash(value: str) -> str:
        value = str(value)
        hex_value = hashlib.md5(value.encode("utf-8")).hexdigest()
        return f"{hex_value}_{value}"

    def _generate_key(self, key_id: str, kind: str) -> datastore.key.Key:
        incomplete_key = self._generate_hash(key_id)
        return self.client.key(kind, incomplete_key)

    def transfer_funds(self, from_account, to_account, amount) -> None:
        kind = 'funds'
        with self.client.transaction():
            from_account = self.client.get(self._generate_key(kind=kind, key_id=from_account))
            to_account = self.client.get(self._generate_key(kind=kind, key_id=to_account))

            from_account["balance"] -= amount
            to_account["balance"] += amount

            self.client.put_multi([from_account, to_account])
        logger.info("transfer completed")


data_store = Datastore()

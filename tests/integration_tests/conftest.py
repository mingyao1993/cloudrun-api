import pytest

from config.env import app_config
from utils.data.datastore_entities import accounts
from utils.datastore import DataStoreUtils
from utils.pubsub import PubSubUtils

SOURCE_TOPIC = 'source-topic'
SOURCE_SUBSCRIPTION = 'source-subscription'
DATASTORE_KIND = 'funds'
PUSH_ENDPOINT = 'http://mloh-sandbox:8000/v1/transfer_funds'


@pytest.fixture(scope="session")
def pubsub_utils():
    return PubSubUtils(project_id=app_config.project_id)


@pytest.fixture(scope="session")
def pubsub_source_topic(pubsub_utils):
    topic_path = pubsub_utils.create_topic(topic_id=SOURCE_TOPIC)

    yield topic_path

    pubsub_utils.delete_topic(topic_path)


@pytest.fixture(scope="session")
def pubsub_source_push_subscription(pubsub_utils, pubsub_source_topic):
    subscription_path = pubsub_utils.create_push_subscription(topic_id=SOURCE_TOPIC,
                                                              subscription_id=SOURCE_SUBSCRIPTION,
                                                              push_endpoint=PUSH_ENDPOINT)

    yield subscription_path

    pubsub_utils.delete_subscription(subscription_path)


@pytest.fixture(scope="session")
def datastore_utils():
    return DataStoreUtils()


@pytest.fixture(scope="function")
def datastore_load_funds_kind(datastore_utils):
    for account in accounts:
        datastore_utils.upsert_entity(
            key_id=account['account'],
            properties=account,
            kind=DATASTORE_KIND
        )
    yield datastore_utils
    datastore_utils.delete_all_entities_in_kind(kind=DATASTORE_KIND)

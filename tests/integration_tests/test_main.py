import time


def test_main(
        pubsub_utils,
        pubsub_source_topic,
        pubsub_source_push_subscription,
        datastore_load_funds_kind

):
    REQUEST_BODY = {"from": "12345", "to": "54321", "amount": 50}
    pubsub_utils.publish_messages(topic_path=pubsub_source_topic, messages=[REQUEST_BODY])
    time.sleep(1)
    assert datastore_load_funds_kind.get_entity(key_id='12345', kind='funds') == {'account': '12345', 'balance': 50}
    assert datastore_load_funds_kind.get_entity(key_id='54321', kind='funds') == {'account': '54321', 'balance': 50}

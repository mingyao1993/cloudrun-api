import json
from typing import List

from google.cloud import pubsub_v1


class PubSubUtils:
    """Class for interacting with a PubSub emulator"""

    def __init__(self, project_id):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def create_topic(self, topic_id: str) -> str:
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        topic = self.publisher.create_topic(name=topic_path)

        print(f"Created topic: {topic.name}")

        return topic_path

    def create_pull_subscription(self, topic_id: str, subscription_id: str) -> str:
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        subscription = self.subscriber.create_subscription(name=subscription_path, topic=topic_path)

        print(f"Subscription created: {subscription}")

        return subscription_path

    def create_push_subscription(self, topic_id, subscription_id, push_endpoint) -> str:
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        push_config = pubsub_v1.types.PushConfig(push_endpoint=push_endpoint)

        subscription = self.subscriber.create_subscription(
            name=subscription_path,
            topic=topic_path,
            push_config=push_config
        )

        print(f"Push subscription created: {subscription}.")
        print(f"Endpoint for subscription is: {push_endpoint}")

        return subscription_path

    def delete_topic(self, topic_path: str) -> None:
        self.publisher.delete_topic(topic=topic_path)

        print(f"Topic deleted: {topic_path}")

    def delete_subscription(self, subscription_path: str) -> None:
        self.subscriber.delete_subscription(subscription=subscription_path)

        print(f"Subscription deleted: {subscription_path}.")

    def publish_messages(self, topic_path: str, messages: List[dict]):
        for msg in messages:
            body = json.dumps(msg).encode('utf-8')
            self.publisher.publish(topic=topic_path, data=body)

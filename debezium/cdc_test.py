from kafka import KafkaConsumer, KafkaAdminClient
from kafka.errors import TopicAuthorizationFailedError


class KafkaCon:
    def __init__(self, brokers: list) -> None:
        self.brokers = brokers
        self.admin_client = KafkaAdminClient(bootstrap_servers=brokers)

    def find_topics_with_prefix(self, prefix: str = None) -> list:
        """prefix로 시작하는 토픽을 찾습니다."""
        topic_metadata = self.admin_client.list_topics()
        if not prefix:
            return topic_metadata

        topics_with_prefix = []
        for topic in topic_metadata:
            if topic.startswith(prefix):
                topics_with_prefix.append(topic)
        return topics_with_prefix

    def get_topic_metadata(self, topic: str):
        """토픽의 메타데이터 조회를 위한 함수를 정의합니다."""
        try:
            topic_metadata = self.admin_client.describe_topics([topic])
            return topic_metadata
        except TopicAuthorizationFailedError:
            print(
                f"Topic '{topic}' does not exist or you don't have permission to access it."
            )
            return None


class MessageConsumer(KafkaCon):
    def __init__(self, brokers, topic: str) -> None:
        super().__init__(brokers)
        self.consumer = KafkaConsumer(
            topic,  # Topic to consume
            bootstrap_servers=self.brokers,
            value_deserializer=lambda x: x.decode(
                "utf-8"
            ),  # Decode message value as utf-8
            group_id="psql-cdc",  # Consumer group ID
            auto_offset_reset="earliest",  # Start consuming from earliest available message
            enable_auto_commit=True,  # Commit offsets automatically
        )

    def receive_message(self, pattern: str = None):
        if pattern:
            self.consumer.subscribe(pattern=pattern)

        try:
            for message in self.consumer:
                print(message)
        except Exception as exc:
            raise exc


# 브로커와 토픽명을 지정한다.
brokers = ["localhost:9092", "localhost:9093", "localhost:9094"]
topic = "test_checkedcrn"
cs = MessageConsumer(brokers, topic)
print(cs.find_topics_with_prefix())
print(cs.get_topic_metadata(topic))
cs.receive_message()

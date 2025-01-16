import psycopg2
from confluent_kafka import Consumer, OFFSET_BEGINNING
import json

# PostgreSQL configuration
DB_NAME = 'flight-info'
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = '192.168.1.12'
DB_PORT = '5432'

# Redpanda configuration
BROKER_URL = 'localhost:9092'
TOPIC_NAME = 'flight-info'
GROUP_ID = 'flight-group'

# Set up PostgreSQL connection
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS "flightinfo" (
        id SERIAL PRIMARY KEY,
        event_data JSONB
    )
""")
conn.commit()

# Set up Redpanda consumer
consumer_config = {
    'bootstrap.servers': BROKER_URL,
    'group.id': GROUP_ID,
    'enable.auto.commit': False,  # Explicitly commit offsets
    'auto.offset.reset': 'earliest',  # Start from earliest offset if no committed offset
    'enable.auto.offset.store': True  # Enable offset storage
}
consumer = Consumer(consumer_config)
consumer.subscribe([TOPIC_NAME])

def consume_events():
    print(f"Subscribed to topic: {TOPIC_NAME}")
    while True:
        msg = consumer.poll(1.0)  # Poll for new messages every one second
        if msg is None:
            print("No new messages, retrying...")
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        event = msg.value().decode('utf-8')
        event_data = json.loads(event)
        event_item_count = len(event_data)
        print(f"Consumed event with {event_item_count} items.")

        # Insert the event data into PostgreSQL as a JSON string
        cursor.execute("INSERT INTO flightinfo (event_data) VALUES (%s)", (json.dumps(event_data),))
        conn.commit()

        # Manually commit the offset after processing
        consumer.commit(asynchronous=False)

if __name__ == "__main__":
    print("Consumer started")
    try:
        consume_events()
    except KeyboardInterrupt:
        print("Consumer stopped")
    finally:
        consumer.close()
        cursor.close()
        conn.close()

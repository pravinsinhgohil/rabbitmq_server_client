import pika
import pymongo
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
from threading import Thread

# Database settings (Mongo)
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "test_data"
MONGO_COLLECTION = "status_messages_test"

# RabbitMQ settings
RABBITMQ_HOST = "localhost"
RABBITMQ_QUEUE = "status_queue"

# Flask app
app = Flask(__name__)

# MongoDB client setup
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]


# RabbitMQ connection setup
def connect_rabbitmq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE)
        return channel
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        return None


channel = connect_rabbitmq()


def callback(body):
    try:
        message = json.loads(body)
        message['timestamp'] = datetime.utcnow()
        collection.insert_one(message)
        print(f"Stored message: {message}")
    except Exception as e:
        print(f"Failed to process msg: {e}")


def start_consuming():
    if channel:
        try:
            print("Starting to consume messages...")
            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        except Exception as e:
            print(f"Error during consuming: {e}")


@app.route('/status_count', methods=['GET'])
def status_count():
    try:
        start_time_str = request.args.get('start')
        end_time_str = request.args.get('end')

        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_time, "$lt": end_time}}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        test_message = {"status": 1, "timestamp": datetime.utcnow()}
        result1 = collection.insert_one(test_message)

        result = list(collection.aggregate(pipeline))
        result_dict = {str(item['_id']): item['count'] for item in result}

        return jsonify(result_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    Thread(target=start_consuming).start()
    app.run(host='0.0.0.0', port=5000)

## **Prerequisites**

#### Before you begin, ensure you have the following installed on your machine:

Python 3.x: Required to run the Python script.(used python 3.12)
RabbitMQ: message broker that  MQTT client will publish to and  Flask server will consume from.
MongoDB:  NoSQL database where the messages will be store.
Pip: Python package manager, used to install requir libraries.


##### Installing Prerequisites

RabbitMQ:

Download and installing RabbitMQ from here.
Ensuring the RabbitMQ management plugin is enabled:
rabbitmq-plugins enable rabbitmq_management
Start RabbitMQ service:
rabbitmq-service start

MongoDB:
Download and install MongoDB.
Start Mongo service:
net start MongoDB




## **Requirements**

The following Python libraries are required and can be installed using pip:
paho-mqtt: For MQTT client functionality.
pika: For RabbitMQ client functionality.
pymongo: For MongoDB client functionality.
flask: For creating the API server.



## Installing Python Dependencies

Run the following command to install  required libraries:

pip install paho-mqtt pika pymongo flask


## **Setup Instructions**

### Clone the Repository (if applicable):

git clone <repository-url>
cd <repository-folder>

## Ensure Services are Running:
Make sure RabbitMQ and MongoDB services are running on your machine.

## Create the Python Script:

Create a single Python file, e.g., app.py, and copy the provided script into this file.



## Running the Application

To run the entire pipeline (MQTT client, RabbitMQ consumer, MongoDB storage, and Flask API) in one go, simply execute the Python script:

python app.py


This will start:
The MQTT client that sends random status messages.
The RabbitMQ consumer that receives those messages and stores them in MongoDB.
The Flask server that provides an API to query the stored data.


## Verifying the Setup

1)Verify RabbitMQ Queue
Open the RabbitMQ management interface at http://localhost:15672.
Login with the default credentials (guest / guest).
Navigate to the Queues tab and ensure that the status_queue is present and active.



## Verify MongoDB Data

Open MongoDB Compass and connect to mongodb://localhost:27017.
Navigate to the test_data database.
Open the status_messages_test collection to view the documents being stored.

## Verify Flask API

Access the Flask API endpoint to check if data retrieval works

http://localhost:5000/status_count?start=2024-01-01%2000:00:00&end=2024-12-31%2023:59:52

## Troubleshooting

RabbitMQ Management Interface is Unavailable
Ensure the management plugin is enabled:
rabbitmq-plugins enable rabbitmq_management
Restart RabbitMQ if necessary:
rabbitmq-service restart




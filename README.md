# Fetch Rewards Project

This project demonstrates how to read messages from an AWS SQS queue, process the messages, and insert the processed data into a PostgreSQL database using Docker containers.

## Project Structure

- `create_queue.py`: Script to create the SQS queue.
- `docker-compose.yml`: Docker Compose file to set up the LocalStack and PostgreSQL services.
- `Dockerfile`: Dockerfile to build the Python application.
- `read_sqs.py`: Script to read messages from SQS, process them, and insert them into PostgreSQL.
- `requirements.txt`: Python dependencies file.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

1. **Clone the Repository**

   First, you need to clone the repository to your local machine. Open your terminal and run:

    ```sh
    git clone <repository-url>
    cd fetch_rewards_project
    ```

2. **Build the Docker Image**

   This step builds the Docker image for our Python application. Run the following command in the terminal:

    ```sh
    docker build -t python-app .
    ```

3. **Start the Services**

   Next, we'll use Docker Compose to start the LocalStack and PostgreSQL services. Execute:

    ```sh
    docker-compose up -d
    ```

    - `-d` flag runs the services in the background.

4. **Create the SQS Queue**

   Now, we need to create the SQS queue. Run:

    ```sh
    docker run --network host python-app python create_queue.py
    ```

5. **Send Messages to SQS**

   You can manually send messages to the SQS queue using the AWS CLI or any other method. Make sure the messages follow this format:

    ```json
    {
        "user_id": "201",
        "device_id": "mno",
        "ip": "192.168.1.11",
        "device_type": "mobile",
        "locale": "en_US",
        "app_version": 1,
        "create_date": "2023-06-11"
    }
    ```

6. **Read Messages from SQS and Insert into PostgreSQL**

   Finally, read messages from the SQS queue, process them, and insert them into the PostgreSQL database by running:

    ```sh
    docker run --network host python-app python read_sqs.py
    ```

## Scripts Overview

### `create_queue.py`

This script creates an SQS queue using LocalStack. LocalStack is a fully functional local AWS cloud stack. It allows you to develop and test your cloud applications offline.

### `read_sqs.py`

This script performs the following tasks:
1. **Read Messages**: It reads messages from the SQS queue.
2. **Process Messages**: It processes each message by hashing sensitive information (like `device_id` and `ip`).
3. **Insert Data**: It inserts the processed data into the PostgreSQL database.

### `Dockerfile`

The Dockerfile is used to create a Docker image for the Python application. It sets up the Python environment and installs all necessary dependencies listed in `requirements.txt`.

### `docker-compose.yml`

The Docker Compose file sets up two services:
- **LocalStack**: For simulating AWS services locally.
- **PostgreSQL**: As the database to store the processed messages.

### `requirements.txt`

This file lists all Python dependencies required for the application.

## Step-by-Step Guide

### Step 1: Build Docker Image

Open your terminal, navigate to the project directory, and run:

```sh
docker build -t python-app .


**Troubleshooting**
    -No credentials error: Ensure your AWS CLI is properly configured and LocalStack is running.
    -Queue does not exist: Make sure the queue was created successfully using create_queue.py.
    -Database insertion issues: Ensure the PostgreSQL container is running and accessible.
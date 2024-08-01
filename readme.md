# Votr

**Votr** is a polling application built with Flask, SQLAlchemy, and Celery, designed to create and manage polls, options, and user votes. The application features a web interface for user interaction, an API for programmatic access, and a database backend for storing data.

## Features

- **User Management**: Users can sign up, log in, and participate in polls.
- **Poll Creation**: Admins can create topics and options for polls.
- **Voting System**: Users can vote on different options within a poll.
- **Real-Time Updates**: Results are updated in real-time using the backend.
- **Task Scheduling**: Background tasks are managed using Celery and RabbitMQ.

## Project Structure

- `votr/`
  - `votr.py`: Main application file.
  - `models.py`: Database models for Users, Topics, Polls, and Options.
  - `config.py`: Configuration settings (database URI, secret key, etc.).
  - `tasks.py`: Background tasks managed by Celery.
  - `admin.py`: Admin functionalities.
  - `api/`: Contains API implementation.
    - `api.py`: API endpoints for accessing and managing data.
    - `__init__.py`: Initializes the API module.
  - `templates/`: HTML templates for the frontend.
  - `static/`: Static files (CSS, JS, images).
  - `migrations/`: Database migration scripts (Alembic).

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd votr

    ```
2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**: 
    - *Initialize the database*:
    ```bash
    flask db upgrade
    ```
5. **Run the application**:

    ```bash
    flask run
    ```
6. **Access the application**:

    - Visit http://127.0.0.1:5000/ in your web browser.

## Configuration
Configuration settings are stored in config.py. This includes settings for:

 - Database URI
 - Secret key
 - Debug mode
 - Celery configuration (broker and backend URLs)

Ensure that you update these settings to match your environment, especially for production deployment.

## Celery and RabbitMQ Setup
The application uses Celery for task scheduling and RabbitMQ as the message broker.

1. ***Install RabbitMQ***:

    - On Ubuntu:

        ```bash
        sudo apt-get install rabbitmq-server
        ```
    - Start RabbitMQ:

        ```bash
        sudo systemctl start rabbitmq-server
        ```

    - Ensure RabbitMQ is running:

        ```bash
        sudo systemctl status rabbitmq-server
        ```

2. **Configure Celery**:

 - In config.py, set the following configurations:
    ```python
    CELERY_BROKER_URL = 'amqp://localhost//'
    CELERY_RESULT_BACKEND = 'rpc://'
    ```

3. **Running Celery Worker**:

    - Start the Celery worker with:

    ```bash
    celery -A votr.tasks worker --loglevel=info
    ```
    - This command should be run in a separate terminal or managed as a background service.

## API Usage
The application exposes a RESTful API for interacting with polls, options, and votes. Detailed API documentation can be found in the api.py module.


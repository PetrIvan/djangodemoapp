# Django REST Framework Demo Project

A simple demo project used in a job application process to showcase proficiency in Python backend development.

## Installation

1. Navigate to the place where you want the app to be downloaded in Command Prompt.

2. Clone the repository: `git clone https://github.com/PetrIvan/djangodemoapp.git`

3. Navigate to the project directory: `cd djangodemoapp`

4. Create a virtual environment: `python -m venv venv`

5. Activate the venv: `venv\Scripts\Activate` (Windows) or `source venv/bin/activate` (MacOS/Linux)

6. Install the packages: `pip install -r requirements.txt`

7. Create a `.env` file in the project root directory with the following content:

```
SECRET_KEY="your_secret_key_here"
DEBUG=1
ALLOWED_HOSTS="localhost 127.0.0.1"
```

> Note: You can generate your secret key using:
> `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
>
> In a production environment, you should set DEBUG=0 and add your production domains to ALLOWED_HOSTS.

8. Start the server: `python manage.py runserver`

9. Open the webpage `http://localhost:8000/` in your browser.

## Running the project with Docker

1. Build the Docker image: `docker build -t djangodemoapp .`

2. Start the container: `docker run -p 8000:8000 djangodemoapp`

3. The API is available at `http://localhost:8000/`

## Running tests

To run the tests, execute the following command: `python manage.py test`

# FEEDBACK GENERATOR

A Django-based evaluation system that allows students to submit code assignments, evaluates them for syntax, indentation, and comments, and provides feedback.

## Features
- User authentication (Students, Tutors, Admins)
- Code submission and automated evaluation
- Admin-configurable evaluation criteria
- Feedback system with grading
- Django Admin Panel for user and evaluation management

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip
- virtualenv
- MySQL (or any other database configured in `settings.py`)

### Clone the Repository
```sh
$ git clone https://github.com/Chin3ll/feedback-pro.git
$ cd feedbackgenerator
```

### Create a Virtual Environment
```sh
$ python -m venv venv
$ source venv/Scripts/activate  # On Windows
```

```sh
$ python3 -m venv venv
$ source venv/bin/activate # On Mac
```

### Install Dependencies
```sh
$ pip install -r requirements.txt
```

1. Run migrations:
    ```sh
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

### Create a Superuser
```sh
$ python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Run the Development Server
```sh
$ python manage.py runserver
```
The project will be available at `http://127.0.0.1:8000/`.

## Usage

### Accessing the Admin Panel
- Navigate to `http://127.0.0.1:8000/admin/`
- Login with the superuser credentials

### Accessing the Admin dashboard
- Navigate to `http://127.0.0.1:8000/dashboard-a/`
- Login with the superuser credentials

### Submitting an Evaluation (Student View)
- Login as a student
- Navigate to `http://127.0.0.1:8000/dashboard-s/`
- View student dashboard

### Reviewing Submissions (Lecturer View)
- Navigate to `http://127.0.0.1:8000/dashboard-t/`
- View Tutor dashboard

## Deployment (Optional)
To deploy on a live server:
- Use **Gunicorn** and **Nginx** for production
- Configure **ALLOWED_HOSTS** in `settings.py`
- Set up a production database

## License
This project is open-source. You can modify and distribute it as needed.

## Contact
For any issues, reach out at `ochinell@outlook.com`.

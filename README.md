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
$ source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```sh
$ pip install -r requirements.txt
```

### Configure Database
1. Update `DATABASES` settings in `settings.py`:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```
2. Run migrations:
    ```sh
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

### Submitting an Evaluation (Student View)
- Login as a student
- Navigate to `http://127.0.0.1:8000/submit_assignment/`
- Submit a code file for evaluation

### Reviewing Submissions (Lecturer View)
- Navigate to `http://127.0.0.1:8000/view_student_assignments/`
- View pending and graded evaluations

## Deployment (Optional)
To deploy on a live server:
- Use **Gunicorn** and **Nginx** for production
- Configure **ALLOWED_HOSTS** in `settings.py`
- Set up a production database

## License
This project is open-source. You can modify and distribute it as needed.

## Contact
For any issues, reach out at `ochinell@outlook.com`.

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

### Starting the project
## step 1
- Navigate to `http://127.0.0.1:8000/login/`
- to login ![alt text](image-1.png)

## step 2
- Navigate to `http://127.0.0.1:8000/login/`
- Login with your super user account ![alt text](image.png)

## step 3 Assigning Roles
- Navigate to `http://127.0.0.1:8000/profile/`
Once on the profile page click on Admin Panel button to enable view the admin panel
- Admin Panel button ![alt text](image-4.png)
Next click on the profile model to assign Admin role to your newly created account
- Asign role to created user ![alt text](image-5.png)
Next click on any desired user from the list 
- User profile list ![alt text](image-11.png)
Now assign a role to that user options includes (Student, Lecturer, Admin)
- User profile role ![alt text](image-12.png)

## step Creating new user
- Navigate to `http://127.0.0.1:8000/admin/`
Once on the admin page click on users model ![alt text](image-7.png)
- Now you'll be taken to this page `http://127.0.0.1:8000/auth/user/`
Next click on add user + at the top right corner of your screen ![alt text](image-8.png)
- Now feel in the user details you want to create and click save ![alt text](image-9.png) ![alt text](image-10.png)
Next Once the user has been created you have to go back to the profile model again to assign a role to that new user you just created
- User profile list ![alt text](image-11.png)
Now assign a role to that user options includes (Student, Lecturer, Admin)
- User profile role ![alt text](image-6.png)

### Accessing the Admin Panel
- Navigate to `http://127.0.0.1:8000/admin/`
- Login with the superuser credentials

### Accessing the Admin dashboard
- Navigate to `http://127.0.0.1:8000/dashboard-a/`
- Login with the superuser credentials

### Accessing the Student dashboard
- Login as a student account
- Navigate to `http://127.0.0.1:8000/dashboard-s/`
- View student dashboard

### Reviewing Submissions (Lecturer View)
-Login as Lecturer account
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

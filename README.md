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
- SQLite (or any other database configured in `settings.py`)

### Clone the Repository
```sh
$ git clone https://github.com/Chin3ll/feedback-pro.git
$ cd feedback-pro
```

### Create a Virtual Environment
```sh
$ python -m venv venv
$  .\venv\Scripts\Activate  # On Windows
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

### Create a Superuser (This is optional defualt admin is already available check below)
```sh
$ python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Run the Development Server
```sh
$ python manage.py runserver
```
The project will be available at `http://127.0.0.1:8000/`.

### Run the Project Test

```sh
$ python manage.py test sorting_feedback.tests
```
## Default Login Account Credentials
- username: admin password: admin
- username: student1 password: 123456!@#$%^
- username: student2 password: 123456!@#$%^
- username: student3 password: 123456!@#$%^
- continuous upto student14 password: 123456!@#$%^ for all
- username: tutor password: 123456!@#$%^

## Usage

### Starting the project
## step 1
- Navigate to `http://127.0.0.1:8000/login/`
- to login ![alt text](zreadmeimages/image-1.png)

## step 2
- Navigate to `http://127.0.0.1:8000/login/`
- Login with your super user account ![alt text](zreadmeimages/image.png)

## step 3 Assigning Roles
- Navigate to `http://127.0.0.1:8000/profile/`
Once on the profile page click on Admin Panel button to enable you view the admin panel
- Click the Admin Panel button ![alt text](zreadmeimages/image-4.png)
Next click on the profile model to assign Admin role to your newly created account.  Note every newly created user will require to be assign a role even a super user will have to assign himself the role of admin when he gets here
- Asign role to created user ![alt text](zreadmeimages/image-5.png)
Next click on any desired user from the list. Note every newly created will require to be assign a role even a super user will have to assign himself the role of admin when he gets here
- User profile list ![alt text](zreadmeimages/image-11.png)
Now assign a role to that user options includes (Student, Tutor, Admin)
- User profile role ![alt text](zreadmeimages/image-12.png)

## step 4 Creating new user (Student)
- Navigate to `http://127.0.0.1:8000/admin/`
Once on the admin page click on users model ![alt text](zreadmeimages/image-7.png)
- Now you'll be taken to this page `http://127.0.0.1:8000/auth/user/`
Next click on add user + at the top right corner of your screen ![alt text](zreadmeimages/image-8.png)
- Now feel in the user details you want to create and click save ![alt text](zreadmeimages/image-9.png) ![alt text](zreadmeimages/image-10.png)
Next Once the user has been created you have to go back to the profile model again to assign a role (Students) to that new user you just created
- User profile list ![alt text](zreadmeimages/image-11.png)
Now assign a role to that user. Options includes (Student, Tutor, Admin)
- User profile role ![alt text](zreadmeimages/image-6.png)

## step 5 Creating new user (Tutor)
- Navigate to `http://127.0.0.1:8000/admin/`
Once on the admin page click on users model ![alt text](zreadmeimages/image-7.png)
- Now you'll be taken to this page `http://127.0.0.1:8000/auth/user/`
Next click on add user + at the top right corner of your screen ![alt text](zreadmeimages/image-8.png)
- Now feel in the user details you want to create and click save ![alt text](zreadmeimages/image-9.png) ![alt text](zreadmeimages/image-14.png)
Make sure to check mark all three permissions Active, Staff status and Superuser status.
Next Once the user has been created you have to go back to the profile model again to assign a role (Tutor) to that new user you just created
- User profile list ![alt text](zreadmeimages/image-11.png)
Now assign a role to that user. options includes (Student, Tutor, Admin)
- User profile role ![alt text](zreadmeimages/image-6.png)

## step 6 Creating Evaluation Criteria (Tutor Task) 
In this project feedback generating app, Evaluation Criteria refers to the set of rules or standards used to assess student submissions.

Think of it as the blueprint or rubric for grading code assignments automatically.
There can only be one evaluation criteria however the criteria can be edited to march me test/assignment, this was implemented as a security measure 
to prevent students from gaming the system

- Login as a tutor ![alt text](zreadmeimages/loginimages.png)
- Once you are logged in, You have to click on view students assignment ![alt text](zreadmeimages/viewassignment.png)
- Now you'll be taken to the tutor dashboard. So click on student configuration ![alt text](zreadmeimages/evaluation-crit.png)
- Now you can create evaluation criteria and save it. ![alt text](zreadmeimages/creating-eval-cri.png)
- The title field implies a short description of the construct(s) the student is being tested on, check syntax means the test will be evaluated on syntax inclusive, Check indentation means the test will be evaluated on indentation inclusive, Check comments means the test will be evaluated on proper commenting inclusive, Min comments means the minimum number of comment the student should have in his/her code submission, Submission deadline means the deadline for students to submit their test, created by means the tutor who created the evaluation criteria. Required constructs implies a single or multiple list constructs the the system will be evaluted on. Note The list must be in double qoutes entries. 
- Examples of required constructs includes (while loop, for loop, function, lambda function, list comprehension, dictionary comprehension, set comprehension, try-except, class, return statement, if statement, import statement, import from, dictionary, list, tuple, set). A single or combination of multiple constructs as listed here can be used.
- Note only 1 evaluation criteria instance must exist at any given time. However the evaluation criteria can subsequently be edited to meet new requirements as deemed by the tutor. If an evaluation criteria instance already exist then it should only be edited to meet new assignment requirement.


## step 7 View Submitted Evaluation (Tutor Task) 
- Click the evaluation model to see all the evaluations submitted by student. ![alt text](zreadmeimages/stuevals.png)

## step 8 View Student Performance (Tutor Task) 
- Click the Student Performance model to view student performance directly from the admin panel. ![alt text](zreadmeimages/studper.png)


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

### Reviewing Submissions (Tutor View)
-Login as Tutor account
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

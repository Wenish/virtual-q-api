# Project Virtual Q API

## Name
Virtual Q API

## Description
It's a web app which allows the user to manage virtual ticket queues.
In this repository is the backend code of the web app.


## Developer setup

#### 1. Install the latest Python v3.x on your machine.

https://www.python.org/

#### 2. Initialize your venv

`python -m venv .venv`

#### 3. Activate your environment

For Linux Based OS or Mac-OS

`source .venv/bin/activate`

For Windows with CMD

`.\.venv\Scripts\activate.bat`

#### 4. Install the project dependencies

Run those commands in the root folder of the repository:

`pip install --upgrade pip`

`pip install -r requirements.txt`

#### 5. Run Database Migrations

Run this command in the root folder of the repository:

`python manage.py migrate`

#### 6. Optional: Create a superuser for access to the admin panel

`python manage.py createsuperuser`

#### 7. Start development server

#### 7.1 Run this command in the root folder of the repository:

`python manage.py runserver`

#### 7.2 You also need to start the Frontend Web Client "Virtual Q Web Client". (Check out the other Readme for detail instructions for that.)

## Run Linting

Run this command in the root folder of the repository:

`pylint .`

## Run Tests

Run this command in the root folder of the repository:

`python manage.py test`

## Migrations

Creating a migration:

`python manage.py makemigrations`

Apply migration:

`python manage.py migrate`

## Freeze Dependencies

Run this command in the root folder of the repository:

`pip freeze > requirements.txt`

## Debug

Import pdb in the file you want to start the debug:

`import pdb`

Add this line where the debug should start:

`pdb.set_trace()`

## Contributing
This project is a solo project.

## Authors and acknowledgment
- Jonas Voland

## License
MIT

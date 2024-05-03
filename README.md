# Project Virtual Q API

## Name
Virtual Q API

## Description
It's a web app which allows the user to manage virtual ticket queues.
In this repository is the backend code of the web app.


## Developer setup (local setup)

1. Install latest Python v3.x on your machine. https://www.python.org/

2. Initialize your venv

`python -m venv env`

3. Activate your environment

For Linux Based OS or Mac-OS

`source venv/bin/activate`

For Windows with CMD

`.\venv\Scripts\activate.bat`

4. Install the project dependencies

Run those commands in the root folder of the project:

`pip install --upgrade pip`

`pip install -r requirements.txt`

5. Run Database Migrations

Run this command in the root folder of the project:

`python manage.py migrate`

6. Start development server

6.1 Run this command in the root folder of the project:

`python manage.py runserver`

6.2 You also need to start the Frontend Web Client "Virtual Q Web Client". (Check out the other Readme for detail instructions for that.)

### Freeze Dependencies

Run this command in the root folder of the project:

`pip freeze > requirements.txt`


## Build project to make it ready for deployment

// TODO

## Run Tests

Run this command in the root folder of the project:

`python manage.py test`

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

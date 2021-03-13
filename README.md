# Python Flask Project - Feedback App

This is a web app built in Flask that allows users to sign up and log in to their own accounts and interact with their feedback. This app allows users to view their feedback, add new feedback, edit existing feedback and delete their feedback. This app takes advantage of a PostgreSQL database to persist users and feedback. All routes for accessing feedback use the session to track the current user and prohibit unauthorized queries.

## Routes Supported
- register new user
- login
- logout
- show secret
- add feedback
- edit feedback
- delete feedback
- delete user


## Installation and Setup
1. create virtual environment (venv) inside `backend` directory using `python3 -m venv venv`
2. activate venv w/ `source venv/bin/activate`
3. install dependencies w/ `pip install -r requirements.txt`
4. setup pqsl database called `feedback` on machine the server will be running on (follow guide for your OS of choice)
5. run server with `flask run`
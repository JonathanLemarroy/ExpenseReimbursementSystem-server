# Project 2

## Project Description

This is an manager-employee reimbursement system. This program allows employees to create an account and add, edit, or delete their own reimbursement requests. Each request an employee makes has a reason, amount and date created. The managers can view, approve, or deny the requests and submit a response to each request. Managers also can view a basic statistics of all requests approved and denied.

## Technologies Used

* Flask
* PyTest

## Features

* Create a new employee account
* Log into an account
* Upgrade an account to manager
* Employees can create new requests
* Employees can edit a request
* Employees can delete a request
* Managers can approve or deny a request
* Managers can view basic statistics for all requests

## Future Features

* Create a better statistics viewing
* Allow employees to update their account name or password

## Getting Started

Cloning server (must have git installed)

```bash
git clone https://github.com/JonathanLemarroy/ExpenseReimbursementSystem-server.git
```

Setup python libraries (must have python with pip installed)

```bash
pip install flask
pip install flask-cors
pip install pytest
pip install psycopg2
```

## Usage

To run the backend of the server run:

```bash
python -m server.run.server
```

To use the website clone <https://github.com/JonathanLemarroy/ExpenseReimbursementSystem-website.git>

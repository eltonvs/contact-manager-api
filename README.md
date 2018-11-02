# Contact Manager API

An API for managing contacts and their information

## Description

This RESTful API was developed in Python using the Django Rest Framework, its main purpose is to store and provide contact information and CRUD functionality to his [client](https://github.com/eltonvs/contact-manager-client).

Test-driven development *(TDD)* was used as one of the main development techniques in this project, as a way to guarantee good code quality, maintainability and easier refactoring.

### Endpoints

This API in on version `v1`, so its base url is `http://host:port/contactmanager/v1`.

| URL | Method | Description |
| :-- | :----: | :---------- |
| `/contacts` | GET | Retrieve all contacts |
| `/contacts` | POST | Create a new contact |
| `/contacts/search` | GET | Search a contact by a given `query` |
| `/contacts/birthdays` | GET | Retrive all contacts from birthdays of the month list |
| `/contacts/:contactId` | GET | Retrieve a single contact |
| `/contacts/:contactId` | PUT | Update a single contact |
| `/contacts/:contactId` | DELETE | Remove a single contact |
| `/contacts/:contactId/phone_numbers` | GET | Retrieve all phone numbers from a contact |
| `/contacts/:contactId/phone_numbers` | POST | Add a new phone number to a contact |
| `/contacts/:contactId/phone_numbers/:phone` | GET | Retrieve a single phone number from a contact |
| `/contacts/:contactId/phone_numbers/:phone` | PUT | Update a single phone number from a contact |
| `/contacts/:contactId/phone_numbers/:phone` | DELETE | Remove a single phone number from a contact |
| `/contacts/:contactId/emails` | GET | Retrieve all emails from a contact |
| `/contacts/:contactId/emails` | POST | Add a new email to a contact |
| `/contacts/:contactId/emails/:email` | GET | Retrieve a new email to a contact |
| `/contacts/:contactId/emails/:email` | PUT | Update a new email to a contact |
| `/contacts/:contactId/emails/:email` | DELETE | Remove a new email to a contact |
| `/contacts/:contactId/addresses` | GET | Retrieve all addresses from a contact |
| `/contacts/:contactId/addresses` | POST | Add a new address to a contact |
| `/contacts/:contactId/addresses/:addressId` | GET | Retrieve a new address to a contact |
| `/contacts/:contactId/addresses/:addressId` | PUT | Update a new address to a contact |
| `/contacts/:contactId/addresses/:addressId` | DELETE | Remove a new address to a contact |


## Built With

* [Python - Django Rest Framework](https://www.django-rest-framework.org/)  - Web Framework
* [Pipenv](https://docs.pipenv.org/) - Python Development Workflow

## Author

[![Elton Viana](https://avatars.githubusercontent.com/eltonvs?s=100)<br /><sub>Elton Viana</sub>](https://github.com/eltonvs) 
| :---: | 

### Installation

```shell
$ git clone git@github.com:eltonvs/contact-manager-api.git
$ cd contact-manager-api
$ pipenv install
$ pipenv shell
$ (env) python manage.py migrate
$ (env) python manage.py runserver
```

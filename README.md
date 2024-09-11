# PostgresPyFlaskAPI

Used on AdviceHealth technical test

## Description

Nork-Town is a weird place. Crows cawk the misty morning while old men squint. It’s a small
town, so the mayor had a bright idea to limit the number of cars a person may possess. One
person may have up to 3 vehicles. The vehicle, registered to a person, may have one color,
‘yellow’, ‘blue’ or ‘gray’. And one of three models, ‘hatch’, ‘sedan’ or ‘convertible’.
Carford car shop want a system where they can add car owners and cars. Car owners may
not have cars yet, they need to be marked as a sale opportunity. Cars cannot exist in the
system without owners.

### Requirements

- [x] Setup the dev environment with docker

- [x] Using docker-compose with as many volumes as it takes

- [x] Use Python’s Flask framework and any other library

- [x] Use any SQL database

- [x] Secure routes

- [x] Write tests

## Run this project

`docker-compose up`

|route|method|description|
|-|-|-|
|<http://localhost:8000>|GET|home|
|<http://localhost:5000/login>|POST|API login|
|<http://localhost:5000/owner>|POST|API create owner|
|<http://localhost:5000/owner/{owner_id}/vehicle>|POST|API add vehicle|
|<http://localhost:5000/owners>|GET|API list all|

## Run tests

`docker-compose run test`

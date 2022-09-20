# handshake-provisioner

[![Build Status](https://github.com/uw-it-aca/handshake-provisioner/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=main)](https://github.com/uw-it-aca/handshake-provisioner/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/handshake-provisioner/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/handshake-provisioner?branch=main)

Provisions UW data to Handshake through a CSV file.


## System Requirements

- Python (3+)
- Docker
- Node

## Development Stack

- [Django](https://www.djangoproject.com) (3.2)
- Vue (3.2)
- Vite (2.9)
- Vitest (0.10.2)

## Design Stack

- Bootstrap (5.2)
- Bootstrap Icons (1.9.0)

## Installation

Clone the repository

        $ git clone git@github.com:uw-it-aca/app_name.git

Go to your working directory

        $ cd app_name

Copy the sample .env file so that your environment can be run.

        $ cp .env.sample .env

Update any .env variables for local development purposes

## Development (using Docker)

Docker/Docker Compose is used to containerize your local build environment and deploy it to an 'app' container which is exposed to your localhost so you can view your application. Docker Compose creates a 'devtools' container - which is used for local development. Changes made locally are automatically syncd to the 'app' container.

        $ docker-compose up --build

View your application using your specified port number in the .env file

        Demo: http://localhost:8000/

## Testing

### Front-end Testing (using Vitest)

Run Vitest test scripts and generate coverage report

        $ npm run test
        $ npm run coverage

### Linting (using ESLint and Stylelint)

Run ESLint for JS linting

        $ npm run eslint

Run Stylelint for CSS linting

         $ npm run stylelint

### Python Testing (using Django)

Run unittest locally,

        $ docker-compose run --rm app bin/python manage.py test

or from anywhere:

        $ docker exec -ti sis_provisioner_app bin/python manage.py test

### Validation

There is a script to validate and compare CSV files with the file produced by this app. The script is run by running the following:

        $ python3 scripts/validate.py my_generated.csv [--example/-e example_file.csv --column/c column_name --remove-cols/-r column_names]

By default, the script will compare the generated CSV file with a file in the `handshake-provisioner` directory called `example.csv`.
You can change the file name by passing the file name as an argument to the script through `--example` or `-e`. You can also specify the column name to compare by by passing the column name as an argument to the script through `--column` or `-c`. By default, this is the 'username' column. You can specify the column names to remove from the comparison output by passing the column names as an argument to the script through `--remove-cols` or `-r` like

        ... -r auth_identifier last_name ...

## Deployment

To be completed.

## Authors

- [Academic Experience Design & Delivery](https://github.com/uw-it-aca)

## License

Copyright 2022 UW Information Technology, University of Washington

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# handshake-provisioner

[![Build Status](https://github.com/uw-it-aca/handshake-provisioner/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=main)](https://github.com/uw-it-aca/handshake-provisioner/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/handshake-provisioner/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/handshake-provisioner?branch=main)

Provisions UW data to Handshake through a CSV file.

## Getting Started

### Prerequisites

- Docker
- docker-compose
- git

## How to Run

Clone the app to a directory of your choice:

```$ git@github.com:uw-it-aca/handshake-provisioner.git```

Then run the following to start the app:

```$ docker-compose up --build```

## Additional Settings and Commands

There are additiional settings that can be configured in a `.env` file. A sample.env file is included in the repository.
Run `$ cp sample.env .env` to use the sample file for your settings. You can edit the file to change the settings and
each group of settings is explained in the file itself.

### Validation

There is a script to validate and compare CSV files with the file produced by this app. The script is run by running the following:

```$ python3 scripts/validate.py my_generated.csv [--example/-e example_file.csv --column/c column_name --remove-cols/-r column_names]```

By default, the script will compare the generated CSV file with a file in the `handshake-provisioner` directory called `example.csv`.
You can change the file name by passing the file name as an argument to the script through `--example` or `-e`. You can also specify the column name to compare by by passing the column name as an argument to the script through `--column` or `-c`. By default, this is the 'username' column. You can specify the column names to remove from the comparison output by passing the column names as an argument to the script through `--remove-cols` or `-r` like

```... -r auth_identifier last_name ...```

## Running Tests

You can run tests by running the following within the app directory:

```$ docker-compose run --rm app bin/python manage.py test```

or this from anywhere:

```$ docker exec -ti app-handshake bin/python manage.py test```

## Deployment

To be completed.

## Built With

- [Django](https://www.djangoproject.com)

## Authors

- [Academic Experience Design & Delivery](https://github.com/uw-it-aca)

## License

Copyright 2022 UW Information Technology, University of Washington

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

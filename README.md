# The tapas framework

[![Join the chat at https://gitter.im/tapas-cantina/tapas](https://badges.gitter.im/tapas-cantina/tapas.svg)](https://gitter.im/tapas-cantina/tapas?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Install

Create a fresh virtualenv and install the checked out module via `pip install -e .`. 

##  Getting started

* Make your personal copy of sample-config.json. You might want to adjust the path to the database.
* Make sure your virtualenv is activated. This makes the `tapas` command line tool available.
* Init your database by running `tapas init_db path/to/your-config.json`.
* Start the service by running `tapas serve path/to/your-config.json`.
* Point your browser to http://localhost:8089. You should see a simple text message.

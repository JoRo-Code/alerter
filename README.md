
# What?
Alerts given a certain check

## Requirements
- python3 
- libraries: smtplib, email, bs4, tinydb, pickle, selenium

## Usage
### Setup
- install python libraries: `pip3 install <library>`
- add a `config.py`. See `config.example.py`
- add a `credentials.py`. See `credentials.example.py`
### Run
- `python3 main.py`
### Reset
- `make reset` (works on unix)
- delete `checks.pickle` to reset alerts
- delete .json-files to remove any other persistance




# What?
Sends an alert when certain services at Bokadirekt is available. 

# Why?
Gives an advantage to book the services faster than others, since the public alert goes off ~15-30 minutes after the actual published services.

## Requirements
- python3 
- libraries: see `requirements.txt`

## Usage
### Setup
- install python libraries: `pip3 install -r requirements.txt`
- add a `config.py`. See `config.example.py`
- add a `credentials.py`. See `credentials.example.py`
### Run
- `python3 main.py`
### Reset
- `make reset` (works on unix)
- delete `checks.pickle` to reset alerts
- delete .json-files to remove any other persistance



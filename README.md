# Building Exchange Rate program in Python #

## Author
<h3>Name: Bipin Chaskar </h3>

## Description

This is a Python application that allows users to analyse currencies. This application leverages the Fixer API to fetch the latest exchange rates and historical rates for various currencies.

### Features

- Connect to FIXER exchange rates API to get exchange rates for the past 30 days and store into json output format
- Pre process the JSON data to manage any expected issues
- Perform some data analysis
	- Find the best and worst exchange rates for that time period
	- Calculate the average exchange rate for the month
	- Plot the graph to show rate changes within a month

### Challenges

Some of the challenges faced during the development of this project include:

- Integrating external APIs and handling API responses. APIs provide limited number of hits for free access.
- Implementing proper error handling for API calls.
- Parsing JSON into CSV/Text format to store values in columnar format.

### Future Features

In the future, the Currency Converter web application could be enhanced with the following features:

- User authentication and profiles to save conversion history.
- Support for a wider range of currencies.
- Real-time currency conversion updates.
- Various currency exchange rate trend analysis.
- Mobile application version for convenience on the go.

The project aims to do a case study for limited features.

## How to Setup
### Prerequisites
- Python 3.x
- pip 23.x

### Python packages or libraries:
- Requests
- Datetime
- JSON
- OS
- CSV
- Pandas
- Matplotlib

## How to Run the Program

1. Navigate to your project folder:
`cd myproject`
2. Create a new virtual environment in that folder and activate that environment:
`python -m venv .venv`
3. Install missing libraries in your environment.
`pip install <package name>`
4. Execute in the terminal.
`python exchange_rate.py`

## Project Structure

The project consists of the following files:

1. exchange_rate.py: Contains code and functions for providing require functionality.
2. README.md: a markdown file containing listing of all Python functions and instructions for running the app

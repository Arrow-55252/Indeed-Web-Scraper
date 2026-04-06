# Indeed Scraper
- An interactive program that scrapes the `indeed.com` website for job listings.
The user types the Occupation, City, and State they wish to search for in the terminal, and gets a detailed csv file in return.

## Getting Started:

- Copy the repository
- Run `python indeed_scrape.py` in your terminal

## Prerequisites:

- Python 3.x
- Code Editor

## Dependencies:
- `pip install BeautifulSoup4`
- `pip install curl_cffi`
- `pip install requests`

## Built with:
- Python

## Notes:

- At times due to indeed.com's bot detection the status code might show up as 403.
- There will be a warning in the terminal stating if the status code is anything other than a 200.
- In case it is a 403 please wait before attempting to run the program again, usually the program will begin working again within a few hours.

- `abbreviation.py` is a helper script that contains a dictionary of all U.S states and their correct abbreviations. 
This file is included in the repositiory.


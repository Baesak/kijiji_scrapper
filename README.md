# kijiji_scrapper

This is Web Scrapper for kijiji. It scraps all data from this page https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273 (including pagination) and records data in PostgreSQL. Database and python app are wrapped in docker.

## How to start
To start scrapping you should enter: `make start_all`. This will start python app and database containers.

To start db only: `make start_db`

To stat app only: `make start_scrapper`

## Dependencies
This project requiers `docker` and `docker-compose` installed on your PC.

## Output example

![alt text](https://imgur.com/8Mu98rh.png)

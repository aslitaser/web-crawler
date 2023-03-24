
# **Web Crawler**

## Overview

This web crawler is a Python-based application that crawls web pages and extracts information from them. It uses Celery for task management and Redis for managing the URL frontier.

The application is composed of the following components:

* **Fetcher:** fetches the contents of web pages using the HTTP protocol.
* **URL Deduplication:** ensures that each URL is processed only once to avoid duplicated work.
* **URL Frontier:** manages the set of URLs to be processed.
* **Parser:** extracts information from the HTML content of web pages.
* **Storage:** stores the extracted information for later use.
* The application also supports dynamic throttling and logging using Logstash for extensive logging.

### Installation

* To install the web crawler, follow these steps:
* Clone the repository from GitHub.
* Install the required Python packages by running pip install -r requirements.txt.


### Configuration

The web crawler can be configured using environment variables. The following variables can be set:

* REDIS_HOST: the host name of the Redis server. Default: localhost.
* REDIS_PORT: the port number of the Redis server. Default: 6379.
* REDIS_DB: the Redis database to use. Default: 0.
* LOGSTASH_HOST: the host name of the Logstash server. Default: localhost.
* LOGSTASH_PORT: the port number of the Logstash server. Default: 5000.

### Usage

To use the web crawler, follow these steps:

* Start the Redis server.
* Start the Logstash server.
* Run the main.py script to start the crawler.
* The crawler will start crawling the web pages and extracting information from them.

# Simple Crawler

## Overview

Simple Crawler is an automated tool developed in Python for searching and downloading PDF files from the web. Using Selenium for web scraping and Requests for file downloads, it is particularly useful for aggregating data from a variety of online sources. This tool is designed to be adaptable for different search queries, making it suitable for a wide range of data retrieval tasks.

## Features

- **Automated Web Scraping**: Utilizes Selenium to navigate search engine results and find PDF links.
- **Efficient File Downloading**: Downloads files using the Requests library, with functionality to skip large files to prevent long wait times.
- **Customizable Search Queries**: Allows users to specify search queries for targeted data retrieval.
- **Pagination Handling**: Capable of processing multiple pages of search results.
- **Duplicate Avoidance**: Maintains a log of processed URLs to prevent re-downloading of the same files.
- **Randomized Delays**: Implements random delays between requests to mimic human interaction and reduce the likelihood of being detected as a bot.

## Requirements

Before running the script, ensure you have the necessary Python packages installed. You can install these packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run the Simple Crawler, execute the script from the command line:

```bash
python download_reports.py
```

## Output

- The script downloads PDF files and stores them in a specified directory (default is `./data/financial_statements`).
- A log file `processed_urls.txt` is updated with each URL processed, preventing duplicate downloads in future runs.

## Customization

- Edit the `queries` list in the script to use different search terms according to your data retrieval needs.
- Adjust `start_page` and `end_page` to define the range of search result pages to be processed.

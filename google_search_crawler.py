import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import random


def load_processed_urls():
    processed_urls = set()
    urls_file_path = "../processed_urls.txt"
    if os.path.exists(urls_file_path):
        with open(urls_file_path, "r") as file:
            for line in file:
                processed_urls.add(line.strip())
    return processed_urls


def download_file(url, download_folder, filename, timeout=30):
    """
    Download a file from a URL with a specified timeout.
    Skip very large files to prevent the script from hanging.
    """
    try:
        # Use stream=True to avoid loading the entire content into memory
        with requests.get(url, timeout=timeout, stream=True) as response:
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

            # Check the content length to skip large files
            content_length = response.headers.get("Content-Length")
            if (
                content_length and int(content_length) > 10_000_000
            ):  # Skip files larger than 10MB
                print(f"Skipping large file: {url}")
                return False

            # Write the content to a file in chunks to manage memory usage
            with open(os.path.join(download_folder, filename), "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
            return True

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

    return False


def download_pdf(url, download_folder, processed_urls):
    if url in processed_urls:
        return

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    parts = url.split("/")
    new_filename = (
        (parts[-3] + "_" + parts[-2] + "_" + parts[-1])
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
        .replace("%20", "_")
    )
    new_file_path = os.path.join(download_folder, new_filename)

    if not os.path.exists(new_file_path):
        if download_file(url, download_folder, new_filename):
            print(f"Downloaded: {new_filename}")
            processed_urls.add(url)
            with open("./processed_urls.txt", "a") as file:
                file.write(url + "\n")
    else:
        print(f"File already exists: {new_filename}")


def selenium_search(
    query, download_folder, processed_urls, start_page=0, end_page=1310
):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    base_url = "https://www.google.com/search?q="
    previous_url = ""

    for page in range(start_page, end_page):
        n_files = len(os.listdir(download_folder))
        print(f"N files downloaded until now: {n_files} - Processing page {page}...")

        page_url = (
            base_url
            + query.replace(" ", "+")
            + "+filetype:pdf"
            + ("&start=" + str((page - 1) * 10) if page > 0 else "")
        )
        print(page_url)

        if page_url == previous_url:  # Detect loop
            print("Loop detected. Exiting.")
            break
        previous_url = page_url

        driver.get(page_url)
        try:
            consent_button = driver.find_element(By.XPATH, '//*[@id="L2AGLb"]')
            consent_button.click()
        except NoSuchElementException:
            pass

        try:
            # wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//a[h3]")))
            # links = driver.find_elements(By.XPATH, "//a[h3]")

            wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@id='search']"))
            )
            links = driver.find_elements(By.XPATH, "//a[h3]")

        except TimeoutException:
            print(f"Timeout occurred on page {page}")
            continue

        for link in links:
            url = link.get_attribute("href")
            if url and url.lower().endswith(".pdf"):
                download_pdf(url, download_folder, processed_urls)

        # Random delay to mimic human behavior and avoid bot detection
        time.sleep(random.uniform(1, 5))

    driver.quit()


if __name__ == "__main__":
    download_folder = "./data/financial_statements"
    start_page = 0  # Set the start page
    end_page = 1310  # Set the end page

    # Create the download folder if it does not exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    queries = ["financial statments"]
    processed_urls = load_processed_urls()

    for query in queries:
        selenium_search(query, download_folder, processed_urls, start_page, end_page)

# CompraFacil

The AutoMercado.py script is a Python-based web scraper designed to extract product information from the Auto Mercado website. The script utilizes Selenium for browser automation and Scrapy for HTML parsing. It dynamically loads products by clicking the "Ver más" button on the website and retrieves details such as product name, price, image, availability, and more. The extracted data is saved in a JSON file for further use.

Features

Automates interaction with the Auto Mercado website.

Dynamically loads all available products by repeatedly clicking "Ver más."

Extracts product details including:

Name

Price

URL

Image

Subtitle

Availability status

Saves the extracted data to a JSON file.

Prerequisites

Python Modules

The script requires the following Python modules:

selenium

tqdm

scrapy

json

time

Install the required modules using pip:

pip install selenium tqdm scrapy

WebDriver

Download the ChromeDriver compatible with your Chrome browser version from https://chromedriver.chromium.org/.

Ensure the ChromeDriver executable is in your system PATH or provide the path directly in the script.

Usage

Running the Script

Clone or download the script.

Update the URL in the driver.get() method if needed. Currently, it is set to scrape for all products (https://automercado.cr/buscar?q=*).

Run the script using Python:

python AutoMercado.py

Output

HTML File: The complete HTML content of the loaded page is saved to html_file.txt.

JSON File: Extracted product details are saved to results.json.

Extracted Data Format

The JSON file contains a list of dictionaries with the following structure:

[
  {
    "name": "Product Name",
    "price": "Product Price",
    "url": "Product URL",
    "image": "Image URL",
    "subtitle": "Subtitle",
    "availability": "Available/Unavailable"
  }
]

Key Functions

number_of_elements_to_be_more_than

Custom Selenium condition that waits for the number of elements matching a given locator to exceed a specified count.

clean_price

Cleans and formats the price text to ensure consistent output.

Error Handling

The script gracefully handles the absence of the "Ver más" button and other errors, logging them to the console.

Notes

Ensure that the target website's structure matches the XPath selectors used in the script.

Excessive scraping may violate the website's terms of service. Use responsibly.

Limitations

The script assumes the product data is available and properly structured in the HTML.

Lazy-loading behavior must be compatible with Selenium's scroll and wait operations.

Troubleshooting

If the script fails to locate elements, verify the website's structure using browser developer tools.

Update the XPath selectors if the website layout changes.

Acknowledgments

Selenium documentation: https://www.selenium.dev/documentation/

Scrapy documentation: https://docs.scrapy.org/

tqdm documentation: https://tqdm.github.io/

For any issues or contributions, please create a pull request or raise an issue in the repository.

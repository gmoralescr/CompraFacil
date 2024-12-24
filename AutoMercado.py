import json  # Import the json module
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm  # Import tqdm for the loading bar
import time

class number_of_elements_to_be_more_than:
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        return len(elements) > self.count

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://automercado.cr/buscar?q=*")

# Wait until the grid-square div is present
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "grid-square"))
)

# Initialize tqdm progress bar
progress_bar = tqdm(desc="Loading products", unit="click")

# Load all products by clicking "Ver más"
while True:
    try:
        # Get the current number of products
        current_count = len(driver.find_elements(By.XPATH, '//div[@class="grid-square"]//div[contains(@class, "card-product")]'))

        # Locate and click the "Ver más" link
        load_more_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Ver más"]'))
        )
        load_more_link.click()

        # Wait for the number of products to increase
        WebDriverWait(driver, 10).until(
            number_of_elements_to_be_more_than(
                (By.XPATH, '//div[@class="grid-square"]//div[contains(@class, "card-product")]'),
                current_count
            )
        )

        # Scroll to the bottom of the page to ensure lazy-loaded elements are rendered
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Update the progress bar
        progress_bar.update(1)

    except Exception as e:
        print(f"No more 'Ver más' link or error occurred: {e}")
        break

# Close the progress bar
progress_bar.close()

# Get the final page source
page_source = driver.page_source

# Save the page source to a .txt file
with open("html_file.txt", "w", encoding="utf-8") as file:
    file.write(page_source)

print("HTML saved to html_file.txt")

# Use Scrapy's Selector to parse the page source
from scrapy.selector import Selector
sel = Selector(text=page_source)

# Extract product cards
products = sel.xpath('//div[@class="grid-square"]//div[contains(@class, "card-product")]')
print(f"Number of products found: {len(products)}")  # Check how many products are detected

# Simplified clean_price function
def clean_price(price_text):
    return price_text.strip() if price_text else "Price not available"

# List to store product information
product_list = []

# If products are found, extract their details
if products:
    for product in products:
        product_name = product.xpath('.//a[contains(@class, "title-product")]/span/text()').get()
        product_price = product.xpath('.//div[contains(@class, "text-currency")]/text()').get()
        product_url = product.xpath('.//a[contains(@class, "title-product")]/@href').get()
        product_image = product.xpath('.//a[contains(@class, "img-product")]/img/@src').get()
        product_subtitle = product.xpath('.//div[contains(@class, "text-subtitle")]/@title').get()
        availability = product.xpath('.//button[contains(@class, "btn-add")]/@disabled').get()

        availability_status = "Available" if not availability else "Unavailable"

        # Clean the price
        product_price_cleaned = clean_price(product_price)

        product_info = {
            'name': product_name,
            'price': product_price_cleaned,
            'url': f"https://automercado.cr{product_url}" if product_url else None,
            'image': product_image,
            'subtitle': product_subtitle,
            'availability': availability_status
        }

        product_list.append(product_info)
else:
    print("No products found.")

# Save the product list to a .json file
print(f"Total products extracted: {len(product_list)}")
with open("results.json", "w", encoding="utf-8") as json_file:
    json.dump(product_list, json_file, ensure_ascii=False, indent=4)

print("Product information saved to results.json")

# Quit the driver
driver.quit()

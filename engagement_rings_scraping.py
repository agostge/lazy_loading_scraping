# %%
import os
import time
import logging
import requests
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()
config.read('config.ini')

BASE_URL = config.get('settings', 'BASE_URL')
DESTINATION_FOLDER = config.get('settings', 'DESTINATION_FOLDER')
CUT_TYPES = ['Round', 'Oval', 'Emerald', 'Radiant', 'Pear', 'Cushion', 'Elongated Cushion', 'Marquise', 'Princess', 'Asscher', 'Heart']

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver
driver = webdriver.Chrome()

def scroll_to_bottom():
    """
    Scrolls the page to the bottom and clicks 'Load More' to load all products.
    """
    try:
        click_load_more()
        time.sleep(10)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                last_height = new_height
    except Exception as e:
        logging.error(f"Error while scrolling to bottom: {e}")

def click_load_more():
    """
    Clicks the 'Load More' button to load additional products if it exists.
    """
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="shine-button load-more svelte-128ewnv"]'))
        )
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(2)  # Wait for content to load after clicking
    except Exception as e:
        logging.warning(f"No more 'Load More' button found or error: {e}")

def create_folder_structure(metal_type, diamond_cut, product_name):
    """
    Creates the folder structure to store images based on metal type, cut, and product name.
    """
    folder_path = os.path.join(DESTINATION_FOLDER, metal_type, diamond_cut, product_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def download_image(product_name, url, folder, number, image_type='img'):
    """
    Downloads an image from a URL and saves it to the specified folder.
    """
    image_name = f"{product_name}_{image_type}_{number}.jpg"
    image_path = os.path.join(folder, image_name)
    try:
        img_data = requests.get(url).content
        with open(image_path, 'wb') as f:
            f.write(img_data)
        logging.info(f"Downloaded {image_name}")
    except Exception as e:
        logging.error(f"Error downloading {image_type}: {e}")

def process_product_page(product_link, metal_type):
    """
    Processes a single product page to extract details and download images.
    """
    driver.execute_script("window.open(arguments[0], '_blank');", product_link)
    WebDriverWait(driver, 10).until(lambda driver: len(driver.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])

    try:
        # Wait for the page to load and check if it's a valid page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//section[@class='details svelte-gwj5u7']")))

        # Check if the page contains a 404 error message. In this case the item will be skipped. 
        if "404" in driver.title or "Page Not Found" in driver.page_source:
            logging.error(f"Broken link: {product_link}. Skipping to next.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return

        details_container = driver.find_element(By.XPATH, "//section[@class='details svelte-gwj5u7']")
        name = details_container.find_element(By.XPATH, "//h1[@class='svelte-gwj5u7']").text.split(' ')[0]
        cut = next((item for item in CUT_TYPES if item in name), "N/A")

        logging.debug(f"Processing product: {name}, Cut: {cut}, Metal Type: {metal_type}")

        thumbnail_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='thumbs svelte-1ysrele']"))
        )

        image_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='scroll-content svelte-rexg8n']"))
        )

        # Download thumbnail images
        number = 1
        thumbnail_elements = thumbnail_container.find_elements(By.XPATH, './/div[@class="thumb"]/img')
        folder_path = create_folder_structure(metal_type, cut, name)
        for img in thumbnail_elements:
            img_url = img.get_attribute('src')
            download_image(name, img_url, folder_path, number, image_type='thumbnail')
            number += 1
            time.sleep(2)

        # Download main product images
        number = 1
        img_elements = image_container.find_elements(By.TAG_NAME, 'img')
        for img in img_elements:
            img_url = img.get_attribute('src')
            download_image(name, img_url, folder_path, number)
            number += 1
            time.sleep(2)

    except Exception as e:
        logging.error(f"Error processing product page: {e}")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def run_scraping(metal_type):
    """
    Initiates the scraping process for a specific metal type.
    """
    driver.get(BASE_URL)
    time.sleep(10)
    scroll_to_bottom()

    li_elements = driver.find_elements(By.XPATH, '//ul[contains(@class, "root") and contains(@class, "Thumbs")]//li')

    for li_element in li_elements:
        try:
            a_element = WebDriverWait(li_element, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, 'a'))
            )
            product_link = a_element.get_attribute('href')
            process_product_page(product_link, metal_type)

        except Exception as e:
            logging.error(f"Error processing product in list: {e}")
            continue

def main():
    """
    Main function to run the scraper.
    """
    metal = '18k Yellow Gold'
    run_scraping(metal)
    driver.quit()

if __name__ == "__main__":
    main()




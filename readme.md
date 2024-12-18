

# Web Scraping Project 

This is a Python-based web scraping project that extracts product images and details  from a website, specifically for engagement rings. The scraper navigates through the website, handles lazy loading, which is used by the website, collects relevant data, and saves images to a structured directory on the local machine.

---

## Table of Contents
1. [Tech Stack](#tech-stack)
2. [Usage](#usage)
3. [Challenges] (#challenges)
4. [Folder Structure](#folder-structure)
5. [Error Handling](#error-handling)
6. [Contributing](#contributing)
7. [License](#license)

---

## Tech Stack

The following tools, libraries were used for this project:

- **Python 3.6+**: This project uses Python for automation.
- **Selenium**: A tool for automating web browsers.
- **Chrome WebDriver**: Used to control the  browser.
- **Requests**: Used to download images from URLs.
- **Logging**:  Logging library for debugging and tracking errors.



## Usage


 **Run the script**:
   
   You can run the scraper by executing the Python script:

   ```bash
   python scraper.py
   ```

   The script will automatically:
   - Open a Chrome browser and navigate to the **Cullen Jewellery Engagement Rings** page.
   - Scroll to the bottom to load all product listings.
   - Click on each product to collect details such as name, diamond cut, and metal type.
   - Download product images (thumbnails and main images) and save them to a structured directory based on product details.

---


## Challenges

There were a number of challenges scraping the product images from this website.

1. Lazy Loading

As the website implemented lazy loading to show only a fraction of the search results, I had to circumvent it in order to facilitate the scraping. After clicking on the 'Load More' button, the script makes my browser client move down a bit every few seconds, thereby imitating user scrolling. Once at the bottom, meaning there are no further search results to be loaded, the script starts the scraping process.

2. Scraping the images.

The images can be accessed on the product page, therefore each product needs to be opened and the details and the images, including the thumbnails can be scraped. This is makes the scraping a relatively time consuming project, as there are around 200 products, and a few seconds of waiting time between downloading the images in order not to overload the website.


## Folder Structure

The images will be downloaded into a folder structure based on metal type, diamond cut, and product name. The structure will look like this:

```
 project_folder/
    └── engagement_rings/
        ├── Metal_Type_1/
        │   ├── Shape_1/
        │   │   ├── ProductName1/
        │   │   │   ├── ProductName1_thumbnail_1.jpg
        │   │   │   ├── ProductName1_img_1.jpg
        │   │   ├── ProductName2/
        │   └── Shape_2/
        └── Metal_Type_2/
```


---

## Error Handling

The scraper includes error handling to manage common issues, such as:

- **Broken Links**: If a product page contains a 404 error, the script logs the error and moves to the next product, so as not to break the script due to the error.
- **Missing Images**: If image URLs are broken or unavailable, the script logs an error and continues scraping.
- **Unexpected Changes in Website Structure**: If the HTML structure changes, the script will log an error and can be debugged using the logs to identify the issue.

Logs are saved using Python's `logging` module, which provides detailed information about each step of the scraping process.

---


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Additional Information

- The scraper uses Selenium to interact with the website, so a graphical interface (GUI) is required for browser automation.
- Make sure to follow the website's terms of service when scraping. Use the scraper responsibly and do not overload the website with requests.

---


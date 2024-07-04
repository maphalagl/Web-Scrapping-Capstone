import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Step 1: Scrape data from the webpage using BeautifulSoup
def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.select(".property-card-link")
    prices = soup.select(".PropertyCardWrapper__StyledPriceLine")
    addresses = soup.select("address")

    link_list = [link.get("href") for link in links]
    price_list = [price.getText()[:6] for price in prices]
    address_list = [address.getText().strip() for address in addresses]

    return link_list, price_list, address_list


# Step 2: Use Selenium to automate form submission
def automate_form_submission(form_url, link_list, price_list, address_list):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    for i in range(len(link_list)):
        driver.get(form_url)

        # Wait for the input elements to be present
        address_property = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        price_monthly = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        link_property = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')))

        # Clear any pre-filled text (if necessary) and input new data
        address_property.clear()
        price_monthly.clear()
        link_property.clear()

        address_property.send_keys(address_list[i])
        price_monthly.send_keys(price_list[i])
        link_property.send_keys(link_list[i])
        submit_btn.click()

        # Wait for the confirmation page to load and click the 'Submit another response' link
        another_response = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
        another_response.click()

        time.sleep(3)  # Optional: adjust the sleep time as needed

    # Close the browser window after completion
    driver.quit()


# Main execution
if __name__ == "__main__":
    zillow_url = "https://appbrewery.github.io/Zillow-Clone/"
    form_url = "https://forms.gle/sH11GyXQJSb2cL6e8"

    link_list, price_list, address_list = scrape_data(zillow_url)
    automate_form_submission(form_url, link_list, price_list, address_list)

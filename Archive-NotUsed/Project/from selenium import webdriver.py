from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def click_element(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    
    # Find the element by class name and click it
    element = driver.find_element(By.CLASS_NAME, "selectable-text")
    element.click()
    
    time.sleep(2)  # Wait before closing
    driver.quit()

# Example usage for WhatsApp Web
click_element("https://web.whatsapp.com")

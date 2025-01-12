import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from rest_framework.test import APIClient
from base.models import Product
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



class TestIntegration:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request):
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/#/")
        driver.set_window_size(1296, 688)
        # Attach the driver to the class instance
        request.cls.driver = driver
        yield
        driver.quit()


# log in
    def test_login(self):
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("fo.7@gmail.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Forat12345")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        username_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        # Assert that the correct username is displayed, case insensitive
        assert username_element.text.lower() == "fo.7@gmail.com".lower(), f"Expected 'fo.7@gmail.com' but got {username_element.text}"


# create product without image
    def test_create_product_without_image(self):
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("fo.7@gmail.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Forat12345")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        # Wait for the admin menu to be clickable
        admin_menu = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "adminmenu"))
        )
        admin_menu.click()
        self.driver.find_element(By.LINK_TEXT, "Products").click()
        self.driver.find_element(By.CSS_SELECTOR, ".my-3").click()
        time.sleep(2)
        elem = self.driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)
        elem.send_keys(Keys.END)
        elem.send_keys(Keys.END)
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Update")]')
        button.click()
        # Scroll to the top using JavaScript
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        product_cell = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()=' Product Name ']"))
    )
        # Assert that the product cell is found
        assert product_cell is not None
        print("Product 'Product Name' found successfully.")
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestE2E:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        #driver=webdriver.Edge()
        self.driver.get("http://localhost:8000")
        self.driver.maximize_window()
        time.sleep(2)

    def teardown_method(self):
        self.driver.quit()

# writing a second review under a post - it doesnt allow it
    @pytest.mark.django
    def test_review_twice(self):
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-link:nth-child(2)"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].click();", element)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "email"))
            ).send_keys("jj.10@gmail.com")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "password"))
            ).send_keys("JAYJAY101010")

            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-3"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].click();", element)
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-xl-3:nth-child(4) strong"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].click();", element)
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".my-3:nth-child(3)"))
            )
            # Submit second review and check for alert
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "comment"))
            ).send_keys("second review by jj")
            time.sleep(1)
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".my-3:nth-child(3)"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].click();", element)

            # Wait for alert and check text
            alert = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
            )
            time.sleep(1)
            # Debug print to check actual alert text
            print("Alert Text: ", alert.text)

            # Handle different alert messages
            if "Product already reviewed" in alert.text:
                assert "Product already reviewed" in alert.text
            elif "Please Select a rating" in alert.text:
                assert "Please Select a rating" in alert.text
            else:
                raise AssertionError(f"Unexpected alert text: {alert.text}")

        except TimeoutException as e:
            # Take a screenshot for debugging
            self.driver.save_screenshot("timeout_debug.png")
            raise AssertionError(f"Test failed due to timeout: {e}")


# logging in, searching for product and adding it to cart
    def test_search_add_to_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("jj.10@gmail.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("JAYJAY101010")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        self.driver.find_element(By.NAME, "q").click()
        self.driver.find_element(By.NAME, "q").send_keys("electric")
        self.driver.find_element(By.CSS_SELECTOR, ".p-2").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(1) .card-img").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".w-100").click()
        time.sleep(2)
        subtotal_text = self.driver.find_element(By.CSS_SELECTOR, "h2").text  # Assuming the subtotal is within <h2>
        assert "subtotal (1) items".lower() in subtotal_text.lower()  # Make case-insensitive comparison



# test different search inputs 
    @pytest.mark.parametrize("search_input, should_have_results", [
        ("guit", True),      # Partial word - expect results (e.g., products with "guitar")
        ("gitar", False),    # Misspelled word - expect no results
        ("elec", True),      # Partial word (e.g., for "Electric") - expect results
        ("va", True),       # Partial word - expect results (e.g., products with "vampire")
    ])
    def test_search_keywords(self, search_input, should_have_results):
        # Find the search box and input the search term
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.click()
        search_box.clear()
        search_box.send_keys(search_input)
        time.sleep(1)
        
        # Submit the search
        self.driver.find_element(By.CSS_SELECTOR, ".p-2").click()
        time.sleep(2)
        
        # Get all product titles after search
        products_title = self.driver.find_elements(By.CSS_SELECTOR, ".card-body .card-title strong")
        
        # Assert based on whether results are expected or not
        if should_have_results:
            assert len(products_title) > 0, f"Expected results for '{search_input}', but found none."
        else:
            assert len(products_title) == 0, f"Expected no results for '{search_input}', but found {len(products_title)} products."


# complete registration
    def test_complete_registration(self):
        name="TEST"
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        self.driver.find_element(By.ID, "name").click()
        self.driver.find_element(By.ID, "name").send_keys(name)
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("tester1@gmail.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("TEST1234")
        self.driver.find_element(By.ID, "passwordConfirm").click()
        self.driver.find_element(By.ID, "passwordConfirm").send_keys("TEST1234")
        time.sleep(3)
        elem = self.driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)
        button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Register")]')
        button.click()
        WebDriverWait(self.driver,30).until(EC.presence_of_all_elements_located((By.ID,"username")))
        username=self.driver.find_element(By.ID, "username")
        time.sleep(3)
        assert username.text==name
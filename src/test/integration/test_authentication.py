import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.driver.timeouts.page_load = 2

    def tearDown(self):
        self.driver.close()

    def test_signin_successful(self):
        driver = self.driver
        driver.get("http://localhost:5000/signin")

        driver.find_element(By.ID, "username").send_keys("user1")
        driver.find_element(By.ID, "password").send_keys("Password123")
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNotNone(driver.get_cookie("Authorization"))

    def test_signin_fails_no_username(self):
        driver = self.driver
        driver.get("http://localhost:5000/signin")

        driver.find_element(By.ID, "username").send_keys()
        driver.find_element(By.ID, "password").send_keys("Password123")
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]

        self.assertIn("Käyttäjätunnus on pakollinen", errors)

    def test_signin_fails_no_password(self):
        driver = self.driver
        driver.get("http://localhost:5000/signin")

        driver.find_element(By.ID, "username").send_keys("user1")
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]
        self.assertIn("Salasana on pakollinen", errors)

    def test_signin_fails_missing_csrf(self):
        driver = self.driver
        driver.get("http://localhost:5000/signin")

        driver.execute_script('document.querySelector("#csrf_token").value = ""')
        csrf_token_field = driver.find_element(By.ID, "csrf_token")
        self.assertEqual(csrf_token_field.get_attribute("value"), "")

        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]

        self.assertIn("CSRF token puuttuu", errors)

    def test_signin_fails_invalid_csrf(self):
        driver = self.driver
        driver.get("http://localhost:5000/signin")

        driver.execute_script('document.querySelector("#csrf_token").value = "INVALID"')
        csrf_token_field = driver.find_element(By.ID, "csrf_token")
        self.assertEqual(csrf_token_field.get_attribute("value"), "INVALID")

        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]

        self.assertIn("CSRF tokenin validointi virhe", errors)

    def test_signup_successful(self):
        driver = self.driver
        driver.get("http://localhost:5000/signup")

        driver.find_element(By.ID, "username").send_keys("user99")
        driver.find_element(By.ID, "password").send_keys("Password312")
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(2)

        self.assertIsNotNone(driver.get_cookie("Authorization"))

    def test_signup_fails_user_exists(self):
        driver = self.driver
        driver.get("http://localhost:5000/signup")

        driver.find_element(By.ID, "username").send_keys("user2")
        driver.find_element(By.ID, "password").send_keys("Password312")
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(1)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]
        self.assertIn("Käyttäjätunnus on jo varattu", errors)

    def test_signup_fails_no_username(self):
        driver = self.driver
        driver.get("http://localhost:5000/signup")

        driver.find_element(By.ID, "username").send_keys()
        driver.find_element(By.ID, "password").send_keys("Password123")
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]
        self.assertIn("Käyttäjätunnus on pakollinen", errors)

    def test_signup_fails_no_password(self):
        driver = self.driver
        driver.get("http://localhost:5000/signup")

        driver.find_element(By.ID, "username").send_keys("user1")
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]
        self.assertIn("Salasana on pakollinen", errors)

    def test_signup_fails_missing_csrf(self):
        driver = self.driver
        driver.get("http://localhost:5000/signup")

        driver.execute_script('document.querySelector("#csrf_token").value = ""')
        csrf_token_field = driver.find_element(By.ID, "csrf_token")
        self.assertEqual(csrf_token_field.get_attribute("value"), "")

        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]

        self.assertIn("CSRF token puuttuu", errors)

    def test_signup_fails_invalid_csrf(self):
        driver = self.driver
        driver.get("http://localhost:5000/signup")

        driver.execute_script('document.querySelector("#csrf_token").value = "INVALID"')
        csrf_token_field = driver.find_element(By.ID, "csrf_token")
        self.assertEqual(csrf_token_field.get_attribute("value"), "INVALID")

        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        sleep(0.5)

        self.assertIsNone(driver.get_cookie("Authorization"))
        errors = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "error__description")
        ]

        self.assertIn("CSRF tokenin validointi virhe", errors)

    def test_authenticated_shows_nav_logout(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.add_cookie({"name": "Authorization", "value": "USER_1_TOKEN"})

        driver.get("http://localhost:5000/")

        navbar = [
            n.text
            for n in driver.find_elements(
                By.CSS_SELECTOR,
                ".navigation-bar__link > a",
            )
        ]

        self.assertIn("Kirjaudu ulos", navbar)

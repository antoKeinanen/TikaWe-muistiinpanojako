import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestNote(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.driver.timeouts.page_load = 1

        self.driver.get("http://localhost:5000")
        self.driver.add_cookie(
            {
                "name": "Authorization",
                "value": "USER_1_TOKEN",
            }
        )

    def tearDown(self):
        self.driver.close()

    def test_unauthenticated_cant_create_note(self):
        driver = self.driver

        driver.delete_all_cookies()

        driver.get("http://localhost:5000/note/create")

        self.assertEqual(
            driver.current_url,
            "http://localhost:5000/signin?next=http://localhost:5000/note/create",
        )

    def test_note_can_be_created(self):
        driver = self.driver

        driver.get("http://localhost:5000/note/create")

        driver.find_element(By.ID, "title").send_keys("Test note")
        driver.find_element(By.ID, "content").send_keys(
            "Here is a lot of text!! \n Another line too"
        )
        driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        self.assertIn("Test note", driver.title)

import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestSignup(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_signin_chrome(self):
        self.driver.get("http://app.finum.online/en/signin/")
        self.driver.find_element('name', 'email').send_keys("test@gmail.com")
        self.driver.find_element('name', 'password').send_keys("test")
        self.driver.find_element('id', 'kt_sign_in_submit').click()
        self.assertIn("https://app.finum.online/en/dashboard/", self.driver.current_url)

    def test_signup_chrome(self):
        self.driver.get("https://app.finum.online/en/signup/")
        self.driver.find_element('name', 'email').send_keys("kirillkozlovec11@gmail.com")
        self.driver.find_element('name', 'password1').send_keys("Kirill22")
        self.driver.find_element('name', 'password2').send_keys("Kirill22")

        self.driver.find_element('id', 'kt_sign_up_submit').click()
        self.assertIn("https://app.finum.online/en/signup/", self.driver.current_url)


if __name__ == '__main__':
    unittest.main()

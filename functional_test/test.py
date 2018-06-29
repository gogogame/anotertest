from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_user_can_access_website(self):

        # User wants to know how much sugar % is in food
        # so he goes to website that has infomation
        self.browser.get(self.live_server_url)

        # He notices the website title and header.
        self.assertIn('FoodSugar', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('FoodSugar', header_text)

        # He wants to know the amount sugar in plain milk
        # and he find it manually (with ctrl + F)
        # Then he saw the amount of sugar of plain milk
        food = self.browser.find_element_by_id('id_food_list')
        sugar = food.find_elements_by_tag_name('tr')
        self.assertIn('Plain milk', str([sugar.text for sugar in sugar]))
        self.assertIn('18%',str([sugar.text for sugar in sugar]))

        # After that he proceed to add the new food data
        # He'd add the "Baked corn snack" "50%" sugar (that's hell lot)
        inputbox = self.browser.find_element_by_id('id_add_food')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter food name.'
        )
        inputbox.send_keys("Baked corn snack")

        inputbox = self.browser.find_element_by_id('id_add_sugar')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter sugar amount. (eg. 10%)'
        )
        inputbox.send_keys("50")

        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        # He make sure that is included in the table
        food = self.browser.find_element_by_id('id_food_list')
        sugar = food.find_elements_by_tag_name('tr')
        self.assertIn('Baked corn snack', str([sugar.text for sugar in sugar]))
        self.assertIn('50%', str([sugar.text for sugar in sugar]))

        # Then he finds some of the food that list as 100% sugar
        # Which is stupid, so he removes it
        food = self.browser.find_element_by_id('id_food_list')
        sugar = food.find_elements_by_tag_name('tr')
        self.assertIn('Brown sugar', str([sugar.text for sugar in sugar]))
        self.assertIn('100%', str([sugar.text for sugar in sugar]))

        button = food.find_element_by_id('id_delete')
        button.click()

        # Again he makes sure this thing doesn't exist anymore in table
        food = self.browser.find_element_by_id('id_food_list')
        sugar = food.find_elements_by_tag_name('tr')
        self.assertNotIn('Brown sugar', str([sugar.text for sugar in sugar]))
        self.assertNotIn('100%', str([sugar.text for sugar in sugar]))

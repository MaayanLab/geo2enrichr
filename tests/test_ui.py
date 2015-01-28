import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chromedriver ='/usr/local/Cellar/chromedriver/2.12/bin/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver

chrome_options = Options()
chrome_options.add_extension('/Users/gwg/g2e/extension.crx')


# TODO: This is a nice-to-have, but I'm too tired to yak shave why basic
# Selenium functionality doesn't seem to work, namely click(). In the future,
# this testing may become more important.
class EmbeddedProperly(unittest.TestCase):

	pass


	'''def setUp(self):
		self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)


	def test_embed_button_exists(self):
		driver = self.driver
		driver.get('http://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc=GDS5077')
		time.sleep(5)
		compare_samples_btn = self.driver.find_element_by_id('yeselect')
		compare_samples_btn.click()
		embed_btn_id = driver.find_element_by_id('g2e-embedded-button')
		self.assertEqual(embed_btn_id.tag_name, 'td')


	def tearDown(self):
		self.driver.close()'''

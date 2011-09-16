import unittest
import logging
from selenium import webdriver

class BaseTestCase(unittest.TestCase):       

    def setUp(self):
        print " - starting: ",self.id()
        
      
    def tearDown(self):
        print " - completed: ",self.shortDescription()
        
        

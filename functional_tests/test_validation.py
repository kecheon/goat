__author__ = 'cheon'
#-*-coding:utf8-*-
from .base import FunctionalTest
from unittest import skip
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_item(self):
        self.fail("Write me!")

__author__ = 'cheon'
#-*-coding:utf8-*-
from .base import FunctionalTest
from unittest import skip
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_item(self):
        """입력한 내용이 없이 처리되었을 경우"""
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, u'입력 냉무!')

#         다시 입력
        self.browser.find_element_by_id('id_new_item').send_keys(u'수박 한 통\n')
        self.check_input_exists(u'수박 한 통')
#         두번째 냉무 실수
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        self.check_input_exists(u'1: 수박 한 통')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, u'입력 냉무')

        self.browser.find_element_by_id('id_new_item').send_keys(u'막걸리 한 병\n')
        self.check_input_exists(u'1: 수박 한 통')
        self.check_input_exists(u'2: 막걸리 한 병')